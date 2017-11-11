---
author: Steph Skardal
gh_issue_number: 224
tags: analytics, seo
title: WordPress Plugin for Omniture SiteCatalyst
---

A couple of months ago, I integrated Omniture SiteCatalyst into an Interchange site for one of End Point's clients, [CityPass](http://www.citypass.com/). Shortly after, the client added a blog to their site, which is a standalone WordPress instance that runs separately from the Interchange ecommerce application. I was asked to add SiteCatalyst tracking to the blog.

I've had some experience with WordPress plugin development, and I thought this was a great opportunity to develop a plugin to abstract the SiteCatalyst code from the WordPress theme. I was surprised that there were limited Omniture WordPress plugins available, so I'd like to share my experiences through a brief tutorial for building a WordPress plugin to integrate Omniture SiteCatalyst.

First, I created the base wordpress file to append the code near the footer of the wordpress theme. This file must live in the ~/wp-content/plugins/ directory. I named the file omniture.php.

```php
  &lt;?php /*
    Plugin Name: SiteCatalyst for WordPress
    Plugin URI: http:www.endpoint.com/
    Version: 1.0
    Author: Steph Powell
    */
    function omniture_tag() {
    }
    add_action('wp_footer', 'omniture_tag');
  ?&gt;
```

In the code above, the wp_footer is a specific WordPress hook that runs just before the </body> tag. Next, I added the base Omniture code inside the omniture_tag function:

```php
...

function omniture_tag() {
?&gt;
&lt;script type="text/javascript"&gt;
&lt;!-- var s_account = 'omniture_account_id'; --&gt;
&lt;/script&gt;
&lt;script type="text/javascript" src="/path/to/s_code.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript"&gt;&lt;!--
s.pageName='' //page name
s.channel='' //channel
s.pageType='' //page type
s.prop1='' //traffic variable 1
s.prop2='' //traffic variable 2
s.prop3='' //traffic variable 3
s.prop4= '' //traffic variable 4
s.prop5= '' //traffic variable 5
s.campaign= '' //campaign variable
s.state= '' //user state
s.zip= '' //user zip
s.events= '' //user events
s.products= '' //user products
s.purchaseID= '' //purchase ID
s.eVar1= '' //conversion variable 1
s.eVar2= '' //conversion variable 2
s.eVar3= '' //conversion variable 3
s.eVar4= '' //conversion variable 4
s.eVar5= '' //conversion variable 5
/************* DO NOT ALTER ANYTHING BELOW THIS LINE ! **************/
var s_code=s.t();if(s_code)document.write(s_code)
--&gt;&lt;/script&gt;
&lt;?php
}

...
```

To test the footer hook, I activated the plugin in the WordPress admin. A blog refresh should yield the Omniture code (with no variables defined) near the </body> tag of the source code.

After verifying that the code was correctly appended near the footer in the source code, I determined how to track the WordPress traffic in SiteCatalyst. For our client, the traffic was to be divided into the home page, static page, articles, tag pages, category pages and archive pages. The Omniture variables pageName, channel, pageType, prop1, prop2, and prop3 were modified to track these pages. Existing WordPress functions is_home, is_page, is_single, is_category, is_tag, is_month, the_title, get_the_category, the_title, single_cat_title, single_tag_title, the_date were used.

```php
...

&lt;script type="text/javascript"&gt;&lt;!--
&lt;?php
if(is_home()) {    //WordPress functionality to check if page is home page
        $pageName = $channel = $pageType = $prop1 = 'Blog Home';
} elseif (is_page()) {    //WordPress functionality to check if page is static page
        $pageName = $channel = the_title('', '', false);
        $pageType = $prop1 = 'Static Page';
} elseif (is_single()) { //WordPress functionality to check if page is article
        $categories = get_the_category();
        $pageName = $prop2 = the_title('', '', false);
        $channel = $categories[0]-&gt;name;
        $pageType = $prop1 = 'Article';
} elseif (is_category()) {    //WordPress functionality to check if page is category page
        $pageName = $channel = single_cat_title('', false);
        $pageName = 'Category: ' . $pageName;
        $pageType = $prop1 = 'Category';
} elseif (is_tag()) {     //WordPress functionality to check if page is tag page
        $pageName = $channel = single_tag_title('', false);
        $pageType = $prop1 = 'Tag';
} elseif (is_month()) {     //WordPress functionality to check if page is month page
        list($month, $year) = split(' ', the_date('F Y', '', '', false));
        $pageName = 'Month Archive: ' . $month . ' ' . $year;
        $channel = $pageType = $prop1 = 'Month Archive';
        $prop2 = $year;
        $prop3 = $month;
}
echo "s.pageName = '$pageName' //page name\n";
echo "s.channel = '$channel' //channel\n";
echo "s.pageType = '$pageType'  //page type\n";
echo "s.prop1 = '$prop1' //traffic variable 1\n";
echo "s.prop2 = '$prop2' //traffic variable 2\n";
echo "s.prop3 = '$prop3' //traffic variable 3\n";
?&gt;
s.prop4 = '' //traffic variable 4

...
```

The plugin allows you to freely switch between WordPress themes without having to manage the SiteCatalyst code and to track the basic WordPress page hierarchy. Here are example outputs of the SiteCatalyst variables broken down by page type:

### Homepage

```php
s.pageName = 'Blog Home' //page name
s.channel = 'Blog Home' //channel
s.pageType = 'Blog Home'  //page type
s.prop1 = 'Blog Home' //traffic variable 1
s.prop2 = '' //traffic variable 2
s.prop3 = '' //traffic variable 3
```

### Tag Page

```php
s.pageName = 'chocolate' //page name
s.channel = 'chocolate' //channel
s.pageType = 'Tag'  //page type
s.prop1 = 'Tag' //traffic variable 1
s.prop2 = '' //traffic variable 2
s.prop3 = '' //traffic variable 3
```

### Category Page

```php
s.pageName = 'Category: Food' //page name
s.channel = 'Food' //channel
s.pageType = 'Category'  //page type
s.prop1 = 'Category' //traffic variable 1
s.prop2 = '' //traffic variable 2
s.prop3 = '' //traffic variable 3
```

### Static Page

```php
s.pageName = 'About' //page name
s.channel = 'About' //channel
s.pageType = 'Static Page'  //page type
s.prop1 = 'Static Page' //traffic variable 1
s.prop2 = '' //traffic variable 2
s.prop3 = '' //traffic variable 3
```

### Archive

```php
s.pageName = 'Month Archive: November 2009' //page name
s.channel = 'Month Archive' //channel
s.pageType = 'Month Archive'  //page type
s.prop1 = 'Month Archive' //traffic variable 1
s.prop2 = '2009' //traffic variable 2
s.prop3 = 'November' //traffic variable 3
```

### Article

```php
s.pageName = 'Hello world!' //page name
s.channel = 'Test Category' //channel
s.pageType = 'Article'  //page type
s.prop1 = 'Article' //traffic variable 1
s.prop2 = 'Hello world!' //traffic variable 2
s.prop3 = '' //traffic variable 3
```

A followup step to this plugin would be to use the wp_options table in WordPress to manage the Omniture account id, which would allow admin to set the Omniture account id through the WordPress admin without editing the plugin code. I've uploaded the plugin to a GitHub repository [here](http://github.com/stephskardal/wordpress-sitecatalyst/).

*Update: This plugin is included in the WordPress plugin registry and can be found at [http://wordpress.org/extend/plugins/omniture-sitecatalyst-tracking/](http://wordpress.org/extend/plugins/omniture-sitecatalyst-tracking/).*
