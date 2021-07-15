---
author: Steph Skardal
title: Blog versus Forum, Blogger versus WordPress in Ecommerce
github_issue_number: 257
tags:
- ecommerce
- seo
date: 2010-01-25
---

![](https://s.w.org/style/images/about/WordPress-logotype-standard.png)

Today, Chris sent me an email with two questions for one of our ecommerce clients:

- For ecommerce client A, should a forum or blog be added?
- For ecommerce client A, should the client use Blogger or WordPress if they add a blog?

These are relevant questions to all of our clients because forums and blogs can provide value to a static site or ecommerce site. I answered Chris’ question and thought I’d expand on it a bit for a brief article.

First, a rundown comparing the pros and cons of blog versus forum:

<table cellpadding="0" cellspacing="5" class="blog_article" width="100%">
<tbody><tr class="alt">
<td width="10%"> </td>
<td align="center" width="45%"><b>Blog</b></td>
<td align="center" width="45%"><b>Forum</b></td>
</tr>
<tr>
<td valign="top"><b>Pros</b></td>
<td valign="top">
<ul>
<li>Content tends to be more organized.</li>
<li>Content can be built to be more targeted for search.</li>
<li>Content can be syndicated easily.</li>
</ul>
</td>
<td valign="top">
<ul>
<li>There can be much more content because users are contributing content.</li>
<li>Since there is more user generated content, it has the potential to cover more of the <a href="https://en.wikipedia.org/wiki/Long_Tail">long tail</a> in search.</li>
<li>There is more potential for user involvement and encouragement to build and contribute to a community.</li>
</ul>
</td>
</tr>
<tr>
<td valign="top"><b>Cons</b></td>
<td valign="top">
<ul>
<li>User generated content will remain minimal if comments are the only form of user generated content in a blog.</li>
<li>If internal staff is responsible for authoring content, you can’t write as much content as users can contribute.</li>
</ul>
</td>
<td valign="top">
<ul>
<li>A forum requires management to prevent user spam.</li>
<li>A forum requires organization to maintain usability and search engine friendliness.</li>
</ul>
</td>
</tr></tbody></table>

If we assume that it takes the same amount of effort to write articles as it does to manage user generated content, the decision comes down to whether or not you want to utilize user contributions as part of the content. If the effort involved to write content or manage user generated content is different, a decision should be made based on how much effort the site owners want to make. Other opportunities for user generated content include product reviews and user QnA.

Next, a rundown comparing the pros and cons of Blogger versus **self-hosted** WordPress:

<table cellpadding="0" cellspacing="5" class="blog_article" width="100%">
<tbody><tr>
<td width="10%"> </td>
<td align="center" style="background-color:#002255;" width="45%"><b><a href="https://www.blogger.com"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5430766117686011266" src="/blog/2010/01/blog-vs-forum-blogger-vs-wordpress/image-0.png" style="margin:5px;width: 75px; height: 20px;"/></a></b></td>

<td align="center" style="background-color:#464646;" width="45%"><b><a href="https://wordpress.org"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5430766118456236978" src="/blog/2010/01/blog-vs-forum-blogger-vs-wordpress/image-0.png" style="margin:5px;width: 151px; height: 26px;"/></a></b></td></tr>
<tr><td valign="top"><b>Pros</b></td>
<td valign="top">
<ul>
<li>There are a decent amount of widgets available to integrate into a Blogger instance.</li>
<li>Fast Google indexing of content may result since the content is hosted by Google.</li>
<li>There is decent search implementation on Blogger.</li>
<li>A Blogger instance is very easy to create and easy to use.</li>
</ul>
</td>
<td valign="top">
<ul>
<li>There is a very large feature set available through the <a href="https://wordpress.org/plugins/">WordPress plugin</a> community.</li>
<li>Self-hosted WordPress blogs are relatively easy to set up. Many hosting platforms include WordPress installation and setup at the click of a button.</li>
<li>WordPress gives you control over the URL structure (articles, categories, tags) through permalinks.</li>
<li>Self-hosted WordPress can live at www.yoursite.com/blog/ which can strengthen your domain value in search through external links.</li>
<li>WordPress has a very flexible taxonomy system.</li>
</ul>
</td>
</tr>
<tr>
<td valign="top"><b>Cons</b></td>
<td valign="top">
<ul>
<li>The Blogger taxonomy system is limited (using labels) and labels pages are blocked in robots.txt to reduce indexation and search traffic of the label pages.</li>
<li>Blogger does not allow for a flexible URL structure. Once an article is published and a title is changed, the URL does not change.</li>
<li>Developers must be familiar with the Blogger template language to customize the template.</li>
<li>With Blogger, a blog can’t be hosted at http://www.yoursite.com/blog/. It can be hosted at http://blog.yoursite.com/. While this results in a strong subdomain, it does not strengthen your domain for search through external links to the blog.</li>
</ul>
</td>
<td valign="top">
<ul>
<li>Self-hosted WordPress requires your own hosting, setup and installation.</li>
<li>Self-hosted WordPress requires management of upgrades and plugins. Plugins may require code changes to the template files.</li>
<li>Self-hosted WordPress allows you to select existing themes, but you must be familiar with the WordPress template structure if you want a custom blog look.</li>
</ul>
</td>
</tr></tbody></table>

The decision to create a Blogger blog or install a WordPress blog will depend on resources such as engineering or designer involvement. A self-hosted blog solution will likely provide a larger feature set and more flexibility, but it also requires more time to enhance, manage and maintain the software. A hosted blog solution such as Blogger will be easy to set up and maintain, but has disadvantages because it is a less flexible solution. I didn’t discuss a WordPress-hosted solution because I’m not very familiar with this type of setup, however, I believe the WordPress-hosted solution limits the use of plugins and themes.

For our ecommerce clients, installing a self-hosted WordPress instance on top of their Spree or [Interchange](/technology/perl-interchange) ecommerce site has been relatively simple. For another one of our clients, we developed a [Radiant](http://radiantcms.org/) plugin to integrate Blogger article links into their site, which has worked well to fit their needs.
