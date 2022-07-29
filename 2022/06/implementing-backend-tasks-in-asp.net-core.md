---
author: "Kevin Campusano"
title: "Implementing Backend Tasks in ASP.NET Core"
date: 2022-06-26
tags:
- csharp
- dotnet
---

# Implementing Backend Tasks in ASP.NET Core

[As we've already established](https://www.endpointdev.com/blog/2022/01/database-integration-testing-with-dotnet/), [Ruby on Rails](https://rubyonrails.org/) is great. The amount and quality of tools that Rails puts at our disposal when it comes to developing web applications is truly outstanding. One aspect of web application development that Rails makes particularly easy is that of creating backend tasks.

These can be anything from database maintenance, filesystem cleanup, overnight heavy computations, bulk email dispatch, etc. In general, functionality that is tipically initiated by an sysadmin in the backend, or scheduled in a [cron](https://en.wikipedia.org/wiki/Cron) job, which has no GUI, but rather, is invoked via command line.

By integrating with [Rake](https://github.com/ruby/rake), Rails allows us to [very easily write such tasks](https://guides.rubyonrails.org/command_line.html#custom-rake-tasks) as plain old [Ruby](https://ruby-doc.org/) scrips. These scripts have access to all the domain logic and data that the full fledged Rails app has access to. The cherry on top is that the command line interface to invoke such tasks is very straightforward. It looks something like this: `bin/rails fulfillment:process_new_orders`.

All this is included right out of the box for new Rails projects.

[ASP.NET Core](https://dotnet.microsoft.com/en-us/apps/aspnet), which is also great, doesn't support this out of the box like Rails does.

However, I think we should be able to implement our own without too much hassle, and have a similar sysadmin experience. Let's see if we can do it.

# What we want to accomplish

So, to put it in concrete terms, we want to create a backend task that has access to all the logic and data of an existing ASP.NET Core application. The task should be ivokable via command line interface, so that it can be easily executed via the likes of cron or other scripts.

In order to meet these requirements, we will create a new .NET console app that:

1. References the existing ASP.NET Core project.
2. Loads all the classes from it and makes instances of them available via dependency injection.
3. Has a usable, UNIX-like command line interface that sysadmins would be familiar with.
4. Is invokable via the [.NET CLI](https://docs.microsoft.com/en-us/dotnet/core/tools/).

We will do all this within the context of an existing web application. One that I've been [building upon](https://www.endpointdev.com/blog/2021/07/dotnet-5-web-api/) [thoughout a few](https://www.endpointdev.com/blog/2022/01/database-integration-testing-with-dotnet/) [articles](https://www.endpointdev.com/blog/2022/06/implementing-authentication-in-asp.net-core-web-apis/).

It is a simple ASP.NET Web API backed by a [Postgres](https://www.postgresql.org/) database. It has a few endpoints for [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)ing automotive related data and for calculating values of vehicles based on various aspects of them.

You can find it [on GitHub](https://github.com/megakevin/end-point-blog-dotnet-5-web-api). If you'd like to follow along, clone the repository and checkout this commit: [TODO](https://github.com/megakevin/end-point-blog-dotnet-5-web-api/tree/TODO). It represents the project as it was before applying all the changes from this article. The finished product can be found [here](TODO).

You can follow the instructions in [the project's README file](https://github.com/megakevin/end-point-blog-dotnet-5-web-api/blob/json-web-token/VehicleQuotes/README.md) if you want to get the app up and running.

For our demo use case; we will try to develop a backend task that creates new user accounts for our existing application.

Let's get to it.

# Creating a new Console App that references the existing Web App as a library

The codebase is structured as a [solution](https://docs.microsoft.com/en-us/dotnet/core/tools/dotnet-sln), as given away by the `vehicle-quotes.sln` file located at the root of the repository. Within this solution, there are two projects: `VehicleQuotes` which is our web app itself, and `VehicleQuotes.Tests` which contains the app's test suite. For this article, we only care about the web app.

Like I said, the backend task that we will crate is nothing fancy in itself. It's a humble console app. So, we start by asking the `dotnet` CLI to create a new console app project for us.

From the repository's root directory, we can do so with this command:

```sh
dotnet new console -o VehicleQuotes.CreateUser
```

That should've resulted in a new `VehicleQuotes.CreateUser` directory being created, and within it, (along with some other nuts and bolts) our new console app's `Program.cs` (the code) and `VehicleQuotes.CreateUser.csproj` (the project definition) files. The name that we've chosen is straightforward: the name of the overall solution and the action that this console app is going to perform.

> There's more info regarding the `dotnet new` command in [the official docs](https://docs.microsoft.com/en-us/dotnet/core/tools/dotnet-new).

Now, since we're using a solution file, let's add our brand new console app project to it with:

```sh
dotnet sln add VehicleQuotes.CreateUser
```

Ok cool. That shoul've produced the following diff on `vehicle-quotes.sln`:

```diff
diff --git a/vehicle-quotes.sln b/vehicle-quotes.sln
index 537d864..5da277d 100644
--- a/vehicle-quotes.sln
+++ b/vehicle-quotes.sln
@@ -7,6 +7,8 @@ Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "VehicleQuotes", "VehicleQuo
 EndProject
 Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "VehicleQuotes.Tests", "VehicleQuotes.Tests\VehicleQuotes.Tests.csproj", "{5F6470E4-12AB-4E30-8879-3664ABAA959D}"
 EndProject
+Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "VehicleQuotes.CreateUser", "VehicleQuotes.CreateUser\VehicleQuotes.CreateUser.csproj", "{EDBB33E3-DCCE-4957-8A69-DC905D1BEAA4}"^M
+EndProject^M
 Global
        GlobalSection(SolutionConfigurationPlatforms) = preSolution
                Debug|Any CPU = Debug|Any CPU
@@ -44,5 +46,17 @@ Global
                {5F6470E4-12AB-4E30-8879-3664ABAA959D}.Release|x64.Build.0 = Release|Any CPU
                {5F6470E4-12AB-4E30-8879-3664ABAA959D}.Release|x86.ActiveCfg = Release|Any CPU
                {5F6470E4-12AB-4E30-8879-3664ABAA959D}.Release|x86.Build.0 = Release|Any CPU
+               {EDBB33E3-DCCE-4957-8A69-DC905D1BEAA4}.Debug|Any CPU.ActiveCfg = Debug|Any CPU^M
+               {EDBB33E3-DCCE-4957-8A69-DC905D1BEAA4}.Debug|Any CPU.Build.0 = Debug|Any CPU^M
+               {EDBB33E3-DCCE-4957-8A69-DC905D1BEAA4}.Debug|x64.ActiveCfg = Debug|Any CPU^M
+               {EDBB33E3-DCCE-4957-8A69-DC905D1BEAA4}.Debug|x64.Build.0 = Debug|Any CPU^M
+               {EDBB33E3-DCCE-4957-8A69-DC905D1BEAA4}.Debug|x86.ActiveCfg = Debug|Any CPU^M
+               {EDBB33E3-DCCE-4957-8A69-DC905D1BEAA4}.Debug|x86.Build.0 = Debug|Any CPU^M
+               {EDBB33E3-DCCE-4957-8A69-DC905D1BEAA4}.Release|Any CPU.ActiveCfg = Release|Any CPU^M
+               {EDBB33E3-DCCE-4957-8A69-DC905D1BEAA4}.Release|Any CPU.Build.0 = Release|Any CPU^M
+               {EDBB33E3-DCCE-4957-8A69-DC905D1BEAA4}.Release|x64.ActiveCfg = Release|Any CPU^M
+               {EDBB33E3-DCCE-4957-8A69-DC905D1BEAA4}.Release|x64.Build.0 = Release|Any CPU^M
+               {EDBB33E3-DCCE-4957-8A69-DC905D1BEAA4}.Release|x86.ActiveCfg = Release|Any CPU^M
+               {EDBB33E3-DCCE-4957-8A69-DC905D1BEAA4}.Release|x86.Build.0 = Release|Any CPU^M
        EndGlobalSection
 EndGlobal
```

This allows the .NET tooling to know that we've got some intentional organization going on in our code base. That these projects each form part of a bigger whole.

> It's also nice to add a [`.gitignore`](https://git-scm.com/docs/gitignore) file for our new `VehicleQuotes.CreateUser` project to keep things manageable. `dotnet new` can help with that if we were to navigate into the `VehicleQuotes.CreateUser` directory and run:
>
> ```sh
> dotnet new gitignore
> ```

> You can learn more about how to work with solutions via the .NET CLI in [the official docs](https://docs.microsoft.com/en-us/dotnet/core/tools/dotnet-sln).

Now let's modify our new project's `.csproj` file so that it references the main web app project under `VehicleQuotes`. This will allow our console app to access all of the classes defined in the web app, as if it was a library or package.

If we move to the `VehicleQuotes.CreateUser` directory, we can do that with the following command:

```sh
dotnet add reference ../VehicleQuotes/VehicleQuotes.csproj
```

The command itsef is pretty self-explanatory. It just expects to be given the `.csproj` file of the project that we want to add as a reference in order to do its magic.

Running that should've added the following snippet to `VehicleQuotes/VehicleQuotes.csproj`:

```xml
<ItemGroup>
  <ProjectReference Include="..\VehicleQuotes\VehicleQuotes.csproj" />
</ItemGroup>
```

This way, .NET knows allows the code defined in the `VehicleQuotes` project to be used within the `VehicleQuotes.CreateUser` project.

> You can learn more about the add reference command in [the official docs](https://docs.microsoft.com/en-us/dotnet/core/tools/dotnet-add-reference).

# Setting up Dependency Injection in the Console App

As a result of the previous steps, our new console app now has access to the classes defined within the web app. However, classes by themselves are no good if we can't actually create instances of them that we can interact with. The premier method for getting instance of classes in .NET is via dependency injection. So, we need to set that up for our little console app.

Dependency injection is something that comes set up out of the box for ASP.NET web apps. Luckily for us, .NET makes it fairly easy for us to leverage the same components for use within console apps as well.

For this app, we want to create user accounts. In the web app, user account management is done via [ASP.NET Core Identity]((https://docs.microsoft.com/en-us/aspnet/core/security/authentication/identity?view=aspnetcore-6.0&tabs=netcore-cli)). Specifically, the `UserManager` class is used to create new user accounts. This console app will do the same.

> Take a look at `VehicleQuotes/Controllers/UsersController.cs` to see how the user accounts are created. If you'd like to know more about integrating ASP.NET Core Identity into an existing web app, I wrote [an article](https://www.endpointdev.com/blog/2022/06/implementing-authentication-in-asp.net-core-web-apis/) about it.

Before we do the dependency injection setup, let's add a new class to our console app project that will encapsulate the logic of leveraging the `UserManager` for user account creation. In other words, this is the core of the backend task that we want the console app to perform. The new class will be defined in `VehicleQuotes.CreateUser/UserCreator.cs` and these will be its contents:

```csharp
using Microsoft.AspNetCore.Identity;

namespace VehicleQuotes.CreateUser;

class UserCreator
{
    private readonly UserManager<IdentityUser> _userManager;

    public UserCreator(UserManager<IdentityUser> userManager) {
        _userManager = userManager;
    }

    public IdentityResult Run(string username, string email, string password)
    {
        var userCreateTask = _userManager.CreateAsync(
            new IdentityUser() { UserName = username, Email = email },
            password
        );

        var result = userCreateTask.Result;

        return result;
    }
}
```

This class is pretty lean. All it does is define a constructor that expects an instance of `UserManager<IdentityUser>`, which will be supplied via dependency injection; and a simple `Run` method that, when given a username, email and password, asks the `UserManager<IdentityUser>` instance that it was given to create a user account.

Moving on to setting up dependency injection now, we will do it in `VehicleQuotes.CreateUser/Program.cs`. Replace the contents of that file with this:

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using VehicleQuotes.CreateUser;

IHost host = Host.CreateDefaultBuilder(args)
    .UseContentRoot(System.AppContext.BaseDirectory)
    .ConfigureServices((context, services) =>
    {
        var startup = new VehicleQuotes.Startup(context.Configuration);
        startup.ConfigureServices(services);

        services.AddTransient<UserCreator>();
    })
    .Build();

var userCreator = host.Services.GetRequiredService<UserCreator>();
userCreator.Run(args[0], args[1], args[2]);
```

Let's dissect this line by line.

First off, we got a few `using` statements that we need in order to access some classes and extension methods that we need down below. `using Microsoft.Extensions.DependencyInjection` gives us access the the `AddTransient` and `GetRequiredService` methods which we will discuss shortly. `using Microsoft.Extensions.Hosting` allows us to use `IHost` and `Host` types. And finally `using VehicleQuotes.CreateUser` allows this file to see the `UserCreator` class that we defined above.

Next, we create and configure a new `IHost` instance. .NET Core introduced the concept of a "host" as an abstraction for programs; and packed in there a lot of functionality to help with things like configuration, logging and, most importantly for us, dependency injection. To put it simply, the simplest way of enabling dependency injection in a console app is to use a `Host` and all the goodies that come within.

> There's much more information about hosts in [.NET's official documentation](https://docs.microsoft.com/en-us/dotnet/core/extensions/generic-host).

`Host.CreateDefaultBuilder(args)` gives us an `IHostBuilder` instance that we can use to configure our host. In our case, we've chosen to call `UseContentRoot(System.AppContext.BaseDirectory)` on it, which makes it possible for the app to find assets (like `appconfig.json` files!) regardless of where its deployed and where its being called from.

This is important for us because, as you will see later, we will install this console app as a [.NET Tool](https://docs.microsoft.com/en-us/dotnet/core/tools/global-tools). .NET Tools are installed in directories picked by .NET and can be run from anywhere in the system. So we need to make sure that our app can find its assets wherever its executable may be. As long as said assets are deployed in the same directory as the executable itself that is!

After that, we call `ConfigureServices` where we do a nice trick in order to make sure our console app has all the same configuration as the web app as far as dependency inejction goes.

You see, in ASP.NET Core, all the service classes that are to be made available to the application via dependency injection are configured within the web app's `Startup` class' `ConfigureServices` method. `VehicleQuotes` is no exception. So, in order for our console app to have access to all of the services (i.e. instances of classes) that the web app does, the console app needs to call that same code. And that's exactly what's happening in these two lines:

```csharp
var startup = new VehicleQuotes.Startup(context.Configuration);
startup.ConfigureServices(services);
```

We create a new instance of the web app's `Startup` class and call its `ConfigureServices` method. That's the key element that makes the console app have access to all the logic that the web app does. Including the services/classes provided by ASP.NET Core Identity like `UserManager<IdentityUser>`, which `UserCreator` needs in order to function.

Once that's done, the rest is straightforward.

We also add our new `UserCreator` to the dependency injection engine via:

```csharp
services.AddTransient<UserCreator>();
```

> Curious about what `Transient` means? [The official .NET documentation](https://docs.microsoft.com/en-us/dotnet/core/extensions/dependency-injection#service-lifetimes) has the answer.

And that allows us to obtain an instace of it with:

```csharp
var userCreator = host.Services.GetRequiredService<UserCreator>();
```

And then, it's just a matter of calling its `Run` method like so, passing it the command line arguments:

```csharp
userCreator.Run(args[0], args[1], args[2]);
```

`args` is a special variable that contains an array with the arguments given by command line. That means that our console app can be called like this:

```sh
dotnet run test_username test_email@email.com mysecretpassword
```

Go ahead, you can try it out and see the app log what it's doing. Once done, it will also have created a new record in the database.

```
$ psql -h localhost -U vehicle_quotes
psql (14.3 (Ubuntu 14.3-0ubuntu0.22.04.1), server 14.2 (Debian 14.2-1.pgdg110+1))
Type "help" for help.

vehicle_quotes=# select user_name, email from public."AspNetUsers";
   user_name   |           email            
---------------+----------------------------
 test_username | test_email@email.com
(1 rows)
```

Pretty neat, huh? At this point we have a console app that creates user accounts for our existing web app. It works, but it could be better. Let's add a nice command line interface experience now.

# Improving the CLI with CommandLineParser

With help from [CommandLineParser](https://github.com/commandlineparser/commandline), we can develop a unix-like command line interface for our app. We can use it to add help text, examples, have strongly typed parameters and useful error messages when said parameters are not correctly provided. Let's do that now.

First, we need to install the package in our console app project by running the following command from within the project's directory (`VehicleQuotes.CreateUser`):

```sh
dotnet add package CommandLineParser
```

After that's done, a new section would've been added to `VehicleQuotes.CreateUser/VehicleQuotes.CreateUser.csproj` that looks like this:

```xml
<ItemGroup>
  <PackageReference Include="CommandLineParser" Version="2.9.1" />
</ItemGroup>
```

That allows our console app to use the classes provided by the package.

All specifications for `CommandLineParser` are done via a plain old C# class that we need to define. For this console app, which accepts three mandatory arguments, such a class could look like this:

```csharp
using CommandLine;
using CommandLine.Text;

namespace VehicleQuotes.CreateUser;

class CliOptions
{
    [Value(0, Required = true, MetaName = "username", HelpText = "The username of the new user account to create.")]
    public string Username { get; set; }

    [Value(1, Required = true, MetaName = "email", HelpText = "The email of the new user account to create.")]
    public string Email { get; set; }

    [Value(2, Required = true, MetaName = "password", HelpText = "The password of the new user account to create.")]
    public string Password { get; set; }

    [Usage(ApplicationAlias = "create_user")]
    public static IEnumerable<Example> Examples
    {
        get
        {
            return new List<Example> {
                new (
                    "Create a new user account",
                    new CliOptions { Username = "name", Email = "email@domain.com", Password = "secret" }
                )
            };
        }
    }
}
```

I've decided to name it `CliOptions` but really, it could have been anything. Go ahead and create it in `VehicleQuotes.CreateUser/CliOptions.cs`. There are a few interesting elements to note here.

The key aspect is that we have a few properties: `Username`, `Email` and `Password`. These represent our three command line arguments. Thanks to the `Value` attributes that they have been annotatted with, `CommandLineParser` will know that that's their purpose. You can see how the attributes themselves also contain each argument's specification like the order in which they should be supplied, as well as their name and help text.

This class also defines an `Examples` getter which is used by `CommandLineParser` to print out usage examples into the console when our app's help is invoked.

Other than that, the class itself is unremarkable. In summary, it's a number of fields annotated with attributes so that `CommandLineParser` know what to do with it.

In order to actually put it to work, we update our `VehicleQuotes.CreateUser/Program.cs` like so:

```diff
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
+using CommandLine;
using VehicleQuotes.CreateUser;

+void Run(CliOptions options)
+{
    IHost host = Host.CreateDefaultBuilder(args)
        .UseContentRoot(System.AppContext.BaseDirectory)
        .ConfigureServices((context, services) =>
        {
            var startup = new VehicleQuotes.Startup(context.Configuration);
            startup.ConfigureServices(services);

            services.AddTransient<UserCreator>();
        })
        .Build();

    var userCreator = host.Services.GetRequiredService<UserCreator>();
-   userCreator.Run(args[0], args[1], args[2]);
+   userCreator.Run(options.Username, options.Email, options.Password);
+}
+
+Parser.Default
+    .ParseArguments<CliOptions>(args)
+    .WithParsed(options => Run(options));
```

We've wrapped the original code that we had in `Program.cs` into a method simply called `Run`.

Also, we've added this snippet at the bottom of the file:

```csharp
Parser.Default
    .ParseArguments<CliOptions>(args)
    .WithParsed(options => Run(options));
```

That's how we ask `CommandLineParser` to parse the incoming CLI arguments, as specified by `CliOptions` and, if it can be done successfully, then execute the rest of the program by calling the `Run` method.

Neatly, we also no longer have to use the `args` array directly in order to get the command line arguments provided to the app, instead we use the `options` object that `CommandLineParser` creates once it has done its parsing. You can see it in this line:

```csharp
userCreator.Run(options.Username, options.Email, options.Password);
```

`options` is an instance of our very own `CliOptions` class, so we can access the properties that we defined within it. These contain the arguments that were passed to the program.

If you were to try `dotnet run` right now, you'd see the following output:

```sh
VehicleQuotes.CreateUser 1.0.0
Copyright (C) 2022 VehicleQuotes.CreateUser

ERROR(S):
  A required value not bound to option name is missing.
USAGE:
Create a new user account:
  create_user name email@domain.com secret

  --help               Display this help screen.

  --version            Display version information.

  username (pos. 0)    Required. The username of the new user account to create.

  email (pos. 1)       Required. The email of the new user account to create.

  password (pos. 2)    Required. The password of the new user account to create.
```

As you can see, `CommandLineParser` detected that no arguments were given, and as such, it printed out an error message, along with the descriptions, help text and example that we defined. Basically the instructions on how to use our console app.

Netx, let's see how we can deploy this console app as a .NET tool.

# Deploying the Console App as a .NET tool

Ok now we have a console app that does what it needs to do, with a decent interface. Let's make it even more accessible by deploying it as a .NET tool. If we do that, we'd be able to invoke it with a command like this:

```sh
dotnet create_user Kevin kevin@gmail.com secretpw
```

.NET makes this easy for us. There's a caveat that we'll discuss later, but for now, let's go through the basic setup.

.NET tools are essentially just glorified NuGet packages. As such, we begin by adding some additional package-related configuration options to `VehicleQuotes.CreateUser/VehicleQuotes.CreateUser.csproj`. We add them as children elements to the `<PropertyGroup>`:

```xml
<PackAsTool>true</PackAsTool>
<PackageOutputPath>./nupkg</PackageOutputPath>
<ToolCommandName>create_user</ToolCommandName>
<VersionPrefix>1.0.0</VersionPrefix>
```

With that, we signal .NET that we want the console app to be packed as a tool, the path where it should put the package itself, and what its name will be. That is, how will it be invoked via the console (remember we want to be able to do `dotnet create_user`).

Finally, we specify a version number. When dealing with NuGet packages, versioning them is very important, as that drives some caching and downloading logic in NuGet. More on that later when we talk about the aforementioned caveats.

Now, to build the package, we use:

```sh
dotnet pack
```

That will build the application and produce a `VehicleQuotes.CreateUser/nupkg/VehicleQuotes.CreateUser.1.0.0.nupkg` file.

We won't make the tool available for the entire system. Instead, we will make it available from within the our solution's directory only. We can make that happen if we create a tool manifest file in the source code's root directory. That's done with this command, ran from the root dir:

```sh
dotnet new tool-manifest
```

That should create a new file: `.config/dotnet-tools.json`.

Now, also from the root directory, we finally install our tool:

```sh
dotnet tool install --add-source ./VehicleQuotes.CreateUser/nupkg VehicleQuotes.CreateUser
```

This is the regular command to install any tools in .NET. The interesting part is that we use the `--add-source` option to point it to the path where our package is located.

After that, .NET shows this output:

```
$ dotnet tool install --add-source ./VehicleQuotes.CreateUser/nupkg VehicleQuotes.CreateUser
You can invoke the tool from this directory using the following commands: 'dotnet tool run create_user' or 'dotnet create_user'.
Tool 'vehiclequotes.createuser' (version '1.0.0') was successfully installed. Entry is added to the manifest file /path/to/solution/.config/dotnet-tools.json.
```

It tells us all we need to know. Check out the `.config/dotnet-tools.json` to see how the tool has been addded there. Anyway, this means we can run our console app as a .NET tool:

```sh
$ dotnet create_user --help
VehicleQuotes.CreateUser 1.0.0
Copyright (C) 2022 VehicleQuotes.CreateUser
USAGE:
Create a new user account:
  create_user name email@domain.com secret

  --help               Display this help screen.

  --version            Display version information.

  username (pos. 0)    Required. The username of the new user account to create.

  email (pos. 1)       Required. The email of the new user account to create.

  password (pos. 2)    Required. The password of the new user account to create.
```

Pretty sweet, huh? And yes, it has taken a lot more effort than what it would've taken in Ruby on Rails, but hey, the end result is pretty fabulous I think, and we learned a new thing. Besides, once you've done it once, the skeleton can be easily reused for all kinds of different backend tasks.

Now, before we wrap this up, there's something we need to consider when actively developing these tools. That is, making changes and re-installing constantly.

The main aspect to understand is that tools are just NuGet packages, and as such are beholden to the NuGet package infrastructure. Whcih includes caching. If you're in the process of developing your tool and are quickly making and deploying changes, NuGet wont update the cache unless you do one of two things:

1. Manually clear it with a command like `dotnet nuget locals all --clear`.
2. Bump up the version of the tool by updating the value of `<VersionSuffix>` in the project (`.csproj`) file.

This means that, unless you do one these, the changes that you make to the app between re-builds (with `dotnet pack`) and re-installs (with `dotnet dotnet tool install`) wont ever make their way to the package that's actually installed. So be sure to keep that in mind.

# Table of contents

- [Implementing Backend Tasks in ASP.NET Core](#implementing-backend-tasks-in-aspnet-core)
- [What we want to accomplish](#what-we-want-to-accomplish)
- [Creating a new Console App that references the existing Web App as a library](#creating-a-new-console-app-that-references-the-existing-web-app-as-a-library)
- [Setting up Dependency Injection in the Console App](#setting-up-dependency-injection-in-the-console-app)
- [Improving the CLI with CommandLineParser](#improving-the-cli-with-commandlineparser)
- [Deploying the Console App as a .NET tool](#deploying-the-console-app-as-a-net-tool)
- [Table of contents](#table-of-contents)