---
title: "Testing user-defined functions with pgTAP"
author: Theo Dimov
featured:
  image_url: /blog/2023/09/testing-user-defined-functions-with-pgtap/people-toy-art-sale-buy-games-998783-pxhere.com.jpg
tags:
- sql
- postgres
- database
- testing
date: 2023-20-08
---


### Testing user-defined functions with pgTAP

For those interested in a great introduction to the pgTAP protocol, please read over my colleague [Josh Tolley's](https://www.endpointdev.com/team/josh-tolley/) article, 
[using pgTAP to automate database testing](https://www.endpointdev.com/blog/2022/03/using-pgtap-automate-database-testing/), for why and how to use pgTAP for your database unit
tests. Also check out [Edgar Mlowe's](https://www.endpointdev.com/team/edgar-mlowe/) article on [how to set up pgTAP for writing PostgreSQL database unit tests](https://www.endpointdev.com/blog/2023/04/pgtap-for-database-unit-tests/). 
Building off of them, I want to demonstrate another example of how to test user-defined stored functions.

First we’ll go over a few basic pgTAP functions that are useful in testing the existence of functions and procedures. Then we’ll use the PostgreSQL port of the Sakila sample 
database for MySQL, called Pagila. We’ll construct two functions and go over a single test case. Using basic Postgres tools, I’ll walk through a few methods of calling and testing
our functions. Finally, we’ll go over a more concise way of testing all cases for said functions. Feel free to work alongside this article and hopefully leave with a comfortable 
idea of how to construct unit test files for your database.

### Functions:

*Note: If performing this first example, remember to have the pgTAP extension in your schema and perform it in a transaction (I’ve omitted `BEGIN` and `ROLLBACK`). Also use `SELECT
plan(<number of tests you’ll run>)` when running the pgTAP functions.*

Starting off, let's create a basic addition function that returns an INTEGER value:

```postgresql
CREATE OR REPLACE FUNCTION add_numbers(
    num1 INTEGER,
    num2 INTEGER
) 
RETURNS INTEGER 
LANGUAGE plpgsql AS $$
BEGIN
    RETURN num1 + num2;
END;
$$;
```
To test this user-defined function, a few of the most relevant functions in pgTAP we can use are:

#### `has_function()`

Variations: 
```postgresql
SELECT has_function( :schema, :function, :args, :description );
SELECT has_function( :schema, :function, :args );
SELECT has_function( :schema, :function, :description );
SELECT has_function( :schema, :function );
SELECT has_function( :function, :args, :description );
SELECT has_function( :function, :args );
SELECT has_function( :function, :description );
SELECT has_function( :function );
```

Example:
```postgresql
SELECT has_function('your_schema', 'add_numbers', ARRAY['INTEGER','INTEGER']);   -- default description used
```
Results:
```postgresql 
ok 1 - Function add_numbers(INTEGER, INTEGER) should exist
```

Parameters
```
:schema
    Name of a schema in which to find the function.
:function
    Name of a function.
:args
    Array of data types of the function arguments.
:description
    A short description of the test.
```

`has_function()` is useful in checking the existence of a specific function. If you want to parse an entire schema, `functions_are()` is your command with pretty straightforward parameters.

#### `functions_are()`
Variations: 
```postgresql
SELECT functions_are( :schema, :functions, :description );
SELECT functions_are( :schema, :functions );
SELECT functions_are( :functions, :description );
SELECT functions_are( :functions );
```
Example:
```postgresql
SELECT functions_are('your_schema', ['add_numbers', <All other functions need to be listed as well>]);   -- default description used
```
Parameters
```
:schema
    Name of a schema in which to find functions.
:functions
    An array of function names.
:description
    A short description of the test.
```
#### `ok()` and `is()`

`ok()` and `is()` have similar a function with slightly different parameters:
```postgresql
SELECT ok( :boolean, :description );
```
Example:
```postgresql
SELECT ok(add_numbers(5,5)=10, 'add_numbers correctly works');
```
Parameters
```
:boolean
    A boolean value indicating success or failure.
:description
    A short description of the test.
```
```postgresql
SELECT is(   :have, :want, :description );
```
Example:
```postgresql
SELECT is(add_numbers(5,5), 10, 'add_numbers correctly works');
```

You can find functions that cover pretty much anything in PostgreSQL here on [pgTAP's documentation site](https://pgtap.org/documentation.html) 


### Testing more complex user-defined stored functions:

An existing client product of ours, utilizes a specific function that also calls several other functions depending on its given argument. This function is called by the application
and is passed an INTEGER as an argument from which the function bases an initial SELECT query’s WHERE condition on, in this case `WHERE id = [argument]’. Variables are then assigned
column values from this queried table. These variables are then used as the conditions to `PERFORM` functions that change parts of the database.

When testing this sort of scenario, it became apparent that I needed a set of test data, an ability to track that test data, run the function with the data, and test to see if the 
changes are correctly, or incorrectly, performed. 

The nice thing about pgTAP is that unit tests are meant to be rollbacked leaving the database as you found it. When faced with a more complex function that nests other functions which
loop through multiple tables, it may make more sense to fill those tables temporarily with the data required for the tests. 

Let's take a nostalgia trip and imagine we’re operating a DVD rental store. The Pagila sample database, which you can download on GitHub, represents our scenario. It comes populated
and we’ll construct a function which utilizes other functions which perform changes on multiple tables.

Say the DVD rental shop gives extensions of rentals for special occasions, one being that a DVD was bought on Christmas week. Suppose we have an initial function that checks if a new
DVD is rented on one of these special occasions. It then calls another function that will extend the return date, based on the specific occasion:

```postgresql
CREATE OR REPLACE FUNCTION extension_check(_rental_id INTEGER)
    RETURNS void
    LANGUAGE plpgsql
AS $function$
DECLARE
    _rental_date date;
    _inventory_id INT;
    _customer_id INT;
    _return_date date;
    christmas_week date;
BEGIN

    SELECT INTO _rental_date
    rental_date FROM rental 
    WHERE rental_id = _rental_id;

    IF EXTRACT(YEAR FROM _rental_date) = EXTRACT(YEAR FROM CURRENT_DATE) AND
       _rental_date <= (EXTRACT(YEAR FROM CURRENT_DATE)::text || '-12-25')::date AND
       _rental_date >  (EXTRACT(YEAR FROM CURRENT_DATE)::text || '-12-25')::date - INTERVAL '7 days' THEN
        	PERFORM christmas_extension(_rental_id);
    END IF;
END;
$function$;

CREATE OR REPLACE FUNCTION christmas_extension(_rental_id INTEGER)
    RETURNS void
    LANGUAGE plpgsql
AS $function$
DECLARE
    _rental_date date;
    _return_date date;
BEGIN
    SELECT return_date FROM rental WHERE rental_id = _rental_id INTO _return_date;

    IF _return_date IS NULL THEN
        UPDATE rental SET return_date = rental_date + INTERVAL '10 days' WHERE rental_id=_rental_id; 
    ELSE 
        UPDATE rental SET return_date = return_date + INTERVAL '10 days' WHERE rental_id=_rental_id; 
    END IF;
END;
$function$;
```

The initial function `extension_check`, simply checks if the rental was checked out on the week prior to and on Christmas (It’s a really dedicated DVD shop). We can also assume a
function like this has other scenarios where it would extend rental dates but we’ll just show one for this exercise. `christmas_extension` is our one extension function that extends
the return date by ten days.

To hold our unit test, we’ll create a file fittingly named `extenstion_unit_tests.sql`. A problem with the current sample database is that we can’t really test out the function
directly since the dates don’t extend to the current year. Rather even if they did, we don’t want to directly affect the existing data especially if the dates were updated and the
database was in production use. 

Relatively basic but handy Postgres tools let us create test cases which we can pass to the functions. Afterwards, we can use pgTAP functions to confirm that our user-defined functions
`extension_check` and `christmas_extension` properly worked.

For test cases in our new file, `extension_unit_tests.sql`, we’ll need a way to create and track them. For this, we’ll use a `temporary table` to track the test ids and a `PROCEDURE`
which can be called at any point to create the test cases. After that, we’ll simply call the procedure and run the user-defined function `extension_check`. Finally test it’s existence,
test it’s result, and rollback our changes.

```postgresql
BEGIN;

CREATE TEMPORARY TABLE test_instance_references (
    test_rental_id INT PRIMARY KEY,
    test_number INT
);


CREATE OR REPLACE PROCEDURE fill_test_data (
    _rental_date DATE,
    _test_number INT
)
LANGUAGE PLPGSQL
AS $procedure$
DECLARE 
    _address_id INT;
    _store_id INT;
    _staff_id INT;
    _inventory_id INT;
    _customer_id INT;
    _rental_id INT;
BEGIN

    SELECT nextval('customer_customer_id_seq1'::regclass) INTO _customer_id;
    SELECT nextval('rental_rental_id_seq'::regclass) INTO _rental_id;
    SELECT nextval('inventory_inventory_id_seq'::regclass) INTO _inventory_id;
    SELECT store_id FROM store LIMIT 1 INTO _store_id; 			-- any store will do
    SELECT address_id FROM address LIMIT 1 INTO _address_id; 		-- any address will do
    
    INSERT INTO customer (customer_id, store_id, first_name, last_name, address_id)
    VALUES (
        _customer_id,
        _store_id,
        'Test First Name',
        'Test Last Name',
        _address_id
    );

    INSERT INTO inventory (inventory_id, film_id, store_id)
    VALUES (
        _inventory_id,
        (SELECT film_id FROM film LIMIT 1),     -- random film
        _store_id
    );
    
    INSERT INTO rental (rental_id, rental_date, inventory_id, customer_id, staff_id)
    VALUES (
        _rental_id, 
        _rental_date,
        _inventory_id,
        _customer_id,
        (SELECT staff_id FROM staff WHERE store_id = _store_id LIMIT 1)   -- select random staff member from store
    );

    INSERT INTO test_instance_references (test_rental_id, test_number)
    values (
        _rental_id, 
        _test_number
    );

END;
$procedure$;

CALL fill_test_data('2023/12/25'::date, 1);  -- Fill the db with our test data

SELECT extension_check((SELECT test_rental_id FROM test_instance_references WHERE test_number = 1));   -- Call our user-defined function

SELECT plan(2);    -- State the number of tests we'll be performing

SELECT has_function( 
    'extension_check',    
    ARRAY['int']
);

SELECT is(
    (SELECT return_date FROM rental WHERE rental_id in (SELECT test_rental_id FROM test_instance_references WHERE test_number = 1))::date, 
    ('2023/12/25'::date + INTERVAL '10 DAYS')::date,
    'Checking test data 1, week of Christmas'
);

 
ROLLBACK;
```



By design pgTAP tests are performed in a transaction block with a ROLLBACK at the end to reverse all changes. Our first transaction is the creation of a temporary table called
`test_instance_references` which will hold the id’s of the sample data we insert specifically in the rental table. This way we keep track of our specific test cases through
their primary identifier. 

Our PROCEDURE works similar to a function, but where a function may have issues being called in a transaction block through pgTAP’s command line `pg_prove`, the use of a procedure
and its CALL command is far more reliable. 

In our example, the procedure simply adds in all the required test data. Note the insertion of test data into other tables that are referenced in `rental`, as well as an insert into
the temporary table for tracking. To avoid using any existing data in the db,  references are also test samples, like for the customer. Some however are selected from existing tables.
It’s important to make sure you’re not affecting real data in the database in the case that a transaction fails. The example is obviously lax when it comes to that, specifically with
the references to `store` and `address`, so please take note in your own unit tests to be careful when referring to existing data.

After we’ve established our procedure, we’re ready to run the tests. The pgTAP function `plan()` defines for pgTAP how many unit tests we are going to run. For the first example we run
two tests. First we call the procedure `fill_test_data` which populates the database with test data and the temporary table to track that data. 

Our first test is to check if the function exists. pgTAP’s `has_function` function is perfect for this. Pretty self explanatory as a function and more details can be found in the introduction
of this article. 

Our procedure is then called with a date for the test rental. This test rental’s id is saved into the temporary `test_instance_references` table which is then passed to the main function we
want to test, `extension_check`. We call this function with the SELECT command, and immediately test the outcome with pgTAP’s `is()`. Our `:have` parameter holds to the return_date of our
test rental which is tested to see if it’s been correctly extended by 10 days. Our final parameter is the description which will be returned in the outcome of pgProve if the test fails. 

The ROLLBACK again is meant to clean the database of all test data.

Let's run this unit test on the command line, with `pg_prove`:
```
pg_prove -d <your_database> <path_to_your_unit_test>/extenstion_unit_tests.sql
```
We should see these results:

```
extenstion_unit_tests.sql .. ok 
All tests successful.
Files=1, Tests=2,  0 wallclock secs ( 0.01 usr +  0.00 sys =  0.01 CPU)
Result: PASS
```

Congrats! We’ve tested out a single case for a function. However, what if we want to test all possible cases for this function to be sure it performs correctly?


To do this, we can alter the procedure `fill_test_data` to loop through a date range given to it through the arguments `_start_date` and `_end_date`.  For our scenario we’ll provide it with
the week of Christmas, but it’ll work for any date range provided the rental store gives extensions for DVDs rented on other dates.

Instead of passing a test number as an argument, we can simply initialize it as a variable that’s incremented with every loop. Inside the `WHILE` loop, every iteration will populate the db with
the test data, perform `extension_check` with the test rental id, and increment the date and test number. 

We’ll end the transaction a little differently by setting our pgTAP plan equal to the number of tests we have in our temporary table, to avoid hard coding our plan count. We’ll also add one for
checking for its existence with `has_function`. 

Finally, our `is()` will also iterate through our temporary table and perform a check in the rental table to confirm that the return date has been correctly extended by ten days. 

```postgresql
BEGIN;

CREATE TEMPORARY TABLE test_instance_references (
    test_rental_id INT PRIMARY KEY,
    test_number INT,
    start_date DATE
);


CREATE OR REPLACE PROCEDURE fill_test_data (
        _start_date DATE,
        _end_date DATE
    )
    LANGUAGE PLPGSQL
    AS $procedure$
    DECLARE 
        _address_id smallint;
        _store_id smallint;
        _inventory_id INTEGER;
        _customer_id INTEGER;
        _rental_id INTEGER;
        _test_number INT;
    BEGIN
        _test_number := 1;

        WHILE _start_date <= _end_date LOOP
            SELECT nextval('customer_customer_id_seq1'::regclass) INTO _customer_id;
            SELECT nextval('rental_rental_id_seq'::regclass) INTO _rental_id;
            SELECT nextval('inventory_inventory_id_seq'::regclass) INTO _inventory_id;
            SELECT store_id FROM store LIMIT 1 INTO _store_id; 			-- any store will do
            SELECT address_id FROM address LIMIT 1 INTO _address_id; 		-- any address will do
        
            INSERT INTO customer (customer_id, store_id, first_name, last_name, address_id)
            VALUES (
                _customer_id,
                _store_id,
                'Test First Name',
                'Test Last Name',
                _address_id
            ); --

            INSERT INTO inventory (inventory_id, film_id, store_id)
            VALUES (
                _inventory_id,
                (SELECT film_id FROM film LIMIT 1),     -- random film
                _store_id
            ); --
            
            INSERT INTO rental (rental_id, rental_date, inventory_id, customer_id, staff_id)
            VALUES (
                _rental_id, 
                _start_date,
                _inventory_id,
                _customer_id::smallint,
                (SELECT staff_id FROM staff WHERE store_id = _store_id LIMIT 1)   -- select random staff member from store
            );

            INSERT INTO test_instance_references (test_rental_id, test_number, start_date)
            VALUES (
                _rental_id, 
                _test_number,
                _start_date
            );

            PERFORM extension_check(_rental_id);

            _start_date := _start_date + INTERVAL '1 day';
            _test_number := _test_number + 1;
        
        END LOOP;
    END;
$procedure$;

CALL fill_test_data(('2023-12-25'::date - INTERVAL '6 days')::date, '2023-12-25'::date);

SELECT plan(count(*)::INTEGER + 1) from test_instance_references;

SELECT * from test_instance_references;

SELECT has_function(
    'extension_check',
    ARRAY['int']
    -- Description optional - default description usually substantial 
);

SELECT is(
    (SELECT return_date FROM rental WHERE rental_id = tf.test_rental_id)::date, 
    (tf.start_date + INTERVAL '10 DAYS')::date
) 
FROM test_instance_references as tf;


ROLLBACK;
```


Our results should be:
```
$ pg_prove -d <your_database> <path_to_your_unit_test>/extenstion_unit_tests.sql
extenstion_unit_tests.sql .. ok   
All tests successful.
Files=1, Tests=8,  0 wallclock secs ( 0.02 usr +  0.00 sys =  0.02 CPU)
Result: PASS
```
Conclusion:

As a protocol, pgTAP provides a great list of functions and commands to easily and clearly test all aspects of a database. As I’ve been tasked with more implementations of unit tests for user-defined
functions, I thought it helpful to share some useful methods. 

As someone who found pgTAP fairly straightforward the challenge of intertwining those functions in a repeatable way was what drove me to write this article and hopefully make it easier for the next
coder to play around and get the most out of this simple but intuitive  `Test Anything Protocol`.

Feel free to share your thoughts and comments below on any more useful tips on pgTAP or general Postgres unit testing.
