---
author: "Kevin Campusano"
title: "Using Razor templates for rendering HTML emails in .NET"
date: 2024-04-23
featured:
  image_url:
description:
tags:
- emails
- dotnet
- csharp
- razor
---

When it comes to sending emails, [Ruby on Rails](https://rubyonrails.org/) has an excellent solution in the form of [Action Mailer](https://guides.rubyonrails.org/action_mailer_basics.html).

The basic idea is that you can define email templates using [ERB](https://github.com/ruby/erb) files. This is the same templating engine/language used for normal web application views. Then, [application-level SMTP settings are configured](https://guides.rubyonrails.org/action_mailer_basics.html#action-mailer-configuration) for email delivery. Finally, a "[Mailer](https://guides.rubyonrails.org/action_mailer_basics.html#sending-emails)" class can be developed that leverages the templates and the underlying email sending mechanism to send emails.

In Rails, all this comes right out the box. Setup is minimal, so this approach is a huge time saver for a task that's very common in web applications.

In [ASP.NET Core](https://dotnet.microsoft.com/en-us/apps/aspnet) (or .NET in general), we don't have such a convenient, built-in solution. However, it is possible to implement our own using the framework's features.

In this article, I'm going to explain step by step what I did in a recent .NET project to develop functionality similar to what Action Mailer provides.

> Throughout this article, I will be using a demo Web API application for code examples. If you'd like to see what the final implementation looks like, [you can find all the code on GitHub](https://github.com/megakevin/end-point-blog-dotnet-8-demo). The API is about calculating quotes for used vehicles. Using the process described here, I added the feature to send emails when new quotes are generated.
>
> In fact, I have all of these changes in a single commit. [Here's the diff](https://github.com/megakevin/end-point-blog-dotnet-8-demo/commit/06abed402302316fad980cfbdd0aa9bfdc14aafe).


## The plan

So here's the problem statement: I want to be able to send emails from my .NET app. The body of those emails need to be HTML, and they need to be built based on Razor templates. That is, I want to be able to define `*.cshtml` files for them. I also want to be able to define a "Mailer" class for each specific transaction or event that I want to send emails for. These "Mailer" classes are what the domain logic components will use directly to send the emails. They are the system's gateway into email sending functionality.

To fulfill those requirements, we will need four elements:

1. A base component for sending emails.
2. A component for turning Razor templates (i.e. `*.cshtml` files) into email bodies.
3. The actual templates.
4. A concrete component that domain logic can invoke to send transactional emails.

## Step 1: Sending emails in .NET with the MailKit NuGet package

Creating a class that sends emails, leveraging the [MailKit](https://github.com/jstedfast/MailKit) [NuGet package](https://www.nuget.org/packages/MailKit/), is easy. I ended up using the approach discussed in [this article](https://mailtrap.io/blog/asp-net-core-send-email/) from [Mailtrap](https://mailtrap.io/)'s blog.

The first thing to do is to install the MailKit NuGet package. This command will do it:

```sh
dotnet add package MailKit --version 4.5.0
```

The next to do is add the necessary SMTP configuration settings into the project's `appsettings.json` file. Here's what one might look like when configured to use Mailtrap.

```json
// VehicleQuotes.WebApi/appsettings.json
{
    // ...
    "MailSettings": {
        "Server": "sandbox.smtp.mailtrap.io",
        "Port": 587, // 25 or 465 or 587 or 2525
        "SenderName": "VehicleQuotes",
        "SenderEmail": "system@vehiclequotes.com",
        "UserName": "YOUR_SMTP_SERVER_USER_NAME",
        "Password": "YOUR_SMTP_SERVER_USER_PASSWORD"
    },
    // ...
}
```

Next, we define a class that contains the data structure of these settings. Here's the one I ended up with:

```csharp
// VehicleQuotes.WebApi/Configuration/MailSettings.cs
namespace VehicleQuotes.WebApi.Configuration;

public class MailSettings
{
    public required string Server { get; set; }
    public required int Port { get; set; }
    public required string SenderName { get; set; }
    public required string SenderEmail { get; set; }
    public required string UserName { get; set; }
    public required string Password { get; set; }
}
```

Now, to make the settings actually accessible to the system, we need to add them to the [Dependency Injection container](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection?view=aspnetcore-8.0). I added this to the application's bootstrapping logic in my `Program.cs` file, before the call to `builder.Build();`:

```csharp
builder.Services.Configure<Configuration.MailSettings>(config.GetSection("MailSettings"));
```

This essentially tells .NET to read the `"MailSettings"` section from `appsettings.json` and load the data in an object of type `MailSettings`. This object will be available to any class in the system thanks to Dependency Injection. We will use it later.

Now we need to define a class for sending emails. This one is low level. All it does is send emails, it doesn't render Razor templates. Other components will take care of that. So for now, here's the class responsible for sending emails:

```csharp
// VehicleQuotes.WebApi/Services/Mailer.cs
using Microsoft.Extensions.Options;
using MailKit.Net.Smtp;
using MimeKit;
using VehicleQuotes.WebApi.Configuration;

namespace VehicleQuotes.WebApi.Services;

public class MailData
{
    public required string To { get; set; }
    public required string ToName { get; set; }
    public required string Subject { get; set; }
    public required string Body { get; set; }
}

public interface IMailer
{
    Task<bool> SendMailAsync(MailData mailData);
}

public class Mailer : IMailer
{
    private readonly MailSettings _mailSettings;

    public Mailer(IOptions<MailSettings> mailSettingsOptions)
    {
        _mailSettings = mailSettingsOptions.Value;
    }

    public async Task<bool> SendMailAsync(MailData mailData)
    {
        try
        {
            using var emailMessage = new MimeMessage();

            emailMessage.From.Add(new MailboxAddress(_mailSettings.SenderName, _mailSettings.SenderEmail));
            emailMessage.To.Add(new MailboxAddress(mailData.ToName, mailData.To));

            emailMessage.Subject = mailData.Subject;

            var emailBodyBuilder = new BodyBuilder
            {
                TextBody = mailData.Body,
                HtmlBody = mailData.Body
            };

            emailMessage.Body = emailBodyBuilder.ToMessageBody();

            using var mailClient = new SmtpClient();

            await mailClient.ConnectAsync(_mailSettings.Server, _mailSettings.Port, MailKit.Security.SecureSocketOptions.StartTls);
            await mailClient.AuthenticateAsync(_mailSettings.UserName, _mailSettings.Password);
            await mailClient.SendAsync(emailMessage);
            await mailClient.DisconnectAsync(true);

            return true;
        }
        catch
        {
            // TODO: log the email delivery failure
            return false;
        }
    }
}
```

This class is straightforward. It has a single method, `SendMailAsync`. The method receives the email subject, body and recipient within a `MailData` object. Then, it uses the conventional MailKit process to send the email: builds the message, sets sender and recipient, sets the body, connects to the server, authenticates, and sends the email.

For this class to be available at runtime, we need to add it to the Dependency Injection container. So, similar to how we did when loading the SMTP server configuration options, we add this line to the `Program.cs` file before the call to `builder.Build();`.

```csharp
builder.Services.AddTransient<Services.IMailer, Services.Mailer>();
```

Ok, with that, our system knows how to send emails. Let's see about the next step now.

## Step 2: Rendering Razor templates into strings

Now that we have our core mailer class, we see that it expects a string to use as a body for the emails it sends. So like I mentioned before, we need a component that can take Razor templates (i.e. `*.cshtml` files) and turn them into strings. Here's how that's done.

This component will live in a new [Razor Class Library project](https://learn.microsoft.com/en-us/aspnet/core/razor-pages/ui-class?view=aspnetcore-8.0&tabs=netcore-cli). The `*.cshtml` templates will also live here. We can create the project and add it to the solution with commands like these:

```sh
dotnet new razorclasslib -o VehicleQuotes.RazorTemplates -s
dotnet sln add ./VehicleQuotes.RazorTemplates/VehicleQuotes.RazorTemplates.csproj
```

Now comes the star of the show, the class that renders Razor templates into strings:

```csharp
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Abstractions;
using Microsoft.AspNetCore.Mvc.ModelBinding;
using Microsoft.AspNetCore.Mvc.Razor;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.AspNetCore.Mvc.ViewEngines;
using Microsoft.AspNetCore.Mvc.ViewFeatures;
using Microsoft.AspNetCore.Routing;
using Microsoft.Extensions.DependencyInjection;

namespace VehicleQuotes.RazorTemplates.Services;

public interface IRazorViewRenderer
{
    Task<string> Render<TModel>(string viewName, TModel model);
}

public class RazorViewRenderer : IRazorViewRenderer
{
    private readonly IRazorViewEngine _viewEngine;
    private readonly ITempDataProvider _tempDataProvider;
    private readonly IServiceScopeFactory _serviceScopeFactory;

    public RazorViewRenderer(
        IRazorViewEngine viewEngine,
        ITempDataProvider tempDataProvider,
        IServiceScopeFactory serviceScopeFactory
    ) {
        _viewEngine = viewEngine;
        _tempDataProvider = tempDataProvider;
        _serviceScopeFactory = serviceScopeFactory;
    }

    public async Task<string> Render<TModel>(string viewName, TModel model)
    {
        using var scope = _serviceScopeFactory.CreateScope();

        var httpContext = new DefaultHttpContext() { RequestServices = scope.ServiceProvider };
        var actionContext = new ActionContext(httpContext, new RouteData(), new ActionDescriptor());

        var view = FindView(actionContext, viewName);

        var viewData = new ViewDataDictionary<TModel>(new EmptyModelMetadataProvider(), new ModelStateDictionary())
        {
            Model = model
        };

        var tempData = new TempDataDictionary(httpContext, _tempDataProvider);

        using var output = new StringWriter();

        var viewContext = new ViewContext(
            actionContext,
            view,
            viewData,
            tempData,
            output,
            new HtmlHelperOptions()
        );

        await view.RenderAsync(viewContext);

        return output.ToString();
    }

    private IView FindView(ActionContext actionContext, string viewName)
    {
        var getViewResult = _viewEngine.GetView(executingFilePath: null, viewPath: viewName, isMainPage: true);
        if (getViewResult.Success)
        {
            return getViewResult.View;
        }

        var findViewResult = _viewEngine.FindView(actionContext, viewName, isMainPage: true);
        if (findViewResult.Success)
        {
            return findViewResult.View;
        }

        var searchedLocations = getViewResult.SearchedLocations.Concat(findViewResult.SearchedLocations);
        var errorMessage = string.Join(
            Environment.NewLine,
            new[] { $"Unable to find view '{viewName}'. The following locations were searched:" }.Concat(searchedLocations)
        );

        throw new InvalidOperationException(errorMessage);
    }
}
```

This class is complicated. It leverages several obscure framework components that are not very commonly used. I was able to piece it together with help from [here](https://scottsauber.com/2018/07/07/walkthrough-creating-an-html-email-template-with-razor-and-razor-class-libraries-and-rendering-it-from-a-net-standard-class-library/), [here](https://github.com/aspnet/Entropy/blob/master/samples/Mvc.RenderViewToString/RazorViewToStringRenderer.cs) and [here](https://stackoverflow.com/questions/63802400/return-view-as-string-in-net-core-3-0/64337478#64337478).

That's quite a bit of code, but most of it is ceremony in the service of executing two main steps:

1. Finding the `*.cshtml` file that corresponds to the given `viewName`.
2. Preparing an `IView` object can be used to render the template. It does so using the given `model` object which contains the actual data to fill out the template placeholders.

Finally, in order to make this class available to the system, we add it to Dependency Injection. Here's what that looks like:

```csharp
builder.Services.AddMvcCore().AddRazorViewEngine(); // Necessary for non-GUI projects.
builder.Services.AddTransient<RazorTemplates.Services.IRazorViewRenderer, RazorTemplates.Services.RazorViewRenderer>();
```

The only interesting thing here is the `services.AddMvcCore().AddRazorViewEngine();` line. I had to add that to my project because it is a Web API. That means that it doesn't include all the services related to rendering views. Other project types, that already include all the view-related services, like MVC or Razor Pages, may not need this line. Remember that our `RazorViewRenderer` class depends on all sorts of framework objects. This line makes sure that they are available.

## Step 3: Defining the email templates

Now that our system knows how to render Razor templates into strings, let's go ahead and actually implement some. The nice thing about this approach is that these templates are full Razor views. That means that features like layouts and partials are supported.

For the purposes of this demo, a simple layout with a header and a footer will suffice. Along with the body of the particular transactional email that we want to send.

Our layout could look like this:

```html
<!-- VehicleQuotes.RazorTemplates/Views/Shared/EmailLayout.cshtml -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email With Razor Templates</title>
</head>
<body>
    <p>Imagine this is a header</p>
    @RenderBody()
    <p>Imagine this is a footer</p>
</body>
</html>
```

Very simple as layouts go. It does little more than defining the basic HTML document structure and calling `@RenderBody()`.

We can also add a `_ViewStart.cshtml` file that specifies this layout as the layout to use for all other templates under the `Emails` directory:


```html
<!-- VehicleQuotes.RazorTemplates/Views/Emails/_ViewStart.cshtml -->
@{
    Layout = "EmailLayout";
}
```

Now, for the core contents of the email, we define a new template, along with a class that will serve as its view model. 

My template ended up looking like this:

```html
<!-- VehicleQuotes.RazorTemplates/Views/Emails/QuoteGenerated.cshtml -->
@using VehicleQuotes.RazorTemplates.ViewModels

@model QuoteGeneratedViewModel

<p>
    A quote has been generated for a @Model.Year @Model.Make @Model.Model.
</p>

<p>Quote ID: @Model.ID</p>
<p>Created At: @Model.CreatedAt.ToLongDateString()</p>
<p>Offered Amount: @Model.OfferedQuote</p>
<p>Message: @Model.Message</p>
```

And the view model:

```csharp
// VehicleQuotes.RazorTemplates/ViewModels/QuoteGeneratedViewModel.cs
namespace VehicleQuotes.RazorTemplates.ViewModels;

public class QuoteGeneratedViewModel
{
    public required int ID { get; set; }
    public required DateTime CreatedAt { get; set; }
    public required int OfferedQuote { get; set; }
    public required string Message { get; set; }
    public required string Year { get; set; }
    public required string Make { get; set; }
    public required string Model { get; set; }
}
```

Very simple. The template specifies the type that it accepts as a view model using the `@model` directive. It then proceeds to render the email contents using regular old Razor syntax. The view model is just a simple [POCO](https://en.wikipedia.org/wiki/Plain_old_CLR_object) that defines the data that the template can work with.

## Step 4: Putting it all together: the class that sends the "quote generated" email

Finally, we can define our specific Mailer class that, leveraging all the infrastructure we've put together, can send one specific type of transactional email. These classes are meant to be simple and boring. Here's mine:

```csharp
// VehicleQuotes.WebApi/Services/QuoteGeneratedMailer.cs
using VehicleQuotes.RazorTemplates.Services;
using VehicleQuotes.WebApi.ResourceModels;
using VehicleQuotes.RazorTemplates.ViewModels;

namespace VehicleQuotes.WebApi.Services;

public class QuoteGeneratedMailer
{
    private readonly IMailer _mailer;
    private readonly IRazorViewRenderer _razorViewRenderer;

    public QuoteGeneratedMailer(IMailer mailer, IRazorViewRenderer razorViewRenderer)
    {
        _mailer = mailer;
        _razorViewRenderer = razorViewRenderer;
    }

    public async Task SendAsync(QuoteGeneratedViewModel payload)
    {
        string body = await _razorViewRenderer.Render(
            "/Views/Emails/QuoteGenerated.cshtml", payload
        );

        await _mailer.SendMailAsync(new() {
            To = "test@email.com",
            ToName = "Mr. Recipient",
            Subject = $"VehicleQuotes - New Quote Generated - Quote #{payload.ID}",
            Body = body
        });
    }
}
```

Pretty neat, huh? This class receives instances of the base `Mailer` and the `RazorViewRenderer` via Dependency Injection and uses them to: 1. render the template; and 2. send the email.

Like everything else, it also needs to be made available via Dependency Injection. All in all, I ended up with this nice bundle in my `Program.cs` file:

```csharp
builder.Services.Configure<Configuration.MailSettings>(config.GetSection("MailSettings"));
builder.Services.AddScoped<Services.QuoteGeneratedMailer>();
builder.Services.AddMvcCore().AddRazorViewEngine();
builder.Services.AddTransient<RazorTemplates.Services.IRazorViewRenderer, RazorTemplates.Services.RazorViewRenderer>();
builder.Services.AddTransient<Services.IMailer, Services.Mailer>();
```

A good idea is to put these into an `IServiceCollection` extension method. That's what I ended up doing in fact.

Instances of a class like this can be used anywhere in the code. For example like this:

```csharp
// VehicleQuotes.WebApi/Services/QuoteService.cs
// _mailer is a QuoteGeneratedMailer
// Imagine response is an object that contains all these fields.
await _mailer.SendAsync(
    new QuoteGeneratedViewModel
    {
        ID = response.ID,
        CreatedAt = response.CreatedAt,
        OfferedQuote = response.OfferedQuote,
        Message = response.Message,
        Year = response.Year,
        Make = response.Make,
        Model = response.Model
    }
);
```

Just build the view model object that it expects and off it goes.

And that's it! That definitely took some elbow grease to get working as well as delving into pretty arcane framework features. In the end, however, we did manage to build something that offers a developer experience that's very similar to Action Mailer. Once the core `Mailer` and the `RazorViewRenderer` are in place; all it takes to send a new transactional email is:

1. Defining a new template, with its view model.
2. Defining a new Mailer class that renders the template, uses it as the email's body, and sends it.
