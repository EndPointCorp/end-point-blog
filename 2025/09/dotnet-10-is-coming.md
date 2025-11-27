---
author: Juan Pablo Ventoso
title: ".NET 10 is Coming: What's New, and Why It Matters"
github_issue_number: 2152
featured:
  image_url: /blog/2025/09/dotnet-10-is-coming/palms-and-sunset.webp
description: "Learn what .NET 10 will bring to the ecosystem in November 2025."
date: 2025-09-29
tags:
- dotnet
- csharp
---

![Two palm trees are silhouetted against a blue and orange sunset](/blog/2025/09/dotnet-10-is-coming/palms-and-sunset.webp)

<!-- Photo by Juan Pablo Ventoso, 2024 -->

Microsoft has everything almost ready for the upcoming release of [.NET 10](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-10/overview) in November this year, and it promises to be a major milestone for developers. Currently in beta, the previews released so far have shown improvements in performance, security, compatibility, and more. Let's take a look and what's coming, and why it matters.

### Performance and runtime improvements

One of the core aspects of .NET 10 will be the improved efficiency in different areas. To mention a few of them:

* Optimized compression streams such as `GZipStream` and async implementations for `ZipArchive` methods
* Devirtualization improvements for interface methods, especially when arrays are involved, resulting in faster code execution
* Faster stack allocation for objects through the expanded use of scape analysis

All of these features (and others) contribute to lower latency and more efficient resource usage. There is a [comprehensive blog post](https://devblogs.microsoft.com/dotnet/performance-improvements-in-net-10/) by Stephen Toub, .NET team developer, where he runs several benchmarks proving how these improvements result in faster responses and smaller allocations.

### Security and increased cryptographic support

.NET 10 also introduces enhancements to encryption and authentication, increasing application security with support for new encryption policies and ways of authentication.

* Enhanced certificate thumbprint support adds the ability to search certificates by thumbprint using more secure hash algorithms (not just SHA-1)
* [WebAuthn](https://webauthn.io/) support enables passwordless logins with secure authentication methods like biometrics or physical security keys
* More cryptographic APIs: Better support for post-quantum cryptography APIs

### API & web enhancements

For Web APIs, services, and Blazor apps, .NET 10 has several useful features aiming to increase productivity, security, and cloud capabilities.

* Minimal APIs now support built-in validation through Data Annotations
* [OpenAPI 3.1](https://spec.openapis.org/oas/v3.1.0.html) support: ASP.NET Core in .NET 10 will generate OpenAPI 3.1 documents with the latest JSON Schema specifications
* Several improvements to Blazor assets delivery and environment configuration. One key change is that Blazor scripts will be served as a static web asset

### AI, cloud, and DevOps

AI developers will also benefit from the new .NET, as well as applications residing in the cloud and serverless environments.

* The [ML.NET Framework](https://dotnet.microsoft.com/en-us/apps/ai/ml-dotnet) will keep evolving with expanded capabilities
* Cloud Native Development: .NET 10 is designed to be fundamental to cloud native deployments, thanks to smaller base images and the automatic trimming of unused bits
* The [HybridCache library](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/hybrid?view=aspnetcore-9.0) unifies in-memory and distributed caching, with tagging for smarter invalidation

### C# 14

With .NET 10, Microsoft is also rolling out [a new version of the C# language](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-14), including several improvements that will result in cleaner syntax and better performance. Let's mention some key features:

* User-defined compound assignment operators: We will be able to define our own operators for types like `+=`, `-=`, etc.
* Using `nameof(List<>)` without specifying type arguments if we only need the name, avoiding boilerplate in generic programming and logging
* Partial constructors and partial events, expanding features like partial methods and properties from the previous language versions

You can find more details about all these upcoming changes on the [official .NET website](https://dotnet.microsoft.com/). Based on what we've seen above, .NET 10 promises to be one of the most significant releases to the .NET ecosystem, consolidating many incremental improvements that will result in measurable gains in performance, security, and productivity.

I encourage you to explore the [.NET 10 Release Candidate 1](https://devblogs.microsoft.com/dotnet/dotnet-10-rc-1/) to try things yourself and get an early look into what's about to come out in the .NET world!
