---
author: "Juan Pablo Ventoso"
title: "Advanced WordPress customizations"
tags: wordpress, php, cms
gh_issue_number: 1692
---

![WordPress](blog/2020/11/27/advanced-wordpress-customizations/wordpress-logo-phone.jpg)

[Photo](https://www.flickr.com/photos/cdharrison/4289847815/) by [Chris Harrison](https://www.flickr.com/photos/cdharrison/) on Flickr, [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/), cropped

WordPress is the [most popular CMS](https://www.isitwp.com/popular-cms-market-share/), allowing you to create a professional-looking website at a relatively low cost. It also has a really strong community behind it, creating great content and supporting developers across the world.

But being popular also means being the main target of hacker attacks, and that’s why it’s crucial to keep the CMS, the theme, and all the plugins updated. When the requirements go beyond what WordPress offers on the surface, we need to find an efficient way to add our custom logic into the CMS without interfering with version upgrades, keeping the focus on security.

### Custom CSS and JavaScript

A pretty common scenario in WordPress consists of installing a theme that fits most of our requirements and writing an extra layer of functionality over it to get that custom look and user experience we are looking for. Updating the theme files means that we cannot easily upgrade or change the theme without backing up our changes, and then restoring them after the upgrade, so that’s definitely not a good approach.

To make our way around this issue, some themes offer a section to add custom JavaScript or CSS rules. But sometimes we need change themes in the middle of our developing process, so I usually rely on plugins to make my frontend changes. One simple, straightforward plugin I usually install to add custom styles and frontend scripts is [Simple Custom CSS and JS](https://wordpress.org/plugins/custom-css-js/).

![Simple Custom CSS and JS](blog/2020/11/27/advanced-wordpress-customizations/wordpress-simple-custom-css-js.jpg)

It has several customization options I usually need for SEO purposes, including the possibility to create several independent code segments and load each one in a different section (header/​footer) to improve loading speed. We can also include our custom content as embedded source/​styles or as external references. It also includes an editor with syntax highlighting, and allows adding custom content to the WordPress admin section.

### Custom PHP code

Another thing I usually need when customizing a WordPress website is the ability to run my own PHP code inside a WordPress page or post. That is not allowed by the CMS by default, but like most things in WordPress, there is a plugin that will make our lives easier: It’s called [Insert PHP Code Snippet](https://wordpress.org/plugins/insert-php-code-snippet/).

You can create your own PHP routines as snippets that can be inserted with shortcodes into a WordPress page, posts, template, or whenever you can add a shortcode. This will allow running any custom backend code anywhere on the website.

![Custom PHP Code Snippet](blog/2020/11/27/advanced-wordpress-customizations/wordpress-custom-php-snippet.jpg)

To run the code on a page or post, all that needs to be done is pasting the shortcode on the content with the “PHP” button that appears on the button bar on the editor:

![Shortcode example](blog/2020/11/27/advanced-wordpress-customizations/wordpress-custom-php-snippet-shortcode.jpg)

### Custom hooks

When our logic needs to be fired up from an event on the CMS, or if we need to make changes to the default WordPress behavior or data, we will need to use the [add_action() function](https://developer.wordpress.org/reference/functions/add_action/) or the [add_filter() function](https://developer.wordpress.org/reference/functions/add_filter/).

- `add_action()` allows us to execute a PHP function on specific points of the WordPress execution, for example when a post is created or commented, or when a user is created. A full list of actions is available [here](https://codex.wordpress.org/Plugin_API/Action_Reference).

- `add_filter()` allows us to update information associated with WordPress, for example, to set a custom CSS class for the body or to replace the login button text. A full list of filters is available [here](https://codex.wordpress.org/Plugin_API/Filter_Reference).

The following example sends an email to the webmaster when a new comment is created, using the `add_action()` function:

```php
function email_comment() {
  wp_mail('webmaster@website.com', 'New comment', 'New comment posted on the website');
}
add_action('comment_post','email_comment');
```

Here’s another example that allows to perform a string replacement across the website by using the `add_filter()` function:

```php
function replace_text($text) {
  return str_replace('Text to search', 'Text to replace with', $text);
}
add_filter('gettext', 'replace_text');
```

We can add these code segments using the PHP Snippet plugin (recommended) or using the `functions.php` file included in our theme. This last option is not recommended since it has the difficulty we discussed above about missing our custom content after upgrading the theme.

### Conclusion

WordPress is a great CMS with an elegant backend and a big list of themes and plugins we can use. But before we start adding custom code, we need to make sure it will persist after upgrading everything else to the latest version.

The techniques we saw in this post are meant for websites that only need some small custom changes or improvements. If we need to include a complete layer of logic into a website, it’s always recommended to write a custom plugin from scratch, if there is nothing out there that serves the purpose. But that’s material for another blog post!

At End Point, we build web solutions in WordPress and many other technologies, keeping security and high standards in mind. [Contact us](/contact) if you want to find out more.
