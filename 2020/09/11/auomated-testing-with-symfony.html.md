---
author: "Kevin Campusano"
title: "Automated Testing with Symfony"
tags: testing, automated-testing, unit-testing, functional-testing, symfony, phpunit, php
---

![Banner](auomated-testing-with-symfony/banner.png)
https://stackoverflow.com/questions/61400/what-makes-a-good-unit-test

# An introduction to automated testing by example with the Symfony framework

Testing is an immense topic in software engineering. A lot has been written and a lot of experience has been collected about it by the greater software development community. There are many types of testing that can be done, many techniques and approaches, filosofies and strategies.

With a big topic such as this, it would be futile to try to touch on every aspect of it in an article like this. Instead, I'll try to take a pragmatic approach and discuss a testing strategy that I've found success with in the past, and the amount of testing with which I feel confortable putting code into production. This article could also serve as a sort of introduction to automated testing, where we use the Symfony framework as a vehicle to explore various types of testing without really diving too deep into edge cases or framework specifics, but instead leaning more into the concepts and design decissions that go into writing them. Still, we will make sure to have a running and competent test suite by the end of it.

So we're going to talk about automated testing, which in its own right is a very important part of the bigger discipline of software testing; and a topic that, as a developer (and as such, responsible for implementing this type of tests), I'm passionate about.

Let's get started.

# What we're going to be talking about

For web applications, as far as automated tests go, there are three categories which I think are essential to have and complement each other very well:

- Unit tests: This is the most low level and, in my opinion, the most important type of developer tests. Unit tests don't only make sure that the system does what it is supposed to do, but also that it is correctly factored, where individual components are decoupled. They need to be that way because unit tests focus on exercizing specific classes and methods running in complete isolation, which becomes harder if the class you want to test is very tighly coupled with its dependencies/collaborators. These tests validate the behavior of basic programing constructs like classes and the algorithms within them.

- Integration tests: These tests go one level of abstraction higher when compared to unit tests. They test how the system interacts with external components. In this article, we're going to use integration level tests to validate functionality that has to do with interaction with a database and an external Web API. 

- Functional tests: These are the tests at the highest level of abstraction. These try to closely mimic the user's experience with the system by interacting with it as a user would. In terms of a web application, this means making HTTP requests, clicking buttons, filling out and submitting forms, inspecting HTML results, etc.

If we can build an automated tests suite that provides good coverage, and exercizes the system at these three levels, I would feel confident that the sytem under test can work properly in production. An added bonus is that with tests like these, we would have a live documentation of the system, the features it provides and, to an extent, how it works.

Virtually all serious software development ecosystems have at least one automated testing framewoek or library which we can leverage to write our tests. For our purposes in this article, we're going to be using the Symfony PHP framework which integrates beatifully with PHPUnit to provide developers with an effective, and even fun way to write tests.

# Getting to know the System Under Test

In order to help illustrate the topic by showing practical examples, I've prepared a simple weather app. The app is very straigt forward. It only offers one feature: it will allow the user to see the current weather of a given city in the US. It does this by presenting a form where people can type in a city and a state, submit it, and get their information back.

The app obtains this information by contacting the OpenWeatherMap Web API. It also stores all requests in a database for posterity.

The site is a typical Symfony web app. It uses the MVC pattern and Domain Driven Design concepts like entities, repositories and services. Here's a diagram explaining the static structure of the app:

STATIC DIAGRAM HERE

For a simple app like this, our entities are litle more than containers for our data, the repositories take care of encapsulating the database access logic, and the services contain the logic that leverages the other objects to fulfill our business logic.

The front end, as you'll see, is super simple. Not really any client side JavaScript logic to speak of (stay tuned for another blog post about unit testing JavaScript front ends!). So this is more of an old-school, backend only app. Good enough for what we're trying to do here though.

So our only use case is the current weather request. We do have, however, a couple alternate scenarios within that use case. First, if the user types in an invalid US state code, the app will show a validation error. Second, if the user inputs a city that does not exist (or, more specifically, one that the OpenWeatherMap Web API can't find), the app will show another error message.

To get a better idea of how the classes interact with each other, here's an sequence diagram detailing how the app serves the main weather query scenario:

SEQUENCE DIAGRAM HERE

As you can see, the controller receives the request and calls upon the service class to validate the input and retrieve the information for the city specified by the user. Then, the service takes care of orchestrating the domain model objects like entities, repositories and other services in order to fulfill the request and return back the weather information that eventually gets rendered with the template.

You can explore the source code for our demo app here: LINK TO SOURCE CODE HERE. The interesting files are under the `src` and `template` directories. contents should be self explanatory: `src/Controller` contains our controller, `src/Service` contain the service classes, and so on.

If you want to run it, you need to have installed PHP, Composer, the Symfony CLI and these extensions: php-sqlite3, php-xml, php-curl.

> If you like Docker, there's a Dockerfile in the repo that you can use to fire up a container ready for running the app.

Once you've got all that set up, the app can be run by:

1. Cloning the git repo with `git clone REPOSITORYURL`.
2. Install dependencies with `composer install`.
3. Initialize the database with `bin/console doctrine:schema:create`.
4. Fire up the application with `composer serve`.
5. Go to `localhost:3000`.

You should now be able to see something like this:

SCREENSHOT OF APP HERE

Ok now that we understand our system under test, what it does and how it works, we're ready to test it.

# Unit tests

## Surveying a class to write unit tests for it

I'd like to start by looking into the simplest kind of tests that we need to write for this app. Those would be unit tests for our entity classes. These tests are simple because the classes that they exercise are simple as well. If you look at our `Weather` and `WeatherQuery` classes inside `src/Entity` you'll see that they contain little more than some fields with their corresponding accessors and some convenience factory methods. They also don't have any dependencies, which is convenient because our test fixtures wont have to account for that.

So, the first step that I always like to take is inspect the class that I'm about to test, to try and determine what's interesting from a testing perspective. I try to think about what's the main responsibility of the class, what sort of logic is actually adding value, what things could be broken inadvertently by other developers, what potential changes in the code would I like the test suite to alert developers of (by failing tests!), what features would benefit from havng their API captured/documented in the form of an automated test. I ask myself these questions because it often times is not feasible to achieve 100% code coverage with unit tests (or with any kind of tests, for that matter). So, in those cases when we need to be strategic as to what tests we write, I try to write those that will add the most value. When faced with the reality of limited resources, I try to approach these things from a "bang for the buck" angle.

With that in mind, if we look at our `WeatherQuery` class, here are the things that come to my attention:

**First**, there are some fields annotated with validation logic. That's the `@Assert` comments on top of the field definitions. For example:

```php
/**
* @ORM\Column(type="string", length=255)
* @Assert\NotBlank(message="The city should not be blank.")
* @Assert\Type("string")
*/
private $city;
```

There are a few more. It'd be interesting to test those validation rules.

**Second**, for every field, there are accessor methods defined as well. That is, getters and setters like these:

```php
public function getState(): ?string
{
    return $this->state;
}

public function setState(string $state): self
{
    $this->state = $state;

    return $this;
}

```

These methods are very simple. If we were going for 100% coverage, we may have wanted to exrcize those accessors. Being the strategic developers that we are though, I think we can ingnore those for now. The logic is very simple, not really a lot of oportunity for things to go wrong here.

These types of methods become even less relevant in other languages like C# or Ruby which support accessors as language level constructs. Testing those would be a moot point in those languages, since it would mean testing language/framework features, and not code that we own. There's no good reason to do that.

**Third**, there's a convenience factory method defined at the bottom of the class. It looks like this:

```php
public static function build(string $city, string $state): WeatherQuery
{
    $city = ucwords($city);
    $state = strtoupper($state);

    $weatherQuery = (new WeatherQuery())
        ->setCity($city)
        ->setState($state)
        ->setCreated(new DateTime())
    ;

    return $weatherQuery;
}
```

This `build` method has some interesting logic to it. There's some preprocessing that happens to the input parameters. It'd also be interesting for a test to exercize that the resulting object is correctly constructed.

## Deciding what tests to write

Ok so by analyzing our class we've identified parts of it that are interesting to test. We want to test the validation logic and the `build` method.

Let's start with the build method as that one's easier.

Now that we've identified the unit that we will test, we need to come up with test cases that exercize it in various ways. Looking at `build`'s code, line by line, I can come up with a few interesting test cases. Here's my though process:

The first thing that I notice is that the method takes two parameters, city and state, and does this with them:

```php
$city = ucwords($city);
$state = strtoupper($state);
```

So that's something that the test suite should validate, that these values get processed like this.

There's also this part here where the object to return gets constructed:

```php
$weatherQuery = (new WeatherQuery())
    ->setCity($city)
    ->setState($state)
    ->setCreated(new DateTime())
;
```

This code is taking the parameters and assigning them to fields in the object. That'd be something interesting to validate. There's also a "created" field that gets initialized with the current date and time. Also interesting.

Having seen that, I can come up with this set of test cases for the `build` method:

- Test that it assigns the parameters to the correct fields in the resulting object.
- Test that it capitalizes the city.
- Test that it capitalizes the state.
- Test that it sets the current moment as the "created" field in the resulting object.

## Deciding what tests not to write

There are other things that this method does that we could write tests for. For example, the method is supposed to return an object of type `WeatherQuery`. The method is also supposed to only accept strings as parameters. If we were writing old PHP, somebody could try to make an argument here for writing such tests. Test cases like "test that the build method returns an instance of type WeatherQuery" or "test that the build method only works with string paramenters", for example. We however, decided to make the code correct by construction by type hinting the return value and the parameters for this method. This makes it unnecessary to write such tests because we are already leveraging PHP's language features to validate these rules for us. In other words, because of how the method is written, the scenarios where non string values are passed as arguments to it, or where it returns something other than a `WeatherQuery`, are simply impossible.

This type of test already is trivial and adds questionable value. But by writing our code like this, we've made it obsolete. Statically typed languages also make these types of testing gymnastics useless.

## Tactics for writing the unit tests

I think that this addresses the main concerns of this method. So now let's write that in PHP with PHPUnit.

### Where to put them and what to name them

In the demo application that hopefully you've downloaded and explored, we write our tests under the `tests` directory. This is the default location that Symfony gives us for our tests and I think it's a good one. For our unit tests, we put them in `tests/unit`. Tests for this class in particular go in the `tests/unit/Entity/WeatherQueryTest.php` file.

Notice our naming and file location convention. The name of the file that contains a given class' test cases is the same as the class itself, only with the word `Test` as a suffix. We've also made sure to mimic the project's `src` dierctory structure in our `tests/unit` directory. So, in this example, the `WeatherQuery` class is located in `src/Entity/WeatherQuery.php`. that means that its tests should live in `tests/unit/Entity/WeatherQueryTest.php`. Following this convention keeps things simple and easy to navigate and maintain.

### What a PHPUnit test class looks like

PHPUnit makes writing tests easy. A collection of tests are defined as a series of methods inside a class that extends the `PHPUnit\Framework\TestCase` class. Here's what our `WeatherQueryTest.php` file looks like:

```php
namespace App\Tests\Unit\Entity;

use PHPUnit\Framework\TestCase;

// ...

class WeatherQueryTest extends TestCase
{
    // build
    public function testBuildAssignsTheParametersToTheCorrectFields()
    {
        // ...
    }

    // ...
}
```

Notice how the test class name is, again, the same name of the class under tests, suffixed with the word `Test`. Notice how it extends from the `TestCase` and notice how our test methods (aka, test cases) all begin with the word `test`. This is necessary for PHPUnit. This is how we signal to it that this is, in fact, a test case that it needs to run.

### How to name the individual test methods

Another important thing to note is the naming convention that we're using here for our test methods. Remember the test cases that we came up with above:

- Test that it assigns the parameters to the correct fields in the resulting object.
- Test that it capitalizes the city.
- Test that it capitalizes the state.
- Test that it sets the current moment as the "created" field in the resulting object.

These are wordy descriptions of exactly what the test cases are about. Just by reading these, we need to be able to get a good idea of what the purpose of the test case is, and what's its expected outcome. For the same reasons of readability and self documentation, the names of our test methods in the actual test suite implementation need to be as close to that as possible. I've come up with these:

- `testBuildAssignsTheParametersToTheCorrectFields`
- `testBuildCapitalizesTheGivenCityParameter`
- `testBuildCapitalizesTheGivenStateParameter`
- `testBuildSetsTheCurrentMomentAsTheCreatedField`

They begin with the word `test` in order to fulfill PHPUnit's requirements. Then, they include as many details as possible on what they are about.

### The anatomy of a test case

When it comes to actually writing the tests, I put great focus on making them as easy to understand as possible. Test cases do not only serve the purpose of validating system behavior. They also can serve as a live documentaiton of the system's features, and, in the case of unit tests, its inner workings. To be able to fulfill that purpose, tests need to be easy to read, navigate, and understand.

That's why I always like to call attention to the general three steps that almost every test follows: "Setup", "Execise" and "Verify". Or, as I like to call them: "Arrange", "Act" and "Assert". So the first thing I do is add those three as comments in the test method body:


```php
public function testBuildAssignsTheParametersToTheCorrectFields()
{
    // Arrange
    // Act
    // Assert
}
```

"Arrange" is the step where we set up our test fixture. That is, we configure the world around the unit under test, the input, dependencies, etc; so that we can control for all the variables that go into the execution of the unit.

"Act" is quite simply where we invoke or otherwise have out unit under test be executed.

"Assert" is where we verify that the unit under test behaved correctly. That it met the test case's expectations. We normally do this by checking the outout of the method or some other side effect that its execution causes. 

> In the Behavior Driven Development world, "Given", "When" and "Then" are parallels for these. You may see that terminology used as well. The spirit is the same.


Usually the next most obvious step is Act. This example is like that: we just need to call our `build` method and capture its output. Adding that, our test method would look like this now:

```php
public function testBuildAssignsTheParametersToTheCorrectFields()
{
    // Arrange
    // Act
    $result = WeatherQuery::build($testCity, $testState);
    // Assert
}
```

By writing our Act portion, we discovered that we need parameters. AKA input values. That's what the Arrange step is for:

```php
public function testBuildAssignsTheParametersToTheCorrectFields()
{
    // Arrange
    $testCity = 'MyCity';
    $testState = 'ST';

    // Act
    $result = WeatherQuery::build($testCity, $testState);

    // Assert
}
```

Finally, we need to actually validate that the `build` method did what we expected. We do that by writing some assertions. What did we expect it to do though? Well, the name of the test method has the answer: we expect it to "assign the given parameters into the correct fields of the resulting object". In PHPUnit, we do it like so:

```php
public function testBuildAssignsTheParametersToTheCorrectFields()
{
    // Arrange
    $testCity = 'MyCity';
    $testState = 'ST';

    // Act
    $result = WeatherQuery::build($testCity, $testState);

    // Assert
    $this->assertEquals($testCity, $result->getCity());
    $this->assertEquals($testState, $result->getState());
}
```

PHPUnit has an extensive number of different types of assertion methods. In this case, we use one of the simpler omes: `assertEquals`. This method will compare two values and report the test as a failure if they are different. It will report it as a success if they are equal.

In this test case, we want PHPUnit to validate for us that the resulting object's `city` field is the same that we passed in. Same of the object's `state` field.

And that does it for our first unit test! We've prepared some input, called the unit that we wanted to test, and inspected its state to validate that it did what it was supposed to do.

### Running PHPUnit tests

Once again, Symfony makes it easy to write and run unit tests. By default, [Symfony projects created with either `symfony new my_project_name --full` or `composer create-project symfony/website-skeleton my_project_name`](https://symfony.com/doc/current/setup.html#creating-symfony-applications) already include the PHPUnit library and the configuration necessary to execute unit tests like this one. You can run it, along with all the others in this test class with this command.

```
bin/phpunit tests/unit/Entity/WeatherQueryTest.php
```

This will result in something like this:

```
$ bin/phpunit tests/unit/Entity/WeatherQueryTest.php
PHPUnit 7.5.20 by Sebastian Bergmann and contributors.

Testing App\Tests\Unit\Entity\WeatherQueryTest
........                                                            8 / 8 (100%)

Time: 64 ms, Memory: 8.00 MB

OK (8 tests, 9 assertions)
```

I prefer the [TestDox](https://en.wikipedia.org/wiki/TestDox) style ouput though, so I like to use this instead:

```
bin/phpunit --testdox tests/unit/Entity/WeatherQueryTest.php
```

Which gives us:

```
$ bin/phpunit --testdox tests/unit/Entity/WeatherQueryTest.php
PHPUnit 7.5.20 by Sebastian Bergmann and contributors.

Testing App\Tests\Unit\Entity\WeatherQueryTest
App\Tests\Unit\Entity\WeatherQuery
 ✔ Build assigns the parameters to the correct fields
 ✔ Build capitalizes the given city parameter
 ✔ Build capitalizes the given state parameter
 ✔ Build sets the current moment as the created field
...

Time: 68 ms, Memory: 8.00 MB

OK (8 tests, 9 assertions)
```

And this is where us giving those really long and detailed names to the test methods pays off. Now running a test suite results in output that reads in plain english and serves as a specification of sorts on how a given class works. Fulfilling the automated tests suite's secondary objective of serving as live documentation for the system.

### Other interesting details

Now that we've disccussed my though process for writing this first unit test, the rest of the `build` unit tests should be pretty self explanatory. They all follow the same pattern, the only difference is the Arrange and Assert parts, which change according to what the particular tests's purpose is.

For instance, notice how the `testBuildCapitalizesTheGivenCityParameter` test passes the `build` function `'my city'` as the value for the city paramenter. Then, it asserts that the return object's property was set to `My City`. Thus, assuring that the `$city = ucwords($city);` line in the `build` method's implementation is working properly. If somebody changes this by mistake, the test will break and let them know that they have to fix it.

Another interesting test case is this one: `testBuildSetsTheCurrentMomentAsTheCreatedField`. Here, we need to assert that the `WeatherQuery` object returned by the `build` method has its "created" field set to the current moment in time. Timestamps are so precise though, that one obtained before calling the method, and one obtained inside it, are different. We need to assert equality though. So, to deal with that, we use this variation of the `assertEquals` assertion:

```php
$this->assertEquals(
    (new DateTime())->getTimestamp(),
    $result->getCreated()->getTimestamp(),
    '', 1
);
```

This one tests for equality, but with a certain allowed difference. If the difference is within this margin of error, then the assertion deems that the two values are equal. Just what we need in this case. This basically says: "assert that the current timestamp and the resulting object's timestamp are 'pretty much' the same". That's as good a job as PHPUnit can do to for that assertion. Luckily, that's good enough for us. 

### Testing the same behavior with varying input

Ok now we've tested one piece of functionality defined within the `WeatherQuery` class. There is something else to test though, the validation rules. The class has several validation rules defined as annotations. We are able to define validation rules like this thanks to Symfony's Validator component. To exercise the rules, we need to use the `Symfony\Component\Validator\Validation` class. This is a concept and style very specific to Symfony. Here's what a test that exercises those validation values looks like:

```php
public function testValidation($city, $state, $expected)
{
    // Arrange
    $subject = WeatherQuery::build($city, $state);

    $validator = Validation::createValidatorBuilder()
        ->enableAnnotationMapping()
        ->getValidator();

    // Act
    $result = $validator->validate($subject);

    // Assert
    $this->assertEquals($expected, count($result) == 0);
}
```

If you are familiar at all with Symfony, then you may know what all this is about. If not, then it's not hard at all. We just need this recipe `Validation::createValidatorBuilder()->enableAnnotationMapping()->getValidator();` to obtain a `Validator` instance. We can pass a `WeatherQuery` object to it and it will validate it for us using the annotations defined within the class.

Now, that's how we validate an object in Symfony. However, validation is a common technique that's done regardless of framework. In general, to test validation rules, we use the same template for the test method: 1. we create the validation subject with some input data, 2. we call whatever component to validate said input data, and 3. we assert that the validation result is what we expect given the input.

This means that testing a set of validation rules boils down to runinng the same process over and over again with different input. The input is the only thing that varies. PHPUnit has the "Data Provider" concept which lends itself beautifully for these scenarios.

To illustrate this, let's continue with our validation example. Consider the annotation and signature of the test method:

```php
/**
* @dataProvider getValidationTestCases
*/
public function testValidation($city, $state, $expected)
{
    // ...
}
```

The `@dataProvider getValidationTestCases` annotation tells PHPUnit to look for a method named `getValidationTestCases` to obtain the list or sets of arguments to pass to the annotated test method.

Our `testValidation` method expects three parameters: a city, a state, and a boolean representing whether the validation should succeed or not. So, the `getValidationTestCases` need to provide them. Let's look at it now then:

```php
public function getValidationTestCases()
{
  return [
    'Succeeds when data is correct' => [ 'New York', 'NY', true ],
    'Fails when city is missing' => [ '', 'NY', false ],
    'Fails when state is missing' => [ 'New York', '', false ],
    'Fails when state is not a valid US state' => [ 'New York', 'AAA', false ],
  ];
}
```

As you can see, `getValidationTestCases` returns an associative array that contains four items. Each item's key is a description of the test case and the value is the data that makes up the test case. That data is what will get passed as parameters to `testValidation`. The keys are used in the TestDox output to make it more descriptive, like so:

```
$ bin/phpunit --testdox tests/unit/Entity/WeatherQueryTest.php
PHPUnit 7.5.20 by Sebastian Bergmann and contributors.

Testing App\Tests\Unit\Entity\WeatherQueryTest
App\Tests\Unit\Entity\WeatherQuery
...
 ✔ Validation with data set "Succeeds when data is correct"
 ✔ Validation with data set "Fails when city is missing"
 ✔ Validation with data set "Fails when state is missing"
 ✔ Validation with data set "Fails when state is not a valid US state"

Time: 68 ms, Memory: 8.00 MB

OK (8 tests, 9 assertions)
```

As you can see, this results in PHPUnit running the `testValidation` method four times, once per each test case defined in `getValidationTestCases`, using their corresponding data as parameters.



<!-- There's a slight mental mapping that we need to do when we talk about our three-tier testing conceptual model and Symfony's. In the Symfony world, they talk about two types of tests: unit tests and functional tests. That's the distiction that the frameworks makes implementation wise. In terms of our conceptual categorization that we did earlier, Symfony's "unit tests" are the same as the "unit tests" that we described. Our other two catergories: integration and functional, fall into the "functional" type of Symfony tests. We'll see how that pans out shortly. -->
