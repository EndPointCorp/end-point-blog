---
author: Tim Case
gh_issue_number: 705
tags: ruby, rails
title: Don't Sleep on Rails 3 SQL Injection Vulnerabilities
---



SQL injection is a problem that every web developer needs to be aware of when accepting parameters that will during the life of the request be converted into SQL statements. Rails historically has done what it can to mitigate this risk for the developer by providing vehicles for sanitizing parameter inputs at the points when they are being converted for use inside of a SQL statement, however with Rails 3 there are numerous ways to execute a SQL statement against the database and some of these methods are safer than others.

Consider two cases where valid Rails code is vulnerable to SQL injection:

```sql
#user inputed parameters
params[:query] = "'robert'; DROP TABLE students; ##"

#CASE 1 - find_by_sql
User.find_by_sql("SELECT * FROM users WHERE (name = '#{params[:query]}'")  ##(BAD BAD BAD)

#generated SQL
SELECT  `users`.* FROM `users`  WHERE (email = 'Robert'); DROP TABLE STUDENTS; ##') ##(THIS STATEMENT WILL DROP TABLE STUDENTS)

```

The example above shows how find_by_sql can allow parameters submitted by a user to be directly entered into a SQL statement and how an attacker might use the vulnerability to wreak havoc.  These types of find_by_sql statements used to be more commonly used in earlier versions of Rails (1.0 - 2.0) and it was through these statements that the Rails community realized that SQL injection was a problem that needed addressing.  Here's another example prominent in the early Rails days:

```sql
User.find :first, :conditions =&gt; "(name = '#{params[:query]}')" ##(BAD BAD BAD)
produces this SQL statement:

#generated SQL
SELECT  `users`.* FROM `users`  WHERE (email = 'Robert'); DROP TABLE STUDENTS; ##') ##(THIS STATEMENT WILL DROP TABLE STUDENTS)

```

The above example shows a common Rails idiom for performing an ActiveRecord query, as with the previous find_by_sql example the find query here is piping the param in directly and generating the exact same tainted SQL.

Fortunately, Rails core decided to make it easier to just do the right thing and provided ways to pass in parameters by using built-in filters that handle special SQL characters, which will escape ’ , " , NULL character and line breaks. Instead of passing in the parameter directly as a raw string, you can pass in an array to sanitize the tainted strings using the built-in filters:

```sql
User.find_by_sql(["SELECT * FROM users WHERE (name = ?)", params])  ##(GOOD)
User.find :first, :conditions =&gt; ["(name = '?')", params] ##(GOOD)
#generated SQL
SELECT * FROM users WHERE (name = 'Robert\'); DROP TABLE STUDENTS; ##') (RETURNS NIL)

```

The distinction in the filtered SQL statement is the escaped single quote right after the t in Robert which prevents the name parameter from terminating and allowing the DROP TABLE STUDENTS from being executed since it remains a part of the string parameter. Additionally, Rails also included these built-in filters automatically when AR queries were called from find_by_*something* or a conditions hash:

```sql
User.find_by_name(params[:query]) ##(GOOD)
#generated SQL
SELECT * FROM `users` WHERE `users`.`name` = 'Robert\'); DROP TABLE STUDENTS; ##' (RETURNS NIL)
User.find :first, :conditions =&gt; {:name =&gt; params} ##(GOOD)
SELECT `users`.* FROM `users` WHERE `users`.`name` = 'Robert\'); DROP TABLE STUDENTS; ##' (RETURNS NIL)

```

Rails 3 introduced [AREL](https://github.com/rails/arel), which is another way to perform ActiveRecord queries and with it came as well, another way to make the exact same SQL injection mistakes that are already listed above. However having gotten accustomed to looking for SQL injection vulnerabilities in the AR query formats above you might be lulled into thinking that the new and improved ActiveRecord query methods would just magically handle the tainted strings for you and you'd be dead wrong:

```sql
User.where("name = '#{params}'") (BAD)
SELECT `users`.* FROM `users`  WHERE (name = 'Robert'); DROP TABLE STUDENTS; ##') ##(THIS STATEMENT WILL DROP TABLE STUDENTS)

```

The nice thing is that the same fix can also be applied:

```sql
User.where(["name = ?", params])
SELECT `users`.* FROM `users`  WHERE (name = ''Robert\'); DROP TABLE STUDENTS; ##'')  ##(RETURNS NIL)

```

