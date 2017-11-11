---
author: Marina Lohova
gh_issue_number: 645
tags: database, postgres, security, sql
title: You shall not pass! Preventing SQL injection
---



Greg Sabino Mullane presented a few extremely useful techniques for preventing SQL injection. His advice was mostly based on his recent real-world experience.

<a href="http://www.flickr.com/photos/80083124@N08/7187106237/" title="IMG_0801.JPG by endpoint920, on Flickr"><img alt="IMG_0801.JPG" height="375" src="/blog/2012/06/14/you-shall-not-pass-preventing-sql/image-0.jpeg" width="500"/></a>

The chunk of simple code was causing a potentially very dangerous security breach to the system:

```
[query … where order_number='[scratch order_number] and username='[session username]']
```

This code can generate this SQL query:

```
select * from orders where order_number = '12345' and username = 'alice';
```

Or this SQL query:

```
select * from orders where order_number=' ';  delete from orders where id IS NOT NULL;
```

This is a vulnerability, and you certainly do not want any random stranger to delete records from the "orders" table in your database.

The problem was solved in no time by escaping user input.

Here is Greg's list of recommendations to make SQL injection impossible:

1. Escape all user input passed to the database.
1. Log extensively. If this system hadn't logged SQL queries, they would have never noticed anything strange. They used tail_n_mail that tracks PostgreSQL logs and sends out emails whenever SQL exception occurs.
1. Introduce fine-grained control for accessing and manipulating the database. Split responsibilities between a lot of database users and selectively grant permissions to them. Run your code as the appropriate database user with the most restrictive set of permissions possible.
1. Database triggers can become very handy. In Greg's case it was impossible to delete the already shipped order because of the triggers assigned to the record.
1. Have a lot of eyes on the code to eliminate the obvious mistakes.
1. And finally, if SQL injection is happening, consider shutting down the database server until you find the cause. This is an emergency!


