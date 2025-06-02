---
author: "Juan Pablo Ventoso"
title: "Implementing Azure Blob Storage in .NET 9"
featured:
  image_url: /blog/2025/06/implementing-azure-blob-storage-net-9/water-and-wood-dock.png
description: "Tips for implementing Azure Blob Storage in a .NET 9 application."
github_issue_number: 2119
date: 2025-06-02
tags:
- dotnet
- cloud
- storage
---

![Shallow water and an old wood dock in southern Patagonia, Argentina](/blog/2025/06/implementing-azure-blob-storage-net-9/water-and-wood-dock.webp)

<!-- Photo by Juan Pablo Ventoso, 2022. -->

Businesses keep moving toward scalable and cloud-based architectures. With this in mind, a client that was dealing with random errors in a [.NET](https://dotnet.microsoft.com/) app when saving files locally on the web server decided to get rid of that process and replace it with an [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs) implementation.

Why use Azure Blob Storage? It's an efficient cloud object storage solution from Microsoft, designed to store unstructured data, optimized for storing and serving documents, media, logs, or binary data, especially in applications that expose this data through an API. The key features are high performance, redundancy, reliability, and scalability. There's an SDK that we can use for easy integration and development, be it in .NET or other languages.

Let's take a look at what that change involves. For this example, we will set up the integration in a .NET 9 application:

Install the [NuGet](https://www.nuget.org/) package required to connect to Azure Blob Storage. We can do it with the [dotnet CLI](https://learn.microsoft.com/en-us/dotnet/core/tools/), or through the NuGet package manager.

```plain
dotnet add package Azure.Storage.Blobs
```

Then, we need to configure our connection in our appsettings.json file. We will use the connection string that Azure provides us when we create the new storage account.

```json
{
  "AzureBlobStorage": {
    "ConnectionString": "{your-connection-string}",
    "ContainerName": "my-container"
  }
}
```

In Azure Blob Storage, containers are like folders that group blobs (or files) together within a storage account. In this setting, the `ContainerName` value tells our application which container inside that account will be used for storing and retrieving blobs.

Create a `BlobService` class to read and write to the container.

```csharp
using Azure.Storage.Blobs;
using Microsoft.Extensions.Configuration;

public class BlobService
{
    private readonly BlobContainerClient _containerClient;

    /// <summary>
    /// Initializes a new instance of the <see cref="BlobService"/> class.
    /// </summary>
    /// <param name="configuration">Application configuration containing Azure Blob Storage settings.</param>
    public BlobService(IConfiguration configuration)
    {
        var connectionString = configuration["AzureBlobStorage:ConnectionString"];
        var containerName = configuration["AzureBlobStorage:ContainerName"];

        _containerClient = new BlobContainerClient(connectionString, containerName);
    }

    /// <summary>
    /// Uploads a file stream to Azure Blob Storage with the specified file name.
    /// </summary>
    /// <param name="fileName">The name of the file to be stored in blob storage.</param>
    /// <param name="fileStream">The stream representing the file content.</param>
    /// <returns>A task that represents the asynchronous upload operation.</returns>
    public async Task UploadFileAsync(string fileName, Stream fileStream)
    {
        var blobClient = _containerClient.GetBlobClient(fileName);
        await blobClient.UploadAsync(fileStream, overwrite: true);
    }

    /// <summary>
    /// Downloads a file from Azure Blob Storage.
    /// </summary>
    /// <param name="fileName">The name of the file to download from blob storage.</param>
    /// <returns>A task that returns a stream containing the blob's content.</returns>
    public async Task<Stream> DownloadFileAsync(string fileName)
    {
        var blobClient = _containerClient.GetBlobClient(fileName);
        var response = await blobClient.DownloadAsync();
        return response.Value.Content;
    }
}
```

Quite simple, isn't it? Now, let's see a way to easily expose file upload/​download endpoints via ASP.NET Core [minimal APIs](https://learn.microsoft.com/en-us/aspnet/core/tutorials/min-web-api). Introduced in .NET 6 and evolving further in .NET 9, minimal APIs provide a lightweight way to build HTTP APIs with a few lines of code. Instead of requiring full controller classes and attributes, minimal APIs let you define routes directly in your main `Program.cs` file, using simple [lambda expressions](https://learn.microsoft.com/dotnet/csharp/language-reference/operators/lambda-expressions). This makes them ideal for microservices, lightweight APIs, and internal tools where fast development and low overhead are essential.

For this example, we will create two endpoints that will use our BlobService class to communicate with Azure Blob Storage to save and retrieve files. In our `Program.cs` file, let's add:

```csharp
/// <summary>
/// Endpoint to upload a file to Azure Blob Storage.
/// </summary>
/// <param name="file">The uploaded file sent from the client (via multipart/form-data).</param>
/// <param name="blobService">Injected service used to handle blob storage operations.</param>
/// <returns>An HTTP 200 OK response when the upload succeeds.</returns>
app.MapPost("/upload", async (IFormFile file, BlobService blobService) =>
{
    using var stream = file.OpenReadStream();
    await blobService.UploadFileAsync(file.FileName, stream);
    return Results.Ok("File uploaded successfully");
});

/// <summary>
/// Endpoint to download a file from Azure Blob Storage.
/// </summary>
/// <param name="fileName">The name of the file to download (provided in the URL path).</param>
/// <param name="blobService">Injected service used to access blob storage.</param>
/// <returns>The file stream as a binary response with a download filename.</returns>
app.MapGet("/download/{fileName}", async (string fileName, BlobService blobService) =>
{
    var stream = await blobService.DownloadFileAsync(fileName);
    return Results.File(stream, "application/octet-stream", fileName);
});
```

Of course, we would want to configure authentication, add validations, and other security measures on these endpoints to prevent spammers from filling out our storage capacity 🙂. But the basics are there.

Also, there are recommended practices for any Azure integrations to consider, as we increase the robustness of our application:

- Monitor and log all storage operations using [Azure Application Insights](https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview). Integrate Application Insights into our .NET app to get detailed logging of the different HTTP calls to the Azure services.

- Use [Managed Identities](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview): Instead of storing secrets in appsettings.json, we can assign a Managed Identity to our application service, and grant it the Storage Blob Data Contributor role at the storage account. That will allow the application to gain access to the container automatically, without storing credentials in our settings files.

- Containers should be private by default. Avoid using "Blob" or "Container" public access levels, unless necessary. When public access is enabled, any person with a link to the container will be able to open or download the blob.

We will cover more details about using Managed Identities and [Shared Access Signatures (SAS)](https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview) for other Azure services in an upcoming blog post. Stay tuned!
