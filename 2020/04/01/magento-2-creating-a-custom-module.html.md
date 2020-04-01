---
author: "Juan Pablo Ventoso"
title: "Magento 2: Creating a custom module"
tags: magento, php, ecommerce
---

<img src="magento-2-creating-a-custom-module/bridge-wires.jpg" alt="Bridge with wires" /> [Photo](https://unsplash.com/photos/q4ZBGVzJskE) by [Babatunde Olajide](https://unsplash.com/@olajidetunde), cropped form original

<b>What is a Magento module?</b> It's a set of classes and routines that will depend and interact with other Magento classes in order to add a specific feature to a Magento application. While a theme is orientated towards the front-end and user experience, a module is orientated towards the backend logic and the business flow.

We will need to create a custom module if we need to add or change the existing business logic at a level where Magento doesn’t provide a setting or option for it. For example, if our business has a specific feature or set of features that are not common to the market.

### Creating a basic Magento module

Luckily, creating a simple Magento 2 module is not that hard. We will need to accomplish the following tasks:

* Creating a new directory for the module
* Creating the registration.php script
* Creating the `etc/module.xml` information file
* Installing the new module

#### Creating a new directory for the module

Where should the new directory for our module be placed? We have two options to choose from:

* `app/code/{vendor}/`
* `vendor/{vendor}/`

If your module is intended for a specific website you're working on, you can use the first option. But if you're creating a module with the intention of it being reused on several websites, it would be best to choose the second option. From now on, let's suppose we chose the first one.

So let's create a directory named `EndPoint` and a subdirectory inside it, `MyModule`, using the command line:

```bash
cd {website_root}
mkdir app/code/EndPoint
mkdir app/code/EndPoint/MyModule
```

#### Creating the registration.php script

The registration.php file’s purpose is to tell Magento to register the new module under a specific name and location.
So we will create a file named `app/code/EndPoint/MyModule/registration.php` with the folllowing content:

```php
<?php
\Magento\Framework\Component\ComponentRegistrar::register(
    \Magento\Framework\Component\ComponentRegistrar::MODULE,
    'EndPoint_MyModule',
    __DIR__
);
```

So we are telling Magento that our module will be named EndPoint_MyModule.

#### Creating the etc/module.xml information file

Now, we are going to create our module information file where we will specify the module version number. First, we need to create the `etc` directory inside `app/code/EndPoint/MyModule`:

```bash
mkdir app/code/EndPoint/MyModule/etc
```

And then we need to create the module.xml file with the following content:

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="urn:magento:framework:Module/etc/module.xsd">
    <module name="EndPoint_MyModule" setup_version="1.0.0">
    </module>
</config>
```

#### Installing the new module

That's it! We have everything we need to install our new module. Now, we need to tell Magento we want to install and enable our new module. So we need to run, from our website root:

```bash
php bin/magento setup:upgrade
```

Magento will output a bunch of module names and configuration updates, and our new module `EndPoint_MyModule` should be listed within that output.

### Adding a custom route to our module

We have a working, enabled module, but it's not doing anything at all! So what would be a simple thing for us to check that our module is enabled? We can set up a custom route, so if we hit an URL like `https://{our_website}/mymodule/test/helloworld` we can return a custom response from a controller.

Creating a custom route will need some steps on its own:

* Creating a new directory for the controller
* Creating the etc/routes.xml file
* Creating the controller
* Upgrading the new module

#### Creating a new directory for the controller

First, we need to create a new directory where we will create the new PHP controller for our custom route. The new directory path should be:

* `app/code/EndPoint/MyModule/Controller`

We can create as many directory levels we want, depending on the desired our path. For example, if we create a class named `Index` on the path `app/code/EndPoint/MyModule/Controller`, the URL that will be routed to this controller will be `https://{our_website}/mymodule/index` (the "Controller" directory is ignored). If we create a class named `HelloWorld` on the path `app/code/EndPoint/MyModule/Controller/Test`, the resulting URL will be `https://{our_website}/mymodule/test/helloworld`.

#### Creating the etc/routes.xml file

The `routes.xml` will tell Magento what base URL will be used for our module. First, we need to create the "frontend" directory where the routes.xml file needs to be placed:

```bash
mkdir app/code/EndPoint/MyModule/etc/frontend
```

In this example, we want the base URL to be `mymodule`, so we need to create an XML file inside the new directory that will route all requests made to the given URL to our module controllers:

```xml
<?xml version="1.0" ?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="urn:magento:framework:App/etc/routes.xsd">
    <router id="standard">
        <route frontName="mymodule" id="mymodule">
            <module name="EndPoint_MyModule"/>
        </route>
    </router>
</config>
```

#### Creating the controller

If we want to respond to requests to the `https://{our_website}/mymodule/test/helloworld` URL, we first need to create the base `Controller` directory and the `Test` subdirectory:

```bash
mkdir app/code/EndPoint/MyModule/Controller
mkdir app/code/EndPoint/MyModule/Controller/Test
```

Under this directory, we'll create our custom Magento controller. All route controllers should extend `\Magento\Framework\App\Action\Action`. Also, we need to have a public `construct()` method to pass the context to our ancestor, and finally, an `execute()` function that will be called when the URL is hit:

```php
<?php

namespace EndPoint\MyModule\Controller\Test;

class HelloWorld extends \Magento\Framework\App\Action\Action
{

    public function __construct(
        \Magento\Framework\App\Action\Context $context
    ) {
        parent::__construct(
            $context
        );
    }

    public function execute()
    {
        echo "Hello world!";
    }

}
```

#### Upgrading the new module

We have everything in place to tell Magento we have new changes to be deployed. How we do that? First, we need to upgrade our Magento setup. But since we added a new controller that gets parameters from the dependency injector in the construct, we also need to compile the dependency injection engine (including factories, proxies and interceptors). And finally, we need to clear the cache so new content will be served from our custom URL:

```bash
php bin/magento setup:upgrade
php bin/magento setup:di:compile
php bin/magento cache:flush
```

This process can take some minutes to complete, but after it's done we can try to reach our new custom URL. If we get a response like the one below:

![Hello world!](magento-2-creating-a-custom-module/magento-hello-world-response.jpg)

That will mean our module is working!

And that's all for now. In the next posts, we'll start complicating things a bit by overriding Magento classes with our custom ones or creating custom controllers that will return information from the Magento core classes. And don't forget to add any questions, suggestions or issues below!