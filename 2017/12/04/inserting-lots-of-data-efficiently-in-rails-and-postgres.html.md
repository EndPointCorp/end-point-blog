---
author: Kamil Ciemniewski
title: "Inserting lots of data efficiently in Rails + PostgreSQL"
tags: rails, postgres
gh_issue_number: 1347
---

This is going to be a very short post about a simple solution to the problem of inserting data fast when you really have a **lot** of it.

### The problem

For the sake of having some example to think about, imagine building an app for managing nests of ants.

You can have thousands of nests with hundreds of thousands of ants in each one of them.

To make the fun example applicable for this blog post, imagine that you’re reading data files coming from a miraculous device that “scans” nests for ants and gives you info about every ant with lots of details. This means that creation of the nest is about providing a name, coordinates, and the data file. The result should be a new nest and hundreds of thousands of ant records in the database.

How do we insert this much data without hitting the browser’s timeout?

### Approaching the problem

Regular `INSERT` statements provide a lot of flexibility that is normally much needed, but is relatively slow. For this reason doing many of them isn’t preferred among database experts for pre-populating databases.

The solution that is typically used instead (apart from the case in which a database needs to be restored, with `pg_restore` having no contenders in terms of speed) is the data-loading method called `COPY`.

It allows you to provide data in a CSV format either from a file or “streaming” this data into the client itself. Now because it’s **almost never** a good idea to use the database-superuser account for connecting with the database from Rails, the first option isn’t available (access to the file system is only allowed for admins). Fortunately, there’s the second option which we are going to make use of.

### The solution

Here’s a short code excerpt showing how the above mentioned approach could be used in Rails for the fun little app described in the beginning:

```ruby
# first, grab the underlying connection object coming
# from the lower level postgres library:
connection = Ant.connection.raw_connection

# generate the ants array based on the data file:
ants = AntImporter.run!(data_file)

# now use the connection’s ability to start streaming
# data via the COPY feature:
connection.copy_data "COPY ants (id, type, age) FROM STDIN CSV" do
  ants.each do |ant|
    connection.put_copy_data [ ant.id, ant.type, ant.age ].to_csv
  end
end
```

If you’re curious, check for yourself. This way you can copy really a **lot** of data without having to wait for the process to finish for too long.

Please do make sure you read and considered the “caveats” section from the [“COPY” page on the Postgres wiki](https://wiki.postgresql.org/wiki/COPY). There are reasons for the (slower) inner workings of the `INSERT` statement. Use this post’s solution with care.
