---
author: "Bimal Gharti Magar"
title: "Introduction to Playwright using C#"
date: 2023-10-12
featured:
  image_url: 
description: This blog post shows basic usage of Playwright while explaining the advantages of the Playwright, which you can use for any kind of web automation tasks.
github_issue_number: 2012
tags:
- csharp
- testing
- automation
---

![In the foreground, the foliage of a light green tree edged with sunlight creates a line across the image. In the background, a mountain hillside with light dirt, intermittent exposed rock, and foliage just starting to turn the yellow, orange, and red colors of fall](/blog/2023/10/introduction-to-playwright-in-csharp/sun-on-green-leaves.webp)

<!-- Photo by Seth Jensen, 2023. -->

Automating web application tasks is a necessary skill for software developers and testers. You need it for performing repetitive tasks, conducting end-to-end testing of web applications, and scraping data from websites. In this blog post, we'll explore how to use C# with Playwright for automating tasks.

### What is Playwright?

Playwright is an open-source automation framework developed by Microsoft that allows you to automate web applications using various programming languages, including C#. Playwright was created specifically to accommodate the needs of end-to-end testing, but we will use it as a library for web automation. Playwright supports Chromium, WebKit, and Firefox. It runs on a variety of systems: Windows, Linux, and macOS, locally or on a continuous integration (CI) platform, headless or headed with native mobile emulation.

To begin web automation using C# and Playwright, follow these steps:

1. **Prerequisites:** You should have .NET Core or .NET 5+ installed on your machine.

2. **Create a New C# Project:** Let's start by creating a new C# console application.

    ```plain
    dotnet new console -n EPWebAutomation
    cd EPWebAutomation
    ```

3. **Install Playwright NuGet Package:** Open new project in Visual Studio or any preferred C# IDE and install the `Microsoft.Playwright` NuGet package and build the project using the following commands:

    ```plain
    dotnet add package Microsoft.Playwright
    dotnet build
    ```

4. **Install required browsers:** Run the following command to install the required browsers for Playwright:

    ```plain
    pwsh bin/Debug/netX/playwright.ps1 install
 
    # If the pwsh command does not work (throws TypeNotFound), make sure to use an up-to-date version of PowerShell.
    dotnet tool update --global PowerShell
    ```

5. **Initialize Playwright Instance:** Initialize Playwright in your C# code by creating a new browser instance and take a screenshot in Chromium:

    ```csharp
    using Microsoft.Playwright;
 
    using var playwright = await Playwright.CreateAsync();
    await using var browser = await playwright.Chromium.LaunchAsync();
    var page = await browser.NewPageAsync();
    ```

6. **Navigate and Interact:** You can now navigate to a web page using ``GotoAsync`` and interact with it using Playwright's APIs. For instance, to navigate to a website and take a screenshot, you can use the below code:

    ```csharp
    await page.GotoAsync("https://playwright.dev/dotnet");
    await page.ScreenshotAsync(new PageScreenshotOptions { Path = "screenshot.png" });
    ```

7. **Locators:** Playwright allows you to locate elements on the page using ID, CSS selectors, or XPaths. It also provides inbuilt [locators](https://playwright.dev/dotnet/docs/locators#quick-guide).

    ```csharp
    await page.GotoAsync("https://computer-database.gatling.io/computers");
    // fill dell in search text field using id selector
    await page.Locator("#searchbox").FillAsync("dell");
    // click on Filter by name button using id selector
    await page.Locator("#searchsubmit").ClickAsync();
    // click on a button using inbuild GetByText selector
    await page.GetByText("Add a new computer").ClickAsync();
    ```

8. **Fill form, select dropdown value and click elements:** Playwright allows you to perform actions like filling out forms, selecting dropdown value and clicking elements. Here's an example:

    ```csharp
    await page.FillAsync("#name", "asus abcde");
    await page.SelectOptionAsync("#company", new[] { new SelectOptionValue() { Label = "ASUS" } });
    await page.Locator("input[type=submit]").ClickAsync();
    ```

9. **Cleanup:** Don't forget to close the browser when you're done:

    ```csharp
    await browser.CloseAsync();
    ```

### Advantages of Using C# and Playwright

Some of the useful features of Playwright with C# include:

1. **Cross-Browser and cross-platform support:** As mentioned above, Playwright works on modern rendering engines including Chromium, WebKit, and Firefox. You also have the option of running it locally or on CI, and of running headless or headed.
3. **C# Language Familiarity:** The Playwright API can be used with C#. If you're already familiar with C#, this reduces the learning curve for web automation.
4. **Robust Documentation:** Playwright's documentation and community support make it easier to troubleshoot issues and find solutions.
5. **Headless and Headful Browsing:** Playwright allows you to choose between headless and headed mode. Debugging issues in headed mode can be much easier, since we can see what's going on in every line of code.
6. **Powerful APIs:** With Playwright's APIs, you can perform complex web automation tasks with ease.
7. **Powerful Tooling:** PLaywright has tooling like [Codegen](https://playwright.dev/dotnet/docs/codegen), [Playwright inspector](https://playwright.dev/dotnet/docs/debug#playwright-inspector), and [Trace Viewer](https://playwright.dev/dotnet/docs/trace-viewer-intro). They can help make using Playwright easier.
8. **Emulation:** You can test your app on any browser or emulate a real device such as mobile phone or tablet. It can emulate behavior such as `userAgent`, `geolocation`, `viewport`, and many more. You can read more about it in the [emulation](https://playwright.dev/dotnet/docs/emulation) documentation.

The powerful combination of C# and Playwright makes it a preferred tool for automating web tasks. When there are repetitive tasks or browser testing involved, Playwright can help you with getting the tasks done.
