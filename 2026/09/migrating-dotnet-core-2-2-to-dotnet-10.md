---
author: "Juan Pablo Ventoso"
title: "Migrating a web app from .NET Core 2.2 to .NET 10"
description: "How we upgraded a Razor Pages and Web API application from .NET Core 2.2 to .NET 10 with Claude Code."
featured:
  endpoint: true
  image_url: /blog/2026/09/migrating-dotnet-core-2-2-to-dotnet-10/cover.webp
date: 2026-09-08
github_issue_number: 2198
tags:
- dotnet
- artificial-intelligence
---

![A narrow canyon of layered red sandstone walls, with a few small trees growing out of the rock](/blog/2026/09/migrating-dotnet-core-2-2-to-dotnet-10/cover.webp)

<!-- Photo by Matías Ventoso, 2026. -->

.NET Core 2.2 reached end of life years ago, so applications running on this version no longer receive security patches or bug fixes. Considering those risks, we recently migrated a client's production application from .NET Core 2.2 to [.NET 10](https://learn.microsoft.com/dotnet/core/whats-new/dotnet-10/overview). The application consists of a Razor Pages web app, a Web API that communicates with their public website, and a unit / integration test project. We also decided to use [Claude Code](https://claude.com/product/claude-code) to assist with the process, which turned out to be a great tool for organizing the work.

Going from .NET Core 2.2 to .NET 10 is a big jump, so before making any changes we put together an assessment of the application dependencies, potential breaking changes, and estimated the work involved in each area. The assessment was useful as a starting point, but some of the estimates changed (mostly for the better!) once we started working through the actual code with Claude. The range of hours from the estimate was ~32–59 hours, with a realistic mid-range of ~45 hours. How many hours did it take in the end? Keep reading :).

### A phased plan

First, we turned the assessment into a plan document, dividing the migration into twelve phases, each with its own scope and risks. As we worked through each phase, we updated the document with what we actually found, compared with the original assessment and estimate. To keep good control over each change, I created one commit per phase and pushed the changes to the migration branch, reviewing the changes as I went.

Phases 1 through 8 were mostly focused on getting the application to build again, so the tests wouldn't work yet. From phase 9 onward, I required both the build and all tests to be passing before committing any changes. I also kept a separate section in the plan for unrelated issues that came up during the migration, making it easier to keep the migration focused and review exactly what changed. This was the phased list we followed:

| # | Phase | Description |
|---|---|---|
| 0 | Baseline | See what builds, what passes, what was already broken |
| 1 | Retarget + packages | Move projects to net10.0, drop the retired Microsoft.AspNetCore.All package and replace others | 
| 2 | Hosting model | Replace WebHost.CreateDefaultBuilder, update routing, authorization and endpoint mapping | 
| 3 | General replacements | IWebHostEnvironment sweep across 35 files | 
| 4 | EF Core updates | Replace calls to FromSql and ExecuteSqlCommandAsync, remove UseRowNumberForPaging | 
| 5 | PDF driver wrapper | Drop Rotativa for a direct wkhtmltopdf process wrapper |
| 6 | CsvHelper	upgrade | Upgrade from version 12 to 33 |
| 7 | Retire bundling | Remove the deprecated bundler, commit the minified assets |
| 8 | First compile pass | Fix everything remaining until all three projects build |
| 9 | Background service | Migrate static thread + BuildServiceProvider() to a proper IHostedService |
| 10 | Test project | xunit / Moq upgrades, rewrite the async query test helpers, swap MiniCover for coverlet |
| 11 | Runtime testing | Manual smoke test, then an automated page harness against a real database |
| 12 | Deployment | Deploy the apps for client testing |

Phase 0 was capturing a baseline, so we ran all the tests and recorded exactly what passed and what did not before making any changes. That baseline ended up being useful throughout the project: When a test failed later, I could compare it with the original results instead of having to determine whether the migration had introduced a problem.

**If you are doing a migration like this, I would recommend capturing a baseline before changing anything.** On an application that has been running for years, you will probably have to answer "was this already broken?" more than once.

The phased structure also let me change the order of some of the work as I went. For example, the PDF library replacement was originally scheduled as phase 5, but it turned out to be blocking some of the other work, so we moved it forward and recorded that change in the plan along with the reason for it.

### What took less time than expected

The assessment identified two areas as the largest risks in the migration: Rotativa (for PDF generation) and CsvHelper (CSV parsing). Luckily, they turned out to be much simpler than expected: The initial assessment suggested that Rotativa was deeply integrated into a base page class inherited by around thirty report pages, so I expected replacing it to require several hours of work.

When I looked at the actual call sites, however, Rotativa was only being used in two places, both doing essentially the same thing: invoking the external executable `wkhtmltopdf.exe`. This binary was already included in the repository, so instead of replacing the PDF generation engine, it was as simple as replacing the small amount of Rotativa code with about forty lines of `System.Diagnostics.Process` code that invoked the same binary with the same switches. This meant that the existing PDF rendering behavior could remain unchanged across the report pages.

On the CsvHelper integration, we needed to upgrade it from version 12 to version 33. Twenty-one major versions of breaking changes sounds like a significant migration, but the code was only relying on a small part of the API. The actual changes were two lines: `Configuration` became `CsvConfiguration`, and `csv.Configuration.RegisterClassMap(...)` became `csv.Context.RegisterClassMap(...)`. The class map API used by the application did not need any changes.

**Takeaway: A package inventory tells you what changed in a dependency, but not necessarily how much of that change affects your application.**

### Fixing compile errors

Once the three projects were retargeted to `net10.0`, the build firstly reported 4 errors related to unresolved `using` directives. But after fixing those, the number went up to 24 errors! Mostly related to several fairly mechanical unexistent declarations that we needed to replace: `IHostingEnvironment` needed to become `IWebHostEnvironment` across thirty-five files, `FromSql` became `FromSqlRaw`, `ExecuteSqlCommandAsync` became `ExecuteSqlRawAsync`, and the application's `Program.cs` needed to be updated for the newer hosting model.

There was also one error that required a bit more investigation. Two page models failed with:

```text
'Inventory' is a namespace but is used like a type
```

Nothing in those files had changed, so what caused this? The issue was related to how Razor compilation changed between .NET Core 2.2 and later versions. In .NET Core 2.2, Razor views were precompiled into a separate assembly, but since .NET Core 3.0, Razor uses source generation as part of the main compilation. This means that folder-related namespaces such as Pages.Inventory can now exist alongside the page models and take precedence over Models.Inventory during name resolution.

Claude Code was particularly useful here: it spotted the problem right away. Once it was clear what was happening, the fix was straightforward. It was just not something I would have found simply by looking at a list of package versions.

**Takeaway: Don't judge the size of a migration by the initial compiler error count, fixing the first layer of errors can reveal many more once the compiler gets deeper into the code.**

### What took more time: EF Core problems

Getting the application to build and having the test suite pass was not enough to finish the migration: I found several problems that only appeared when the application was running against a real database and handling actual requests. The first was the database connection:

`System.Data.SqlClient` had a default of `Encrypt=false`, while `Microsoft.Data.SqlClient` 4.0 and later default to `Encrypt=true`. The upgraded application therefore started negotiating TLS and validating the SQL Server certificate. The database server was using a self-signed certificate, so the connection failed.

The next problem involved SQL Server triggers: EF Core 7 started using an `OUTPUT` clause to read back store-generated values. SQL Server does not allow a bare `OUTPUT` clause on a table that has a trigger, and there are a few tables on this app using them. EF Core 2.2 did not use `OUTPUT` in the same way, so the existing triggers had not caused a problem before the upgrade.

The solution (again, Claude Code spotted this immediately) was to restore the previous behavior globally in `OnModelCreating`:

```csharp
foreach (var entityType in modelBuilder.Model.GetEntityTypes())
{
    entityType.UseSqlOutputClause(false);
}
```

Microsoft's documented approach is to configure this for the specific tables that have triggers, but in this case we chose to disable the `OUTPUT` clause globally to avoid problems in the future if new triggers are added to another table.

Another issue involved eighteen queries that could no longer be translated by EF Core. This was the area the original assessment had correctly identified as the biggest unknown: EF Core 2.2 would evaluate unsupported portions of some queries on the client, while EF Core 3 and later became much stricter about client evaluation.

The affected queries followed a common "latest row per group" pattern:

```csharp
.GroupBy(x => x.ItemNo, (key, g) => g.OrderByDescending(x => x.Date).First())
```

What made this particular problem harder to identify was the exception. Instead of the more familiar "could not be translated" message, the application failed with:

```text
KeyNotFoundException: The given key 'EmptyProjectionMember' was not present in the dictionary
```

That initially looked more like an internal Entity Framework problem than a query translation issue. Again, thanks to Claude's suggestion, the fix was to materialize the query with `ToListAsync()` at the point where the server side query was done, and then perform the final grouping in memory. This reproduced what EF Core 2.2 had been doing implicitly.

The last issue was related to pagination: Removing `UseRowNumberForPaging` changes SQL Server pagination from `ROW_NUMBER()` to `OFFSET/FETCH`. The application's pager logic reports `CurrentPage = 0` when there are no results, producing an offset of `-10`. `ROW_NUMBER()` was working on this situation, but `OFFSET/FETCH` returns:

```text
The offset specified in a OFFSET clause may not be negative.
```

Causing errors on lists that were empty or with a filter that returned no results. The application had tests and manual checks for populated result sets, but not for an empty one, so this was only discovered when I ran and tested the application.

**Takeaway: A successful build and a passing test suite are not enough for a .NET upgrade. Problems caused by database behavior, query translation, or real world data may only appear when you actually run the app.**

### Automating the verification

Manually clicking through ninety pages looking for translation or runtime problems would have been slow and difficult to repeat after each phase was completed. Instead, we added a small integration test project using `WebApplicationFactory<Program>`. The test application boots the real application in-process, discovers the page routes from the application's own `EndpointDataSource`, and requests each page against a real database.

I made three changes to make this practical:

* I removed the background service from the test host so it would not start scheduled work during every test run
* I added an authentication scheme that always succeeds, so the pages would not redirect to the login screen
* I made the factory refuse to start if the connection string points to the production database (important safeguard!)

The first run found the failing pages immediately. More importantly, this turned "test all ninety pages" into `dotnet test`, so the same checks can now run again whenever the application changes.

**Takeaway: If manually testing an application requires opening dozens of pages, it's probably worth automating that. Turning the smoke test into dotnet test makes the verification easily repeatable.**

### Conclusion

All in all, the process was much faster than expected, mainly because I was able to automate several parts of the verification process and use Claude Code to speed up a lot of the repetitive work. While the code review process took more time because I wanted to do a detailed review and understanding of every small change Claude suggested or made, the amount of repetitive work were reduced significantly.

This migration also reinforced the value of having a baseline and a repeatable way to exercise the application: A successful build and a passing unit test suite are useful milestones.

I still need to finalize some internal testing and deploy the new version to production, but the hours for this migration went from the estimation mid-range of ~45 hours, **to only 15 hours**! That's a significant difference from the original estimate, and a useful data point for future migrations. I also came away with a better understanding of what to expect from this kind of upgrades.