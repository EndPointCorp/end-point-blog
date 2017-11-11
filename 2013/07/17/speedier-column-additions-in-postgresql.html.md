---
author: Jeff Boes
gh_issue_number: 835
tags: postgres, sql
title: Speedier column additions in PostgreSQL
---



Say you want to add a column to a large table, e.g.,

```sql
ALTER TABLE transactions ADD COLUMN email_sent BOOLEAN DEFAULT FALSE;
```

You really do want new rows to start out with the column "false" (if no value is supplied when the row is created). However, you also want all *existing* rows to be "true", so innocently:

```sql
UPDATE transactions SET email_sent = TRUE;
```

This is a great time for a coffee break, or a trip to the post office, or maybe (if you're a telecommuter like me), a stroll out to weed the garden. Unfortunately for all those side activities, you really didn't have to take the long way.

```sql
BEGIN;
ALTER TABLE transactions ADD COLUMN email_sent BOOLEAN DEFAULT TRUE;
ALTER TABLE transactions ALTER TABLE email_sent SET DEFAULT FALSE;
COMMIT;
```

This is a *lot* faster; create all the columns with the appropriate value, then set the default for new rows, and all inside a transaction so you know it gets done atomically.


