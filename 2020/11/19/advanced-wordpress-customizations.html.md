---
author: "Juan Pablo Ventoso"
title: "Advanced Wordpress customizations"
tags: wordpress, php
---

![Wordpress](/2020/11/19/advanced-wordpress-customizations/wordpress-logo-phone.jpg)

Photo by [Chris Harrison](https://www.flickr.com/photos/cdharrison/) on Flickr - Cropped from original

Wordpress is the [most popular CMS](https://www.isitwp.com/popular-cms-market-share/), allowing to create a professional-looking website at a relatively low cost. It also has a really strong community behind it, creating great content and supporting developers across the world.

But being popular also means being the main target of hacker attacks, and that’s why it’s crucial to keep the CMS, the theme, and all the plugins updated. When the requirements go beyond what Wordpress offers on the surface, we need to find an efficient way to add our custom logic into the CMS without interfering with version upgrades, keeping the focus on security.


### Custom CSS and Javascript

A pretty common scenario in Wordpress consists of installing a theme that fits most of our basic requirements, but then we need to write a custom layer of functionality over it to get that custom look and user experience we need. Updating the theme files means that we cannot easily upgrade/change the theme without backing up our changes, and then restoring them after the upgrade, so that’s definitely not a good approach.

To make our way around this issue, some themes offer a section to add custom Javascript or CSS rules. But sometimes we need to move into a new theme in the middle of our developing process, so I usually rely on plugins to make my frontend changes. One simple, straightforward plugin I usually install to add custom styles and frontend scripts is [Simple Custom CSS and JS](https://wordpress.org/plugins/custom-css-js/).

![Simple Custom CSS and JS](/2020/11/19/advanced-wordpress-customizations/wordpress-simple-custom-css-js.jpg)

It has several customization options I usually need for SEO purposes, including the possibility to create several independent code segments and load each one in a different section (header/footer) to improve loading speed. We can also include our custom content as embedded source/styles or as external references. It also includes an editor with syntax highlighting, and allows adding custom content to the Wordpress admin section.


### Custom PHP code

Another thing I usually need when customizing a Wordpress website, is the ability to run my own PHP code inside a Wordpress page or post. That is not allowed by the CMS by default, but like most things in Wordpress, there is a plugin that will make our lives easier: It’s called <a href=”https://wordpress.org/plugins/insert-php-code-snippet/” target=”_blank”>Insert PHP Code Snippet</a>.

You can create your own PHP routines as snippets that can be inserted with shortcodes into a Wordpress page, posts, template, or whenever you can add a shortcode on. This will allow running any custom backend code anywhere on the website.

![Custom PHP Code Snippet](/2020/11/19/advanced-wordpress-customizations/wordpress-custom-php-snippet.jpg)

To run the code on a page or post, all that needs to be done is pasting the shortcode on the content with the "PHP" button that appears on the button bar on the editor:

![Shortcode example](/2020/11/19/advanced-wordpress-customizations/wordpress-custom-php-snippet-shortcode.jpg)


### Hook custom logic into Wordpress

When our custom logic needs to be fired up from an event on the CMS, or if we need to make changes to the way Wordpress behaves, we will need to use the [`add_action()`](https://developer.wordpress.org/reference/functions/add_action/) or the [`add_filter()`](https://developer.wordpress.org/reference/functions/add_filter/) functions.

- `add_action()` allow us to execute a PHP function on specific points of the Wordpress execution, for example when a post is created or commented, or when a user is created. A full list of actions is available [here](https://codex.wordpress.org/Plugin_API/Action_Reference).

- `add_filter()` allow us to update information associated with Wordpress, for example, to set a custom CSS class for the body or to replace the login button text. A full list of filters is available [here](https://codex.wordpress.org/Plugin_API/Filter_Reference).

The following example allows to to a text replacement across the website by using the add_filter() hook function:

```php
function replace_text($text) {
	return str_replace('Text to search', 'Text to replace with', $text);
}
add_filter('gettext', 'replace_text');
```

We can add this function using the PHP Snippet plugin (recommended) or using the `functions.php` file included in our theme. This second option is not recommended since it has the difficulty we discussed above about missing our custom content after upgrading the theme.


### Conclusion

Wordpress is a great CMS with an elegant backend, a big list of themes and plugins we can use, but before we start adding custom code, we need to pay extra attention to do it in such a way that will persist after upgrading everything to the latest version.

The techniques we saw in this post are meant for websites that only need some small custom changes or improvements. If we need to include a complete layer of logic into a website, it's always recommended to write a custom plugin from scratch, if there is nothing out there that serves the purpose. But that's material for another blog post!

At End Point, we build web solutions in Wordpress and several other technologies, but we always keep security and high standards in mind. [Contact us](/contact) if you want to find out more.