---
author: Terry Grant
gh_issue_number: 594
tags: database, php
title: Integrating Propel ORM
---



### Propel ORM Integration

Most of us have worked in environments that are organized in an less than desirable manner. A common recurring problem is the organization and communication between the business logic and the database model. One helpful methodology to help with a problem like this is implementing an ORM (Object-Relational Mapping) system. There are many to choose from, but I would like to discuss use and integration of Propel ORM.

Propel is currently only used in PHP, but supports many different databases. Currently Propel supports the following databases: MySQL, Postgres, Sqlite, MsSQL, and Oracle.

### Installation and Setup

The main point of this post is to show how easily you can start integrating an ORM into your working environment. The explanation and examples below assume that you have installed the correct packages and configured Propel to work with your environment properly.

The Propel website offers great documentation on how to do that:

[Installation](http://propelorm.org/documentation/01-installation.html)

[Configuration](http://propelorm.org/documentation/02-buildtime.html)

### Integration

After you have set everything up, in particular the build.properties file, you can now generate your schema.xml file. This generated file describes your database in XML, everything form datatypes to the relationships between tables. Run the following command to generate this XML file:

```nohighlight
  propel-gen reverse
```

Now we want to generate the PHP classes that you will use to interact with your data. Do this by running the following command.

```nohighlight
  propel-gen .
```

If everything went well you should now have a directory called ‘build/’ where you ran the propel_gen commands. Look in ‘build/classes/’ you will see the name of the project you named earlier in build.properties. Within this directory you will see a list of files, one for each of your tables. Copy these somewhere you can easily include them from a PHP file.

From now on each time you make a change to your database you will need to either modify your schema.xml to reflect that change, or simply run the propel-gen reverse to have it generated for you. You will also need to copy the generated PHP classes to your project when changes are made. There are many different ways you can use Propel for data model management, this is just one way to get you up and running.

### Usage

Propel offers very elaborate functionality for interfacing with your data-model. I have included two quick examples to give you an idea of how you can easily begin to use it. I have included two examples showing some simple retrieval functionality. For this example let’s say we have a table called ‘Customers’ with a few common columns like name and address.

#### Simple Select Statement

```perl
$query = new CustomerQuery();
$customers = CustomerQuery::create()->orderByName()->limit(2)->find();
$first_customer = $query->findPK(1); // This would give us the first in the list
```

#### Custom SQL

```perl
$con = Propel::getConnection(CustomerPeer::DATABASE_NAME);
$sql = "SELECT * FROM customer WHERE name ilike ('%:name%');
$stmt = $con->prepare($sql);
$stmt->execute(array(':name' => 'Terry'));

```

These are just two ‘very’ simple examples but Propel offers many ways to access and update your data. Please visit the [Propel website](http://propelorm.org/) if you would like to read more about this ORM.


