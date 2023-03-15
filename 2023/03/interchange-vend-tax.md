---
author: "Mark Johnson"
title: "Interchange 3rd Party Tax Support"
date: 2023-03-28
tags:
- interchange
- salestax
---

New 3rd-party tax API support has been added to core Interchange. In the wake of the Wayfair decision<sup>1</sup>, many businesses running Interchange catalogs lack the necessary tools for full compliance. A new translation layer has been created in `Vend::Tax` to connect the standard salestax structures and routines that operate within Interchange, and the development of vendor-specific 3rd-party tax providers. The goal of the `Vend::Tax` framework is to create a space to allow for development of any number of vendor-specific tax services to support tax calculation in Interchange.

`Vend::Tax` defines 3 new tags to support its function:

* `[tax-lookup]` returns calculated tax amount determined by specific 3rd-party provider. Tax may be estimated or live lookup, depending on settings. Data required to calculate tax will be provider dependent.
* `[load-tax-averages]` requests and stores tax averages for running in estimate mode, for providers that support it. Stores estimates by default in "tax_averages" table. Further, allows for local tracking of jurisdictions with nexus, which can be used by live lookups to determine if a particular lookup can be skipped entirely. See load_tax_averages Job and "tax_averages" table definition in strap demo.
* `[send-tax-transaction]` reports to provider the resulting tax transaction for a given order, for providers that support it. By default, operates based on "transactions"."tax_sent" field. 0/empty indicates transaction not reported.  1 indicates transaction successfully reported. -1 indicates an error attempting to report transaction, requiring manual intervention. See send_tax_transactions Job in strap demo.

Conceptually, `Vend::Tax` is patterned off of `Vend::Payment` for payment transactions. It provides the defined interface that Interchange will use, via the 3 tags shown above, but must delegate to vendor-specific implementations through tax gateway modules.

Additionally, connectors have already been constructed for Tax Jar<sup>2</sup> and Avalara<sup>3</sup> in core Interchange, so that catalogs can convert to use either of these popular services for calculating their salestax with an upgrade and a few adjustments to their catalog configuration. Both Tax Jar and Avalara provide sales tax calculation, product categorization, and reporting tools that allow merchants to comply with Wayfair and keep their focus on their business.

While currently only Tax Jar and Avalara are supported - see `Vend::Tax::TaxJar` and `Vend::Tax::Avalara` -- `Vend::Tax` was designed to facilitate and encourage the development of any 3rd-party providers through the creation of new `Vend::Tax::Service` modules. A review of either of the Tax Jar or Avalara tax gateway modules should be instructive for the expected interface with the 3 usertags.

For merchants who have, or wish to establish, relationships with other tax providers, they are free to build, or contract with consultants to build, their own provider's vendor-specific module and use that to back the work performed within `Vend::Tax`. Any such development projects are encouraged to be submitted for inclusion in Interchange core, giving the merchant and developer the benefit of community improvements and core inclusion on future upgrades.

### Configuring your Catalog to Use `Vend::Tax`

In order to leverage `[tax-lookup]` to back the `[salestax]` tag, use it with the SalesTax directive. E.g.:

```plain
SalesTax  [tax-lookup service=TaxJar]
```

The service parameter should correspond with the segment of the namespace of the tax gateway module after `Vend::Tax`. Here, the example enables Tax Jar in module `Vend::Tax::TaxJar`.

If your business requires sufficient customization, the existing tax gateway modules can be subclassed, keeping all your customizations separate from core code and safe from collisions during upgrades. An example of such an expansion to Avalara would be to create module `Vend::Tax::Avalara::MyBiz` to subclass `Vend::Tax::Avalara` and change the config setup to:<p>

```plain
SalesTax  [tax-lookup service=Avalara::MyBiz]
```

Additionally, using the strap setup, you can easily enable Tax Jar specifically by setting the following variables in variable.txt:

```plain
TAXSERVICE TaxJar
TAXTOKEN [your Tax Jar token]
NEXUS_ADDRESS [business address]
NEXUS_CITY [business city]
NEXUS_STATE [business state postal code]
NEXUS_ZIP [business zip]
NEXUS_COUNTRY [business iso two-letter country code]
```

For Avalara in strap, you also would set the taxservice and nexus variables, but then set your account API user and password:

```plain
TAXSERVICE Avalara
AVALARA_USER [your API user]
AVALARA_PASSWORD [your API password]
NEXUS_ADDRESS [business address]
NEXUS_CITY [business city]
NEXUS_STATE [business state postal code]
NEXUS_ZIP [business zip]
NEXUS_COUNTRY [business iso two-letter country code]
```

Finally, like the payment modules, in order to make a particular tax service available, it must be required from interchange.cfg. E.g.:

```plain
Require module Vend::Tax::TaxJar
```

### Links

1. [https://www.lbmc.com/blog/wayfair-case-sales-tax/](https://www.lbmc.com/blog/wayfair-case-sales-tax/)
1. [https://www.taxjar.com/](https://www.taxjar.com/)
1. [https://www.avalara.com/](https://www.avalara.com/)
