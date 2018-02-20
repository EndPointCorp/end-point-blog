---
author: Gaurav Soni
title: Multi-tenancy architecture.
tags: ruby, rails
gh_issue_number: 1384
---

### Definition

Multi-tenancy is an architecture that allow one instance of the application to serve multiple customers/organizations. Each customer/organization is called a tenant. Tenant has its own dedicated instance.Tenants are not aware of the other tenants. Tenant has ability to customize their own UI, users and groups etc. Every tenant has below listed features.

<b>View:-</b> Tenants can defined the Overall styling to their application.

<b>Business Rule:-</b> Tenant can defined their own business rules, logic for their application.

<b>DataBase Schema:-</b> Tenant can defined their own database schema for the application. They can add/remove database tables. Rename the database fields etc.

<b>Users and Groups:-</b> Tenant can defined their own rules to achieve data access control.

### Types of Multi-tenancy

There are 3 main types of Multi-tenancy Architecture.

<b>1) Multi-tenancy with a single multi-tenant database:-</b> It is the simplest form of the Multi-tenancy. It uses single application instance and the single database instance to host the tenants. It means that all the tenant uses single database to store/retrieve the data. This architecture is highly scalable, when more tenants are added the database is easily scaled up with more data storage.This architecture has low in the cost due to shared database. operational complexity is high due sharing of database.

<img src="/blog/2018/02/20/multi-tenancy/single-multi-tenant-database.png" alt="Multi-tenancy with a single multi-tenant database" /><br />

<b>2) Multi-tenancy with database-per-tenant:-</b> It is the another type of Multi-tenancy. It uses single application instance and  individual database for each tenant. The scalability of this architecture is lower than the Multi-tenancy with a single multi-tenant database. We can increase the scalability of this architecture by adding more database nodes but it depends on the workload. This architecture has higher cost due to usage individual database.operational complexity is low due to usage of individual the database.

<img src="/blog/2018/02/20/multi-tenancy/database-per-tenant.png" alt="Multi-tenancy with database-per-tenant" /><br />

<b>3) Standalone single-tenant app with single-tenant database:-</b> It is the another type of Multi-tenancy. In this architecture install whole application for each tenant. Each tenant has its own app instance as well as database instance. This architecture provide highest level of data isolation.The cost of this architecture is very high due standalone application and database.

<img src="/blog/2018/02/20/multi-tenancy/standalone.png" alt="Standalone single-tenant app with single-tenant database" /><br />

### How to achieve Multi-tenancy in Rails

[Apartment Gem](https://github.com/influitive/apartment) provides tools to help you deal with multiple tenants in your Rails application.

### Installation

Add the following to your Gemfile:

```ruby
  gem 'apartment'
```

and run

```nohighlight
  bundle install
```

Then generate your Apartment config file using

```nohighlight
  bundle exec rails generate apartment:install
```

You can create new Tenants by using below commands

```ruby
  Apartment::Tenant.create('tenant_name')
```

To switch tenants using Apartment, use the following command:

```ruby
  Apartment::Tenant.switch('tenant_name') do
    # ...
  end
```

When switch is called, all requests coming to ActiveRecord will be routed to the tenant you specify

### Multi-tenancy using subdomain with Apartment Gem
```ruby
  module MyApplication
    class Application < Rails::Application
      config.middleware.use Apartment::Elevators::Subdomain
    end
  end
```

### Advantages

1)Lower cost due to shared in infrastructure.

2)High Scalability

3)Easy Customizations

4)Ongoing maintenance and updates

### Disadvantage

1)Complex Structure

2)Lesser flexibility
