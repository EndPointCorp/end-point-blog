---
author: Daniel Gomm
title: "Monitoring Settings Changes in ASP.NET Core"
date: 2021-09-22
github_issue_number: 1771
tags:
- monitoring
- dotnet
---

![Ripples in water](/blog/2021/09/monitoring-settings-changes-in-asp-net-core/ripples.jpg)  
[Photo](https://unsplash.com/photos/Q5QspluNZmM) by [Linus Nylund](https://unsplash.com/@dreamsoftheoceans) on Unsplash

Did you know you can directly respond to config file changes in ASP.NET Core? By using the `IOptionsMonitor<T>` interface, it’s possible to run a lambda function every time a config file is updated.

For those who aren’t too familiar with it, ASP.NET Core configuration is handled using the [Options Pattern](https://docs.microsoft.com/en-us/aspnet/core/fundamentals/configuration/options?view=aspnetcore-5.0). That is, you create a model class that has a field for each property in your config file, and then set up the application to map the configuration to that class, which can be injected into controllers and services. In your controllers, you can request the configuration class `T` as a dependency by using an options wrapper class like `IOptions<T>`.

While this works just fine in some cases, it doesn’t allow you to actually run code when the configuration is changed. However, if you request your configuration using `IOptionsMonitor<T>`, you get the ability to define a lambda function to run every time `appsettings.json` is changed.

One use case for this functionality would be if you wanted to maintain a list in the config file, and log every time that list was changed. In this article I’ll explain how to set up an ASP.NET Core 5.0 API to run custom code whenever changes are made to `appsettings.json`.

### Setting up the API

In order to use the options pattern in your API, you’ll first need to add the options services to the container using the `services.AddOptions()` method. Then, you can register your custom configuration class (in this example, `MyOptions`) to be bound to a specific section in `appsettings.json` (in this example, `"myOptions"`).

```csharp
public void ConfigureServices(IServiceCollection services)
{
  // ...

  // Add options services to the container
  services.AddOptions();

  // Configure the app to map the "myOptions" section of
  // the config file to the MyOptions model class
  services.Configure<MyOptions>(
    Configuration.GetSection("myOptions")
  );
}
```

### Monitoring Configuration Changes

Now that the API is set up correctly, in your controllers you can directly request the configuration using `IOptionsMonitor<T>`. You can also unpack the configuration instance itself by using the `IOptionsMonitor<T>.CurrentValue` property. This value will automatically get updated by `IOptionsMonitor<T>` when the configuration is changed, so you only need to retrieve it once in the constructor.

```csharp
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;

[Route("api/[controller]")]
[ApiController]
public class MyController : ControllerBase
{
  private MyOptions MyOptions;

  public MyController(IOptionsMonitor<MyOptions> MyOptionsMonitor)
  {
    // Stores the actual configuration in the controller
    // to reference later. Changes to the config will be
    // reflected in MyOptions.
    this.MyOptions = MyOptionsMonitor.CurrentValue;

    // Registers a lambda function to be called every time
    // a configuration change is made
    MyOptionsMonitor.OnChange(async (opts) =>
    {
      // Write some code!
    });
  }
}
```

One small gotcha worth noting is that the OnChange function isn’t debounced. So if you’re using an IDE that automatically saves as you type, it’ll trigger the `OnChange` function rapidly as you edit `appsettings.json`.

### Conclusion

And that’s it! It doesn’t take much to get your API to run custom code on config file changes.

Have any questions? Feel free to leave a comment!
