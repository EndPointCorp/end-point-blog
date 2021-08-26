---
author: Ron Phipps
title: Guidelines for Interchange site migrations
github_issue_number: 345
tags:
- ecommerce
- environment
- git
- interchange
- perl
date: 2010-09-03
---



I’m involved at End Point often with Interchange site migrations. These migrations can be due to a new client coming to us and needing hosting or migrating from one server to another within our own infrastructure. 

There are many different ways to do a migration, in the end though we need to hit on certain points to make sure that the migration goes smoothly. Below you will find steps which you can adapt for your specific migration.

During the start of the migration it might be a good time to introduce git for source control. You can do this by creating the repository and cloning it to /home/account/live, setting up .gitignore files for logs, counter files, gdbm files. Then commit the changes back to the repo and you’ve now introduced source control without much effort, improving the ability to make changes to the site in the future. This is also helpful to document the changes you make to the code base along the way during the migration in case you need to merge changes from the current production site before completing the migration.

- Export all of the gdbm databases to their text file equivalents on the production server

- Take a backup from production of the database, catalog, interchange server, htdocs

- Setup an account

- Create the database and user

- Restore the database, catalog, interchange server and htdocs

- Update the paths in interchange/bin for each script to point at the new location

- Grep the restored code for hard coded paths and update those paths to the new locations. Better yet move these paths out to a catalog_local.cfg where environment specific information can go.

- Grep the restored code for hard coded urls and use the [area] tag to generate the urls

- Update the urls in products/variable.txt to point at the test domain

- Update the sql settings in products/variable.txt to point at the new database using the new user

- Remove the gdbm databases so they will be recreated on startup from the source text files

- Install a local Perl if it’s not already installed (./configure -des will compile and install Perl locally)

- Install Bundle::InterchangeKitchenSink

- Install the DBD module for MySQL or PostgreSQL

- Review the code base looking for use statements in custom code and Require module settings in interchange.cfg. Install the Perl modules found into the local Perl.

- Setup a non ssl and ssl virtual host using a temporary domain. Configure the temporary domain to use the SSL certificate from the production domain.

- Firewall or password protect the virtual host so it is not accessible to the public

- Generate a vlink using interchange/bin/compile and copy it into the cgi-bin directory and name it properly

- Startup the new Interchange

- Review error messages and resolve until Interchange will start properly

- Test the site thoroughly, resolving issues as they appear. Make sure that checkout, charging credit cards, sending of emails, using the admin, etc all function.

- Migrate any cron jobs running on the current production site, such as session expiration scripts

- Setup logrotation for the new logs that will be created

- Verify that you have access to make DNS changes

- Set the TTL for the domain to a low value such as 5 minutes

- Modify the new production site to respond to the production url, test by updating your hosts file to manually set the IP address of the domain

- Shutdown the new Interchange

- Restore a copy of the original backup for Interchange, the catalog and htdocs to /tmp on the production server

- Shutdown the production Interchange, put up a maintenance note on the production site.

- Take a backup of the production database and restore on the new server

- Diff the Interchange, catalog and htdocs directory between /tmp and the current production locations, making note of the files that have changed since we took the original copy.

- Copy the files that have changed, making sure to merge with any changes we have made on the new production site. Making sure to copy over all .counter and .autonumber files to the new production site.

- Start Interchange on the new production server

- Test the site thoroughly on the new production server, using the production url. Make sure that checkout with charging the credit card functions properly.

- Resolve any remaining issues found during the testing

- Setup the Interchange daemon to start at boot for this site in /etc/rc.d/rc.local or in cron using @reboot

- Update DNS to point at the new production IP address

- Update the TTL of the domain to a longer value

- Open the site to the public by opening the firewall or removing the password protection

- Keep an eye on the error logs for any issues that might crop up

This will hopefully give you a solid guide for performing an Interchange site migration from one server to another and some of the things to watch out for that might cause issues during the migrations.


