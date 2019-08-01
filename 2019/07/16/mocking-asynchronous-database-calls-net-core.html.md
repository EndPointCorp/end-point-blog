---
author: "Juan Pablo Ventoso"
title: "Mocking asynchronous database calls in .NET Core"
tags: dotnet, testing
gh_issue_number: 1538
---

<img src="/blog/2019/07/16/mocking-asynchronous-database-calls-net-core/image-0.jpg" alt="Mocking asynchronous database calls in .NET Core" /> [Photo](https://flic.kr/p/59cz7W) by [Björn Söderqvist](https://www.flickr.com/photos/kapten/), used under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)

### Introduction

Whenever we like—or are forced!—to develop using a TDD (test-driven development) approach or a more traditional practice, unit testing should be always a part of our development process. And when it comes to .NET Core, no matter what framework we choose (xUnit, MSTest or other), we will probably need to use a mock library.

**What is mocking?** By definition, it’s making an imitation. Objects usually depend on other objects, which could rely on database connections, local files or external APIs. So when we need to test the behavior of a particular object, we will have to isolate its dependencies, replacing those objects with fake versions. And that’s where mocking—and the Moq library—comes into place: it’s a set of classes that allows us to easily create and handle those fake objects.

So, assuming we already have a .NET Core solution with a test project included, all we need to do to add Moq is install the package from the NuGet console in Visual Studio:

```
Install-Package Moq
``` 

### Mocking data with async calls support

One of the first showstoppers I’ve encountered when trying to add unit tests to an existing project was to mock objects that contain asynchronous calls to the database: If we want to run offline (in-memory) tests against a set of code that performs an asynchronous query over a `DbSet<T>`, we’ll have to set up some helpers first.

So for example, let’s suppose we have a simple function called `GetUserIDByEmail()` that returns the ID of the user that matches an email passed by parameter, and that function uses an asyncronous query to the database to find that user:

- **UserHandler.cs**

```c#
public async Task<int?> GetUserIDByEmail(string Email)
{
    var User = await _DbContext.Users.Where(x => x.Email.Equals(Email)).FirstOrDefaultAsync();
    
    if (User != null)
        return User.ID;

    return null;
}
```

Where \_DbContext is a reference to the interface ```IMockProjectDbContext```, defined as:

- **MockProjectDbContext.cs**

```c#
public interface IMockProjectDbContext
{
    DbSet<User> Users { get; set; }
}
```

`GetUserIDByEmail()` will return a `Task<int?>` that will be created by the `FirstOrDefaultAsync()` method from Entity Framework. If we want to test this function with a in-memory set of data, the test will fail because our test data won’t support the interfaces needed to make the asynchronous call.

Why? Because the traditional provider for `IQueryable` and `IEnumerable` (the interfaces used for traditional sets) doesn’t implement the `IAsyncQueryProvider` interface needed for the Entity Framework asynchronous extension methods. So what we need to do is create a set of classes that will allow us to mock asynchronous calls to our in-memory lists.

- **TestClasses.cs**

```c#
// Async query provider for unit testing
internal class TestAsyncQueryProvider<TEntity> : IAsyncQueryProvider
{
    private readonly IQueryProvider _inner;

    internal TestAsyncQueryProvider(IQueryProvider inner)
    {
        _inner = inner;
    }

    public IQueryable CreateQuery(Expression expression)
    {
        return new TestAsyncEnumerable<TEntity>(expression);
    }

    public IQueryable<TElement> CreateQuery<TElement>(Expression expression)
    {
        return new TestAsyncEnumerable<TElement>(expression);
    }

    public object Execute(Expression expression)
    {
        return _inner.Execute(expression);
    }

    public TResult Execute<TResult>(Expression expression)
    {
        return _inner.Execute<TResult>(expression);
    }

    public IAsyncEnumerable<TResult> ExecuteAsync<TResult>(Expression expression)
    {
        return new TestAsyncEnumerable<TResult>(expression);
    }

    public Task<TResult> ExecuteAsync<TResult>(Expression expression, CancellationToken cancellationToken)
    {
        return Task.FromResult(Execute<TResult>(expression));
    }
}

// Async enumerable for unit testing
internal class TestAsyncEnumerable<T> : EnumerableQuery<T>, IAsyncEnumerable<T>, IQueryable<T>
{
    public TestAsyncEnumerable(IEnumerable<T> enumerable)
        : base(enumerable)
    { }

    public TestAsyncEnumerable(Expression expression)
        : base(expression)
    { }

    public IAsyncEnumerator<T> GetEnumerator()
    {
        return new TestAsyncEnumerator<T>(this.AsEnumerable().GetEnumerator());
    }

    IQueryProvider IQueryable.Provider
    {
        get { return new TestAsyncQueryProvider<T>(this); }
    }
}

// Async enumerator for unit testing
internal class TestAsyncEnumerator<T> : IAsyncEnumerator<T>
{
    private readonly IEnumerator<T> _inner;

    public TestAsyncEnumerator(IEnumerator<T> inner)
    {
        _inner = inner;
    }

    public void Dispose()
    {
        _inner.Dispose();
    }

    public T Current
    {
        get
        {
            return _inner.Current;
        }
    }

    public Task<bool> MoveNext(CancellationToken cancellationToken)
    {
        return Task.FromResult(_inner.MoveNext());
    }
}
```

- The `TestAsyncQueryProvider` class implements the `IAsyncQueryProvider` interface supplying the provider methods needed to make asynchronous calls.
- The `TestAsyncEnumerable` class implements the `IAsyncEnumerable` interface, returning our provider class when required by the framework.
- Finally, the `TestAsyncEnumerator` class implements the `IAsyncEnumerator` interface, returning a Task when the `MoveNext()` function is called.

Now we can create a function (taking advantage of [generics](https://www.geeksforgeeks.org/c-sharp-generics-introduction/)) that will return a mock version of a `DbSet<T>` containing the data we pass as the TestData parameter. The resulting `DbSet<T>` will have support to asynchronous calls because it will implement our custom classes.

- **TestFunctions.cs**

```c#
// Return a DbSet of the specified generic type with support for async operations
public static Mock<DbSet<T>> GetDbSet<T>(IQueryable<T> TestData) where T : class
{
    var MockSet = new Mock<DbSet<T>>();
    MockSet.As<IAsyncEnumerable<T>>().Setup(x => x.GetEnumerator()).Returns(new TestAsyncEnumerator<T>(TestData.GetEnumerator()));
    MockSet.As<IQueryable<T>>().Setup(x => x.Provider).Returns(new TestAsyncQueryProvider<T>(TestData.Provider));
    MockSet.As<IQueryable<T>>().Setup(x => x.Expression).Returns(TestData.Expression);
    MockSet.As<IQueryable<T>>().Setup(x => x.ElementType).Returns(TestData.ElementType);
    MockSet.As<IQueryable<T>>().Setup(x => x.GetEnumerator()).Returns(TestData.GetEnumerator());
    return MockSet;
}
```

### Defining the data

Next step will be to declare the data that we want to use for our tests. This can be declared as a set of properties that will return `IQueryable<T>` interfaces.

- **TestData.cs**

```c#
// Test data for the DbSet<User> getter
public static IQueryable<User> Users
{
    get
    {
        return new List<User>
        {
            new User { ID = 1, Username = "admin", Email = "admin@host.com" },
            new User { ID = 2, Username = "guest", Email = "guest@host.com" }
        }
        .AsQueryable();
    }
}
```

In this example, we’re adding two users to the set because that’s the minimum data we need to properly use our unit test.


### Putting it all together

Now that we have the test data and the helper functions needed for that data to be accessed asynchronously by Entity Framework, we’re ready to write our test function. So given our function `GetUserIDByEmail()`, we want to test it to make sure it works and it’s returning the correct value.

- **UserHandlerTests.cs**

```c#
// Should return a user with ID 1
[Fact]
public async void GetUserIDByEmailTest()
{
    // Create a mock version of the DbContext
    var DbContext = new Mock<IMockProjectDbContext>();

    // Users getter will return our mock DbSet with test data
    // (Here is where we call our helper function)
    DbContext.SetupGet(x => x.Users).Returns(TestFunctions.GetDbSet<User>(TestData.Users).Object);

    // Call the function to test
    var UserHandler = new MockProject.Common.UserHandler(DbContext.Object);
    var Result = await UserHandler.GetUserIDByEmail("admin@host.com");

    // Verify the results
    Assert.Equal(1, Result);
}
```

And now we have it ready to go. Visual Studio will first compile both projects and then run all the tests. The result looks good:

![MockProject test results](/blog/2019/07/16/mocking-asynchronous-database-calls-net-core/image-1.jpg)

Finally, I would recommend checking how much code is actually being covered by unit tests. There are different tools to achieve this, but I like using [MiniCover](https://dev.to/nlowe/easy-automated-code-coverage-for-net-core-1khh). It’s one of the simplest tools and we can prepare a simple batch file to get a detailed list of lines covered per file. This batch file is located in the root of the `MockProject.Tests` project.

This batch file will first clean and build the project, and then it calls `MiniCover` to evaluate the source code and report the current code coverage in lines and percentage.

- **CodeCoverage.bat**

```batch
@echo off

REM Clean and build the project
dotnet clean
dotnet build /p:DebugType=Full

REM Instrument assemblies in our test project to detect hits to source files on our main project
dotnet minicover instrument --workdir ../ --assemblies MockProject.Tests/**/bin/**/*.dll --sources MockProject/**/*.cs --exclude-sources MockProject/*.cs

REM Reset previous counters
dotnet minicover reset --workdir ../

REM Run the tests
dotnet test --no-build

REM Uninstrument assemblies in case we want to deploy
dotnet minicover uninstrument --workdir ../

REM Print the console report
dotnet minicover report --workdir ../ --threshold 70
```

After running the script, we’ll come to these results:

![MiniCover results](/blog/2019/07/16/mocking-asynchronous-database-calls-net-core/image-2.jpg)

The percentage of code that should be covered by tests depends greatly on the type of application (for example, a WebAPI project will probably have more testable code than a Razor Pages project), but as a general rule, we can expect that a well-tested project will exceed 70% of code coverage.


### Summary

We can take advantage of mocking and [generics](https://www.geeksforgeeks.org/c-sharp-generics-introduction/) to create an easy way to test our app using sample data and resources. We can emulate connecting and querying data asynchronously from a database with test data and a couple of helper classes that will support all interfaces needed by Entity Framework to run asynchronous operations.

I’ve uploaded the main and test projects (`MockProject` and `MockProject.Tests`) into a [GitHub repository](https://github.com/juanpabloventoso/MockProject) if you want to try it. And please leave any comment or suggestion below!
