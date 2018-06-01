---
author: Steph Skardal
gh_issue_number: 576
tags: jquery, rails, tips
title: 'Three Things: Startups, Rails news, jQuery index'
---

*I recently had a conversation with [Jon](/team/jon_jensen) about End Point blogging, microblogging, and tweeting. Many of us End Pointer’s have tips and tools that we encounter regularly that aren’t worthy of an entire blog post, but are worthy of sharing. Here’s my first attempt at sharing smaller bits of info – stay tuned to see how it works out.*

### 1. Paul Graham’s Ambitious Startup

[Here](http://paulgraham.com/ambitious.html) is an interesting recent article by Paul Graham entitled *Frighteningly Ambitious Startup Ideas*. It’s great. Read it.

### 2. Rails Vulnerability Hack

If you aren’t up to speed on things going on in the Rails world, check out [this recent commit](https://github.com/rails/rails/commit/b83965785db1eec019edf1fc272b1aa393e6dc57). A GitHub user was able to exploit Rails’ mass-assignment vulnerability to commit to the Rails core. Check out a few more related links at [A Fresh Cup’s post](https://web.archive.org/web/20120307145424/http://afreshcup.com/home/2012/3/5/double-shot-831.html) on the incident.

### 3. jQuery’s index method

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td valign="top"><p>I recently came across the <a href="https://api.jquery.com/index/">index method in jQuery</a>, and wanted to share an example of its use.</p>

<p>I’m using <a href="https://api.jqueryui.com/accordion/">jQuery UI’s accordion</a> on four categories (Period, Genre, Theme, Nationality) that have a set of options. A user can click any of the options to filter products, e.g. clicking on <i>Folk Songs</i> in the screenshot to the right would bring up products that have a Genre of <i>Folk Songs</i>. On the subsequent page load, the accordion region that includes the filtered option must be visible. Here’s what I came up with using the index method:</p>
<pre class="brush:jscript">
$(function() {
    var active = 0;
    if($('#accordion a.current').length) {
        active = $('#accordion div').index($('#accordion a.current').parent());
    }
    $('#accordion').accordion({ active: active, autoHeight: false });
});
</pre>
<p>And here’s how it breaks down:</p>
<ul>
<li>First, the default active region is set to 0.</li>
<li>Next, if an accordion link has a class of current (or a filtered option is selected), the index method is used to determine the position of that link’s parent divider among all the accordion regions.</li>
<li>The accordion UI is created, set with the active option, which contains the selected link or defaults to the first accordion region.</li>
</ul>
</td>
<td style="padding-left:10px;" valign="top"><img height="359" src="/blog/2012/03/23/three-things-startups-rails-news-jquery/image-0.png" style="border: 1px solid #999;"/><p>jQuery’s index method was used to set the active accordion region.</p></td>
</tr>
</tbody></table>
