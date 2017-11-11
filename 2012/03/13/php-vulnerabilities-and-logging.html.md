---
author: Steph Skardal
gh_issue_number: 565
tags: hosting, security
title: PHP Vulnerabilities and Logging
---

I've recently been working on a Ruby on Rails site on my personal [Linode](http://www.linode.com/) machine. The Rails application was running in development with virtually no caching or optimization, so page load was very slow. While I was not actively developing on the site, I received a Linode alert that the disk I/O rate exceeded the notification threshold for the last 2 hours.

<img border="0" src="/blog/2012/03/13/php-vulnerabilities-and-logging/image-0.png" width="740"/>

Since I was not working on the site and I did not expect to see search traffic to the site, I was not sure what caused the alert. I logged on to the server and checked the Rails development log to see the following:

```nohighlight
Started GET "/muieblackcat" for 200.195.156.242 at 2012-02-15 10:01:18 -0500
Started GET "/admin/index.php" for 200.195.156.242 at 2012-02-15 10:01:21 -0500
Started GET "/admin/pma/index.php" for 200.195.156.242 at 2012-02-15 10:01:22 -0500
Started GET "/admin/phpmyadmin/index.php" for 200.195.156.242 at 2012-02-15 10:01:24 -0500
Started GET "/db/index.php" for 200.195.156.242 at 2012-02-15 10:01:25 -0500
Started GET "/dbadmin/index.php" for 200.195.156.242 at 2012-02-15 10:01:27 -0500
Started GET "/myadmin/index.php" for 200.195.156.242 at 2012-02-15 10:01:28 -0500
Started GET "/mysql/index.php" for 200.195.156.242 at 2012-02-15 10:01:30 -0500
Started GET "/mysqladmin/index.php" for 200.195.156.242 at 2012-02-15 10:01:32 -0500
Started GET "/typo3/phpmyadmin/index.php" for 200.195.156.242 at 2012-02-15 10:01:33 -0500
Started GET "/phpadmin/index.php" for 200.195.156.242 at 2012-02-15 10:01:35 -0500
Started GET "/phpMyAdmin/index.php" for 200.195.156.242 at 2012-02-15 10:01:36 -0500
Started GET "/phpmyadmin/index.php" for 200.195.156.242 at 2012-02-15 10:01:38 -0500
Started GET "/phpmyadmin1/index.php" for 200.195.156.242 at 2012-02-15 10:01:39 -0500
Started GET "/phpmyadmin2/index.php" for 200.195.156.242 at 2012-02-15 10:01:41 -0500
Started GET "/pma/index.php" for 200.195.156.242 at 2012-02-15 10:01:42 -0500
Started GET "/web/phpMyAdmin/index.php" for 200.195.156.242 at 2012-02-15 10:01:44 -0500
Started GET "/xampp/phpmyadmin/index.php" for 200.195.156.242 at 2012-02-15 10:01:46 -0500
Started GET "/web/index.php" for 200.195.156.242 at 2012-02-15 10:01:48 -0500
Started GET "/php-my-admin/index.php" for 200.195.156.242 at 2012-02-15 10:01:50 -0500
Started GET "/websql/index.php" for 200.195.156.242 at 2012-02-15 10:01:52 -0500
Started GET "/phpmyadmin/index.php" for 200.195.156.242 at 2012-02-15 10:01:53 -0500
Started GET "/phpMyAdmin/index.php" for 200.195.156.242 at 2012-02-15 10:01:55 -0500
Started GET "/phpMyAdmin-2/index.php" for 200.195.156.242 at 2012-02-15 10:01:57 -0500
Started GET "/php-my-admin/index.php" for 200.195.156.242 at 2012-02-15 10:01:59 -0500
Started GET "/phpMyAdmin-2.2.3/index.php" for 200.195.156.242 at 2012-02-15 10:02:00 -0500
Started GET "/phpMyAdmin-2.2.6/index.php" for 200.195.156.242 at 2012-02-15 10:02:02 -0500
Started GET "/phpMyAdmin-2.5.1/index.php" for 200.195.156.242 at 2012-02-15 10:02:04 -0500
Started GET "/phpMyAdmin-2.5.4/index.php" for 200.195.156.242 at 2012-02-15 10:02:07 -0500
Started GET "/phpMyAdmin-2.5.5-rc1/index.php" for 200.195.156.242 at 2012-02-15 10:02:09 -0500
Started GET "/phpMyAdmin-2.5.5-rc2/index.php" for 200.195.156.242 at 2012-02-15 10:02:10 -0500
Started GET "/phpMyAdmin-2.5.5/index.php" for 200.195.156.242 at 2012-02-15 10:02:12 -0500
Started GET "/phpMyAdmin-2.5.5-pl1/index.php" for 200.195.156.242 at 2012-02-15 10:02:14 -0500
Started GET "/phpMyAdmin-2.5.6-rc1/index.php" for 200.195.156.242 at 2012-02-15 10:02:16 -0500
Started GET "/phpMyAdmin-2.5.6-rc2/index.php" for 200.195.156.242 at 2012-02-15 10:02:17 -0500
Started GET "/phpMyAdmin-2.5.6/index.php" for 200.195.156.242 at 2012-02-15 10:02:19 -0500
Started GET "/phpMyAdmin-2.5.7/index.php" for 200.195.156.242 at 2012-02-15 10:02:21 -0500
Started GET "/phpMyAdmin-2.5.7-pl1/index.php" for 200.195.156.242 at 2012-02-15 10:02:23 -0500
Started GET "/phpMyAdmin-2.5.5-pl1/index.php" for 174.111.11.143 at 2012-02-15 14:09:10 -0500
```

As it turns out, the domain somehow got picked up by crawlers that were looking for PHP vulnerabilities. It's interesting to see the various versions of phpMyAdmin the crawler is attempting to exploit. Judging from the crawled pages, there may also be a few other applications (e.g. [TYPO3](http://typo3.com/)) that the crawler was trying to exploit. I'm not up to date on the various security exploits in PHP applications, but I was surprised to not see anything directly related to [WordPress](http://wordpress.org/) in the log, since I often hear of WordPress security issues.

Luckily, this particular application and all other applications on this server have virtually no private data, since most applications running on the server are CMS-type applications where all content is displayed on the front-end.
