---
author: Juan Pablo Ventoso
title: "Running Magento 2 in Windows with XAMPP"
tags: magento, e-commere, mysql, xampp, windows, php
---

<img src="/blog/2019/03/05/running-magento-2-windows-xampp/e-commerce-safe.jpg" alt="E-commerce" /><br><a href="https://burst.shopify.com/photos/computer-security-lock-and-payment?q=e-commerce">Photo by Nicole De Khors</a> · <a href="https://burst.shopify.com/licenses/shopify-some-rights-reserved">Burst Some Rights Reserved</a>

Magento is an open source e-commerce platform, written in PHP and relying on MySQL/MariaDB for persistence. According to <a href="https://trends.builtwith.com/shop" target="_blank">BuiltWith</a>, Magento is the third most used platform in e-commerce websites. It began its life in 2008 with its first release version, and a major update (Magento 2) was later relased in 2015.

And now, more than three years after, <b>Magento 1 is slowly dying</b>: There won't be any more quality fixes, no more security updates from June 2020, and lack of extensions support for fixes or new payment methods. So the obvious choice will be Magento 2 from now on.

But is it fully tested yet? Is it stable enough? If we already have a website running with Magento 1, what should we do? Because migrating to Magento 2 is not just hitting an “Update” button: Themes are incompatible, most extensions won't work, and of course, there's a big set of changes to get familiar with.

So a good approach might be to get a clean Magento 2 version deployed locally, to look what we need to do to get our website updated and running, test the backend, find where the configuration sections are located, and so on. And many business users, and even some developers like myself, have Microsoft Windows installed on our computers.

##Environment setup

The environment I used for this testing installation was Windows 10 Professional. As a first step, we'll need to make sure that localhost is published in our local hosts file:

* Navigate to the folder ```%SystemRoot%\system32\drivers\etc```
* Backup the existing hosts file
* Open a text editor (like Notepad) with administrator rights
* Open the hosts file
* Make sure the first line after the commented (#) lines is ```127.0.0.1 localhost``` and the second is ```::1 localhost```
* Open a cmd Window with administrator rights and run the command ```ipconfig /flushdns```


Now we're ready to install the environment needed to run Magento. I recommend using <a href="https://www.apachefriends.org/" target="_blank">XAMPP</a>, a free Apache distribution for Windows that includes MariaDB, PHP and Perl on a single package. Magento 2 currently runs with PHP 7.2 and it will not work with newer versions.

* Install XAMPP 7.2 with default settings: <a href="https://www.apachefriends.org/xampp-files/7.2.15/xampp-win32-7.2.15-0-VC15-installer.exe" target="_blank">apachefriends.org/xampp-files/7.2.15/xampp-win32-7.2.15-0-VC15-installer.exe</a>

* Download Magento 2. You will need to register in the website first: <a href="https://magento.com/tech-resources/download" target="_blank">magento.com/tech-resources/download</a>

* Create a new “magento” subfolder (or whatever name you prefer) inside the htdocs folder in the XAMPP installation (usually ```C:\xampp```) and uncompress the Magento 2 archive there.

* Start the XAMPP Control Panel from the Windows start menu. In the “Apache” section, click the “Config” button and, on the menu that appears, select “PHP (php.ini)”. Remove the “;” before the ```extension=intl```, ```extension=soap```, ```extension=xsl``` texts (this will enable the intl, soap and xsl extensions).

<img src="/blog/2019/03/05/running-magento-2-windows-xampp/xampp-control-panel.jpg" /><br><small>Screenshot of the XAMPP Control Panel with the PHP config menu displayed.</small>


##MySQL and Magento setup

We have all the files in place and the environment ready to start configuring the database and install Magento 2.

* Start the Apache and MySQL services from the XAMPP Control Panel. Wait for the green status texts to appear.

* Create a “magento” (or whatever name you prefer) database in MySQL from phpMyAdmin, installed already on XAMPP: <a href="http://localhost/phpmyadmin" target="_blank">localhost/phpmyadmin</a>

* Run the Magento 2 setup from <a href="http://localhost/magento" target="_blank">localhost/magento</a> (replace the “magento” part of the URL with whatever name you have choosen to host Magento). If the setup program requires to do any additional configuration change, do it as instructed. Do a screenshot or save the final page contents for later use.

<img src="/blog/2019/03/05/running-magento-2-windows-xampp/magento-2-installation-success.jpg" /><br><small>Example of the page that will be displayed when the Magento 2 installation finishes.</small>


##Fixing known issues

When we finish the installation process, we will have a Magento 2 instance running on our host. But we're not ready yet! There's a couple known bugs with Magento 2 and XAMPP at the moment I'm writing this article:

* The Magento admin page may not work (it shows a blank page): Fix this issue by updating the “isPathInDirectories” function inside the ```Validator.php``` file as instructed in this article: <a href="https://magento.stackexchange.com/questions/252188/magento-2-2-7-admin-panel-blank-page" target="_blank">magento.stackexchange.com/questions/252188/magento-2-2-7-admin-panel-blank-page</a>

* We might not be able to upload images (like a custom logo or product pictures): Fix this issue by updating the ```design_config_form.xml``` file as shown in the reference: <a href="https://community.magento.com/t5/Magento-2-x-Technical-Issues/A-technical-problem-with-the-server-created-an-error-Try-again/m-p/115085#M7549" target="_blank">community.magento.com/t5/Magento-2-x-Technical-Issues/A-technical-problem-with-the-server-created-an-error-Try-again/m-p/115085#M7549</a>

After we finish making this changes, we will need to <b>restart the Apache service</b> from the XAMPP control panel. And that's it! We should be ready to open the Magento front page, and login into the backend.

<img src="/blog/2019/03/05/running-magento-2-windows-xampp/magento-2-front-end.jpg" /><br><small>An empty home page with the default theme enabled in Magento 2.</small>

<img src="/blog/2019/03/05/running-magento-2-windows-xampp/magento-2-back-end.jpg" /><br><small>This is how the Magento 2 back-end dashboard looks like once we login.</small>


##Setting up the store: A roadmap

The purpose of this article is to get Magento 2 up and running on Windows computer, and that's what -I hope- we've achieved so far. But just to point in a direction on what to do next, below is my usual roadmap to set up the store, add a few products and publish the catalog on the home page.

* Change the default store name and logo from the section Content > Design > Configuration and choose “Edit” in the “Default store view”.

* Set up the default store configuration from the section Stores > Configuration.

* Create the product categories from the section Catalog > Categories. Set up a category name and it’s dependency from another category, or from the default master category.

* Create/edit the product attributes from the section Stores > Attributes (check the option “visible in storefront” to show the products in the product page). For example, custom attributes for book products would be Author, Publisher...

* Add the attributes to the default attribute set from the section Stores > Attribute. This is required for the attributes to show up when adding a new product by default.

* Create a set of products from the section Catalog > Products. Set the custom variations for each product from the “Customizable options” section. Set up a short and long description, a custom SKU for each customizable option, and a tax mode.

* Add a widget to the homepage to show the product catalog from the section Content > Homepage > Edit > Show/Hide Editor > Add widget > Products list. Here we can also add any content we like, including HTML tags, images and third-party content.


##Conclusion

It's possible -and pretty straightforward- to run a Magento 2 instance in Windows with XAMPP. But this is just a kick-off, a simple overview: there's a lot more to do if we want to get a full e-commerce website that is ready to scale up and support enterprise-level traffic, like caching optimization, load balancing and advanced server-side monitoring.

At <b>End Point</b>, we have professionals with a strong background in deploying powerful, reliable, fully responsive, fast and SEO optimized e-commerce websites. We have experience in migrating Magento to newer versions, or even create a full Magento 2 website from scratch. <b>Drop a line if you want to hear more.</b>