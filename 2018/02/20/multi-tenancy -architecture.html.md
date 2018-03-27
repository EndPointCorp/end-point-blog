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

<svg width="820px" height="520px" viewBox="0 0 820 520" preserveAspectRatio="xMidYMid meet"  >  <rect id="svgEditorBackground" x="0" y="0" width="820" height="520" style="fill: none; stroke: none;"/>
  <defs id="svgEditorDefs">
    <polygon id="svgEditorShapeDefs" style="fill:khaki;stroke:black;vector-effect:non-scaling-stroke;stroke-width:1px;"/>
  </defs>
  <rect x="175" y="24" style="fill:#57c1f2;stroke:black;stroke-width:1px;" id="e1_rectangle" width="267" height="78" transform="matrix(1 0 0 1 -2 13)" ry="0" rx="0"/>
  <text style="fill:black;font-family:Arial;font-size:20px;" x="238.277" y="83.1093" id="e3_texte" >App Instance</text>
  <path d="M-4,-2.5v5q0,1,4,1t4,-1v-5q0,1,-4,1t-4,-1q0,-1,4,-1t4,1t-4,1t-4,-1Z" style="fill:khaki; stroke:black; vector-effect:non-scaling-stroke;stroke-width:1px;" id="e14_shape" transform="matrix(0.125 0 0 0.125 210.5 313.438)"/>
  <path d="M-5.8715596330275295,-2.389908256880747v5.000000000000002q0,1.0000000000000044,3.9999999999999982,1.0000000000000044t4.0000000000000036,-1.0000000000000018v-4.999999999999998q0,0.9999999999999996,-4.0000000000000036,0.9999999999999996t-3.9999999999999982,-0.9999999999999996q0,-1.000000000000004,3.9999999999999982,-1.000000000000004t4.0000000000000036,1.000000000000004t-4.0000000000000036,0.9999999999999978t-3.9999999999999982,-0.9999999999999978Z" style="fill:#57c1f2; stroke:black; vector-effect:non-scaling-stroke;stroke-width:1px;" id="e15_shape" transform="matrix(27.25 0 0 27.25 360 383.375)"/>
  <text style="fill:black;font-family:Arial;font-size:20px;" x="250" y="394" id="e17_texte" >
    <tspan x="229" dy="1.25em" y="" dx="">Sharing DataBase</tspan>
    <tspan x="233" dy="1.25em" y="">Tennants A, B, C</tspan>
  </text>
  <path d="M8.542935428837389,-0.45576000689452606h2l-4,4l-3.999999999999999,-4.000000000000001h2.000000000000001v-3.9999999999999987h3.9999999999999982Z" style="fill:khaki; stroke:black; vector-effect:non-scaling-stroke;stroke-width:1px;" id="e20_shape" transform="matrix(5.18116 0 0 17.5531 271.1 220)"/>
</svg>
</br>
<b>2) Multi-tenancy with database-per-tenant:-</b> It is the another type of Multi-tenancy. It uses single application instance and  individual database for each tenant. The scalability of this architecture is lower than the Multi-tenancy with a single multi-tenant database. We can increase the scalability of this architecture by adding more database nodes but it depends on the workload. This architecture has higher cost due to usage individual database.operational complexity is low due to usage of individual the database.

<svg width="820px" height="520px" viewBox="-0.210084 0 820.42 520" preserveAspectRatio="xMidYMid meet"  >
  <rect id="svgEditorBackground" x="0" y="0" width="820" height="520" style="fill: none; stroke: none;"/>
  <defs id="svgEditorDefs">
    <polygon id="svgEditorShapeDefs" style="fill:khaki;stroke:black;vector-effect:non-scaling-stroke;stroke-width:1px;"/>
  </defs>
  <rect x="175" y="24" style="fill:#57c1f2;stroke:black;stroke-width:1px;" id="e1_rectangle" width="267" height="78" transform="matrix(1 0 0 1 -2 13)" ry="0" rx="0"/>
  <text style="fill:black;font-family:Arial;font-size:20px;" x="238.277" y="83.1093" id="e3_texte" >App Instance</text>
  <path d="M-4,-2.5v5q0,1,4,1t4,-1v-5q0,1,-4,1t-4,-1q0,-1,4,-1t4,1t-4,1t-4,-1Z" style="fill:khaki; stroke:black; vector-effect:non-scaling-stroke;stroke-width:1px;" id="e14_shape" transform="matrix(0.125 0 0 0.125 210.5 313.438)"/>
  <path d="M-6.595970253845273,-0.41427898485836245v5.000000000000003q0,1,3.999999999999999,1t4,-1v-5.000000000000001q0,1.0000000000000024,-4,1.0000000000000024t-3.999999999999999,-1.0000000000000024q0,-1,3.999999999999999,-1t4,0.9999999999999991t-4,1.0000000000000029t-3.999999999999999,-1.0000000000000029Z" style="fill:#57c1f2; stroke:black; vector-effect:non-scaling-stroke;stroke-width:1px;" id="e1_shape" transform="matrix(12.6246 0 0 14.0205 206.807 337.679)"/>
  <path d="M-5.436785649295584,-0.4548840572206862v5.0000000000000036q0,1.0000000000000053,4,1.0000000000000053t4.000000000000004,-1.0000000000000053v-5.000000000000004q0,1.0000000000000033,-4.000000000000004,1.0000000000000033t-4,-1.0000000000000033q0,-1.0000000000000022,4,-1.0000000000000022t4.000000000000004,1.0000000000000022t-4.000000000000004,1.0000000000000033t-4,-1.0000000000000033Z" style="fill:#57c1f2; stroke:black; vector-effect:non-scaling-stroke;stroke-width:1px;" id="e2_shape" transform="matrix(12.3259 0 0 14.3097 326.432 342.385)"/>
  <path d="M-4,-2.5v5q0,1,4,1t4,-1v-5q0,1,-4,1t-4,-1q0,-1,4,-1t4,1t-4,1t-4,-1Z" style="fill:#57c1f2; stroke:black; vector-effect:non-scaling-stroke;stroke-width:1px;" id="e4_shape" transform="matrix(12.8098 0 0 14.2111 452.059 369.995)"/>
  <text style="fill:black;font-family:Arial;font-size:20px;" x="149.454" y="367.059" id="e5_texte" >
    <tspan x="143.992" y="" dx="">Tenant</tspan>
    <tspan x="162.563" dy="1.25em" y=""> A</tspan>
  </text>
  <text style="fill:black;font-family:Arial;font-size:20px;" x="294.748" y="355.042" id="e6_texte" ></text>
  <text style="fill:black;font-family:Arial;font-size:20px;" x="273.992" y="379.076" id="e16_texte" >
    <tspan x="272.9" y="" dx="">Tenant</tspan>
    <tspan x="288.194" dy="1.25em" y=""> B</tspan>
  </text>
  <text style="fill:black;font-family:Arial;font-size:20px;" x="428.025" y="364.874" id="e17_texte" ></text>
  <text style="fill:black;font-family:Arial;font-size:20px;" x="424.748" y="363.782" id="e18_texte" ></text>
  <text style="fill:black;font-family:Arial;font-size:20px;" x="422.563" y="372.521" id="e19_texte" >
    <tspan x="422.563"> Tenant</tspan>
    <tspan x="444.412" dy="1.25em" y="">C</tspan>
  </text>
  <path d="M2,0h2l-4,4l-4,-4h2v-4h4Z" style="fill:khaki; stroke:black; vector-effect:non-scaling-stroke;stroke-width:1px;" id="e20_shape" transform="matrix(4.82758 1.17793 -3.89766 16.9362 182.579 221.602)"/>
  <path d="M2,0h2l-4,4l-4,-4h2v-4h4Z" style="fill:khaki; stroke:black; vector-effect:non-scaling-stroke;stroke-width:1px;" id="e21_shape" transform="matrix(4.41869 0 0 17.9037 305.126 219.58)"/>
  <path d="M2,0h2l-4,4l-4,-4h2v-4h4Z" style="fill:khaki; stroke:black; vector-effect:non-scaling-stroke;stroke-width:1px;" id="e22_shape" transform="matrix(4.28827 -1.9671 4.12185 17.8648 408.022 221.427)"/>
</svg>
<br />

<b>3) Standalone single-tenant app with single-tenant database:-</b> It is the another type of Multi-tenancy. In this architecture install whole application for each tenant. Each tenant has its own app instance as well as database instance. This architecture provide highest level of data isolation.The cost of this architecture is very high due standalone application and database.

<svg width="820px" height="520px" viewBox="-0.210084 0 820.42 520" preserveAspectRatio="xMidYMid meet" >
  <rect id="svgEditorBackground" x="0" y="0" width="820" height="520" style="fill: none; stroke: none;"/>
  <defs id="svgEditorDefs">
    <polygon id="svgEditorShapeDefs" style="fill:khaki;stroke:black;vector-effect:non-scaling-stroke;stroke-width:1px;"/>
  </defs>
  <rect x="175" y="24" style="fill:#57c1f2;stroke:black;stroke-width:1px;" id="e1_rectangle" width="158.856" height="69.2605" transform="matrix(1.0665 0 0 1 -12.911 13)" ry="0" rx="0"/><text style="fill:black;font-family:Arial;font-size:20px;" x="190.21" y="76.5547" id="e3_texte" >App Instance A</text>
  <path d="M-4,-2.5v5q0,1,4,1t4,-1v-5q0,1,-4,1t-4,-1q0,-1,4,-1t4,1t-4,1t-4,-1Z" style="fill:khaki; stroke:black; vector-effect:non-scaling-stroke;stroke-width:1px;" id="e14_shape" transform="matrix(0.125 0 0 0.125 210.5 313.438)"/>
  <path d="M-0.6252346416877963,-1.1155330517316193v5.0000000000000036q0,1,4,1t4.000000000000002,-1v-5q0,1.0000000000000064,-4.000000000000002,1.0000000000000064t-3.9999999999999996,-1.0000000000000064q0,-1,3.9999999999999996,-1t4.000000000000002,0.9999999999999987t-4.000000000000002,1.0000000000000062t-3.9999999999999996,-1.0000000000000062Z" style="fill:#57c1f2; stroke:black; vector-effect:non-scaling-stroke;stroke-width:1px;" id="e1_shape" transform="matrix(12.6246 0 0 14.0205 206.807 337.679)"/>
  <path d="M7.5917343192359485,-1.60002019613494v5.000000000000005q0,1.000000000000008,4.000000000000002,1.000000000000008t4.0000000000000036,-1.0000000000000058v-5.000000000000005q0,1.0000000000000044,-4.0000000000000036,1.0000000000000044t-4.000000000000003,-1.0000000000000044q0,-1.0000000000000044,4.000000000000003,-1.0000000000000044t4.0000000000000036,1.0000000000000044t-4.0000000000000036,1.0000000000000044t-4.000000000000003,-1.0000000000000044Z" style="fill:#57c1f2; stroke:black; vector-effect:non-scaling-stroke;stroke-width:1px;" id="e2_shape" transform="matrix(12.3259 0 0 14.3097 326.432 342.385)"/>
  <text style="fill:black;font-family:Arial;font-size:20px;" x="294.748" y="355.042" id="e6_texte"/>
  <text style="fill:black;font-family:Arial;font-size:20px;" x="431.303" y="369.244" id="e16_texte" >Tenant B</text>
  <text style="fill:black;font-family:Arial;font-size:20px;" x="428.025" y="364.874" id="e17_texte"/>
  <text style="fill:black;font-family:Arial;font-size:20px;" x="424.748" y="363.782" id="e18_texte"/>
  <rect x="351.555" y="39.3277" style="fill:#57c1f2;stroke:black;stroke-width:1px;" id="e2_rectangle" width="163.866" height="66.6387" transform="matrix(1 0 0 1.04938 26.2185 -5.77238)" ry="0" rx="0"/>
  <text style="fill:black;font-family:Arial;font-size:20px;" x="393.067" y="76.4706" id="e4_texte" >App Instance B</text>
  <text style="fill:black;font-family:Arial;font-size:20px;" x="206.26" y="369.244" id="e5_texte" >Tenant A</text>
  <path d="M2,0h2l-4,4l-4,-4h2v-4h4Z" style="fill:khaki; stroke:black; vector-effect:non-scaling-stroke;stroke-width:1px;" id="e7_shape" transform="matrix(5.96032 0 0 14.9103 249.412 207.017)"/>
  <path d="M2,0h2l-4,4l-4,-4h2v-4h4Z" style="fill:khaki; stroke:black; vector-effect:non-scaling-stroke;stroke-width:1px;" id="e8_shape" transform="matrix(6.06618 0 0 14.2279 467.899 210.294)"/>
</svg>

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
