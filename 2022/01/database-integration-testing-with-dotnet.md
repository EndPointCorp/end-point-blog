---
author: "Kevin Campusano"
title: "Database integration testing with .NET"
date: 2022-01-03
tags:
- dotnet
- integration testing
- database testing
---

Ruby on Rails is great. We use it in End Point for many projects with great success. One of the cool features it has is how easy it is to write database integration tests. Out of the box, Rails projects come with all the configuration necessary to set up a database that's exclusive for testing. This database includes all the tables and other objects that exist within the regular database that the app uses during its normal execution. So, it is very easy to write automated tests that cover the application components that interact with the databse.

ASP.NET Core (which is also great!) however, doesn't have this feature out of the box. Let's see how hard would it be if we were to do it ourselves.

# Sample project

As a sample project we will use a web api that I developed for other article. You can find the source code here: https://github.com/megakevin/end-point-blog-dotnet-5-web-api

The app is very straightforward. blabal TODO COMPLETE THIS

There's one specific class that has some interesting logic that depends heavily on database interactions. As such, that class is a great candidate to cover with a few automated integration tests. The class in question is `QuotesService` (TODO: PUT LINK AND FULL PATH HERE). It provides features for fetching records from the database as well as creating new records based on data from the incoming request and a set of rules stored in the databse itself.

The first step is to organize our project so that it supports automated testing.

# Organizing the source code to allow for automated testing

In general, the source code of most real world .NET applications is organized as one or more "projects" under one "solution". Our sample app is a simple stand-alone "webapi" project, that's not within a solution. For automated tests however, we need to create a new project, parallel to the existing one, that's dedicated to tests. So, what we want to end up with is one solution with two projects inside of it. One project will be the webapi one we already have, and the other one will be our new test project.

That means that we need to reorganize the sample app's source code in order to comply with the "one solution and two projects" that I just described.

Let's start by moving all the files in the root directory into a new `VehicleQuotes` directory. That's one project. Then, we create a new automated tests project by running the following, still from the root directory:

```sh
dotnet new xunit -o VehicleQuotes.Tests
```

That creates a new automated tests project named `VehicleQuotes.Tests` which uses the xUnit.net test framework. There are other options when it comes to test frameworks in .NET. E.g. MSTest and Nunit. We're going to use xUnit.net which is the new hotness, but the others should work just as well for our purposes.

Now, we need to create a new solution to contain those two projects. Solutions come in the form of *.sln files and can be created like so:

```sh
dotnet new sln blabla
```

We should now have a file structure like this:

```
TODO: POT THE FILE STRUCTURE HERE
```

Now, we need to tell dotnet that the two projects that we created before belong in the same solution. These commands do that:

```sh
dotnet add blabla VehicleQuotes
dotnet add blabla VehicleQuotes.Tests
```

Finally, we update `VehicleQuotes.Tests` so that it references the webapi project. That way, the test suite will have access to all the classes defined in the webapi project. Here's the command for that:

```
dotnet add reference blablabl
```

# Creating a DbContext instance to talk to the database

# Defining the test database connection string in the appsettings.json file

# Writing a simple test case that fetches data

# Resetting the state of the database after each test

# Writing another simple test case that stores data

# Refactoring into a fixture for reusability

# Using transactions to reset the state of the database
