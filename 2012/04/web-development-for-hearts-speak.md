---
author: Steph Skardal
title: Web Development for HeARTs Speak
github_issue_number: 581
tags:
- performance
- rails
- tips
- tools
date: 2012-04-04
---



<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr><td width="55%"><p>Many of my colleagues know that I’m fairly involved in animal rescue as a <a href="http://stephskardal.com/">photographer</a> and more recently as a foster. I recently became involved in <a href="https://www.heartsspeak.org/">HeARTs Speak</a>, a non-profit, volunteer-driven organization that brings together artists (photographers and more) who volunteer at animal rescue organizations.</p>
</td>
<td align="center" rowspan="3">
<p>
<img border="0" src="/blog/2012/04/web-development-for-hearts-speak/image-0.jpeg" width="250"/><br/>
Frank the Foster</p>
</td>
</tr>
<tr>
<td align="center" style="padding-left:10px;">
<a href="https://www.heartsspeak.org/" target="_blank"><img border="0" src="/blog/2012/04/web-development-for-hearts-speak/image-1.jpeg" width="300"/></a>
</td>
</tr>
<tr>
<td valign="top">
<p>I worked with them to help launch a new website with a design from <a href="https://web.archive.org/web/20111224181613/http://ensoblue.com/">Enso Blue</a>, which brings us to the point of the article. Given a choice of many platforms and tools, what tools did I use in development of a new site with the only restriction being how much time I was able to put into development and maintenance? Here’s a quick rundown the tools I used for the new website.</p>
</td>
</tr>
</tbody></table>

<table cellpadding="15" cellspacing="0" width="100%">
 <tbody><tr>
  <td style="background:#DDE4DF;" valign="top" width="50%">
   <p style="margin:0px;"><a href="https://rubyonrails.org/">Ruby on Rails</a>: Here at End Point, we develop many applications in Ruby and Ruby on Rails. It’s a platform that encourages decent code organization and efficient development. Another option that came up was PHP with WordPress. However, since the website required a custom application and voting process for joining members, I concluded that WordPress would be a bit of a hassle with this level of customization (though I’m personally a big fan of WordPress and its community).</p>
  </td>
  <td valign="top">
   <p style="margin:0px;"><a href="https://github.com/sferik/rails_admin">RailsAdmin</a>: I blog about RailsAdmin a lot because it’s become my go-to tool for providing a thorough admin interface that integrates nicely with <a href="https://github.com/plataformatec/devise">Devise</a> (user authentication) and <a href="https://github.com/ryanb/cancan">CanCan</a> (user authorization).
  </p></td>
 </tr>
 <tr>
  <td valign="top">
   <p style="margin:0px;"><a href="https://github.com/stephskardal/rails_admin_import">RailsAdminImport</a>. This is  an open source Ruby on Rails gem that I developed for an End Point client to import data, because RailsAdmin doesn’t include import functionality out of the box. By installing this gem into the HeARTs Speak application, I introduced the ability to import data from CSV easily. Read more about it <a href="/blog/2012/02/railsadmin-import-part-2">here</a>.</p>
  </td>
  <td style="background:#DDE4DF;" valign="top">
   <p style="margin:0px;"><a href="https://newrelic.com/">New Relic</a>. I installed New Relic’s free offering’s for both Rails application monitoring and server monitoring. New Relic is a very popular performance analytics and monitoring tool in the Rails space. They offer paid membership levels as well, but I am satisfied with the free basic monitoring at this point.</p>
  </td>
 </tr>
 <tr>
  <td style="background:#DDE4DF;" valign="top">
   <p style="margin:0px;"><b>Full Page Caching</b>. Known Rails pitfalls include poor performance and a demanding server load. I added full page caching to all front-end facing pages to mitigate the effects of poor performance. I recently wrote about page caching in RailsAdmin <a href="/blog/2012/03/cache-expiration-railsadmin">here</a>.</p>
  </td>
  <td valign="top">
   <p style="margin:0px;"><a href="https://www.google.com/analytics/">Google Analytics</a>. This is an obvious and popular choice. Google Analytics offers so much in the way of traffic analysis, conversion analytics, and now even real-time tracking. If you aren’t using it on your site, you should be!</p>
  </td>
 </tr>
 <tr>
  <td valign="top">
   <p style="margin:0px;"><b>UI Elements</b>. The HeARTs Speak website includes several user interface elements such as the <a href="https://developers.google.com/maps/documentation/javascript/tutorial">Google Maps API</a>, <a href="https://developers.facebook.com/docs/javascript/quickstart">Facebook integration</a>, and the popular jQuery plugin <a href="https://themeisle.com/plugins/nivo-slider/">Nivo Slider</a>.</p>
  </td>
  <td style="background:#DDE4DF;" valign="top">
   <p style="margin:0px;"><b>Apache Performance Configuration</b>. My server was already configured to include <a href="https://developer.yahoo.com/performance/rules.html">best practice performance tweaks</a>, also described by Jon <a href="/blog/2009/10/performance-optimization-of">here</a> and <a href="/blog/2010/11/speeding-up-spree-demo-site">here</a>.</p>
  </td>
 </tr>
 <tr>
  <td style="background:#DDE4DF;" valign="top">
   <p style="margin:0px;"><a href="https://www.webpagetest.org/">WebPageTest</a>. This is a nice service for examining performance of a website. Several of us End Pointers have mentioned it in blog articles before. If you aren’t using a performance analysis tool like WebPageTest or <a href="http://yslow.org/">YSlow</a>, I’d highly recommend it.</p>
  </td>
  <td valign="top">
   <p style="margin:0px;"><a href="https://getfirebug.com/">Firebug</a> and <a href="https://www.screencast-o-matic.com/">Screencast-O-Matic</a>. Firebug is always a huge part of development for me. In this project, I used Screencast-O-Matic to provide an example of what it’s like to work with Firebug to speed up the design iteration process, similar to process described <a href="/blog/2012/03/video-firebug-action">in this blog article</a>.</p>
  </td>
 </tr>
</tbody></table>


