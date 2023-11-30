---
author: Phineas Jensen
title: Using PostgreSQL cidr and inet types, operators, and functions
github_issue_number: 1327
tags:
- database
- networking
- postgres
date: 2017-09-28
---



A common problem in database design is how to properly store IP addresses: They are essentially positive 32 or 128 bit integers, but they’re more commonly written as blocks of 8 or 16 bit integers written in decimal and separated by periods (in IPv4) or written in hexadecimal and separated by colons (in IPv6). That may lead many people to store IP addresses as strings, which comes with a host of downsides.

For example, it’s difficult to do subnet comparisons and validation requires complex logic or regular expressions, especially when considering the variety of ways IPv6 addresses can be stored with upper- or lower-case hexadecimal letters, :0000: or :0: for a group of zeros, or :: as several groups of zeros (but only once in an address).

Storing them as integers or a fixed number of bytes forces parsing and a uniform representation, but is otherwise no better.

To solve these problems in PostgreSQL, try using the [inet](https://www.postgresql.org/docs/9.6/static/datatype-net-types.html#DATATYPE-INET) and [cidr](https://www.postgresql.org/docs/9.6/static/datatype-net-types.html#DATATYPE-CIDR) types, which are designed for storing host and network addresses, respectively, in either IPv4 or IPv6 or both.

In many cases, these types could end up simply being used as glorified integers: they display nicely as IP addresses should be, and support addition, subtraction, and bitwise operations, and basic numeric comparisons:

```sql
phin=> select inet '192.168.0.1' + 256;
  ?column?
-------------
 192.168.1.1
(1 row)

phin=> select inet '::2' - 1;
 ?column?
----------
 ::1
(1 row)

phin=> select inet '192.168.0.1' - inet '192.168.0.0';
 ?column?
----------
        1
(1 row)

phin=> select inet 'Fff0:0:007a::' > inet '192.168.0.0';
 ?column?
----------
 t
(1 row)
```

(It’s worth noting that there is no addition operation for two inet or cidr values.)

But if you take a look at the fantastic [official documentation](https://www.postgresql.org/docs/current/static/functions-net.html), you’ll see that these types support also support helpful containment operators and utility functions which can be used when working with historical IP addresses of ecommerce customers stored in a database.

These include operators to check if one value contains or is contained by another (>> and <<), or the same with equality (>>= and <<=), or containment going either way (&&). Take this very real™ table of ecommerce orders, where order #3 from IP address 23.239.26.78 has committed or attempted some sort of ecommerce fraud:

```sql
phin=> select * from orders order by id;
 id |        ip        | fraud
----+------------------+-------
  1 | 23.239.26.161/24 | f
  2 | 23.239.232.78/24 | f
  3 | 23.239.26.78/24  | t
  4 | 23.239.23.78/24  | f
  5 | 23.239.26.78/24  | f
  6 | 23.239.232.78/24 | f
(6 rows)
```

By using the network(inet) function, we can identify other orders from the same network:

```sql
phin=> select * from orders where network(ip) = (
    select network(ip) from orders where id=3
);
 id |        ip        | fraud
----+------------------+-------
  1 | 23.239.26.161/24 | f
  5 | 23.239.26.78/24  | f
  3 | 23.239.26.78/24  | t
(3 rows)
```

Or, if we’ve identified 23.239.20.0/20 as a problematic network, we can use the <<= “is contained by or equals” operator:

```sql
phin=> select * from orders where ip <<= inet '23.239.20.0/20'
 id |        ip        | fraud
----+------------------+-------
  1 | 23.239.26.161/24 | f
  4 | 23.239.23.78/24  | f
  5 | 23.239.26.78/24  | f
  3 | 23.239.26.78/24  | t
(4 rows)
```

This is a bit of a juvenile example, but given a larger and more real database, these tools can be used for a variety of security and analytics purposes. Identifying common networks for fraud was already given as an example. They can also be used to find common network origins of attacks; tie historic data to known problematic networks, addresses, and proxies; help correlate spam submissions on forums, blogs, or in email; and create and analyze complex network or security auditing records.

At any rate, they’re a useful tool and should be taken advantage of whenever the opportunity presents itself.


