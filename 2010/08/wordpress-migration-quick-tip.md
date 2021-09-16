---
author: Steph Skardal
title: A WordPress Migration Quick Tip
github_issue_number: 335
tags:
- php
date: 2010-08-04
---

This morning Chris Kershaw asked me about a [WordPress](https://wordpress.org/) migration issue he was experiencing. Chris dumped the database from the current live server and imported it to another server with a temporary domain assigned and then tried to access the blog. Whenever he would attempt to visit the login (wp-admin) page, he would be redirected to the live domain admin login URL instead of the temporary domain. Luckily, there’s a quick fix for this.

The simplified explanation for this is that throughout the WordPress code, there are various places where the base URL is retrieved from the database. There is a table (wp_options by default) that includes option settings and a function to retrieve data from the wp_options table (get_option). You’ll see something similar to the following two lines scattered throughout the WordPress source to retrieve the base URL to be used in redirects or link creation. In Chris’ case, my guess is that the wp-admin page was attempting to redirect him to the secure login page, which uses one of the examples below to get the base URL.

```php
$home = parse_url( get_option('siteurl') );
$home_path = parse_url(get_option('home'));
```

If we take a look at the database wp_options table for option_name’s home and siteurl immediately after the import, you might see something like the following, where http://www.myawesomesite.com/blog is the live blog.

```sql
mysql> SELECT option_name, option_value FROM wp_options WHERE option_name IN ('siteurl', 'home');
+-------------+-----------------------------------+
| option_name | option_value                      |
+-------------+-----------------------------------+
| home        | http://www.myawesomesite.com/blog |
| siteurl     | http://www.myawesomesite.com/blog |
+-------------+-----------------------------------+
```

To correct any redirect and link issues, you’ll just want to update the wp_options values with the following, where http://myawesomesite.temphost.net/blog is the temporary blog location:

```sql
UPDATE wp_options SET option_value = 'http://myawesomesite.temphost.net/blog' WHERE option_name IN ('siteurl', 'home');
```

Yielding:

```sql
mysql> SELECT option_name, option_value FROM wp_options WHERE option_name IN ('siteurl', 'home');
+-------------+----------------------------------------+
| option_name | option_value                           |
+-------------+----------------------------------------+
| home        | http://myawesomesite.temphost.com/blog |
| siteurl     | http://myawesomesite.temphost.com/blog |
+-------------+----------------------------------------+
```

This is just a quick tip that I’ve learned after working through several WordPress migrations. The developer needs direct access to the database to make this change, either via SSH or a database control panel—​I have not found a way to apply this change from the WordPress admin easily. Also, when the new server goes live, these values must be updated again to force redirects to the regular (non-temphost) domain.
