---
author: "Kevin Campusano"
title: "Writing integration tests for an ASP.NET Web API"
date: 2024-05-13
featured:
  image_url: /blog/2024/05/writing-integration-tests-for-an-asp.net-web-api/thumbs-up-shadow.webp
description: How to write full integration tests using a persistent data store, like a database, for a Web API built using ASP.NET.
github_issue_number: 2045
tags:
- testing
- dotnet
- aspdotnet
- csharp
- rest
- api
---

![A concrete wall is patchily covered in shadows from a tree or something similar. Standing out against the sporadic texture of the shadows is the shadow of an arm and hand pointing up and to the right in a thumbs-up.](/blog/2024/05/writing-integration-tests-for-an-asp.net-web-api/thumbs-up-shadow.webp)

<!-- Photo by Seth Jensen, 2024. -->

[Integration tests](https://en.wikipedia.org/wiki/Integration_testing) exercise a system by instantiating major components and making them interact with each other. They are great for validating important use case scenarios in an end-to-end or close to end-to-end manner.

Full integration tests seldom use mocks or fake objects. Usually, the full stack is tested as if the entire system were running for real. For REST APIs, that generally means tests that involve issuing HTTP requests, validating HTTP responses, and asserting on changes made to a persistent data store, like a database.

In this article, we're going to discuss how to write such tests for a Web API built using ASP.NET.

### Introducing the project

I'll use an existing ASP.NET Web API project to demonstrate how to write these tests. The API is part of a system that calculates the value of used cars and offers quotes for them. As such, the API has an endpoint for calculating a vehicle quote, given its information and condition: `POST /api/Quotes`. It also has an endpoint for administration purposes that returns all the quotes that have been stored in the system's database: `GET /api/Quotes`. These are the two endpoints that we'll want to test.

The source code [is on GitHub](https://github.com/megakevin/end-point-blog-dotnet-8-demo), so feel free to browse. I've organized it so that the changes that we'll make throughout this article are all contained in a single commit. [You can see the diff here](https://github.com/megakevin/end-point-blog-dotnet-8-demo/commit/5f971115e871f9d60792b825b4b9f590600b529b).

The code base is organized as a [.NET solution](https://learn.microsoft.com/en-us/visualstudio/ide/solutions-and-projects-in-visual-studio?view=vs-2022), as evidenced by the [`vehicle-quotes.sln`](https://github.com/megakevin/end-point-blog-dotnet-8-demo/blob/main/vehicle-quotes.sln) file at the root of the repository. The Web API project can be found inside the [`VehicleQuotes.WebApi`](https://github.com/megakevin/end-point-blog-dotnet-8-demo/tree/main/VehicleQuotes.WebApi) directory. The endpoints that we want to test are defined in the controller at [`VehicleQuotes.WebApi/Controllers/QuotesController.cs`](https://github.com/megakevin/end-point-blog-dotnet-8-demo/blob/main/VehicleQuotes.WebApi/Controllers/QuotesController.cs).

Our plan is to develop integration tests that exercise the entire stack. That is, the API's HTTP request handling as well as its database interactions. These are the steps that we'll take in order to do that:

1. Create a new [xUnit](https://xunit.net/) project where we will put our integration tests.
2. Define a [test class fixture](https://xunit.net/docs/shared-context#class-fixture) that will connect our tests to a test database.
3. Write some logic to run the tests within their own database transactions. This makes sure they don't affect one another, and that they encounter the database in a clean state and also leave it that way.
4. Write some tests that interact with the API over HTTP.

### Setting up the integration tests project

The first step is to create a new xUnit project and add it to our solution. This can be done with this pair of commands:

```plain
dotnet new xunit -o VehicleQuotes.IntegrationTests
dotnet sln add ./VehicleQuotes.IntegrationTests/VehicleQuotes.IntegrationTests.csproj
```

That will create a new xUnit project under the `VehicleQuotes.IntegrationTests` directory. It will have an empty test class file that can be deleted.

The project needs the `Microsoft.AspNetCore.Mvc.Testing` [NuGet package](https://www.nuget.org/packages/Microsoft.AspNetCore.Mvc.Testing). If we move into the `VehicleQuotes.IntegrationTests` directory, the package can be installed with this command:

```plain
dotnet add package Microsoft.AspNetCore.Mvc.Testing --version 8.0.4
```

This package will allow our tests to issue HTTP requests to the Web API. We'll see how that's done soon.

We also need to add a reference to the Web API project. Also from within the `VehicleQuotes.IntegrationTests` directory, we can do that with:

```plain
dotnet add reference ../VehicleQuotes.WebApi/VehicleQuotes.WebApi.csproj
```

That way our testing project will have access to the classes defined in the Web API project. Specifically, we'll need the [DB context](https://www.entityframeworktutorial.net/efcore/entity-framework-core-dbcontext.aspx) and some entities. We'll see why soon.

There's one additional step that we need to do in the Web API project so that it is testable, and that's explicitly defining its "Program" class. To do that, we add this line at the end of the `VehicleQuotes.WebApi/Program.cs` file:

```csharp
// VehicleQuotes.WebApi/Program.cs
// ...
public partial class Program { }
```

I'll admit: this is quite strange. But it is a requirement for integration testing. You'll see how this comes into play when we start writing the tests. You can read more about it in [the official docs](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-8.0#basic-tests-with-the-default-webapplicationfactory).

With that, the project is set up. In the end, our [`VehicleQuotes.IntegrationTests/VehicleQuotes.IntegrationTests.csproj`](https://github.com/megakevin/end-point-blog-dotnet-8-demo/blob/main/VehicleQuotes.IntegrationTests/VehicleQuotes.IntegrationTests.csproj) should look like this:

```xml
<!-- VehicleQuotes.IntegrationTests/VehicleQuotes.IntegrationTests.csproj -->
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>

    <IsPackable>false</IsPackable>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="coverlet.collector" Version="6.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="8.0.4" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <PackageReference Include="xunit" Version="2.5.3" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.3" />
  </ItemGroup>

  <ItemGroup>
    <Using Include="Xunit" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\VehicleQuotes.WebApi\VehicleQuotes.WebApi.csproj" />
  </ItemGroup>

</Project>
```

### Writing a database fixture

Now, we need to make it possible for our API to interact with a test instance of our database when running within the context of our tests. This can be done with a properly configured [test class fixture](https://xunit.net/docs/shared-context#class-fixture). Let's see what that looks like.

First of all we need an `appsettings` file for our test project that contains the test database connection string. I created a [`VehicleQuotes.IntegrationTests/appsettings.Test.json`](https://github.com/megakevin/end-point-blog-dotnet-8-demo/blob/main/VehicleQuotes.IntegrationTests/appsettings.Test.json) file with these contents:

```json
{
  "ConnectionStrings": {
    "VehicleQuotesContext": "Host=db;Database=vehicle_quotes_test;Username=vehicle_quotes;Password=password;Include Error Detail=True"
  },
  "Jwt": {
    "Key": "this is the secret key for the jwt, it must be kept secure",
    "Issuer": "vehiclequotes.endpointdev.com",
    "Audience": "vehiclequotes.endpointdev.com",
    "Subject": "JWT for vehiclequotes.endpointdev.com"
  },
  "DefaultOffer": 77
}
```

We also have to tell .NET that it needs to include this file when building the project to run the tests. We do so by adding the following to the [`VehicleQuotes.IntegrationTests/VehicleQuotes.IntegrationTests.csproj`](https://github.com/megakevin/end-point-blog-dotnet-8-demo/blob/main/VehicleQuotes.IntegrationTests/VehicleQuotes.IntegrationTests.csproj#L13) file:

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <!-- ... -->
  <ItemGroup>
    <Content Include="appsettings.Test.json" CopyToOutputDirectory="PreserveNewest" />
  </ItemGroup>
  <!-- ... -->
</Project>
```

The important thing in this `appsettings` file is the `ConnectionStrings.VehicleQuotesContext` setting, which contains the test database connection string. Notice the value for `Database` in the connection string is appended with `_test`. This is how we make sure the tests run against a different database. The rest of the settings are unrelated to the test database, but need to be defined for the Web API to work. These will obviously be different for every project. All in all, this file is meant to be a test version of the Web API's own `appsettings.json` file. [You can find it here](https://github.com/megakevin/end-point-blog-dotnet-8-demo/blob/main/VehicleQuotes.WebApi/appsettings.json).

> Our Web API supports [authentication via Bearer Token](https://swagger.io/docs/specification/authentication/bearer-authentication/). If you want to learn more about how I implemented that, [here's another blog post](/blog/2022/06/implementing-authentication-in-asp.net-core-web-apis/) describing the process.

Next, we develop the [test class fixture](https://xunit.net/docs/shared-context#class-fixture) for enabling database access. We define a [`VehicleQuotes.IntegrationTests/Fixtures/DatabaseFixture.cs`](https://github.com/megakevin/end-point-blog-dotnet-8-demo/blob/main/VehicleQuotes.IntegrationTests/Fixtures/DatabaseFixture.cs) file that looks like this:

```csharp
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using VehicleQuotes.WebApi;

namespace VehicleQuotes.IntegrationTests.Fixtures;

// For more info about this class, check:
// https://learn.microsoft.com/en-us/ef/core/testing/testing-with-the-database#creating-seeding-and-managing-a-test-database
public class DatabaseFixture
{
    private static readonly object _lock = new();
    private static bool _databaseInitialized;

    // Initializes the database specified in the connection string defined in
    // the appsettings.Test.json file.
    public DatabaseFixture()
    {
        // Tests can run in parallel. This lock is meant to make this code
        // thread safe.
        lock (_lock)
        {
            if (!_databaseInitialized)
            {
                using (var dbContext = CreateDbContext())
                {
                    // Delete the database and recreate it.
                    dbContext.Database.EnsureDeleted();
                    dbContext.Database.EnsureCreated();
                }

                _databaseInitialized = true;
            }
        }
    }

    // Creates a new VehicleQuotesContext instance configured with the
    // connection string defined in the appsettings.Test.json file.
    public VehicleQuotesContext CreateDbContext()
    {
        // Load up the appsettings.Test.json file
        var config = new ConfigurationBuilder()
            .AddJsonFile("appsettings.Test.json")
            .Build();

        // Create an instance of DbContextOptions using the connection string
        // defined in the appsettings.Test.json file.
        var options = new DbContextOptionsBuilder<VehicleQuotesContext>()
            .UseNpgsql(config.GetConnectionString("VehicleQuotesContext"))
            .UseSnakeCaseNamingConvention()
            .Options;

        var dbContext = new VehicleQuotesContext(options);

        return dbContext;
    }

    // Runs the given "test" within a database transaction created using the
    // given "dbContext". It rolls back the transaction when the "test" is done.
    public async Task WithTransaction(VehicleQuotesContext dbContext, Func<Task> test)
    {
        dbContext.Database.BeginTransaction();

        try
        {
            await test.Invoke();
        }
        catch
        {
            throw;
        }
        finally
        {
            dbContext.Database.RollbackTransaction();
        }
    }
}
```

I've made sure to include some comments on that class trying to explain what it does, so feel free to review. Much of it was inspired by [.NET's official docs](https://learn.microsoft.com/en-us/ef/core/testing/testing-with-the-database#creating-seeding-and-managing-a-test-database).

This class serves the purpose of allowing the tests suite to connect to and interact with the test database. It does so by performing three tasks:

1. Resetting the database at the beginning of every test run. This happens in the constructor.
2. Allowing the creation of new [`VehicleQuotesContext`](https://github.com/megakevin/end-point-blog-dotnet-8-demo/blob/main/VehicleQuotes.WebApi/Data/VehicleQuotesContext.cs) instances which connect to the test database. Tests will use that to interact with the database.
3. Offering the capability for tests to be run within DB transactions. This makes sure they don't affect one another, and that they encounter the database in a clean state and also leave it that way.

### Writing some integration tests

Now we can finally start writing some tests. Let's start with a simple one that makes a GET request to the "fetch all quotes" endpoint that I mentioned at the beginning: `GET /api/Quotes`. The one defined in the `GetAll` method in the [`VehicleQuotes.WebApi/Controllers/QuotesController.cs`](https://github.com/megakevin/end-point-blog-dotnet-8-demo/blob/main/VehicleQuotes.WebApi/Controllers/QuotesController.cs) controller.

We create a new [`VehicleQuotes.IntegrationTests/Controllers/QuotesControllerTests.cs`](https://github.com/megakevin/end-point-blog-dotnet-8-demo/blob/main/VehicleQuotes.IntegrationTests/Controllers/QuotesControllerTests.cs) file and write our test in there. It looks like this:

```csharp
using System.Net;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.TestHost;
using Microsoft.Extensions.DependencyInjection;
using VehicleQuotes.IntegrationTests.Fixtures;
using VehicleQuotes.WebApi;

namespace GifBackend.IntegrationTests.WebApi.Controllers;

public class OldQuotesControllerTests : IClassFixture<WebApplicationFactory<Program>>, IClassFixture<DatabaseFixture>
{
    private readonly WebApplicationFactory<Program> _factory;
    private readonly VehicleQuotesContext _dbContext;

    public OldQuotesControllerTests(WebApplicationFactory<Program> factory, DatabaseFixture database)
    {
        _factory = factory;
        _dbContext = database.CreateDbContext();
    }

    protected HttpClient CreateHttpClient()
    {
        return _factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureTestServices(services =>
            {
                services.AddSingleton(_ => _dbContext);
            });
        })
        .CreateClient();
    }

    [Fact]
    public async Task GetQuotes_ReturnsOK()
    {
        // Arrange
        var client = CreateHttpClient();

        // Act
        var response = await client.GetAsync("/api/Quotes");

        // Assert
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
```

First, turn your attention to the `GetQuotes_ReturnsOK` test case. Very simple as tests go, but there are a few interesting things taking place here.

The test case itself is indeed simple. All it does is create an HTTP client, use it to send a GET request to the endpoint that we want to test (using the client's `GetAsync` method), and finally validate that the response is a `200 OK`. How it does these things is the interesting part.

The HTTP client is created using the `CreateHttpClient` method. This method leverages `_factory`, a `WebApplicationFactory<Program>` instance that's injected by the framework into our test class. Here, the [generic type parameter](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/generics/generic-type-parameters) `Program` is referring to the "Program" class from the Web API project. The one we defined in the `Program.cs` file. Notice also how our test class implements the `IClassFixture<WebApplicationFactory<Program>>` interface. That's what signals to the framework that a `WebApplicationFactory<Program>` instance needs to be passed/injected via the constructor. This is the way that the `Microsoft.AspNetCore.Mvc.Testing` package allows us to express that "this test class contains tests for this web application".

> Full details in [the official docs](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-8.0).

Notice also how when creating the HTTP client, a `VehicleQuotesContext` instance is set up as a singleton service. This is key. This DB context is obtained thanks to our `DatabaseFixture`. That means that it connects to the test database. We configured it to do so. By setting it up as a service like this, we make sure that the Web API application uses that instance whenever it interacts with the database. And using that instance means that it will use the test database. Since this is the same instance that we will use within our tests, both the tests suite and the application (when running within the context of the tests) will share the same database.

Long story short: This way of constructing the HTTP client and injecting our own DB context into the running application is the secret sauce that allows our tests to utilize the test instance of the database.

Obtaining an instance of the `DatabaseFixture` is the same as obtaining an instance of the `WebApplicationFactory<Program>`: all we have to do is make our test class implement the `IClassFixture<DatabaseFixture>` interface and define the constructor parameter so that the framework passes it in.

### Writing some more integration tests

OK, now that we understand the basics, let's write a few more test cases in order to demonstrate some other common scenarios.

#### A test that writes to and reads from the database

For example, here's one that validates that the `GET /api/Quotes` endpoint actually returns the data that's stored in the database.

```csharp
[Fact]
public async Task GetQuotes_ReturnsTheQuotesFromTheDatabase()
{
    await _database.WithTransaction(_dbContext, async () => {
        // Arrange
        await CreateNewQuote("2024", "Toyota", "Corolla");
        await CreateNewQuote("2024", "Honda", "Civic");

        var client = CreateHttpClient();

        // Act
        var response = await client.GetAsync("/api/Quotes");

        // Assert
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        var quotes = await response.Content.ReadFromJsonAsync<IEnumerable<SubmittedQuoteRequest>>();

        Assert.NotNull(quotes);
        Assert.Equal(2, quotes.Count());

        Assert.Equal("2024", quotes.First().Year);
        Assert.Equal("Toyota", quotes.First().Make);
        Assert.Equal("Corolla", quotes.First().Model);

        Assert.Equal("2024", quotes.Last().Year);
        Assert.Equal("Honda", quotes.Last().Make);
        Assert.Equal("Civic", quotes.Last().Model);
    });
}

private async Task<Quote> CreateNewQuote(string year, string make, string model)
{
    var bodyType = await _dbContext.BodyTypes.SingleAsync(bt => bt.Name == "Sedan");
    var size = await _dbContext.Sizes.SingleAsync(s => s.Name == "Compact");

    var quote = new Quote {
        Year = year,
        Make = make,
        Model = model,
        BodyTypeID = bodyType.ID,
        SizeID = size.ID,
        ItMoves = true,
        HasAllWheels = true,
        HasAlloyWheels = false,
        HasAllTires = true,
        HasKey = true,
        HasTitle = true,
        RequiresPickup = true,
        HasEngine = true,
        HasTransmission = true,
        HasCompleteInterior = false,
        OfferedQuote = 123,
        Message = "test_message",
        CreatedAt = DateTime.UtcNow
    };

    _dbContext.Quotes.Add(quote);

    _dbContext.SaveChanges();

    return quote;
}
```

This method introduces a few more interesting features:

1. It runs within a database transaction. Ensuring that any data changes are rolled back once the test is done.
2. It uses the singleton DB context to interact with the database. Inserting new records before executing the application under test.
3. It parses a JSON response body into a .NET object.

In detail, here's what it does: It uses our `DatabaseFixture`'s `WithTransaction` method to run within a database transaction. The test's strategy is simple: it first inserts new records into the database, leveraging the `CreateNewQuote` helper method. Then it sends a request to the Web API's `GET /api/Quotes` endpoint. Finally, in the assertion section, it validates that the response came back with the correct HTTP status code. Then it parses the JSON response body into an object, and inspects that object to make sure that it has the correct data in it — that is, it contains the database records that were inserted at the beginning of the test case.

#### A test that makes a POST request

Using all these concepts, we can also write a test for the `POST /api/Quotes` endpoint. For example, here's a test that validates that the endpoint stores new records in the database using the given payload:

```csharp
[Fact]
public async Task PostQuote_CreatesANewQuoteRecord()
{
    await _database.WithTransaction(_dbContext, async () => {
        // Arrange
        var client = CreateHttpClient();

        Assert.Empty(_dbContext.Quotes);

        // Act
        var response = await client.PostAsJsonAsync(
            "/api/Quotes",
            new
            {
                Year = "1990",
                Make = "Toyota",
                Model = "Corolla",
                BodyType = "Sedan",
                Size = "Compact",
                ItMoves = true,
                HasAllWheels = true,
                HasAlloyWheels = false,
                HasAllTires = true,
                HasKey = true,
                HasTitle = true,
                RequiresPickup = false,
                HasEngine = true,
                HasTransmission = true,
                HasCompleteInterior = true
            }
        );

        // Assert
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);

        Assert.Single(_dbContext.Quotes);

        var quote = _dbContext.Quotes.First();
        Assert.NotNull(quote);
        Assert.Equal("1990", quote.Year);
        Assert.Equal("Toyota", quote.Make);
        Assert.Equal("Corolla", quote.Model);
    });
}
```

The only new concept that this test introduces is the use of the HTTP client's `PostAsJsonAsync` method to send POST requests. Notice how we can send any payload we want using an [anonymous object](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/anonymous-types). In the assertion phase, the test queries the database to check if the expected record was inserted.

All of this is made possible by the singleton `VehicleQuotesContext` instance. Both test code and application code are talking to the test database. And thanks to the transactions, each test cleans up after it's done so that the next test can run with a clean slate.

#### A test that makes many requests

We can also write tests that span multiple requests. Here's one for example that registers a new user account and logs in, so that it can then be allowed access to a secure endpoint:

```csharp
using System.Net.Http.Headers;

// ...

[Fact]
public async Task GetQuotesSecure_ReturnsOK_WhenTheUserHasLoggedIn()
{
    await _database.WithTransaction(_dbContext, async () => {
        // Arrange
        var client = CreateHttpClient();

        await RegisterUser(client);
        var response = await Login(client);
        var authResponse = await response.Content.ReadFromJsonAsync<AuthenticationResponse>();

        Assert.NotNull(authResponse);

        // Act
        using var requestMessage = new HttpRequestMessage(HttpMethod.Get, "/api/Quotes/Secure");
        requestMessage.Headers.Authorization = new AuthenticationHeaderValue("Bearer", authResponse.Token);

        response = await client.SendAsync(requestMessage);

        // Assert
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    });
}

private async Task<HttpResponseMessage> RegisterUser(HttpClient client)
{
    var response = await client.PostAsJsonAsync(
        "/api/Users",
        new
        {
            UserName = "test_user_name",
            Password = "test_password",
            Email = "test@email.com"
        }
    );

    Assert.Equal(HttpStatusCode.Created, response.StatusCode);

    return response;
}

private async Task<HttpResponseMessage> Login(HttpClient client)
{
    var response = await client.PostAsJsonAsync(
        "/api/Users/BearerToken",
        new
        {
            UserName = "test_user_name",
            Password = "test_password"
        }
    );

    Assert.Equal(HttpStatusCode.OK, response.StatusCode);

    return response;
}
```

This test is a little more complicated and introduces a few new concepts. All within its own database transaction, this test:

1. Uses the `RegisterUser` helper method to register a new user account. It calls the `POST /api/Users` endpoint for this.
2. Uses the `Login` helper method to log in. In our demo Web API project, this means obtaining a token that can be used for [Bearer Token authentication](https://swagger.io/docs/specification/authentication/bearer-authentication/). It calls the `POST /api/Users/BearerToken` endpoint for this.
3. Extracts the generated token from the response, and prepares a new request for the `GET /api/Quotes/Secure` endpoint using that token as an authentication header.
4. Sends the request and validates that it results in a successful HTTP status code.

Notice that we had to use the HTTP client's more verbose `SendAsync` method instead of the more convenient `GetAsync`. This is because `GetAsync` doesn't support sending headers, which we needed.

#### Disabling some application services

Before we're done here, something useful about this approach is that it is possible to disable some services on the application under test. We've been writing full integration tests where all system components are exercised. It could be the case, however, that we would like to exclude some components from testing. For example, if the app under test sends emails, we might want to disable that. Or if it invokes another third party service, we might want the tests to not do that.

Because we're able to inject services of our choosing to the running application (like we do with the DB context), it's certainly possible for us to disable parts of the system. For example, imagine an application that sends emails using an `IMailer` derived class. One could inject a [null object](https://en.wikipedia.org/wiki/Null_object_pattern) in its place. We could do this when creating the test HTTP client. Something like this:


```csharp
private HttpClient CreateHttpClient()
{
    // Disable emails for integration tests
    var mockMailer = new Mock<IMailer>();
    mockMailer.Setup(m => m.SendMailAsync()).ReturnsAsync(true);

    return _factory.WithWebHostBuilder(builder =>
    {
        builder.ConfigureTestServices(services =>
        {
            services.AddSingleton(_ => _dbContext);
            services.AddTransient(_ => mockMailer.Object);
        });
    })
    .CreateClient();
}
```

Here, I created a [mock object](https://en.wikipedia.org/wiki/Mock_object) of the same type as the "Mailer" service that the application uses; then I added it to its [Dependency Injection container](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection). Now, every time the application calls for an `IMailer` instance, it will get the mock. A mock that does nothing.

And that's it! I think a good amount of integration tests will end up utilizing and remixing various combinations of these basic concepts. I invite you to look at [the demo app's source code on GitHub](https://github.com/megakevin/end-point-blog-dotnet-8-demo/commit/5f971115e871f9d60792b825b4b9f590600b529b), where I've added a few more tests. I also did some refactoring to make these features a little easier to reuse. Happy testing!
