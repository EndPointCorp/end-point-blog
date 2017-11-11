---
author: Steph Skardal
gh_issue_number: 413
tags: php, wordpress
title: A Simple WordPress Theme In Action
---



I’m a big fan of [WordPress](http://wordpress.org/). And I’m a big fan of building WordPress themes from the ground up. Why am I a big fan of building them from the ground up? Because...

- It's very easy to setup and build if you plan to move to utilize WordPress's blog architecture for your site, but just have a set of static pages initially.
- It allows you to incrementally add elements to your theme from starting from the ground up, rather than cutting out elements from a complex theme.
- It allows you to leave out features that you don’t need (search, comments, archives, listing of aticles), but still take advantage of the WordPress plugin community and core functionality.
- The learning curve of WordPress APIs and terminology can be complicated. It's nice to start simple and build up.

Here are some screenshots from my simple WordPress theme in action, a site that contains several static pages.

<table cellpadding="10" cellspacing="0" width="100%"><tbody><tr>
<td valign="top"><a href="/blog/2011/02/22/simple-wordpress-theme/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5576659759871325570" src="/blog/2011/02/22/simple-wordpress-theme/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width:230px;"/></a></td>
<td valign="top"><a href="/blog/2011/02/22/simple-wordpress-theme/image-1-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5576659770767853234" src="/blog/2011/02/22/simple-wordpress-theme/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 230px;"/></a></td>
<td valign="top"><a href="/blog/2011/02/22/simple-wordpress-theme/image-2-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5576659759059857778" src="/blog/2011/02/22/simple-wordpress-theme/image-2.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 230px;"/></a></td>
</tr></tbody></table>

The template is comprised of several files:

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td>File</td>
<td style="padding: 0px 0px 10px 10px;">Notes</td>
</tr>
<tr>
<td valign="top">header.php</td>
<td style="padding: 0px 0px 10px 10px;">Includes doctype, header html, and global stylesheets included here. <a href="http://codex.wordpress.org/Plugin_API/Action_Reference/wp_head">wp_head()</a> is called in the header, which will call any executables tied to the header hook using WordPress’s hook API. <a href="http://codex.wordpress.org/Function_Reference/wp_list_pages">wp_list_pages()</a> is also called, which is WordPress’s core method for listing pages.</td>
</tr>
<tr>
<td valign="top">footer.php</td>
<td style="padding: 0px 0px 10px 10px;">Includes footer navigation elements, global JavaScript, and Google Analytics. <a href="http://codex.wordpress.org/Plugin_API/Action_Reference/wp_footer">wp_footer()</a>, is also called here, which will call any executables tied to the footer hook using WordPress's hook API.</td>
</tr>
<tr>
<td valign="top">index.php</td>
<td style="padding: 0px 0px 10px 10px;">Calls get_header() and get_footer(), WordPress's core methods for displaying the header and footer. This also contains static content for the homepage for now (text and images).</td>
</tr>
<tr>
<td>page.php</td>
<td style="padding: 0px 0px 10px 10px;">Calls get_header() and get_footer(). Uses <a href="”http://codex.wordpress.org/The_Loop”">The Loop</a>, or WordPress's core functionality for display individual posts or pages to display the page content to render the single page static content.</td>
</tr>
<tr>
<td valign="top">404.php</td>
<td style="padding: 0px 0px 10px 10px;">Calls get_header() and get_footer(). This is similar to the index page as it contains a bit of static text and an image and is displayed for any pages not found.</td>
</tr>
<tr>
<td valign="top">CSS, images, JS</td>
<td style="padding: 0px 0px 10px 10px;">Static CSS, images, and JavaScript files used throughout the theme.</td>
</tr>
</tbody></table>

Files that are more traditionally seen in WordPress templates excluded from this template are the sidebar.php, archive.php, archives.php, single.php, search.php, and searchform.php. I plan to add some of these later as the website grows to include blog content, but these templates are unnecessary for now.

Below are a couple snapshots of the shared elements between pages.

<table cellpadding="10" cellspacing="0" width="100%">
<tbody><tr>
<td>
<a href="/blog/2011/02/22/simple-wordpress-theme/image-3-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5576665372793032274" src="/blog/2011/02/22/simple-wordpress-theme/image-3.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width:270px;"/></a>
</td>
<td>The header (red) and footer (blue) are shared between the page.php and index.php templates shown here.
</td>
<td>
<a href="/blog/2011/02/22/simple-wordpress-theme/image-4-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5576659774972935746" src="/blog/2011/02/22/simple-wordpress-theme/image-4.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width:270px;"/></a>
</td>
</tr>
</tbody></table>

You can see the site in the wild [here](http://stephskardal.com/).

*Update: Since this article was published, the website shown here has been updated to include a "blog" page, which is one more page that uses the [exec-php plugin](http://wordpress.org/extend/plugins/exec-php/) to list blog articles.*


