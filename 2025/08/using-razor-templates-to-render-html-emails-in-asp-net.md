---
author: "Kevin Campusano"
title: "Using Razor templates to render HTML emails in ASP.NET Core"
date: 2025-08-12
tags:
- csharp
- aspdotnet
- razor
- emails
---

A while ago [I blogged](https://www.endpointdev.com/blog/2024/04/using-razor-templates-to-render-emails-dotnet/) about using Razor templates to render HTML emails in [.NET](https://dotnet.microsoft.com/en-us/). The method that I discussed there worked, but it was very verbose. Since then, [.NET 8 has released](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-8/overview), and with it came [a simpler way of doing this](https://andrewlock.net/exploring-the-dotnet-8-preview-rendering-blazor-components-to-a-string/). In this post we'll explore how to use these new features to render HTML emails.

> You can find all the code in this post on [GitHub](https://github.com/megakevin/end-point-blog-razor-emails).

## The plan

Similar to the original article, the objective is simple: Sending emails from an ASP.NET Core app, and having the contents of those emails be rendered based on Razor templates. To that end, we need four pieces:

1. A class for sending emails.
2. A class for rendering Razor templates into strings.
3. A Razor template.
4. A class that puts it all together. That is, takes in parameters, renders the email, and sends it.

## Step 1: Sending emails with the MailKit NuGet package

With the help of the MailKit NuGet package, sending emails in .NET is easy. Let's install it with:

```sh
dotnet add package MailKit --version 4.13.0
```

We also need some configuration on the `appsettings.json` file, to define the settings needed to establish a connection with an SMTP server:

```json
// ./appsettings.json

{
    // ...
    "MailSettings": {
        "Server": "<YOUR_SMTP_SERVER>",
        "Port": 587, // 25 or 465 or 587 or 2525
        "SenderName": "RazorEmails",
        "SenderEmail": "test@razoremails.com",
        "UserName": "<YOUR_SMTP_SERVER_USER_NAME>",
        "Password": "<YOUR_SMTP_SERVER_USER_PASSWORD>"
    },
    // ...
}
```

And here's a simple `Mailer` class that uses the `MailKit` library and the configuration above to send emails:

```csharp
// ./Mailers/Mailer.cs

using MailKit.Net.Smtp;
using MimeKit;

namespace RazorEmails.Mailers;

public class MailData
{
    public required string To { get; set; }
    public required string ToName { get; set; }
    public required string Subject { get; set; }
    public required string Body { get; set; }
}

public class Mailer
{
    private readonly ILogger<Mailer> _logger;
    private readonly IConfiguration _config;

    public Mailer(IConfiguration config, ILogger<Mailer> logger)
    {
        _logger = logger;
        _config = config;
    }

    // Not much to see here, just a method for sending emails using MailKit.
    // Docs are here: https://github.com/jstedfast/MailKit
    public async Task<bool> SendMailAsync(MailData mailData)
    {
        try
        {
            var emailMessage = new MimeMessage();

            emailMessage.From.Add(new MailboxAddress(MailSenderName, MailSenderEmail));
            emailMessage.To.Add(new MailboxAddress(mailData.ToName, mailData.To));

            emailMessage.Subject = mailData.Subject;

            var emailBodyBuilder = new BodyBuilder
            {
                TextBody = mailData.Body,
                HtmlBody = mailData.Body
            };

            emailMessage.Body = emailBodyBuilder.ToMessageBody();

            using var smtpClient = new SmtpClient();

            await smtpClient.ConnectAsync(
                MailServer,
                MailPort,
                MailKit.Security.SecureSocketOptions.StartTls
            );

            await smtpClient.AuthenticateAsync(MailUserName, MailPassword);
            await smtpClient.SendAsync(emailMessage);
            await smtpClient.DisconnectAsync(true);

            return true;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to send email to {To}", mailData.To);
            return false;
        }
    }

    private string MailSenderName => _config["MailSettings:SenderName"]!;
    private string MailSenderEmail => _config["MailSettings:SenderEmail"]!;
    private string MailServer => _config["MailSettings:Server"]!;
    private int MailPort => int.Parse(_config["MailSettings:Port"]!);
    private string MailUserName => _config["MailSettings:UserName"]!;
    private string MailPassword => _config["MailSettings:Password"]!;
}
```

## Step 2: Rendering Razor templates into strings

Of course, we also need a way of rendering Razor templates. As mentioned in the beginning, .NET 8 made this easy. There's [a page in the official documentation](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/render-components-outside-of-aspnetcore?view=aspnetcore-9.0) and [community blog posts](https://andrewlock.net/exploring-the-dotnet-8-preview-rendering-blazor-components-to-a-string/) talking about it. For our purposes, here's a class that does it:

```csharp
// ./Rendering/RazorViewRenderer.cs

using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Web;

namespace RazorEmails.Rendering;

public class RazorViewRenderer
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILoggerFactory _loggerFactory;

    public RazorViewRenderer(IServiceProvider serviceProvider, ILoggerFactory loggerFactory)
    {
        _serviceProvider = serviceProvider;
        _loggerFactory = loggerFactory;
    }

    public async Task<string> Render<TView, TViewModel>(TViewModel model) where TView : IComponent
    {
        await using var htmlRenderer = new HtmlRenderer(_serviceProvider, _loggerFactory);

        var html = await htmlRenderer.Dispatcher.InvokeAsync(async () =>
        {
            var output = await htmlRenderer.RenderComponentAsync<TView>(
                ParameterView.FromDictionary(
                    new Dictionary<string, object?> { { "Model", model } }
                )
            );

            return output.ToHtmlString();
        });

        return html;
    }
}
```

The `Render` method is where the magic happens. We'll see how to use it soon, but for now, it's interesting to look at the generic type parameters.

`TView` represents the strongly-typed Razor template that will be rendered. Technically, the "template" is actually a "[Razor component](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/?view=aspnetcore-9.0)", as we'll see later. That's why we use `where TView : IComponent` as a [generic type constraint](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/where-generic-type-constraint). With it, we're specifying that the given `TView` must inherit from `Microsoft.AspNetCore.Components.IComponent`, which is the base class of Razor components.

`TViewModel` on the other hand, represents the type of the data structure that will be passed to the template as a parameter. It will contain data that the template will use to render itself.

## Step 3: Defining the email templates

OK now we need to define our templates, along with the vehicles to pass data to them. These will be simple [DTOs](https://en.wikipedia.org/wiki/Data_transfer_object).

When sending emails from web applications, it is often useful to define a layout that all emails use to keep their styling consistent. Using Razor components, such a layout could look like this:

```html
<!-- ./Rendering/Views/MainLayout.razor -->

@inherits LayoutComponentBase

<!DOCTYPE html>
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body>
  @Body
</body>
</html>
```

This is just a basic shell for an HTML document. Notice two interesting aspects of it:

1. `@inherits LayoutComponentBase` declares that our layout inherits from the `LayoutComponentBase`. This is necessary for the layout to actually act as a layout.
2. `@Body` determines where the contents of the components that use this layout will be rendered. In this case, we put it inside the `<body>` HTML tag, which seems appropriate.

Now to define the template for a basic email that uses this layout:

```html
<!-- ./Rendering/Views/MessageEmail.razor -->

@using RazorEmails.Rendering.ViewModels

<LayoutView Layout="@typeof(MainLayout)">

<p>
  Hello @Model.Greeting.
</p>

<p>
  We have a message for you: @Model.Message
</p>

<p>
  Message sent at @DateTime.Now.ToString().
</p>

</LayoutView>

@code {
  [Parameter]
  public MessageEmailViewModel Model { get; set; } = default!;
}
```

This is a very straightforward Razor component that takes in a `MessageEmailViewModel` as a parameter and renders a few lines of text using the data coming in the parameter. By virtue of its file name, this component can be referenced in code by the `MessageEmail` class name. It uses tried and true Razor syntax, so little of this should be surprising if you've already worked with Razor before.

One thing to notice is how we're explicitly declaring the `LayoutView` element, pointing to the `MainLayout` that we wrote. This is how we tell the renderer to use our layout when rendering this component. `MainLayout` exists because that's what we named the file that contains the layout.

Like I mentioned before, `MessageEmailViewModel` is a simple DTO that serves to pass some data to the template. It's not very exciting, but this is what it looks like:

```csharp
// ./Rendering/ViewModels/MessageEmailViewModel.cs

namespace RazorEmails.Rendering.ViewModels;

public class MessageEmailViewModel
{
    public required string Greeting { get; set; }
    public required string Message { get; set; }
}
```

## Step 4: Putting it all together: the class that sends the email

And finally, here we have a class that puts these separate elements to work to send an email:

```csharp
// ./Mailers/MessageMailer.cs

using RazorEmails.Rendering;
using RazorEmails.Rendering.ViewModels;
using RazorEmails.Rendering.Views;

namespace RazorEmails.Mailers;

public class MessageMailer
{
    private readonly Mailer _mailer;
    private readonly RazorViewRenderer _razorViewRenderer;

    public MessageMailer(Mailer mailer, RazorViewRenderer razorViewRenderer)
    {
        _mailer = mailer;
        _razorViewRenderer = razorViewRenderer;
    }

    public async Task SendAsync(string to, string toName, string greeting, string message)
    {
        string body = await _razorViewRenderer.Render<MessageEmail, MessageEmailViewModel>(
            new MessageEmailViewModel() { Greeting = greeting, Message = message }
        );

        await _mailer.SendMailAsync(new()
        {
            To = to,
            ToName = toName,
            Subject = $"{greeting}, we have a message for you.",
            Body = body
        });
    }
}
```

The `SendAsync` method sends the email. It takes a series of parameters and uses them to construct a `MessageEmailViewModel` object which is passed to the `RazorViewRenderer`'s `Render` method. It also specifies `MessageEmail` as the Razor component to render. `RazorViewRenderer` returns a string which is then sent to `Mailer`'s `SendMailAsync` method as the `Body` parameter, along with other parameters. The `Mailer` then uses these parameters to construct an email and send it.

To send emails, this class can be used like so:

```csharp
// Imagine we're running this in an ASP.NET Core app and getting an instance of MessageMailer via DI...
private readonly MessageMailer _messageMailer;

//... then, within some method, we can do:
await _messageMailer.SendAsync(
    "recipient@example.com",
    "Recipient Name",
    "Mr. Recipient",
    "Have a good day."
);
```

Simple and clean.

Alright! That's it for now. In this article we saw how to leverage new .NET 8 features for rendering Razor components into strings. We implemented an email sending capability based on that and the MailKit NuGet package. It was a nice way of revisiting an old topic, now made easier thanks to the latest updates from .NET.
