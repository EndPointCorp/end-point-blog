---
author: "Juan Pablo Ventoso"
title: ".NET 5 will be released at .NET Conf 2020"
tags: dotnet, windows, microsoft
gh_issue_number: 1684
---

![.NET 5 Platform](/blog/2020/11/04/dotnet-5-released-net-conf-2020/dotnet-5-platform.png)

[.NET — A unified platform](https://devblogs.microsoft.com/dotnet/introducing-net-5/) by Microsoft

Last year, at .NET Conf 2019, Microsoft announced that the new .NET 5 will have a base class library that will allow creation of any type of application for any platform — Windows, Linux, Android, iOS, and IoT. And that’s finally about to happen: .NET 5 will be launched at [.NET Conf 2020](https://www.dotnetconf.net/), starting November 10th!

According to Microsoft, [.NET 5](https://devblogs.microsoft.com/dotnet/introducing-net-5/) will take the best of .NET Core, .NET Framework, Xamarin, and Mono and merge them into one framework, offering the same experience for all developers, regardless of the type of application or platform targeted. It will also include two different compiler models: just-in-time (JIT, prepared for client-server and desktop apps) and static compilation with ahead-of-time (AOT, optimized to decrease startup times, ideal for mobile and IoT devices).

Some of the key features will be:

### Windows Desktop development (WPF/​Windows Forms/​UWP)

This was already a part of the current .NET Core 3 release, and it will stay while getting some updates like a Chromium-based WebView control, improvements to the visual designer, and customizable task dialogs. It will also include all the latest features of C# 8.

### Full-stack web development (C#/​Blazor)

This feature is also present on the current .NET Core 3 version, and will be updated for this release. With Blazor, we can write full-stack web applications only using C#, removing the need to use a separate language for the frontend. While it’s still a discussed feature, the advantage of using it will depend on the type of web application we’re working on. But it’s there and it will be fully supported on .NET 5.

### C# 8

This version tries to reduce the well-known (by all of us!) null reference exceptions as a source of program failures by [introducing a nullability modifier for nullable reference types](https://docs.microsoft.com/en-us/archive/msdn-magazine/2018/february/essential-net-csharp-8-0-and-nullable-reference-types). Other main improvements include asynchronous streams, default interface methods and pattern matching enhancements. A full reference of all the new features can be found [here](https://docs.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-8).

### Updates to Entity Framework

EF will now integrate with the new C# 8, allowing us to consume the query results as [asynchronous streams](https://docs.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-8#asynchronous-streams), and automatically mapping the new non-nullable types to non-nullable fields on the database, among other improvements.

### Updates to ML.NET

.NET 5 will also include the latest version of [ML.NET](https://dotnet.microsoft.com/learn/ml-dotnet/what-is-mldotnet), a free, open-source, and cross-platform machine learning framework for .NET, with some key features like the `DatabaseLoader` class, which allows loading the data from any relational database with a connection string, and improvements to the object detection capabilities.

### And more

And of course, everything that was already on .NET Core 3 will be a part of .NET 5: multi-platform mobile development, Azure Cloud access tools, gaming development with Unity and traditional ASP.NET development, etc.

The long-term support (LTS) version of .NET Core is aimed to be launched in 2021, and it will be called .NET 6, hopefully recollecting everything that might be improved based on the feedback for this General Availability (GA) release.

The .NET development team at End Point will be attending the main talks that will happen at the .NET Conf 2020. On Day 1, the focus will be put on this new release, so stay tuned for more to come!
