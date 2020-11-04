---
author: "Juan Pablo Ventoso"
title: ".NET 5 will be released on the .NET Conf 2020"
tags: dotnet, windows, microsoft
---

![.NET 5 Platform](/blog/2020/11/04/dotnet-5-released-net-conf-2020/dotnet-5-platform.png)

[Photo](https://devblogs.microsoft.com/dotnet/introducing-net-5/) by [Microsoft](https://www.microsoft.com/)

Last year, on the .NET Conf 2019, Microsoft announced that the new .NET 5 will have a base class library that will allow creating any type of application for any platform - Windows, Linux, Android, iOS and IoT. And that's finally about to happen - .NET 5 will be launched at <a href="https://www.dotnetconf.net/" target="_blank">.NET Conf 2020</a>, starting November 10th!

According to Microsoft, <a href="https://devblogs.microsoft.com/dotnet/introducing-net-5/" target="_blank">.NET 5</a> will take the best out of .NET Core, .NET Framework, Xamarin and Mono and merge them into one framework, offering the same experience for all developers, regardless of the type of application or platform aimed. It will also include two different compiler models: just-in-time (JIT, prepared for client-server and desktop apps) y static compilation with ahead-of-time (AOT, optimized to decrease startup times, ideally for mobile and IoT devices).

Some of the key features will be:

### Windows Desktop development (WPF/Windows Forms/UWP)

This was already a part of the current .NET Core 3 release, and it will keep its way through with some updates, like a Chromium-based WebView control, updates to the visual designer and customizable task dialogs. It will also include all the latest features of C# 8.

### Full-stack web development (C#/Blazor)

This feature is also present on the current .NET Core 3 version, and it will be updated on this release. With Blazor, we can write full-stack web applications only using C#, removing the need of using a separate language for the frontend. While it's still a discussed feature, the advantage of using it will depend on the type of web application we're working on. But it's there and it will be fully supported on .NET 5.

### C# 8

This version tries to reduce the well-known (by all of us!) null reference exceptions as a source of program failures by <a href="https://docs.microsoft.com/en-us/archive/msdn-magazine/2018/february/essential-net-csharp-8-0-and-nullable-reference-types" target="_blank">introducing a nullability modifier for nullable reference types</a>. Other main improvements include asynchronous streams, default interface methods and pattern matching enhancements. A full reference of all the new features can be found <a href="https://docs.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-8" target="_blank">here</a>.

### Updates to Entity Framework

EF will now integrate with the new C# 8, allowing to consume the query results as <a href="https://docs.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-8#asynchronous-streams" target="_blank">asynchronous streams</a>, and automatically mapping the new non-nullable types to non-nullable fields on the database, among other improvements.

### Updates to ML.NET

.NET 5 will also include the latest version of <a href="https://dotnet.microsoft.com/learn/ml-dotnet/what-is-mldotnet" target="_blank">ML.NET</a> (a free, open-source and cross-platform machine learning framework for .NET), with some key features like the DatabaseLoader (allowing to load the data from any relational database with a connection string) or improvements to the object detection capabilities.


And of course, everything that was already on .NET Core 3 will be a part of .NET 5 (multi-platform mobile development, Azure Cloud access tools, gaming development with Unity and traditional ASP.NET development). The long-term support version of .NET Core is aimed to be launched in 2021, it will be called .NET 6, hopefully recollecting everything that might be improved based on the feedback for this GA release.

The .NET development team at End Point will be attending the main talks that will happen at the .NET Conf 2020. On Day 1, the focus will be the big .NET 5 release, so stay tuned! More to come.