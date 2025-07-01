---
author: "Bimal Gharti Magar"
title: "Creating Invoice Generator API using C# and Minimal APIs"
featured:
  image_url: /blog/2025/01/learning-vue-3-composables-by-creating-an-invoice-generator/scaffolding.webp
description: How to create Vue 3 composables to properly separate business logic in an invoice generator application.
date: 2025-06-17
tags:
- vue
- javascript
- frameworks
- programming
---
![Regularly spaced curved steel beams hold up a metal roof with windows. The back of the room is visible, and a wall lined with windows that have faint light peeking through.](/blog/2025/01/learning-vue-3-composables-by-creating-an-invoice-generator/scaffolding.webp)

<!-- Photo by Seth Jensen, 2024. -->

### Introduction

In this blog post, we will explore how to create a robust Invoice Generator API using .NET 9 and [Minimal APIs](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/overview?view=aspnetcore-9.0), with a focus on integrating it with an existing Vue frontend implementation that we covered in [previous blog post](/blog/2025/01/learning-vue-3-composables-by-creating-an-invoice-generator/).

We will use Minimal APIs framework to create a RESTful API that can be easily used by our Vue application. Minimal APIs requires less boilerplate code and configuration compared to traditional controller based approach. It is suited for smaller APIs, microservices or serverless functions. We can learn more about choosing between controller based APIs and minimal APIs [here](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/apis?view=aspnetcore-9.0).

### Prerequisites

Before going further into the code, we should make sure we have the following tools and technologies installed:

* .NET 9 (the latest version of the .NET runtime)

Additionally, we already have an existing Vue frontend implementation that lacks API connectivity from our previous post. We will guide you through the process of integrating the Invoice Generator API with vue application.

### Setting up the Project

We will use the `dotnet` command to create a new .NET 9 project and set up the Minimal APIs framework using below steps:
- Create a new .NET Core Web API project using the following command:
```
dotnet new webapi -n invoice-generator-api
```
-
- Navigate to the newly created project directory:
```
cd invoice-generator-api
```
-
- Open `Program.cs` file which should look like below.
```csharp
var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();

var summaries = new[]
{
    "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
};

app.MapGet("/weatherforecast", () =>
{
    var forecast =  Enumerable.Range(1, 5).Select(index =>
        new WeatherForecast
        (
            DateOnly.FromDateTime(DateTime.Now.AddDays(index)),
            Random.Shared.Next(-20, 55),
            summaries[Random.Shared.Next(summaries.Length)]
        ))
        .ToArray();
    return forecast;
})
.WithName("GetWeatherForecast");

app.Run();

record WeatherForecast(DateOnly Date, int TemperatureC, string? Summary)
{
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
}

```
-
- We will also add the following packages for swagger UI, Entity Framework and EF Core provider for PostgreSQL.
```bash 
dotnet add package Microsoft.Extensions.ApiDescription.Server
dotnet add package Swashbuckle.AspNetCore.SwaggerUi
dotnet add package Microsoft.EntityFrameworkCore
dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL
dotnet add package Microsoft.EntityFrameworkCore.Design
```

### Setting up the Swagger UI
Update `Program.cs` to include Swagger UI configuration to point to open API json file.
```diff Program.cs
 if (app.Environment.IsDevelopment())
 {
     app.MapOpenApi();
+    app.UseSwaggerUI(config =>
+    {
+        config.SwaggerEndpoint("/openapi/v1.json", "v1");
+    });
 }

 app.UseHttpsRedirection();
```
Once the application is running using `dotnet run`, you can access Swagger UI at http://localhost:<PORT>/swagger on your browser, which should look like below.
![Swagger base page.](/blog/2025/06/creating-invoice-generator-api-using-c-sharp-and-minimal-apis/swagger.png)

 
### Setting up the Database Context with Entity Framework
- Create a file `InvoiceDbContext.cs` on the root of the project and add the following code.
```csharp
using Microsoft.EntityFrameworkCore;

public class InvoiceDbContext : DbContext
{
    public InvoiceDbContext(DbContextOptions<InvoiceDbContext> options)
     : base(options)
    {

    }
}
```
-
- Update `Program.cs` file to include the configuration for connecting to postgresql database using Entity Framework.
```diff
+using Microsoft.EntityFrameworkCore;
+
 var builder = WebApplication.CreateBuilder(args);

+builder.Services.AddDbContext<InvoiceDbContext>(options =>
+    options.UseNpgsql(builder.Configuration.GetConnectionString("InvoiceDbcontext")));
+
+
```
-
- Add the connection string `InvoiceDbcontext` in the appsettings.json file as shown below:
```diff

       "Microsoft.AspNetCore": "Warning"
     }
   },
-  "AllowedHosts": "*"
+  "AllowedHosts": "*",
+  "ConnectionStrings": {
+    "InvoiceDbcontext": "Host=<HOSTNAME>;Port=<PORT>;Database=<DATABASE>;Username=<USERNAME>;Password=<PASSWORD>;"
+  }
 }
```


### Designing the Invoice Generator API

The next step is to design the API endpoints required for invoice generation. We will need the following endpoints:

1. `GET /api/invoice`: Get list of invoices
2. `POST /api/invoice`: Create a new invoice
3. `GET /api/invoice/{id}`: Get an invoice using id
4. `PUT /api/invoice/{id}`: Update an invoice using id
6. `DELETE /api/invoice/{id}`: Soft delete an invoice using id
7. `PUT /api/invoice/{id}/upload-logo`: upload logo to saved invoice using id
8. `DELETE /api/invoice/{invoiceId}/detail/{id}`: Soft delete invoice line item using line item id and invoice id

We will also need data models and entities to represent invoices and invoice line items. Let's create the following classes in model folder:
```csharp
public class Base
{
    public int Id { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? ModifiedAt { get; set; }
    public bool IsDeleted { get; set; } = false;
    public DateTime? DeletedAt { get; set; }
}

```
```csharp
public class Invoice : Base
{
    public string? Name { get; set; }
    public string? logo { get; set; }
    public string? Number { get; set; }
    public string? PONumber { get; set; }
    public virtual List<InvoiceItem> InvoiceItems { get; set; } = new();
    public UsageAmount? DiscountAmount { get; set; }
    public UsageAmount? TaxAmount { get; set; }
    public UsageAmount? ShippingAmount { get; set; }
    public decimal TotalAmount { get; set; }
    public decimal PaidAmount { get; set; }
    public string? Sender { get; set; }
    public string? Buyer { get; set; }
    public Status? Status { get; set; }
    public string? Notes { get; set; }
    public string? Terms { get; set; }
    public DateTime? Date { get; set; }
    public DateTime? DueDate { get; set; }
    public bool SentToBuyer { get; set; } = false;
}
```
```csharp
public class InvoiceItem : Base
{
    public string Description { get; set; } = string.Empty;
    public int Quantity { get; set; }
    public decimal Rate { get; set; }
    public decimal Amount { get => this.Quantity * this.Rate; }
}
```
```csharp
public class UsageAmount : Base
{
    public bool IsUsed { get; set; } = false;
    public bool IsPercentage { get; set; } = false;
    public decimal Value { get; set; } = 0;
}
```

Will will now use these classes to create tables in the database and then define a `DBSet` for each class in our `InvoiceDbContext.cs`.

```diff
public InvoiceDbContext(DbContextOptions<InvoiceDbContext> options)
 : base(options)
{

}
+    public DbSet<Invoice> Invoices => Set<Invoice>();
+    public DbSet<InvoiceItem> InvoiceItems => Set<InvoiceItem>();
+    public DbSet<UsageAmount> UsageAmounts => Set<UsageAmount>();
 }
```

Since we will be using soft delete feature in our API, we will use [Global Query Filters](https://learn.microsoft.com/en-us/ef/core/querying/filtering) to filter out the deleted records from our table. So, we configure the query filters in `OnModelCreating` using the `HasQueryFilter` API in `InvoiceDbContext.cs`. After which, the file should look like below.

```diff
public InvoiceDbContext(DbContextOptions<InvoiceDbContext> options)
 : base(options)
{

}
+    protected override void OnModelCreating(ModelBuilder modelBuilder)
+    {
+        modelBuilder.Entity<Invoice>().HasQueryFilter(p => !p.IsDeleted);
+        modelBuilder.Entity<InvoiceItem>().HasQueryFilter(p => !p.IsDeleted);
+        modelBuilder.Entity<UsageAmount>().HasQueryFilter(p => !p.IsDeleted);
+    }
+
+    public DbSet<Invoice> Invoices => Set<Invoice>();
+    public DbSet<InvoiceItem> InvoiceItems => Set<InvoiceItem>();
+    public DbSet<UsageAmount> UsageAmounts => Set<UsageAmount>();
 }
```

### Creating and running database migrations
We have defined models for our data models, but we need to create a database and tables for them. We can do this using Entity Framework tool `dotnet ef`. On the command prompt, in the root path of project, run the following command:
```bash
dotnet ef migrations add "create table and columns"
```
This command will create migration files in the `Migrations` folder. We can run this migration using the following command:
```bash
dotnet ef database update
```

### Implementing API Endpoints

Now that we have designed the API endpoints and data models, let's implement them using Minimal APIs. We will create a new `endpoints` folder and add an `InvoiceEndpoints.cs` file in it. This file will contain the implementation for the Invoice API endpoints. 
```csharp
// InvoiceEndopints.cs

using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Hosting.Internal;

public static class InvoiceEndpoints
{
    public static List<Invoice> Invoices = new();
    public static RouteGroupBuilder MapInvoiceEndpoints(this RouteGroupBuilder group)
    {
      // Return list of invoices
        group.MapGet("/", async (InvoiceDbContext db) =>
        {
            return await db.Invoices.Include(x => x.InvoiceItems).ToListAsync();
        })
            .WithSummary("Get list of invoices");
        
        // Return an existing invoice
        group.MapGet("/{id}", async (int id, InvoiceDbContext db) =>
        {
            return await db.Invoices.Include(x => x.InvoiceItems).FirstOrDefaultAsync(x => x.Id == id)
            is Invoice invoice
                ? Results.Ok(invoice)
                : Results.NotFound();
        })
            .WithSummary("Get an invoice using id");

        // Create an invoice
        group.MapPost("/", async (Invoice invoice, InvoiceDbContext db) =>
        {
            invoice.DueDate = invoice.DueDate.HasValue ? invoice.DueDate.Value.ToUniversalTime() : null;
            invoice.Date = invoice.Date.HasValue ? invoice.Date.Value.ToUniversalTime() : null;
            db.Invoices.Add(invoice);
            await db.SaveChangesAsync();
            return Results.Created($"/api/invoice/{invoice.Id}", invoice);
        })
            .WithSummary("Create a new invoice");

        // Create a new line item for an existing invoice
        group.MapPost("/{id}/items", async (int id, List<InvoiceItem> invoiceItems, InvoiceDbContext db) =>
        {
            if (await db.Invoices.FindAsync(id)
            is not Invoice invoice)
            {
                return Results.NotFound();
            }
            invoice.InvoiceItems.AddRange(invoiceItems);
            await db.SaveChangesAsync();
            return Results.Created($"/api/invoice/{invoice.Id}", invoice);
        })
            .WithSummary("Create new line items for invoice");

        // Update an existing invoice
        group.MapPut("/{id}", async (int id, Invoice inputInvoice, InvoiceDbContext db) =>
        {
            var invoice = await db.Invoices.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);

            if (invoice is null) return Results.NotFound();

            invoice.Id = id;
            db.Invoices.Update(inputInvoice);
            await db.SaveChangesAsync();
            return Results.NoContent();
        })
            .WithSummary("Update invoice");

        // Upload invoice logo image file for an existing invoice
        group.MapPut("/{id}/upload-logo", async (int id, IFormFile uploadImageFile, InvoiceDbContext db) =>
        {
            var invoice = await db.Invoices.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);

            if (invoice is null) return Results.NotFound();

            if (uploadImageFile == null)
            {
                throw new ArgumentNullException(nameof(uploadImageFile));
            }

            var contentPath = Environment.CurrentDirectory;
            var uploadPath = Path.Combine("Uploads", id.ToString());
            var rootPath = Path.Combine(contentPath, uploadPath);

            if (!Directory.Exists(rootPath))
            {
                Directory.CreateDirectory(rootPath);
            }
            string[] allowedFileExtensions = [".jpg", ".jpeg", ".png"];
            var ext = Path.GetExtension(uploadImageFile.FileName);
            if (!allowedFileExtensions.Contains(ext))
            {
                throw new ArgumentException($"Please upload only .jpg, .jpeg, and .png images.");
            }

            // generate a unique filename
            var fileName = $"{Guid.NewGuid().ToString()}{ext}";
            var fileNameWithPath = Path.Combine(uploadPath, fileName);
            var rootPathWithFileName = Path.Combine(rootPath, fileName);
            using var stream = new FileStream(rootPathWithFileName, FileMode.Create);
            await uploadImageFile.CopyToAsync(stream);

            invoice.logo = fileNameWithPath;
            db.Update(invoice);
            await db.SaveChangesAsync();
            return Results.NoContent();
          })
          .DisableAntiforgery()
          .WithSummary("upload logo");
        
        // soft delete an invoice
        group.MapDelete("/{id}", async (int id, InvoiceDbContext db) =>
        {
            if (await db.Invoices.FindAsync(id) is Invoice todo)
            {
                todo.IsDeleted = true;
                todo.DeletedAt = DateTime.Now.ToUniversalTime();
                await db.SaveChangesAsync();
                return Results.NoContent();
            }
            return Results.NotFound();
        })
            .WithSummary("Soft delete an invoice");

        return group;
    }
}
```

Then we will also implement `InvoiceDetailEndpoint.cs`. We will only define a delete endpoint for soft deleting the line items. We created this also to demonstrate how to use multiple files in the `Program.cs` to map the endpoints to a certain url.
```csharp
// InvoiceDetailEndpoint.cs

public static class InvoiceDetailEndpoints
{
    public static RouteGroupBuilder MapInvoiceDetailEndpoints(this RouteGroupBuilder group)
    {
        group.MapDelete("/{id}", async (int id, InvoiceDbContext db) =>
        {
            if (await db.InvoiceItems.FindAsync(id) is InvoiceItem invoiceItem)
            {
                invoiceItem.IsDeleted = true;
                invoiceItem.DeletedAt = DateTime.Now.ToUniversalTime();
                await db.SaveChangesAsync();
                return Results.NoContent();
            }
            return Results.NotFound();
        }).WithSummary("Soft delete invoice line item");

        return group;
    }
}
```

Similar to how traditional controller APIs are separated in their own files, we now have the implementation for the endpoints in two files. We will now register and map the endpoints to a preferred URL using `MapGroup` in `Program.cs` file.
```diff
// Program.cs

+var root = app.MapGroup("api");
+var invoice = root.MapGroup("invoice").MapInvoiceEndpoints();
+var invoiceDetail = root.MapGroup("invoice/{invoiceId}/detail").MapInvoiceDetailEndpoints();
+
 app.Run();
```
We also need to add a config to expose the `Uploads` folder so the images can be loaded from the running API server. Also, make sure to create the `Uploads` folder before running the application, otherwise the application wouldn't run.
```diff
// Program.cs

 var invoice = root.MapGroup("invoice").MapInvoiceEndpoints();
 var invoiceDetail = root.MapGroup("invoice/{invoiceId}/detail").MapInvoiceDetailEndpoints();

+app.UseStaticFiles(new StaticFileOptions
+{
+    FileProvider = new PhysicalFileProvider(
+        Path.Combine(builder.Environment.ContentRootPath, "Uploads")),
+    RequestPath = "/Uploads"
+});
+
 app.Run();
 ```

 
### Adding CORS for development
While working locally we usually run the frontend application and the api application in different ports, so CORS is required for the frontend application to access the api. To enable CORS in development mode, we can add the following code snippet to our `Program.cs` file:

```diff

# Program.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.FileProviders;

 var builder = WebApplication.CreateBuilder(args);
-
+var MyAllowSpecificOrigins = "_myAllowSpecificOrigins";
+builder.Services.AddCors(options =>
+{
+    options.AddPolicy(name: MyAllowSpecificOrigins,
+                      policy =>
+                      {
+                          policy.AllowAnyOrigin();
+                          policy.AllowAnyHeader();
+                          policy.AllowAnyMethod();
+                      });
+});
 builder.Services.AddDbContext<InvoiceDbContext>(options =>
     options.UseNpgsql(builder.Configuration.GetConnectionString("InvoiceDbcontext")));

 app.MapGet("/weatherforecast", () =>
 var root = app.MapGroup("api");
 var invoice = root.MapGroup("invoice").MapInvoiceEndpoints();
 var invoiceDetail = root.MapGroup("invoice/{invoiceId}/detail").MapInvoiceDetailEndpoints();
-
+app.UseCors(MyAllowSpecificOrigins);
 app.UseStaticFiles(new StaticFileOptions
 {
     FileProvider = new PhysicalFileProvider(
```

 Now, we can start the application and test our API. When we go to `/swagger`, we can see our API endpoints.

 ![Swagger base page.](/blog/2025/06/creating-invoice-generator-api-using-c-sharp-and-minimal-apis/swagger-apis.png)

The source code is available [here](https://github.com/bimalghartimagar/invoice-generator-api).

**Integrating with Vue 3 Application**

We already created a Vue 3 application in the [previous blog](/blog/2025/01/learning-vue-3-composables-by-creating-an-invoice-generator/). Now, we will integrate our API with the Vue application.

To integrate the Invoice Generator API with our Vue 3 application, we will need to configure API calls from the frontend to interact with the API. We will follow the following steps:

1. Install the `axios` package in our Vue 3 project:
```bash
npm install axios
```
2. Create a new file called `index.ts` in the `services` folder of our Vue 3 project and add the following code. Also, add `.env` file with key `VITE_API_URL` and value of the API URL:
```typescript
// services/index.ts

import axios from 'axios'
export default axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    timeout: 5000,
});

```
```dot
# .env
VITE_API_URL=https://localhost:7041/api/
VITE_BACKEND_URL=https://localhost:7041/
```
3. Create a new file called `invoiceService.ts` in the `services` folder of your Vue 3 project. Add the methods that calls the API endpoints:
```javascript
import { Invoice, InvoiceItem } from "../types/index.type"
import axios from "./"

export default {
    getInvoices: async () => {
        return await axios.get('invoice')
    },
    getInvoice: async (id) => {
        return await axios.get(`invoice/${id}`)
    },
    saveInvoice: async (data: Invoice) => {
        return await axios.post('invoice', data)
    },
    deleteInvoice: async (id: number) => {
        return await axios.delete(`invoice/${id}`)
    },
    updateInvoice: async (id: number, data: Invoice) => {
        return await axios.put(`invoice/${id}`, data)
    },
    uploadLogo: async (invoiceId, file) => {
        const formData = new FormData();
        formData.append("imageFile", file);
        return axios.put(`invoice/${invoiceId}/upload-logo`, formData, { headers: { "Content-Type": "multipart/form-data" } });
    },
    addLineItem: async (id: number, data: InvoiceItem) => {
        return await axios.post(`invoice/${id}/detail/`, data);
    },
    updateLineItem: async (id: number, lineId: number, data: InvoiceItem) => {
        return await axios.put(`invoice/${id}/detail/${lineId}`, data)
    },
    deleteLineItem: async (id: number, lineId: number) => {
        return await axios.delete(`invoice/${id}/detail/${lineId}`)
    },
}
```
3. We will use `invoiceService.ts` to make API calls in our application. Normally, the api calls are usually made from vue 3 components, but in this case we will use it to make API calls from our composable `useInvoiceStorage.ts` where all the business logic related to invoice are handled. Below are the code changes done to integrate the API calls from `invoiceService.ts`.
```diff
// composables/useInvoiceStorage.ts

import { useStorage } from '@vueuse/core'
-import { reactive } from 'vue';
+import { computed, ref } from 'vue';
 import { Invoice, InvoiceStore } from '../types/index.type';
+import invoiceService from '../services/invoiceService';

 const storage = useStorage<InvoiceStore>('invoice-store', {
-    currentInvoiceNumber: 10000,
-    invoices: {}
+    currentInvoiceNumber: "10000",
 }, localStorage);
-
+const state = ref({
+    ...storage.value,
+    invoices: {},
+});
 export default function useState() {
-    const state = reactive(storage);
 
     function saveInvoice(invoice: Invoice) {
         state.value.invoices[invoice.number] = { ...invoice };
-        state.value.currentInvoiceNumber = invoice.number + 1;
+        state.value.currentInvoiceNumber = `${+invoice.number + 1}`;
+        invoiceService.saveInvoice(invoice);
     }
 
-    function updateInvoice(invoice: Invoice) {
+    function updateInvoice(id: number, invoice: Invoice) {
         state.value.invoices[invoice.number] = { ...invoice };
+        invoiceService.updateInvoice(id, invoice);
     }
 
-    function deleteInvoice(invoiceId: number) {
+    async function deleteInvoice(invoiceId: number) {
         // delete state.value.invoices[invoiceId];
+        await invoiceService.deleteInvoice(invoiceId);
         state.value.invoices = Object.keys(state.value.invoices).filter(x => x != invoiceId.toString()).reduce((acc, curr) => {
             return {
                 ...acc,
@@ -40,15 +45,33 @@ export default function useState() {
         })
             .map(x => ({ ...state.value.invoices[x] }))
 
+
+    }
+
+    async function fetchInvoices() {
+        const result = await invoiceService.getInvoices();
+        state.value.invoices = result.data.reduce((acc, curr) => {
+            return { ...acc, [curr.id]: curr }
+        }, {})
+    }
+    async function fetchInvoice(id) {
+        const result = await invoiceService.getInvoice(id);
+        console.log(result);
+        state.value.invoices[result.data.id] = result.data;
+        console.log(state.value.invoices);
+        return result.data;
     }
     return {
         // variables
         storage: state,
+        invoices: computed(() => state.value.invoices),
 
         // methods
         saveInvoice,
         updateInvoice,
         deleteInvoice,
-        findInvoices
+        findInvoices,
+        fetchInvoices,
+        fetchInvoice
     }
 }
```

The above `fetchInvoices` method is then used by `Invoices.vue` to fetch the invoices. Similarly, all other endpoints are used in the application for CRUD operations.

The source code is available [here](https://github.com/bimalghartimagar/invoice-generator)

### Deployment

To deploy our API to Azure App Service, we can follow the documentation provided by Microsoft [here](https://learn.microsoft.com/en-us/aspnet/core/tutorials/publish-to-azure-api-management-using-vs?view=aspnetcore-9.0).

### Conclusion

In this blog post, we explored how to create a robust Invoice Generator API using .NET 9 and Minimal APIs. We designed the API endpoints, implemented them using Minimal APIs, and integrated the API with an existing Vue 3 application. This approach allowed us to leverage the power of Minimal APIs while maintaining a clean and modular codebase.