---
author: "Juan Pablo Ventoso"
title: "Prepare for .NET Core 3 and .NET 5"
tags: dotnet
gh_issue_number: 1546
---

<img src="/blog/2019/08/03/prepare-for-dotnet-core-3-dotnet-5/image-0.jpg" alt="Prepare for .NET 5" /> [Photo](https://unsplash.com/photos/fPkvU7RDmCo) by Caspar Camille Rubin on Unsplash, edited by Juan Pablo Ventoso


### Introduction

It’s been a while now since .NET Core is out there: It was released back in June 2016 and it kept growing since then. The main advantages when comparing with .NET Framework is that .NET Core is free, open-source and cross-platform. It also has several <a href="https://devblogs.microsoft.com/dotnet/performance-improvements-in-net-core/" target="_blank">performance improvements</a> that gains up to 600% increase for some particular functions like converting elements to a string, or more than 200% for some LINQ queries, and a general performance boost in application startup.

But it also has drawbacks: Some third party libraries are still not fully supported, so while they can still be used, the compiled results will only be portable to Windows. Also, .NET Core 2.2 (the latest release to date) doesn’t yet have support for Windows Presentation Foundation (WPF) or Windows Forms applications... **But it looks like this is going to change soon.**


### Next stop: .NET Core 3

In the 2019 Build Conference that took place in May, <a href="https://devblogs.microsoft.com/dotnet/announcing-net-core-3/" target="_blank">.NET Core 3 was announced</a>: It’s expected to be released in November this year, and it will finally include support for Windows desktop development (WPF, UWP and Windows Forms). It will also include Entity Framework 6, since most existing Windows Forms and WPF applications use that framework to access data.

![.NET Core 3 features and tools](/blog/2019/08/03/prepare-for-dotnet-core-3-dotnet-5/image-1.jpg)

.NET Core 3 will also include support for IoT (Internet-of-things) applications, aiming for internet-enabled devices like smart locks or glasses, and will allow AI development through ML.NET (an open-source machine learning framework built for .NET). For those who can’t wait and want to try it out before its release, previews are <a href="https://devblogs.microsoft.com/dotnet/announcing-net-core-3-0-preview-7/" target="_blank">available to download</a>.


### Game changer: .NET 5

In the same conference, on May 7, Microsoft also announced that they are planning to release a new platform for building applications targetting all devices and operative systems in november 2020: <a href="https://devblogs.microsoft.com/dotnet/introducing-net-5/" target="_blank">.NET 5</a>. And while it will be based on .NET Core, the word “core” will be removed because Microsoft is aiming to unify .NET Framework into this new platform as well (that’s why its version number will be 5: to avoid confusion with existing 4.x versions of .NET Framework).

![.NET 5 features and tools](/blog/2019/08/03/prepare-for-dotnet-core-3-dotnet-5/image-2.jpg)

Microsoft defines .NET 5 as a “game changer”: In one hand, we can expect some important features to be improved. So far, Microsoft has stated that cross-platform will be mantained and even improved, and we will have two runtimes to choose (<a href="https://github.com/mono/mono" target="_blank">Mono</a> or <a href="https://github.com/dotnet/coreclr" target="_blank">CoreCLR</a>). Java, Objective-C and Swift interoperability will be also supported for all platforms.

But, on the other hand, **other features will be discontinued**: ASP.NET Web Forms will not be included, so legacy apps with this technology will have to stick with .NET Framework, or migrated to an alternative like the new client-based <a href="https://dotnet.microsoft.com/apps/aspnet/web-apps/client" target="_blank">Blazor</a>, or <a href="https://www.endpoint.com/blog/2018/11/20/whats-the-deal-with-asp-net-core-razor-pages" target="_blank">Razor Pages</a> (both development frameworks will be fully supported). And on desktop development, we can expect WCF (Windows Communication Foundation) and WWF (Windows Workflow Foundation) to be out of the equation too.

But having .NET 5 built upon .NET Core doesn’t mean that .NET Framework will cease to exist: John Montgomery, Microsoft’s corporate VP in Developer Tools, <a href="https://www.theregister.co.uk/2019/05/16/will_net_5_really_unify_microsoft_development_stack/" target="_blank">stated in an interview</a> that “The big thing (.NET 5) it’s doing is unifying Mono and Xamarin with .NET Core. It is not bringing all the technology from full .NET Framework, which remains the thing that’s going to be in Windows for a long time and will not move forward very much”.


### And beyond

After .NET 5 is released, Microsoft plans to ship a new major release of .NET once a year, as we can see from the schedule roadmap posted on their .NET blog.

![.NET schedule roadmap](/blog/2019/08/03/prepare-for-dotnet-core-3-dotnet-5/image-3.jpg)


### Conclusion

<b>Microsoft is clearly taking a new direction</b>. They are planning to use .NET 3 as an intermediate step to merge .NET Core architecture with Windows desktop development. And one year after, they are planning to have multiple devices, architectures, operative systems and application types covered with a single unified framework, .NET 5.

Is clear that many existing applications will not have an easy way to be migrated into .NET Core, so we can expect .NET Framework to remain supported for many years. But Microsoft is showing us the path that .NET will take as the main road in the future: To grow steadily based on the community .NET Core has built itself upon.
