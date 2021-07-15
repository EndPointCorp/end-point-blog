---
author: Mark Johnson
title: Parallel Inventory Access using PostgreSQL
github_issue_number: 81
tags:
- postgres
- ecommerce
date: 2008-12-12
---

Inventory management has a number of challenges. One of the more vexing issues with which I’ve dealt is that of forced serial access. We have a product with X items in inventory. We also have multiple concurrent transactions vying for that inventory. Under any normal circumstance, whether the count is a simple scalar, or is comprised of any number of records up to one record/quantity, the concurrent transactions are all going to hone in on the same record, or set of records. In doing so, all transactions must wait and get their inventory serially, even if doing so isn’t of interest.

If inventory is a scalar value, we don’t have much hope of circumventing the problem. And, in fact, we wouldn’t want to under that scenario because each transaction must reflect the part of the whole it consumed so that the next transaction knows how much is left to work with.

However, if we have inventory represented with one record = one quantity, we aren’t forced to serialize in the same way. If we have multiple concurrent transactions vying for inventory, and the sum of the need is less than that available, why must the transactions wait at all? They would normally line up serially because, no matter what ordering you apply to the selection (short of random), it’ll be the same ordering for each transaction (and even an increasing probability of conflict with random as concurrency increases). Thus, to all of them, the same inventory record looks the “most interesting” and, so, each waits for the lock from the transaction before it to resolve before moving on.

What we really want is for those transactions to attack the inventory like an easter-egg hunt. They may all make a dash for the “most interesting” egg first, but only one of them will get it. And, instead of the other transaction standing there, coveting the taken egg, we want them to scurry on unabated and look for the next “most interesting” egg to throw in their baskets.

We can leverage some PostgreSQL features to accomplish this goal. The key for establishing parallel access into the inventory is to use the row lock on the inventory records as an indicator of a “soft lock” on the inventory. That is, we assume any row-locked inventory will ultimately be consumed, but recognize that it *might not be*. That allows us to pass over locked inventory, looking for other inventory to fill the need; but if we find we don’t have enough inventory for our need, those locked records indicate that we should take another pass and try again. Eventually, we either get all the inventory we need, or we have consumed all the inventory there is, meaning less than we asked for but with no locked inventory present.

We write a pl/pgsql function to do all the dirty work for us. The function has the following args:

- Name of table on which we want to apply parallel access
- Query that retrieves all pertinent records, and in the desired order
- Integer number of records we ultimately want locked for this transaction.

The function returns a setof ctid. Using the ctid has the advantage of the function needing to know nothing about the composition of the table and providing exceedingly fast access back to the records of interest. Thus, the function can be applied to any table if desired and doesn’t depend on properly indexed fields in the case of larger tables.

```
CREATE OR REPLACE FUNCTION getlockedrows (
       tname TEXT,
       query TEXT,
       desired INT
   )
RETURNS SETOF TID
STRICT
VOLATILE
LANGUAGE PLPGSQL
AS $EOR$
DECLARE
   total   INT NOT NULL := 0;
   locked  BOOL NOT NULL := FALSE;
   myst    TEXT;
   myrec   RECORD;
   mytid   TEXT;
   found   TID[];
   loops   INT NOT NULL := 1;
BEGIN
   -- Variables: tablename, full query of interest returning ctids of tablename rows, and # of rows desired.
   RAISE DEBUG 'Desired rows: %', desired;
   <<outermost>>
   LOOP
/*
   May want a sanity limit here, based on loops:
   IF loops > 10 THEN
       RAISE EXCEPTION 'Giving up. Try again later.';
   END IF;
*/
       BEGIN
           total := 0;
           FOR myrec IN EXECUTE query
           LOOP
               RAISE DEBUG 'Checking lock on id %',myrec.ctid;
               mytid := myrec.ctid;
               myst := 'SELECT 1 FROM '
                   || quote_ident(tname)
                   || ' WHERE ctid = $$'
                   || mytid
                   || '$$ FOR UPDATE NOWAIT';
               BEGIN
                   EXECUTE myst;
                   -- If it worked:
                   total := total + 1;
                   found[total] := myrec.ctid;
                   -- quit as soon as we have all requested
                   EXIT outermost WHEN total >= desired;
               -- It did not work
               EXCEPTION
                   WHEN LOCK_NOT_AVAILABLE THEN
                       -- indicate we have at least one candidate locked
                       locked := TRUE;
               END;
           END LOOP; -- end each row in the table
           IF NOT locked THEN
               -- We have as many in found[] as we can get.
               RAISE DEBUG 'Found % of the requested % rows.',
                   total,
                   desired;
               EXIT outermost;
           END IF;
           -- We did not find as many rows as we wanted!
           -- But, some are currently locked, so keep trying.
           RAISE DEBUG 'Did not find enough rows!';
           RAISE EXCEPTION 'Roll it back!';
       EXCEPTION
           WHEN RAISE_EXCEPTION THEN
               PERFORM pg_sleep(RANDOM()*0.1+0.45);
               locked := FALSE;
               loops := loops + 1;
       END;
   END LOOP outermost;
   FOR x IN 1 .. total LOOP
       RETURN NEXT found[x];
   END LOOP;
   RETURN;
END;
$EOR$
;
```

The function makes a pass through all the records, attempting to row lock each one as it can. If we happen to lock as many as requested, we exit <<outermost>> immediately and start returning ctids. If we pass through all records without hitting any locks, we return the set even though it’s less than requested. The calling code can decide how to react if there aren’t as many as requested.

To avoid artificial deadlocks, with each failed pass of <<outermost>>, we raise exception of the encompassing block. That is, with each failed pass, we start over completely instead of holding on to those records we’ve already locked. Once a run has finished, it’s all or nothing.

We also mix up the sleep times just a bit so any two transactions that happen to be locked into a dance precisely because of their timing will (likely) break the cycle after the first loop.

Example of using our new function from within a pl/pgsql function:

```
...
   text_query := $EOQ$
SELECT ctid
FROM inventory
WHERE sku = 'COOLSHOES'
   AND status = 'AVAILABLE'
ORDER BY age, location
$EOQ$
;

   OPEN curs_inv FOR
       SELECT inventory_id
       FROM inventory
       WHERE ctid IN (
               SELECT *
               FROM getlockedrows(
                   'inventory',
                   text_query,
                   3
               )
       );

   LOOP

       FETCH curs_inv INTO int_invid;

       EXIT WHEN NOT FOUND;

       UPDATE inventory
       SET status = 'SOLD'
       WHERE inventory_id = int_invid;

   END LOOP;
...
```

The risk we run with this approach is that our ordering will not be strictly enforced. In the above example, if it’s absolutely critical that the sort on age and location never be violated, then we cannot run our access to the inventory in parallel. The risk comes if T1 grabs the first record, T2 only needs one and grabs the second, but T1 aborts for some other reason and never consumes the record it originally locked.
