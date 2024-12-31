Reducing page load times: Cloudflare and caching with ASP.NET



When designing the architecture for a new website, it's important to keep caching in mind. Caching allows to store a copy of the pages or resources used by your web application in your local browser. Content distribution networks such as [Cloudflare](https://www.cloudflare.com/) also leverage on cache directives to distribute content to the users more efficiently.

This means that, when we define the page content that will be returned on the response, we should not include any content that depends on the identity context: We should return the same exact content to every user that hits the same URL. If we include any identity-specific content in the response, the CDN will reuse it for other requests, with the subsequent security risk.

A simple example is an e-commerce site where the customer logs in to make a purchase: If the homepage shows the user name and icon at the top bar, that content should be rendered from a non-cached request. Otherwise, CDN caching will show the same user and icon to other visitors. And worse: Depending on the validations appied to the website, the profile page could even display personal information to other users!

## Adding response caching

In .NET Core, we have a neat way of adding [response caching](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/response) to an ASP.NET Core application. Let's see how easy it is to enable caching on a Razor Pages app. First, in our Program.cs file, we need to add the lines:

```diff
+ builder.Services.AddResponseCaching();

var app = builder.Build();

+ app.UseResponseCaching();
```

Second, on our action methods, we need to include the `[ResponseCache]` attribute to specify the caching options for that request. In the example below, we are adding a response cache directive of 30 seconds that will vary depending on the User-Agent header sent on the request:

```diff
+ [ResponseCache(VaryByHeader = "User-Agent", Duration = 30)]
public async Task<IActionResult> OnGet()
{
    return Page();
}
```



