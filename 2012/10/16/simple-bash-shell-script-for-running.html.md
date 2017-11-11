---
author: Barrett Griffith
gh_issue_number: 707
tags: shell, mysql
title: Simple bash shell script for running batch MySQL jobs
---

The other day I needed to run a simple mysql job to backup and delete some database records on a live server. Being a live server, it is important to make sure you aren't asking the database to take on jobs that could potentially lock it up. Better to run a batch job. Running a batch is simple. You can call it right from the mysql console with:

```sql
source [path_to]/[the_batch_script].sql
```

But what if there are millions of records that need deleting? **Bash shell script to the rescue.**

Here is the idea of the SQL job that needed to get run a few times:

```sql
START TRANSACTION;

/* Find what you want to delete and put a LIMIT on your batch size */
CREATE TEMPORARY TABLE records_to_delete_temp SELECT id from `records` where ..... limit 1000;

/* Creating backup table to archive spam orders */
CREATE TABLE IF NOT EXISTS `records_backup` LIKE `records`;
INSERT INTO `records_backup` SELECT * from `records` where id in (select id from `records_to_delete_temp`);

/* Delete Dependents - If your records have foreign key dependencies, delete them first */
DELETE FROM `dependent_1` where record_id in (select id from `records_to_delete_temp`);
DELETE FROM `dependent_2` where record_id in (select id from `records_to_delete_temp`);

/* Delete the records */
DELETE FROM `records` where id in (select id from `records_to_delete_temp`);

/* Return count of remaining records - the where clause should be the same as the original select for the records to delete */
SELECT COUNT(*) from `records` where .... ;

COMMIT ;
```

Note:

```sql
SELECT COUNT(*)
```

This will return the remaining record count to the shell script.

And the shell script...

```bash
ret=$(mysql -u [user] -p[password] --skip-column-names [database_name]  < [the_batch_script].sql)

while [ $ret -gt 0 ]
do
  echo "rows left: $ret"
  sleep 3
  ret=$(mysql -u [user] -p[password] --skip-column-names [database_name]  < [the_batch_script].sql)
done
```

Notes:

```bash
--skip-column-names
```

This is the little nugget that gives you clean output from the mysql script. Without --skip-column-names you will have to get more creative with parsing the returned table.

```bash
-p[password]
```

Just a friendly reminder, no space after the -p option.

Should you really be running batches to remove millions of records from a live server with a shell script?

Just because you can doesn't mean you should. Before pulling the trigger, back up, consider what could go wrong, have a plan in place to address the possible failure.

Find something fun for your hands to do while bash takes care of running the jobs. At the least, cross your fingers!
