---
author: Josh Tolley
gh_issue_number: 171
tags: postgres, pentaho, reporting
title: Subverting PostgreSQL Aggregates for Pentaho
---

In a [recent post](/blog/2009/07/14/mdx) I described MDX and a project I’m working on with the Mondrian MDX engine. In this post I’ll describe a system I implemented to overcome one of Mondrian’s limitations.

Each Mondrian measure has an associated aggregate function defined. For instance, here’s a measure from the sample data that ships with Pentaho:

```xml
<Measure name="Quantity" column="QUANTITYORDERED" aggregator="sum" />
```

The schema defines the database connection properties and the table this cube deals with elsewhere; this line says there’s a column called QUANTITYORDERED which Mondrian can meaningfully aggregate with the sum() function. Mondrian knows about six aggregates: count, avg, sum, min, max, and distinct-count. And therein lies the problem. In this case, the client wanted to use other aggregates such as median and standard deviation, but Mondrian didn’t provide them[1].

Mondrian uses the aggregator attribute of the measure definition to generate SQL statements exactly as you might expect. In the case of the measure above, the SQL query involving that measure would read “sum(QUANTITYORDERED)”. In our case, Mondrian is backed by a PostgreSQL database, which offers a much richer set of aggregates (such as stddev() for the standard deviation, one of the numbers we need), but Mondrian doesn’t know how to get to them.

Measures can be defined in terms of SQL expressions, rather than simple column names, but this doesn’t immediately help. If I wanted the standard deviation of the quantity ordered, I might try something like this:

```xml
<Measure name="Quantity">
    <KeyExpression><SQL dialect="postgres">
        stddev(quantityordered)
    </SQL></KeyExpression>
</Measure>
```

Here, Mondrian would complain that the measure was defined without an aggregator attribute. And if I define one, such as sum, the resulting SQL becomes “sum(stddev(quantityordered))”, which is illegal and makes PostgreSQL complain about nested aggregates.

But PostgreSQL’s function overloading can help here. Although Mondrian’s generated SQL will always include a call to a “count()” function if the aggregator is defined as “count”, but there’s no reason we can’t make PostgreSQL use some other count() function. For instance, let’s defined a new “count()” function that isn’t an aggregate, but simply returns whatever argument it is passed. Then we can use it to wrap whatever function we want, including arbitrary aggregate functions.

Consider an attempt to get Mondrian to use the stddev() aggregate. It returns a DOUBLE PRECISION type, so our fake count function must simply accept a DOUBLE PRECISION variable and return it:

```sql
CREATE FUNCTION count(DOUBLE PRECISION) RETURNS DOUBLE PRECISION AS $$
    SELECT $1
$$ LANGUAGE SQL IMMUTABLE;
```

Then we define a measure like this:

```xml
<Measure name="Quantity Std. Dev" aggregator="count">
    <KeyExpression><SQL dialect="postgres">
        stddev(quantityordered)
    </SQL></KeyExpression>
</Measure>
```

The resulting SQL is “count(stddev(quantityordered))”, but in this case PostgreSQL uses our new count() function, and we get exactly the return value we want.

There’s a catch: if we have a double precision column “foo” in a table “bar”, and write:

```sql
SELECT count(foo) FROM bar;
```

...it uses our new count function, and rather than returning the number of rows in bar, it returns the value for foo from each row in bar.

To get around this problem, we can define a new data type. We’ll write a function to create that datatype from another data type, and rewrite our count function to accept only that data type, and return the original data type, like this:

```sql
CREATE TYPE dp_cust AS (dp DOUBLE PRECISION);

CREATE FUNCTION make_dpcust(a DOUBLE PRECISION) RETURNS dp_cust IMMUTABLE AS $$
DECLARE
    dpc dp_cust;
BEGIN
    dpc.dp := a;
    RETURN dpc;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION count(double precision);

CREATE FUNCTION count(dp_cust) RETURNS DOUBLE PRECISION IMMUTABLE AS $$
    SELECT $1.dp
$$ LANGUAGE sql;
```

Now our count() function will only be called when we’re dealing with the dp_cust type, and we can control precisely when that happens, because the only way we make dp_cust values will be with the make_dpcust function. Our measure now looks like this:

```xml
<Measure name="Quantity Std. Dev" aggregator="count">
    <KeyExpression><SQL dialect="postgres">
        make_dpcust(stddev(quantityordered))
    </SQL></KeyExpression>
</Measure>
```

With this new data type and our custom count() function we can use whatever PostgreSQL aggregate we want as a measure aggregate in Mondrian.

[1] Note that the Mondrian developers already recognize this as a shortcoming worth removing. Allowing user-defined aggregates is on the Mondrian roadmap.
