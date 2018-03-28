---
author: Gaurav Soni
title: Multi-Tenant Architecture
tags: rails, architecture, development
gh_issue_number: 1388
---

<img src="/blog/2018/03/27/multi-tenant-architecture/17167859758_a2873522ab_o-crop.jpg" width="770" alt="Multi-tenant living, with grazing cows" /><br />
<small>[Photo by Rüdiger Stehn](https://www.flickr.com/photos/rstehn/17167859758/), cropped, [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/)</small>

### Definition

Multi-tenant architecture allows one instance of an application to serve multiple customers/​organizations. Each customer/​organization is called a tenant. Each has its own apparent separate application and is not aware of the other tenants. The tenant has the ability to customize their own UI, users and groups, etc. Every tenant typically has these features:

<b>View:</b> Tenants can define the overall styling to their application.

<b>Business rules:</b> Tenant can define their own business rules and logic for their application.

<b>Database schema:</b> Tenant can define their own database schema (real or apparent) for the application. They can add/​remove database tables, rename database fields, etc.

<b>Users and groups:</b> Tenant can define their own rules to achieve data access control.

### Types of multi-tenancy

There are 3 main types of multi-tenant architecture:

<b>(1) Multi-tenancy with a single multi-tenant database:</b> This is the simplest form of multi-tenancy. It uses single application instance and the single database instance to host the tenants and store/​retrieve the data. This architecture is highly scalable, and when more tenants are added the database is easily scaled up with more data storage. This architecture is low-cost due to shared resources. Operational complexity is high, especially during application design and setup.

<img src="/blog/2018/03/27/multi-tenant-architecture/single-multi-tenant-database.svg" alt="Multi-tenancy with a single multi-tenant database" /><br />

<b>(2) Multi-tenancy with one database per tenant:</b> This is another type of multi-tenancy. It uses a single application instance and an individual database for each tenant. The scalability of this architecture may be lower and the cost higher than multi-tenancy with a single multi-tenant database because each database adds overhead. We can increase the scalability of this architecture by adding more database nodes but it depends on the workload. Operational complexity is low due to usage of individual databases.

<img src="/blog/2018/03/27/multi-tenant-architecture/database-per-tenant.svg" alt="Multi-tenancy with database-per-tenant" /><br />

<b>(3) Standalone single-tenant app with single-tenant database:</b> In this architecture you install the whole application separately for each tenant. Each tenant has its own app instance as well as database instance. This architecture provides highest level of data isolation. The cost of this architecture is high due to the standalone applications and databases.

<img src="/blog/2018/03/27/multi-tenant-architecture/standalone.svg" alt="Standalone single-tenant app with single-tenant database" /><br />

### How to achieve multi-tenancy in Rails

The [Apartment Gem](https://github.com/influitive/apartment) provides tools to help you deal with multiple tenants in your Rails application.

#### Apartment Gem Installation

Add the following to your Gemfile:

```ruby
gem 'apartment'
```

and run

```bash
bundle install
```

Then generate your Apartment config file using

```bash
bundle exec rails generate apartment:install
```

You can create new tenants like this:

```ruby
Apartment::Tenant.create('tenant_name')
```

To switch tenants using Apartment, use the following command:

```ruby
Apartment::Tenant.switch('tenant_name') do
  # ...
end
```

When the switch is called, all requests coming to ActiveRecord will be routed to the tenant you specify.

#### Multi-tenancy using subdomain with Apartment Gem

```ruby
module MyApplication
  class Application < Rails::Application
    config.middleware.use Apartment::Elevators::Subdomain
  end
end
```

### Summary

Try the Apartment gem! And consider the trade-offs of your application and user needs.
