---
author: "Bimal Gharti Magar"
title: "Introduction to Playwright using C#"
date: 2004-09-30
tags:
- c-sharp
- playwright
---

Automating web application tasks is one of the necessary skills for software developers and testers. You need it for performing repetitive tasks or conducting end-to-end testing of web applications and sometimes scraping data from websites. In this blog post, we'll explore how to use C# with Playwright for automating tasks.

### What is Playwright?

Playwright is an open-source automation framework developed by Microsoft that allows you to automate web applications using various programming languages, including C#. Playwright was created specifically to accommodate the needs of end-to-end testing, however we will use it as a library for web automation. Playwright supports all modern rendering engines including Chromium, WebKit, and Firefox. Test on Windows, Linux, and macOS, locally or on CI, headless or headed with native mobile emulation.

To begin web automation using C# and Playwright, follow these steps:

1. **Prerequisites:** You should have .NET Core or .NET 5+ installed on our machine.

2. **Create a New C# Project:** Lets start by creating a new C# console application.
   ```pwsh
   dotnet new console -n EPWebAutomation
   cd EPWebAutomation
   ```

3. **Install Playwright NuGet Package:** Open new project in Visual Studio or any preferred C# IDE and install the ``Microsoft.Playwright`` NuGet package and build the project using the following commands:

   ```pwsh
   dotnet add package Microsoft.Playwright
   dotnet build
   ```


4. **Install required browsers:** Run the following command to install the required browsers for Playwright:
   ```pwsh
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

7. **Locators:** Playwright allows you to locate elements on the page using id, css selectors or XPaths. It also provides inbuilt [locators](https://playwright.dev/dotnet/docs/locators#quick-guide).
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

**Advantages of Using C# and Playwright**

1. **Cross-Browser Support:** Playwright supports all modern rendering engines including Chromium, WebKit, and Firefox.

3. **Cross-Platform Support:** Test on Windows, Linux, and macOS, locally or on CI, headless or headed.

2. **C# Language Familiarity:** Playwright API can be used with C#. Having familiarity with C# and usign it for web automation can reduce the learnig curve.

3. **Robust Documentation:** Playwright's documentation and community support are robust, making it easier to troubleshoot issues and find solutions.

4. **Headless and Headful Browsing:** Playwright allows you to choose between headless and headed mode. It makes it easier to write tests and debug an issue in headed mode as we can see what's going on in every line of code.

5. **Powerful APIs:** With Playwright's APIs, you can perform complex web automation tasks with ease.

6. **Powerful Tooling:** It has powerful tooling like [Codegen](https://playwright.dev/dotnet/docs/codegen), [Playwright inspector](https://playwright.dev/dotnet/docs/debug#playwright-inspector) and [Trace Viewer](https://playwright.dev/dotnet/docs/trace-viewer-intro). They help in making the playwright usage easier 

7. **Emulation:** You can test your app on any browser or emulate a real device such as mobile phone or tablet. It can emulate behavior such as ``userAgent``, ``geolocation``, ``viewport`` and many  more. You can read more about it in the [emulation](https://playwright.dev/dotnet/docs/emulation) documentation

There are many other features in playwright which are surely useful for any use cases.

**Conclusion**

The powerful combination of C# and Playwright makes it a preferred tool for automating web tasks. When there are repetitive tasks or browser testing involved, Playwright can help you with getting the tasks done. This blog post shows basic usage of Playwright while explaining the advantages of the Playwright, which you can use for any kind of web automation tasks.