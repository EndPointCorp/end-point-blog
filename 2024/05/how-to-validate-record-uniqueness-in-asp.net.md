---
author: "Kevin Campusano"
title: "How to validate record uniqueness in ASP.NET"
date: 2024-05-10
featured:
  image_url:
description:
tags:
- dotnet
- aspdotnet
- csharp
- efcore
---

In ASP.NET, the [`System.ComponentModel.DataAnnotations` namespace](https://learn.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations?view=net-8.0) includes many [attributes](https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/reflection-and-attributes/) that can be used to instruct the framework to perform [basic validation tasks](https://learn.microsoft.com/en-us/aspnet/core/mvc/models/validation?view=aspnetcore-8.0) for us. There are built-in validators [for ensuring that certain fields are present](https://learn.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.requiredattribute), [that they meet character length limits](https://learn.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.stringlengthattribute), [that they don't exceed or fall short of certain amounts](https://learn.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.rangeattribute), [that they match certain formats](https://learn.microsoft.com/en-us/dotnet/api/system.componentmodel.dataannotations.regularexpressionattribute?view=net-8.0), and more.

One omission however, is checking for record uniqueness. That is, checking that no other record in the entity's underlying persistent data storage has the same "name", or the same "code", or the same "any other field".

In this article, we're going to try to address this shortcoming by implementing this type of uniqueness validation ourselves. We will see two approaches: a simpler solution using a database index, and a more flexible one using a custom validation attribute. Let's get started.

> Throughout this article, I will be using a demo Web API application for code examples. If you'd like to see what the final implementation looks like, [you can find all the code on GitHub](https://github.com/megakevin/end-point-blog-dotnet-8-demo).
> 
> The API is about calculating quotes for used vehicles based on their condition. It runs on .NET 8 and uses a [PostgreSQL](https://www.postgresql.org/) database, to which it connects using [Entity Framework Core](https://learn.microsoft.com/en-us/ef/core/). As such it has various [endpoints](https://github.com/megakevin/end-point-blog-dotnet-8-demo/tree/main/VehicleQuotes.WebApi/Controllers), [entities](https://github.com/megakevin/end-point-blog-dotnet-8-demo/tree/main/VehicleQuotes.WebApi/Models) and [tables](https://github.com/megakevin/end-point-blog-dotnet-8-demo/tree/main/VehicleQuotes.WebApi/Migrations) related to vehicle information like makes, models, etc.

## Using a database unique index to enforce uniqueness

If your application uses a [relational database](https://en.wikipedia.org/wiki/Relational_database) to store its data, then the easiest solution to enforce record uniqueness is implementing a [unique index](https://www.w3schools.com/sql/sql_ref_create_unique_index.asp). This way, we let the database itself enforce the rule.

With Entity Framework Core, we can apply an attribute to an entity class to specify that its underlying database table should define an index.

For example, imagine we have a [`Make`](https://github.com/megakevin/end-point-blog-dotnet-8-demo/blob/main/VehicleQuotes.WebApi/Models/Make.cs) entity class that looks like this:

```csharp
public class Make
{
    public int ID { get; set; }
    public required string Name { get; set; }
}
```

If we need every `Make` record to have a unique `Name`, we can do so by adding this attribute to the class:

```diff
+ using Microsoft.EntityFrameworkCore;

// ...

+ [Index(nameof(Name), IsUnique = true)]
public class Make
{
    // ...
}
```

The [`Index`](https://learn.microsoft.com/en-us/dotnet/api/microsoft.entityframeworkcore.indexattribute?view=efcore-8.0) attribute from the `Microsoft.EntityFrameworkCore` namespace, with its `IsUnique` property set to `true` takes care of that.

Now, if we were to [create a migration](https://github.com/megakevin/end-point-blog-dotnet-8-demo/blob/main/VehicleQuotes.WebApi/Migrations/20210625224443_AddUniqueIndexesToLookupTables.cs) with a command like this:

```sh
dotnet ef migrations add AddUniqueIndexToMakes
```

We'll see something like this in the generated code:

```csharp
// ...
migrationBuilder.CreateIndex(
    name: "ix_makes_name",
    table: "makes",
    column: "name",
    unique: true);
// ...
```

See how the framework takes notice of the `Index` attribute and produces some code to create an index in the database with the column and uniqueness constraint that we specified.

After applying the migration with `dotnet ef database update`, any attempt at inserting or updating records that violate this constraint will result in an error.

Suppose we have [an endpoint](https://github.com/megakevin/end-point-blog-dotnet-8-demo/blob/main/VehicleQuotes.WebApi/Controllers/MakesController.cs#L83) for registering new makes that looks like this:

```csharp
// ...

private readonly VehicleQuotesContext _context;

// ...

[HttpPost]
public async Task<ActionResult<Make>> PostMake(Make make)
{
    _context.Makes.Add(make);

    await _context.SaveChangesAsync();

    return Created();
}
```

If we `POST` to it, and give it a payload with a non-unique name...

```sh
$ curl -X 'POST' 'http://localhost:5000/api/Makes' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Toyota"
}'
```

...here's what we get back:

```sh
Microsoft.EntityFrameworkCore.DbUpdateException: An error occurred while saving the entity changes. See the inner exception for details.
 ---> Npgsql.PostgresException (0x80004005): 23505: duplicate key value violates unique constraint "ix_makes_name"
```

This is only a portion of the output, but sure enough, we see a `Microsoft.EntityFrameworkCore.DbUpdateException` being thrown with the message indicating that a unique constraint was not met. The request results in a `500 Internal Server Error` response.

That gets the job done for sure: it prevents bad data from entering the system. But generally we don't want to expose such verbose errors to our API clients. It'd be better, for example, to catch that exception and return a `400` series status code. A simple `400 Bad Request` seems appropriate in this case. We can make the endpoint behave this way with these tweaks:

```diff
[HttpPost]
public async Task<ActionResult<Make>> PostMake(Make make)
{
    _context.Makes.Add(make);

+    try
+    {
        await _context.SaveChangesAsync();
+    }
+    catch (DbUpdateException)
+    {
+        return BadRequest();
+    }

    return Created();
}
```

Simple enough, we use a `try-catch` to handle the `Microsoft.EntityFrameworkCore.DbUpdateException` and return a response of our choosing. Trying the same request again, now results in a `400 Bad Request` response with this body:

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
  "title": "Bad Request",
  "status": 400,
  "traceId": "00-7ea5139de6f4ce471aa096dcf4a79ce5-dd308a30c4dd2b33-00"
}
```

## Writing a custom validation attribute to enforce uniqueness

The database index solution will work in a lot of cases. There are some scenarios however, where it won't. For example, the validation may need to be applied to input data that is not directly tied to a database table; or maybe the app does not use a relational database at all. In cases where we can't rely on unique indexes, a [custom validation attribute](https://learn.microsoft.com/en-us/aspnet/core/mvc/models/validation?view=aspnetcore-8.0#custom-attributes) is the best option.

The validation logic that the attribute would have to implement is simple. All it would have to do is query the underlying data store to see if a record with the given field value already exists. And if it does, trigger a validation error.

We'll start by implementing a first iteration that works specifically for `Make` names. Then, we'll extract the generic parts and create a reusable base attribute that can be used in many situations, with any class and field.

Before we can develop the attribute, consider the same Make class that we worked with before:

```csharp
public class Make
{
    public int ID { get; set; }
    public required string Name { get; set; }
}
```

Also, we have a [repository](https://martinfowler.com/eaaCatalog/repository.html) class that we use to access the underlying storage. Its public interface looks like this:

```csharp
public interface IMakeRepository
{
    Make? FindByName(string name);
}
```

The actual implementation is not important to us right now (although [you can find it here](https://github.com/megakevin/end-point-blog-dotnet-8-demo/blob/main/VehicleQuotes.WebApi/Repositories/MakeRepository.cs)). It's enough to know that we can use objects of this type to search for `Make` records by name.

Suppose also that we've included an instance of this type as a service via [Dependency Injection](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection?view=aspnetcore-8.0). With something like this in the project's [`Program.cs`](https://github.com/megakevin/end-point-blog-dotnet-8-demo/blob/main/VehicleQuotes.WebApi/Program.cs):

```csharp
services.AddScoped<IMakeRepository, MakeRepository>();
```

With those pieces in place, a custom validation attribute that prevents `Makes` with the same name could look [like this](https://github.com/megakevin/end-point-blog-dotnet-8-demo/commit/2017c2f45da7d839337e15c70b740be9d9ce5135):

```csharp
// Annotating the class with the AttributeUsage attribute is our way of letting
// the framework know that our UniqueMakeNameAttribute is meant to be applied to
// classes. It's produce a build error if we try to apply it to anything else.
[AttributeUsage(AttributeTargets.Class)]
// In order for our attribute to integrate correctly with the framework's model
// validation functionality, it needs to inherit from ValidationAttribute.
public class UniqueMakeNameAttribute : ValidationAttribute
{
    // Inheriting from ValidationAttribute requires implementing this method.
    // This is the method that gets called by the framework during model
    // validation.
    // Here, we're using it only to prepare the validation algorithm to run,
    // which is defined in the private Validate method.
    protected override ValidationResult? IsValid(
        // The framework uses this "value" parameter to pass in the full Make
        // object that's being validated.
        object? value,
        // The "context" parameter will contain various objects related to the
        // execution environment. It is used to obtain instances made available
        // by Dependency Injection.
        ValidationContext context
    ) {
        if (value == null) return ValidationResult.Success;

        // Here we use the validation context parameter to obtain an instance of
        // the repository
        var repo = context.GetService<IMakeRepository>();
        if (repo == null) return ValidationResult.Success;

        return Validate((Make)value, repo);
    }

    // This is where we actually run the custom validation logic.
    // Like I mentioned before, the logic is simple...
    private static ValidationResult? Validate(Make input, IMakeRepository repo)
    {
        // ...first it calls on the repository to try and find an existing
        // record wiht the same name...
        var existing = repo.FindByName(input.Name);

        // ...then, if another record with the same name exists, one which is
        // not its not the same being validated right now...
        if (existing != null && input.ID != existing.ID)
        {
            // ...return a ValidationResult which contains an understandable
            // error message.
            return new ValidationResult(
                $"The Make name '{input.Name}' is already in use."
            );
        }

        // If, on the other hand, no problem was found, return a successful
        // ValidationResult.
        return ValidationResult.Success;
    }
}
```

In order to put this logic to work, we use the attribute to annotate our `Make` class, like so:

```diff
+[UniqueMakeName]
public class Make
{
    public int ID { get; set; }
    public required string Name { get; set; }
}
```

Now, if we make a request to create a new `Make` and use an existing name, we get back a `400 Bad Request` response with this payload:

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
  "title": "One or more validation errors occurred.",
  "status": 400,
  "errors": {
    "": [
      "The Make name 'Toyota' is already in use."
    ]
  },
  "traceId": "00-30bc11fbb22071998c05660fdc454f5b-1ef36a85ecfeaf9b-00"
}
```

OK that's maybe the best response we've had so far. It includes not only a proper HTTP status code but also a human readable message that a frontend app can display to its users. Also, with this approach, we don't have to use a `try-catch` in the endpoint's action method like we did before. This is because our attribute plugs right into ASP.NET's [model validation functionality](https://learn.microsoft.com/en-us/aspnet/core/mvc/models/validation?view=aspnetcore-8.0), which triggers automatically at the beginning of every API request.

## A generic custom validation attribute to enforce uniqueness

The only disadvantage of our validation attribute is that it only works for one particular class and one particular property. I'm thinking we can make something a little bit more generic which we can reuse in many scenarios.

We could implement an [abstract base class](https://www.geeksforgeeks.org/c-sharp-abstract-classes/) that defines the core validation logic as a [template method](https://en.wikipedia.org/wiki/Template_method_pattern). The overall algorithm will be implemented in the abstract base class. Then, more concrete derived classes will provide the specializations to handle particular objects and fields.

We can refactor our code to make that happen. We should identify the parts of the code that are generic and the ones that are specific. The generic ones won't change, regardless of what's being validated. So they will be part of the abstract base class. On the other hand, the specific ones will vary, so they are better defined in derived classes. The base class will provide [hooks](https://en.wikipedia.org/wiki/Hooking) for the derived ones to implement and supply specializations.

Looking at our current code, here's what I can identify:

```csharp
[AttributeUsage(AttributeTargets.Class)]
public class UniqueMakeNameAttribute : ValidationAttribute
{
    protected override ValidationResult? IsValid(
        object? value,
        ValidationContext context
    ) {
        if (value == null) return ValidationResult.Success;

        // Depending on the entity being validated, the repository to use to
        // try to find a would-be duplicated record in the database will be
        // different. So, this line for obtaining a reference to the repository
        // is better implemented in a derived class.
        var repo = context.GetService<IMakeRepository>();
        if (repo == null) return ValidationResult.Success;

        // The type of "value" will be different depending on the class that
        // this attribute is applied to. That means that this casting to "Make"
        // belongs in a derived class.
        return Validate((Make)value, repo);
    }

    private static ValidationResult? Validate(Make input, IMakeRepository repo)
    {
        // Each repository will have its own method for trying to find records.
        // What's more, each entity will have its own field through which its
        // uniqueness is established. This is the responsibility of derived
        // classes.
        var existing = repo.FindByName(input.Name);

        // Every object being validated has its own method for determining if
        // they are equal to or different than what's found in the underlying
        // storage. That can't be part of the generic class.
        if (existing != null && input.ID != existing.ID)
        {
            // Depending on the object being validated, the error message will
            // need to be adjusted. That message belongs in derived classes.
            return new ValidationResult(
                $"The Make name '{input.Name}' is already in use."
            );
        }

        return ValidationResult.Success;
    }
}
```

With that figured out, here's an abstract, and generic, base class that can be used as a basis for implementing many concrete custom validation attributes:

```csharp
[AttributeUsage(AttributeTargets.Class)]
// This class is generic. TEntity is the type of the object that derived classes
// will validate. TRepo is the type of the repository that derived classes will
// use to query the database.
public abstract class BaseUniqueAttribute<TEntity, TRepo> : ValidationAttribute
{
    // These abstract methods are the hooks that derived classes will implement
    // in order to provide specializations for the core algorithm.
    // This one takes care of finding would-be repeated records.
    protected abstract TEntity? FindRecord(TEntity input, TRepo repository);
    // This one checks whether the existing record, if found, is the same being
    // validated.
    protected abstract bool IsSameRecord(TEntity input, TEntity existing);
    // This one produces the error message to return when validation fails.
    protected abstract string GetErrorMessage(TEntity input);

    protected override ValidationResult? IsValid(
        object? input,
        ValidationContext context
    ) {
        if (input == null) return ValidationResult.Success;

        // Here we use TRepo as a type parameter instead of IMakeRepository.
        // Derived classes will be responsible of defining which type the repo
        // will be.
        var repo = context.GetService<TRepo>();
        if (repo == null) return ValidationResult.Success;

        // Here we cast to TEntity instead of Make or any other concrete class.
        // The derived classes will specify the type.
        return Validate((TEntity)input, repo);
    }

    // The overall algorithm in this method remains pretty much identical.
    // Only some of the particular pieces have been replaced by abstract hooks
    // that are to be implemented in derived classes.
    private ValidationResult? Validate(TEntity input, TRepo repo)
    {
        var existing = FindRecord(input, repo);

        if (existing != null && !IsSameRecord(input, existing))
        {
            return new ValidationResult(GetErrorMessage(input));
        }

        return ValidationResult.Success;
    }
}
```

With that generic abstract class in place, we can develop new specific custom validation attributes very easily. For example, here's a new version of our `UniqueMakeNameAttribute`:

```csharp
public class UniqueMakeNameAttribute : BaseUniqueAttribute<Make, IMakeRepository>
{
    protected override Make? FindRecord(Make input, IMakeRepository repo) =>
        repo.FindByName(input.Name);

    protected override bool IsSameRecord(Make input, Make existing) =>
        input.ID == existing.ID;

    protected override string GetErrorMessage(Make input) =>
        $"The Make name '{input.Name}' is already in use.";
}
```

Very compact, huh? With this base class, new concrete validation attributes just need to inherit from `BaseUniqueAttribute`, provide it the proper type parameters (`Make` and `IMakeRepository` in this case), and implement the three abstract methods. All of which are simple one liners.

You can test the endpoint again now and should see the same behavior as before. That means the refactoring was successful!

## Writing a unit test for the custom validation attribute

Talking about tests, let's write a unit test for this. Testing custom validation attributes involves calling their `GetValidationResult` method and checking that it returns as expected. This is a public method defined in the `ValidationAttribute` base class. This method is defined by the framework, but it eventually calls our own custom logic that we wrote in the `IsValid` override.

For our validator, since it depends on an `IMakeRepository`, we're going to have to provide it as a [mock object](https://en.wikipedia.org/wiki/Mock_object). The validator also needs a `ValidationContext` instance that it can use to fetch services from the Dependency Injection container. Our test will also have to provide that in some way.

Here's what such a test could look like:

```csharp
[Fact]
public void GetValidationResult_ReturnsFailure_WhenAnotherMakeExistsWithTheSameName()
{
    // Arrange

    var attribute = new UniqueMakeNameAttribute();

    var existingMake = new Make() { ID = 10, Name = "test_name" };
    var makeToValidate = new Make() { ID = 20, Name = "test_name" };

    // We have to build a mock of type IMakeRepository for the service provider
    // to return. The attribute uses this class to query the database.
    // This test wants to trigger a validation failure. As such, this mock repo
    // is configured to return an object. This simulates that there is already
    // another record in the database that has the same name as the one being
    // validated.
    var mockRepository = new Mock<IMakeRepository>();
    mockRepository
        .Setup(m => m.FindByName(It.IsAny<string>()))
        .Returns(existingMake);

    // We also have to build a IServiceProvider mock. This will be used to
    // create a ValidationContext instance that the attribute will use to obtain
    // services available via Dependency Injection. Specifically, the repo.
    // With this configuration, it will return the mock repository.
    var mockServiceProvider = new Mock<IServiceProvider>();
    mockServiceProvider
        .Setup(m => m.GetService(typeof(IMakeRepository)))
        .Returns(mockRepository.Object);

    // The validation attribute needs a ValidationContext instance in order to
    // work. So we build this one, giving it the mock we've constructed.
    var context = new ValidationContext(makeToValidate, mockServiceProvider.Object, null);

    // Act

    // Here we invoke the public method that's available for us to run the
    // validation logic. This test expects the validation to fail.
    var result = attribute.GetValidationResult(makeToValidate, context);

    // Assert

    // Two simple assertions here. One checking that the result is not a success
    // and another checking that the expected error message is returned.
    Assert.NotEqual(ValidationResult.Success, result);
    Assert.Equal("The Make name 'test_name' is already in use.", result?.ErrorMessage);
}
```

And that's how you can test a custom validation attribute like the one we've built. This is very conventional as unit tests go. The only unusual things to keep in mind is the method we need to call in order to exercise the validation logic: `GetValidationResult`. And also how to construct and configure the `ValidationContext` object that the method needs as a parameter.

And that's all for now. We've seen two ways of implementing uniqueness validation in ASP.NET. One approach was leveraging an underlying relational database to create unique indexes. Another, more complicated but also more flexible approach, leverages framework features to create custom validation attributes. And we even saw how we can test them!
