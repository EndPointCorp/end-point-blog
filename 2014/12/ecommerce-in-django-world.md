---
author: Kirk Harr
title: Ecommerce in the Django World
github_issue_number: 1063
tags:
- django
- ecommerce
- python
- cms
date: 2014-12-03
---

Mezzanine ([http://mezzanine.jupo.org/](http://mezzanine.jupo.org/)) is a powerful piece of software written for the Django Framework in Python that functions like a structured content management system similar to Drupal, WordPress, and others. Built on top of this CMS structure is a module which adds features for Ecommerce which is known as Cartridge ([http://cartridge.jupo.org/](http://cartridge.jupo.org/)).

### Installing Cartridge/Mezzanine

Installing the Mezzanine CMS system from scratch can be accomplished in two methods, either by using the pip python package manager, or you can clone the current source from the git repository from the software maintainers. If you were planning to modify either Mezzanine or Cartridge to customize the setup for your own needs the latter would likely be preferable as you could then easily begin creating custom branches off the original source to track the customization work. However for this example I will show the pip method of installation:

```plain
pip install -U cartridge
```

Once installed, there is a mezzanine-project command which will allow you to create a new blank Mezzanine environment within a new directory, and in this case we will also send an option to instruct the command to install the Cartridge module as well.
```plain
mezzanine-project -a cartridge new_cartridge_project
```

At this point you will have a blank Mezzanine environment with the cartridge module installed, now the Django database must be populated with the model information for the application, and then the Django application server will be started.

```plain
cd new_cartridge_project
python manage.py createdb
python manage.py runserver
```

If all went well, you should see the startup messages for the Django application server which will list the version numbers of the various libraries it will use, and then should be up and listening on the loopback interface. At this point to complete the setup you would just need to point your httpd at this loopback socket to send connections there.

### Cartridge Product Models

Products within Cartridge are defined within the python models for the application, there are three primary models to be concerned with in a Product definition, the Product, ProductVariation and ProductImage models specifically.

- Product — Defines the primary attributes for a product like name, price, SKU, and can be populated with optional fields for sale prices, etc.
- ProductVariation — Defines a variant of a product SKU, these would be most commonly used for things like product sizes and colors.
- ProductImage — Defines the image for the picture of each product.

Each of these three models exist within Django as their own data sets, but then they have foreign key references from each Product to all of its Variants and Images. While you can alter these model definitions using the django shell and other methods within python, you can also update and manage the products within the admin interface for the django site.

### Adding Products / Tracking Orders

Adding products through the admin interface for Django was relatively easy and quick:

<a href="/blog/2014/12/ecommerce-in-django-world/image-0-big.png" imageanchor="1"><img border="0" src="/blog/2014/12/ecommerce-in-django-world/image-0.png"/></a>

Within this interface you would provide the details for the products name, published status, date range for the product to be on the site, and product description in addition to any Variants or Images for the product. This is where the Mezzanine foundation of Cartridge start to show through, where this process mirrors the creating of a content page within Mezzanine, but has added these attributes of the product to the definition.

In the same way, Product Variants, Discount Codes, and Sales can be created in much the same way within the admin interface. In this way, once you had a basic Cartridge setup in place on your server, within most use cases for setting up a simple web store, Cartridge would remove the need to do any further hacking of python code, and would allow any user familiar with a CMS workflow for creating and managing the objects within the environment to manage the store.

In addition, Cartridge provides order management within the admin interface as well:

<a href="/blog/2014/12/ecommerce-in-django-world/image-1-big.png" imageanchor="1"><img border="0" src="/blog/2014/12/ecommerce-in-django-world/image-1.png"/></a>

From this interface you can update orders, create new orders, print the PDF invoices for the orders and track whether orders have been fulfilled and shipped to the customer.

### Conclusions

Like other Ecommerce applications built on top of a Content Management System, Cartridge and Mezzanine work well together to create a stack that allows for both ease of getting started with the system, and a massive degree of customization possible. Each component of Cartridge is defined within Django, and can be rewritten and customized to serve any number of use cases. The setup process for Cartridge was pretty straightforward, but one recommendation I can make is that once you have a working system up, you should place all of the files for Mezzanine and Cartridge into a source code management system like Git. Like other web applications of this type, the complexity of each change to the system can create a possible point of failure. Once you start making changes to the Mezzanine configuration files and the python for the Models and Views for Cartridge, controlling those changes becomes critical. In this way Mezzanine and Cartridge are spanning the normal continuum of software with the polar extremes of ease of use and customization by providing a good example to start with in the setup, and also exposing the full range of customization to the developer.
