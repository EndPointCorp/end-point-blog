---
author: Edgar Mlowe
title: 'How to Set Up pgTap for Writing Postgres Database unit tests'
tags:
- Postgres
- PL/pgSQL
- SQL
- pgTap

date: 2023-03-20
featured:
  endpoint: true
description: This article walks readers through how to setup pgTap a unit testing framework for Postgres.
---




### How to Set Up pgTap for Writing Postgres Database unit tests

#### Introduction
In a previous blog post by [Josh Tolley](https://www.endpointdev.com/team/josh-tolley), he introduced the concept of using pgTap, a set of Postgres functions designed for writing unit tests within the database. This post will serve as a supplement to [Josh's blog, Using pgTAP to automate database testing
](https://www.endpointdev.com/blog/2022/03/using-pgtap-automate-database-testing/), focusing on setting up pgTap for testing postgres database.

#### pgTap in EpiTrax 
EpiTrax relies on Postgres and its functions, making pgTap an ideal tool for testing the platform's database functions, ensuring data integrity, and maintaining the robustness of the system. By utilizing pgTap, EpiTrax  efficiently validates various aspects of its database structure and behavior.

#### Installing & setting up pgTap
**Note**: make sure you have Postgres installed on your system. If you don't have it, you can follow [postgres documentation](https://www.postgresql.org/download/) to learn how to install it.

To install pgtap for Postgres, you will need to follow these steps:

1. download the pgtap source code from its GitHub repository

```bash
git clone https://github.com/pgtap/pgtap.git
```
2. Navigate to the pgtap directory

```bash
cd pgtap
```

3. Install the required dependencies for pgtap
```bash
make && make install
```

4. Finally, connect to your Postgres database using psql or any other Postgres client and run the following SQL command to create the pgtap extension:
```sql
CREATE EXTENSION pgtap;
```

Now you should have pgtap installed and ready to use in your Postgres database. In case you face issues with Installation visit [pgtap documentation](https://pgtap.org/documentation.html#installation) for further help.


####  Writing Simple Database tests with pgTap:
Test to check if a table exists:
```sql
SELECT plan(1);
SELECT has_table('public', 'your_table', 'Table your_table should exist');
SELECT finish();
```

Test to check if a column exists in a table:
```sql
SELECT plan(1);
SELECT has_column('public', 'your_table', 'your_column', 'Column your_column should exist in your_table');
SELECT finish();
```

Test to check if a function returns the expected result:
```sql
SELECT plan(1);
SELECT is(your_function(), expected_result, 'your_function() should return expected_result');
SELECT finish();
```

Test to check if a trigger is triggered:
```sql
SELECT plan(1);
SELECT has_trigger('public', 'your_table', 'your_trigger', 'Trigger your_trigger should exist on your_table');
SELECT finish();
```

Test to check if a constraint is enforced:
```sql
SELECT plan(1);
SELECT has_fk('public', 'your_table', 'referenced_table', 'your_column', 'Constraint should exist between your_table and referenced_table');
SELECT finish();
```

#### Organizing and Naming your test files based on Test Anything Protocol (TAP)

Test Anything Protocol (TAP) is a convention for naming test files and organizing them within a project directory structure. The naming convention involves adding a numeric prefix to the test file name to indicate the order in which the tests should be run. For example, 00-test.sql is the first test file to be executed, followed by 01-another-test.sql, and so on.

The project directory structure usually includes a directory called t (short for "test") under the project root directory. This t directory contains all the test files following the TAP naming convention.

Using this structure makes it easier to maintain and organize tests, as well as to run them in the correct order. This is especially important when tests depend on the results of previous tests, or when you want to ensure that tests are executed in a specific sequence.

Here's an example of a project directory structure using the TAP-related naming convention:
```
my_project/
│
├─ src/
│   ├── function1.sql
│   ├── function2.sql
│   └── function3.sql
│
└─ t/
    ├── 00-test.sql
    ├── 01-another-test.sql
    └── 02-yet-another-test.sql
```
In this example, the project contains a src directory for the source code (database functions) and a t directory for the test files following the TAP naming convention.


#### Running your tests using pg_prove

Now that we have written some tests using pgTAP, let's see how we can run them. We'll use pg_prove, a utility included with pgTAP, to automate the process and get a summary of the results.

To run your tests with pg_prove, you'll need to specify the name of the database you want to connect to and the path to your test file. For example, if your test file is located at t/00-test.sql and your database is named epitrax_db, you can run the following command:

```bash
pg_prove -d epitrax_db t/00-test.sql
```
When you run this command, pg_prove will execute all the tests in the specified file and print a summary of the results. The output will include the number of tests run, the number of tests passed, the number of tests failed, and any diagnostic messages or errors that were encountered.

Here's an example of what the output might look like:

```bash
t/00-test.sql .. ok
All tests successful.
Files=1, Tests=5,  0 wallclock secs ( 0.01 usr  0.00 sys +  0.02 cusr  0.00 csys =  0.03 CPU)
Result: PASS
```
In this example, pg_prove ran one test file (00-test.sql) and executed 5 tests. All of the tests passed, so the output shows that the result was PASS.

If any of the tests fail, pg_prove will print a detailed report of the failures, including any error messages or diagnostic information. This can help you quickly identify and fix any issues in your code.

Using pg_prove to automate your tests can save you a lot of time and effort, especially if you have a large number of tests to run. It also makes it easy to integrate your tests into your build process or continuous integration pipeline.


#### Conclusion:
pgTap database unit tests provide numerous benefits, including ensuring code quality and simplifying the testing process. This guide should serve as a starting point for setting up pgTap, and we encourage you to explore the [pgTap documentation](https://pgtap.org/documentation.html#usingpgtap) and [Josh Tolley's blog post on Using pgTAP to automate database testing](https://www.endpointdev.com/blog/2022/03/using-pgtap-automate-database-testing/) for more in-depth information on writing and running tests with pgTap. By integrating pgTap in projects like EpiTrax, it's possible to improve overall database performance, stability, and security.
