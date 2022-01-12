---
author: "Kevin Campusano"
title: "Database integration testing with .NET"
date: 2022-01-11
tags:
- dotnet
- integration
- database
- testing
github_issue_number: 1821
---

![Sunset over lake in mountains](/blog/2022/01/database-integration-testing-with-dotnet/banner.jpg)

<!-- Image by Zed Jensen, 2021 -->

[Ruby on Rails](https://rubyonrails.org/) is great. We use it at End Point for many projects with great success. One of Rails' cool features is how easy it is to write database integration tests. Out of the box, Rails projects come with all the configuration necessary to set up a database that's exclusive for the automated test suite. This database includes all the tables and other objects that exist within the regular database that the app uses during its normal execution. So, it is very easy to write automated tests that cover the application components that interact with the database.

[ASP.NET Core](https://dotnet.microsoft.com/en-us/apps/aspnet) (which is also great!), however, doesn't have this feature out of the box. Let's see if we can't do it ourselves.

### The sample project

As a sample project we will use a REST API that I wrote for [another article](https://www.endpointdev.com/blog/2021/07/dotnet-5-web-api/). Check it out if you want to learn more about the ins and outs of developing REST APIs with .NET. You can find the source code [on GitHub](https://github.com/megakevin/end-point-blog-dotnet-5-web-api).

The API is very straightforward. It provides a few endpoints for [CRUDing](https://developer.mozilla.org/en-US/docs/Glossary/CRUD) some database tables. It also provides an endpoint which, when given some vehicle information, will calculate a monetary value for that vehicle. That's a feature that would be interesting for us to cover with some tests.

The logic for that feature is backed by a specific class and it depends heavily on database interactions. As such, that class is a great candidate for writing a few automated integration tests against. The class in question is `QuotesService` which is defined in [Services/QuoteService.cs](https://github.com/megakevin/end-point-blog-dotnet-5-web-api/blob/master/Services/QuoteService.cs). The class provides features for fetching records from the database (the [`GetAllQuotes`](https://github.com/megakevin/end-point-blog-dotnet-5-web-api/blob/master/Services/QuoteService.cs#L23) method) as well as creating new records based on data from the incoming request and a set of rules stored in the database itself (the [`CalculateQuote`](https://github.com/megakevin/end-point-blog-dotnet-5-web-api/blob/master/Services/QuoteService.cs#L53) method).

In order to add automated tests, the first step is to organize our project so that it supports them. Let's do that next.

### Organizing the source code to allow for automated testing

In general, the source code of most real world .NET applications is organized as one or more "projects" under one "solution". A solution is a collection of related projects, and a project is something that produces a deployment artifact. An artifact is a library (i.e. a `*.dll` file) or something that can be executed like a console or web app.

Our sample app is a stand-alone ["webapi" project](https://docs.microsoft.com/en-us/aspnet/core/tutorials/first-web-api?view=aspnetcore-6.0&tabs=visual-studio-code), meaning that it's not within a solution. For automated tests, however, we need to create a new project for tests, parallel to our main one. Now that we have two projects instead of one, we need to reorganize the sample app's source code to comply with the "projects in a solution" structure I mentioned earlier.

Let's start by moving all the files in the root directory into a new `VehicleQuotes` directory. That's one project. Then, we create a new automated tests project by running the following, still from the root directory:

```sh
dotnet new xunit -o VehicleQuotes.Tests
```

That creates a new automated tests project named `VehicleQuotes.Tests` (under a new aptly named `VehicleQuotes.Tests` directory) which uses the [xUnit.net](https://xunit.net) test framework. There are other options when it comes to test frameworks in .NET. E.g. [MSTest](https://docs.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-mstest) and [NUnit](https://nunit.org/). We're going to use xUnit.net, but the others should work just as well for our purposes.

Now, we need to create a new solution to contain those two projects. Solutions come in the form of `*.sln` files and we can create ours like so:

```sh
dotnet new sln -o vehicle-quotes
```

That should've created a new `vehicle-quotes.sln` file for us. We should now have a file structure like this:

```
.
├── vehicle-quotes.sln
├── VehicleQuotes
│   ├── VehicleQuotes.csproj
│   └── ...
└── VehicleQuotes.Tests
    ├── VehicleQuotes.Tests.csproj
    └── ...
```

Like I said, the `*.sln` file indicates that this is a solution. The `*.csproj` files identify the individual projects that make up the solution.

Now, we need to tell dotnet that those two projects belong in the same solution. These commands do that:

```sh
dotnet sln add ./VehicleQuotes/VehicleQuotes.csproj
dotnet sln add ./VehicleQuotes.Tests/VehicleQuotes.Tests.csproj
```

Finally, we update the `VehicleQuotes.Tests` project so that it references the `VehicleQuotes` project. That way, the test suite will have access to all the classes defined in the REST API. Here's the command for that:

```
dotnet add ./VehicleQuotes.Tests/VehicleQuotes.Tests.csproj reference ./VehicleQuotes/VehicleQuotes.csproj
```

With all that setup out of the way, we can now start writing some tests.

> You can learn more about project organization in the [official online documentation](https://docs.microsoft.com/en-us/dotnet/core/tutorials/testing-with-cli).

### Creating a DbContext instance to talk to the database

The `VehicleQuotes.Tests` automated tests project got created with a default test file named `UnitTest1.cs`. You can delete it or ignore it, since we will not use it.

In general, it's a good idea for the test project to mimic the directory structure of the project that it will be testing. Also, we already decided that we would focus our test efforts on the `QuoteService` class from the `VehicleQuotes` project. That class is defined in `VehicleQuotes/Services/QuoteService.cs`, so let's create a similarly located file within the test project which will contain the test cases for that class. Here: `VehicleQuotes.Tests/Services/QuoteServiceTests.cs`. These would be the contents:

```csharp
// VehicleQuotes.Tests/Services/QuoteServiceTests.cs

using System;
using Xunit;

namespace VehicleQuotes.Tests.Services
{
    public class QuoteServiceTests
    {
        [Fact]
        public void GetAllQuotesReturnsEmptyWhenThereIsNoDataStored()
        {
            // Given

            // When

            // Then
        }
    }
}
```

This is the basic structure for tests using xUnit.net. Any method annotated with a `[Fact]` attribute will be picked up and ran by the test framework. In this case, I've created one such method called `GetAllQuotesReturnsEmptyWhenThereIsNoDataStored` which should give away its intention. This test case will validate that `QuoteService`'s `GetAllQuotes` method returns an empty set when called with no data on the database.

Before we can write this test case, though, the suite needs access to the test database. Our app uses [Entity Framework Core](https://docs.microsoft.com/en-us/ef/core/) for database interaction, which means that the database is accessed via a `DbContext` class. Looking at the source code of our sample app, we can see that the `DbContext` being used is `VehicleQuotesContext`, defined in `VehicleQuotes/Data/VehicleQuotesContext.cs`. Let's add a utility method to the `QuoteServiceTests` class which can be used to create new instances of `VehicleQuotesContext`:

```csharp
// VehicleQuotes.Tests/Services/QuoteServiceTests.cs

// ...
using Microsoft.EntityFrameworkCore;
using VehicleQuotes.Services;

namespace VehicleQuotes.Tests.Services
{
    public class QuoteServiceTests
    {
        private VehicleQuotesContext CreateDbContext()
        {
            var options = new DbContextOptionsBuilder<VehicleQuotesContext>()
                .UseNpgsql("Host=db;Database=vehicle_quotes_test;Username=vehicle_quotes;Password=password")
                .UseSnakeCaseNamingConvention()
                .Options;

            var context = new VehicleQuotesContext(options);

            context.Database.EnsureCreated();

            return context;
        }

        // ...
    }
}
```

As you can see, we need to go through three steps to create the `VehicleQuotesContext` instance and get a database that's ready for testing:

First, we create a `DbContextOptionsBuilder` and use that to obtain the `options` object that the `VehicleQuotesContext` needs as a constructor parameter. We needed to include the `Microsoft.EntityFrameworkCore` namespace in order to have access to the `DbContextOptionsBuilder`. For this, I just copied, and slightly modified this statement from the `ConfigureServices` method in the REST API's `VehicleQuotes/Startup.cs` file:

```csharp
// VehicleQuotes/Startup.cs

public void ConfigureServices(IServiceCollection services)
{
    // ...

    services.AddDbContext<VehicleQuotesContext>(options =>
        options
            .UseNpgsql(Configuration.GetConnectionString("VehicleQuotesContext"))
            .UseSnakeCaseNamingConvention()
            .UseLoggerFactory(LoggerFactory.Create(builder => builder.AddConsole()))
            .EnableSensitiveDataLogging()
    );

    // ...
}
```

This is a method that runs when the application is starting up to set up all the services that the app uses to work. Here, it's setting up the `DbContext` to enable database interaction. For the test suite, I took this statement as a starting point and removed the logging configurations and specified a hardcoded connection string that specifically points to a new `vehicle_quotes_test` database that will be used for testing.

If you're following along, then you need a Postgres instance that you can use to run the tests. In my case, I have one running that is reachable via the connection string I specified: `Host=db;Database=vehicle_quotes_test;Username=vehicle_quotes;Password=password`.

If you have Docker, a quick way to get a Postgres database up and running is with this command:

```sh
docker run -d \
    --name vehicle-quotes-db \
    -p 5432:5432 \
    --network host \
    -e POSTGRES_DB=vehicle_quotes \
    -e POSTGRES_USER=vehicle_quotes \
    -e POSTGRES_PASSWORD=password \
    postgres
```

That'll spin up a new Postgres instance that's reachable via `localhost`.

Secondly, now that we have the options parameter ready, we can quite simply instantiate a new `VehicleQuotesContext`:

```csharp
var context = new VehicleQuotesContext(options);
```

Finally, we call the `EnsureCreated` method so that the database that we specified in the connection string is actually created.

```csharp
context.Database.EnsureCreated();
```

This is the database that our test suite will use.

### Defining the test database connection string in the appsettings.json file

One quick improvement that we can do to the code we've written so far is move the connection string for the test database into a separate configuration file, instead of having it hardcoded. Let's do that next.

We need to create a new `appsettings.json` file under the `VehicleQuotes.Tests` directory. Then we have to add the connection string like so:

```json
{
  "ConnectionStrings": {
    "VehicleQuotesContext": "Host=db;Database=vehicle_quotes_test;Username=vehicle_quotes;Password=password"
  }
}
```

This is the standard way of configuring connection strings in .NET. Now, to actually fetch this value from within our test suite code, we make the following changes:

```diff
// ...
+using Microsoft.Extensions.Hosting;
+using Microsoft.Extensions.Configuration;
+using Microsoft.Extensions.DependencyInjection;

namespace VehicleQuotes.Tests.Services
{
    public class QuoteServiceTests
    {
        private VehicleQuotesContext CreateDbContext()
        {
+           var host = Host.CreateDefaultBuilder().Build();
+           var config = host.Services.GetRequiredService<IConfiguration>();

            var options = new DbContextOptionsBuilder<VehicleQuotesContext>()
-               .UseNpgsql("Host=db;Database=vehicle_quotes_test;Username=vehicle_quotes;Password=password")
+               .UseNpgsql(config.GetConnectionString("VehicleQuotesContext"))
                .UseSnakeCaseNamingConvention()
                .Options;

            var context = new VehicleQuotesContext(options);

            context.Database.EnsureCreated();

            return context;
        }

        // ...
    }
}
```

First we add a few `using` statements. We need `Microsoft.Extensions.Hosting` so that we can have access to the `Host` class through which we obtain access to the application's execution context. This allows us to access the built-in configuration service. We also need `Microsoft.Extensions.Configuration` to have access to the `IConfiguration` interface which is how we reference the configuration service which allows us access to the `appsettings.json` config file. And we also need the `Microsoft.Extensions.DependencyInjection` namespace which allows us to tap into the built-in dependency injection mechanism, through which we can access the default configuration service I mentioned before. Specifically, that namespace is where the `GetRequiredService` extension method lives.

All this translates into the few code changes that you see in the previous diff: First getting the app's host, then getting the configuration service, then using that to fetch our connection string.

> You can refer to [the official documentation](https://docs.microsoft.com/en-us/dotnet/core/extensions/configuration) to learn more about configuration in .NET.

### Writing a simple test case that fetches data

Now that we have a way to access the database from within the test suite, we can finally write an actual test case. Here's the `GetAllQuotesReturnsEmptyWhenThereIsNoDataStored` one that I alluded to earlier:

```csharp
// ...

namespace VehicleQuotes.Tests.Services
{
    public class QuoteServiceTests
    {
        // ...

        [Fact]
        public async void GetAllQuotesReturnsEmptyWhenThereIsNoDataStored()
        {
            // Given
            var dbContext = CreateDbContext();
            var service = new QuoteService(dbContext, null);

            // When
            var result = await service.GetAllQuotes();

            // Then
            Assert.Empty(result);
        }
    }
}
```

This one is a very simple test. We obtain a new `VehicleQuotesContext` instance that we can use to pass as a parameter when instantiating the component that we want to test: the `QuoteService`. We then call the `GetAllQuotes` method and assert that it returned an empty set. The test database was just created, so there should be no data in it, hence the empty resource set.

To run this test, we do `dotnet test`. I personally like a more verbose output so I like to use this variant of the command: `dotnet test --logger "console;verbosity=detailed"`. Here's what the output looks like.

```plaintext
$ dotnet test --logger "console;verbosity=detailed"
  Determining projects to restore...
  All projects are up-to-date for restore.
  VehicleQuotes -> /app/VehicleQuotes/bin/Debug/net5.0/VehicleQuotes.dll
  VehicleQuotes.Tests -> /app/VehicleQuotes.Tests/bin/Debug/net5.0/VehicleQuotes.Tests.dll
Test run for /app/VehicleQuotes.Tests/bin/Debug/net5.0/VehicleQuotes.Tests.dll (.NETCoreApp,Version=v5.0)
Microsoft (R) Test Execution Command Line Tool Version 16.11.0
Copyright (c) Microsoft Corporation.  All rights reserved.

Starting test execution, please wait...
A total of 1 test files matched the specified pattern.
/app/VehicleQuotes.Tests/bin/Debug/net5.0/VehicleQuotes.Tests.dll
[xUnit.net 00:00:00.00] xUnit.net VSTest Adapter v2.4.3+1b45f5407b (64-bit .NET 5.0.12)
[xUnit.net 00:00:01.03]   Discovering: VehicleQuotes.Tests
[xUnit.net 00:00:01.06]   Discovered:  VehicleQuotes.Tests
[xUnit.net 00:00:01.06]   Starting:    VehicleQuotes.Tests
[xUnit.net 00:00:03.25]   Finished:    VehicleQuotes.Tests
  Passed VehicleQuotes.Tests.Services.QuoteServiceTests.GetAllQuotesReturnsEmptyWhenThereIsNoDataStored [209 ms]

Test Run Successful.
Total tests: 1
     Passed: 1
 Total time: 3.7762 Seconds
```

### Resetting the state of the database after each test

Now we need to write a test that actually writes data into the database. However, every test case needs to start with the database in its original state. In other words, the changes that one test case does to the test database should not be seen, affect or be expected by any subsequent test. That will make it so our test cases are isolated and repeatable. That's not possible with our current implementation, though.

> You can read more about the FIRST principles of testing [here](https://medium.com/@tasdikrahman/f-i-r-s-t-principles-of-testing-1a497acda8d6).

Luckily, that's a problem that's easily solved with Entity Framework Core. All we need to do is call a method that ensures that the database is deleted just before it ensures that it is created. Here's what it looks like:

```diff
private VehicleQuotesContext CreateDbContext()
{
    var host = Host.CreateDefaultBuilder().Build();
    var config = host.Services.GetRequiredService<IConfiguration>();

    var options = new DbContextOptionsBuilder<VehicleQuotesContext>()
        .UseNpgsql(config.GetConnectionString("VehicleQuotesContext"))
        .UseSnakeCaseNamingConvention()
        .Options;

    var context = new VehicleQuotesContext(options);

+   context.Database.EnsureDeleted();
    context.Database.EnsureCreated();

    return context;
}
```

And that's all. Now every test case that calls `CreateDbContext` in order to obtain a `DbContext` instance will effectively trigger a database reset. Feel free to `dotnet test` again to validate that the test suite is still working.

Now, depending on the size of the database, this can be quite expensive. For integration tests, performance is not as big of a concern as for unit tests. This is because integration tests should be fewer in number and less frequently run.

We can make it better though. Instead of deleting and recreating the database before each test case, we'll take a page out of Ruby on Rails' book and run each test case within a database transaction which gets rolled back after the test is done. For now though, let's try and write another test case; this time, one where we insert new records into the database.

> If you want to hear a more in-depth discussion about automated testing in general, I go into further detail on the topic in this article: [An introduction to automated testing for web applications with Symfony](https://www.endpointdev.com/blog/2020/09/automated-testing-with-symfony/).

### Writing another simple test case that stores data

Now let's write another test that exercises `QuoteService`'s `GetAllQuotes` method. This time though, let's add a new record to the database before calling it so that the method's result is not empty. Here's what the test looks like:

```csharp
// ...
using VehicleQuotes.Models;
using System.Linq;

namespace VehicleQuotes.Tests.Services
{
    public class QuoteServiceTests
    {
        // ...

        [Fact]
        public async void GetAllQuotesReturnsTheStoredData()
        {
            // Given
            var dbContext = CreateDbContext();

            var quote = new Quote
            {
                OfferedQuote = 100,
                Message = "test_quote_message",

                Year = "2000",
                Make = "Toyota",
                Model = "Corolla",
                BodyTypeID = dbContext.BodyTypes.Single(bt => bt.Name == "Sedan").ID,
                SizeID = dbContext.Sizes.Single(s => s.Name == "Compact").ID,

                ItMoves = true,
                HasAllWheels = true,
                HasAlloyWheels = true,
                HasAllTires = true,
                HasKey = true,
                HasTitle = true,
                RequiresPickup = true,
                HasEngine = true,
                HasTransmission = true,
                HasCompleteInterior = true,

                CreatedAt = DateTime.Now
            };

            dbContext.Quotes.Add(quote);

            dbContext.SaveChanges();

            var service = new QuoteService(dbContext, null);

            // When
            var result = await service.GetAllQuotes();

            // Then
            Assert.NotEmpty(result);
            Assert.Single(result);
            Assert.Equal(quote.ID, result.First().ID);
            Assert.Equal(quote.OfferedQuote, result.First().OfferedQuote);
            Assert.Equal(quote.Message, result.First().Message);
        }
    }
}
```

First we include the `VehicleQuotes.Models` namespace so that we can use the `Quotes` model class. In our REST API, this is the class that represents the data from the `quotes` table. This is the main table that `GetAllQuotes` queries. We also include the `System.Linq` namespace, which allows us to use various collection extension methods (like `Single` and `First`) which we leverage throughout the test case to query lookup tables and assert on the test results.

Other than that, the test case itself is pretty self-explanatory. We start by obtaining an instance of `VehicleQuotesContext` via the `CreateDbContext` method. Remember that this also resets the whole database so that the test case can run over a clean slate. Then, we create a new `Quote` object and use our `VehicleQuotesContext` to insert it as a record into the database. We do this so that the later call to `QuoteService`'s `GetAllQuotes` method actually finds some data to return this time. Finally, the test case validates that the result contains a record and that its data is identical to what we set manually.

Neat! At this point we have what I think is the bare minimum infrastructure when it comes to serviceable and effective database integration tests (namely, access to a test database). We can take it one step further though, and make things more reusable and a little bit better performing.

### Refactoring into a fixture for reusability

We can use the test fixture functionality offered by xUnit.net in order to make the database interactivity aspect of our test suite into a reusable component. That way, if we had other test classes focused on other components that interact with the database, we could just plug that code in. We can define a fixture by creating a new file called, for example, `VehicleQuotes.Tests/Fixtures/DatabaseFixture.cs` with these contents:

```csharp
using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace VehicleQuotes.Tests.Fixtures
{
    public class DatabaseFixture : IDisposable
    {
        public VehicleQuotesContext DbContext { get; private set; }

        public DatabaseFixture()
        {
            DbContext = CreateDbContext();
        }

        public void Dispose()
        {
            DbContext.Dispose();
        }

        private VehicleQuotesContext CreateDbContext()
        {
            var host = Host.CreateDefaultBuilder().Build();
            var config = host.Services.GetRequiredService<IConfiguration>();

            var options = new DbContextOptionsBuilder<VehicleQuotesContext>()
                .UseNpgsql(config.GetConnectionString("VehicleQuotesContext"))
                .UseSnakeCaseNamingConvention()
                .Options;

            var context = new VehicleQuotesContext(options);

            context.Database.EnsureDeleted();
            context.Database.EnsureCreated();

            return context;
        }
    }
}
```

All this class does is define the `CreateDbContext` method that we're already familiar with but puts it in a nice reusable package. Upon instantiation, as seen in the constructor, it stores a reference to the `VehicleQuotesContext` in its `DbContext` property.

With that, our `QuoteServiceTests` test class can use it if we make the following changes to it:

```diff
using System;
using Xunit;
-using Microsoft.EntityFrameworkCore;
using VehicleQuotes.Services;
-using Microsoft.Extensions.Hosting;
-using Microsoft.Extensions.Configuration;
-using Microsoft.Extensions.DependencyInjection;
using VehicleQuotes.Models;
using System.Linq;
+using VehicleQuotes.Tests.Fixtures;

namespace VehicleQuotes.Tests.Services
{
-   public class QuoteServiceTests
+   public class QuoteServiceTests : IClassFixture<DatabaseFixture>
    {
+       private VehicleQuotesContext dbContext;

+       public QuoteServiceTests(DatabaseFixture fixture)
+       {
+           dbContext = fixture.DbContext;
+       }

-       private VehicleQuotesContext CreateDbContext()
-       {
-           var host = Host.CreateDefaultBuilder().Build();
-           var config = host.Services.GetRequiredService<IConfiguration>();

-           var options = new DbContextOptionsBuilder<VehicleQuotesContext>()
-               .UseNpgsql(config.GetConnectionString("VehicleQuotesContext"))
-               .UseSnakeCaseNamingConvention()
-               .Options;

-           var context = new VehicleQuotesContext(options);

-           context.Database.EnsureDeleted();
-           context.Database.EnsureCreated();

-           return context;
-       }

        [Fact]
        public async void GetAllQuotesReturnsEmptyWhenThereIsNoDataStored()
        {
            // Given
-           var dbContext = CreateDbContext();

            // ...
        }

        [Fact]
        public async void GetAllQuotesReturnsTheStoredData()
        {
            // Given
-           var dbContext = CreateDbContext();

            // ...
        }
    }
}
```

Here we've updated the `QuoteServiceTests` class definition so that it inherits from [`IClassFixture<DatabaseFixture>`](https://github.com/xunit/xunit/blob/main/src/xunit.v3.core/IClassFixture.cs). This is how we tell xUnit.net that our tests use the new fixture that we created. Next, we define a constructor that receives a `DatabaseFixture` object as a parameter. That's how xUnit.net allows our test class to access the capabilities provided by the fixture. In this case, we take the fixture's `DbContext` instance, and store it for later use in all of the test cases that need database interaction. We also removed the `CreateDbContext` method because now that's defined within the fixture. We also removed a few `using` statements that became unnecessary.

One important aspect to note about this fixture is that it is initialized once per whole test suite run, not once per test case. Specifically, the code within the `DatabaseFixture`'s constructor gets executed once, before all of the test cases. Similarly, the code in `DatabaseFixture`'s `Dispose` method get executed once at the end, after all test cases have been run.

This means that our test database deletion and recreation step now happens only once for the entire test suite. This is not good with our current implementation because that means that individual test cases no longer run with a fresh, empty database. This can be good for performance though, as long as we update our test cases to run within database transactions. Let's do just that.

### Using transactions to reset the state of the database

Here's how we update out test class so that each test case runs within a transaction:

```diff
// ...

namespace VehicleQuotes.Tests.Services
{
-   public class QuoteServiceTests : IClassFixture<DatabaseFixture>
+   public class QuoteServiceTests : IClassFixture<DatabaseFixture>, IDisposable
    {
        private VehicleQuotesContext dbContext;

        public QuoteServiceTests(DatabaseFixture fixture)
        {
            dbContext = fixture.DbContext;

+           dbContext.Database.BeginTransaction();
        }

+       public void Dispose()
+       {
+           dbContext.Database.RollbackTransaction();
+       }

        # ...
    }
}
```

The first thing to note here is that we added a call to `BeginTransaction` in the test class constructor. xUnit.net creates a new instance of the test class for each test case. This means that this constructor is run before each and every test case. We use that opportunity to begin a database transaction.

The other interesting point is that we've updated the class to implement the [`IDisposable` interface's `Dispose` method](https://docs.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose). xUnit.net will run this code after each test case, so we rollback the transaction.

Put those two together and we've updated our test suite so that every test case runs within the context of its own database transaction. Try it out with `dotnet test` and see what happens.

> To learn more about database transactions with Entity Framework Core, you can look at [the official docs](https://docs.microsoft.com/en-us/ef/core/saving/transactions).

> You can learn more about xUnit.net's test class fixtures in [the samples repository](https://github.com/xunit/samples.xunit/tree/main/ClassFixtureExample).

Alright, that's all for now. It is great to see that implementing automated database integration tests is actually fairly straightforward using .NET, xUnit.net and Entity Framework. Even if it isn't quite as easy as it is in Rails, it is perfectly doable.
