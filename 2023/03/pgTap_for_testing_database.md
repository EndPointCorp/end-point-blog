---
author: Edgar Mlowe
title: 'How to Set Up pgTAP for Writing Postgres Database unit tests'
tags:
- Postgres
- PL/pgSQL
- SQL
- pgTAP

date: 2023-03-20
featured:
  endpoint: true
description: This article walks readers through how to setup pgTAP a unit testing framework for Postgres.
---




### How to Set Up pgTAP for Writing Postgres Database unit tests

#### Introduction
In a previous blog post, [Josh Tolley](https://www.endpointdev.com/team/josh-tolley) introduced the concept of using pgTAP, a set of Postgres functions designed for writing unit tests within the database. This post will serve as a supplement to [Josh's blog, Using pgTAP to automate database testing
](https://www.endpointdev.com/blog/2022/03/using-pgtap-automate-database-testing/), focusing on setting up pgTAP for testing Postgres database.

#### pgTAP in EpiTrax 
EpiTrax relies on Postgres and its functions, making pgTAP an ideal tool for testing the platform's database functions, ensuring data integrity, and maintaining the robustness of the system. By utilizing pgTAP, EpiTrax  efficiently validates various aspects of its database structure and behavior.

#### Installing & setting up pgTAP
**Note**: make sure you have Postgres installed on your system. If you don't have it, you can follow [postgres documentation](https://www.postgresql.org/download/) to learn how to install it.

To install pgTAP for Postgres, you will need to follow these steps:

1. download the pgTAP source code from its GitHub repository

```bash
git clone https://github.com/pgtap/pgtap.git
```
2. Navigate to the pgtap directory

```bash
cd pgtap
```

3. Install the required dependencies for pgTAP
```bash
make && make install
```

4. Finally, connect to your Postgres database using psql or any other Postgres client and run the following SQL command to create the pgTAP extension:
```sql
CREATE EXTENSION pgtap;
```

Now you should have pgTAP installed and ready to use in your Postgres database. In case you face issues with Installation visit [pgtap documentation](https://pgtap.org/documentation.html#installation) for further help.


####  Writing Simple Database tests with pgTAP:
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

#### More pgTAP Tests...

##### Test to check if a trigger is triggered:
Consider the following example. We have a table named employees and a table named audit_log. When a new employee is added to the employees table, a trigger named insert_employee_trigger fires and logs the new employee's ID and creation timestamp in the audit_log table. Let's test if the trigger gets fired and produces the expected outcome.


1. Create the tables:
```sql
CREATE TABLE employees (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE audit_log (
  id SERIAL PRIMARY KEY,
  employee_id INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL
);

```

2. Create the trigger and trigger function:
``` sql
CREATE OR REPLACE FUNCTION insert_employee_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO audit_log (employee_id, created_at) VALUES (NEW.id, NOW());
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER insert_employee_trigger
  AFTER INSERT ON employees
  FOR EACH ROW
  EXECUTE FUNCTION insert_employee_trigger_function();
```
3. Now, write a test using pgTAP to test the trigger:
``` sql
-- Set the test plan
SELECT plan(1);

  -- Prepare test data and perform operations that should fire the trigger
  INSERT INTO employees (name) VALUES ('John Doe');


-- Check if the desired outcome of the trigger has occurred
SELECT is( 
  (SELECT name FROM employees WHERE id = (SELECT employee_id FROM audit_log ORDER BY id DESC LIMIT 1)),
  'John Doe',
  'The insert_employee_trigger should have been fired and produced the expected outcome'
);
```


##### Test to check if a constraint is enforced:

Let's assume we have the following two tables. `orders` table with columns `id`, `customer_id`, and `amount`. `customers` table with columns `id` and `name`.

There is a foreign key constraint between the `orders` table and the `customers` table on the `customer_id` column.

1. First, create the two tables and add the foreign key constraint:

```sql
CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id INTEGER REFERENCES customers(id),
  amount INTEGER
);
```

2. Now, create a test script named fk_test.sql with the following content
``` sql
BEGIN;

-- Create test data in customers table
INSERT INTO customers (id, name) VALUES (1, 'Customer 1');

-- Declare the number of tests
SELECT plan(1);

-- Attempt to insert an order with an invalid customer_id
-- This should fail due to the foreign key constraint
SELECT throws_ok(
    'INSERT INTO orders (id, customer_id, amount) VALUES (1, 969, 100);',
    '23503',
    'insert or update on table "orders" violates foreign key constraint "orders_customer_id_fkey"'
);

-- Conclude the test and discard changes
SELECT finish();
ROLLBACK;
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
pgTAP database unit tests provide numerous benefits, including ensuring code quality and simplifying the testing process. This guide should serve as a starting point for setting up pgTAP, and we encourage you to explore the [pgTap documentation](https://pgtap.org/documentation.html#usingpgtap) and [Josh Tolley's blog post on Using pgTAP to automate database testing](https://www.endpointdev.com/blog/2022/03/using-pgtap-automate-database-testing/) for more in-depth information on writing and running tests with pgTAP. By integrating pgTAP in projects like EpiTrax, it's possible to improve overall database performance, stability, and security.
