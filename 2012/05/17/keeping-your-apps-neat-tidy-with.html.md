---
author: Greg Davidson
gh_issue_number: 616
tags: css, javascript, jquery, open-source, tools
title: Keeping Your Apps Neat &amp; Tidy With RequireJS
---



[RequireJS](http://requirejs.org/) is a very handy tool for loading files and modules in JavaScript. A short time ago I used it to add a feature to [Whiskey Militia](http://www.whiskeymilitia.com/) that promoted a new section of the site. By developing the feature as a RequireJS module, I was able to keep all of its JavaScript, HTML and CSS files neatly organized. Another benefit to this approach was the ability to turn the new feature "on" or "off" on the site by editing a single line of code. In this post I'll run through a similar example to demonstrate how you could use RequireJS to improve your next project.

## File Structure

The following is the file structure I used for this project:
```nohighlight
├── index.html
└── scripts
    ├── main.js
    ├── my
    │   ├── module.js
    │   ├── styles.css
    │   └── template.html
    ├── require-jquery.js
    ├── requirejs.mustache.js
    └── text.js
```

The dependencies included RequireJS bundled together with [jQuery](http://jquery.com/), [mustache.js](https://github.com/janl/mustache.js/) for templates and the RequireJS [text plugin](http://requirejs.org/docs/download.html#text) to include my HTML template file.

## Configuration

RequireJS is included in the page with a script tag and the data-main attribute is used to specify additional files to load. In this case "scripts/main" tells RequireJS to load the main.js file that resides in the scripts directory. Require will load the specified files asynchronously. This is what index.html looks like:

```nohighlight
&lt;!DOCTYPE html&gt;<br/>&lt;html&gt;<br/>&lt;head&gt;<br/>    &lt;title&gt;RequireJS Example&lt;/title&gt;<br/>&lt;/head&gt;<br/>&lt;body&gt;<br/>    &lt;h1&gt;RequireJS Example&lt;/h1&gt;<br/>    &lt;!-- This is a special version of jQuery with RequireJS built-in --&gt;<br/>    &lt;script data-main="scripts/main" src="scripts/require-jquery.js"&gt;&lt;/script&gt;<br/>&lt;/body&gt;<br/>&lt;/html&gt;<br/>
```

I was a little skeptical of this approach working on older versions of Internet Explorer so I tested it quickly with IE6 and confirmed that it did indeed work just fine.

## Creating a Module

With this in place, we can create our module. The module definition begins with an array of dependencies:

```js
define([
  "require",
  "jquery",
  "requirejs.mustache",
  "text!my/template.html"
  ],
```

This module depends on require, jQuery, mustache, and our mustache template. Next is the function declaration where our module's code will live. The arguments specified allow us to map variable names to the dependencies listed earlier:

```js
  function(require, $, mustache, html) { ... }
```

In this case we're mapping the $ to jQuery, mustache to requirejs.mustache and, html to our template file.

Inside the module we're using Require's .toUrl() function to grab a URL for our stylesheet. While it is possible to load CSS files asynchronously just like the other dependencies, there are some issues that arise that [are specific to CSS files](http://requirejs.org/docs/faq-advanced.html#css). For our purposes it will be safer to just add a <link> element to the document like so:

```js
  var cssUrl = require.toUrl("./styles.css");
  $('head').append($('<link/>',
    { rel: "stylesheet", media: "all", type: "text/css", href: cssUrl }));
```

Next, we define a view with some data for our Mustache template and render it.

```js
  var view = {
    products: [
      { name: "Apples", price: 1.29, unit: 'lb' },
      { name: "Oranges", price: 1.49, unit: 'lb'},
      { name: "Kiwis", price: 0.33, unit: 'each' }
    ],
    soldByPound: function(){
      return (this['unit'] === 'lb') ? true : false;
    },
    soldByEach: function() {
      return (this['unit'] === 'each') ? true : false;
    }
  }

  // render the Mustache template
  var output = mustache.render(html, view);

  // append to the HTML document
  $('body').append(output);
});
```

## The Template

I really like this approach because it allows me to keep my HTML, CSS and JavaScript separate and also lets me write my templates in HTML instead of long, messy JavaScript strings. This is what our template looks like:

```nohighlight
&lt;ul class="hot-products"&gt;<br/>  {{#products}}<br/>  &lt;li class="product"&gt;<br/>    {{name}}: ${{price}} {{#soldByEach}}each{{/soldByEach}}{{#soldByPound}}per lb{{/soldByPound}}<br/>  &lt;/li&gt;<br/>  {{/products}}<br/>&lt;/ul&gt;<br/>
```

## Including the Module

To include our new module in the page, we simply add it to our main.js file:

```js
require(["jquery", "my/module"], function($, module) {
    // jQuery and my/module have been loaded.
    $(function() {

    });
});
```

When we view our page, we see that the template was was rendered and appended to the document:

<img alt="Require rendered" border="0" height="370" src="/blog/2012/05/17/keeping-your-apps-neat-tidy-with/image-0.png" title="require-rendered.png" width="600"/>

## Optimizing Your Code With The r.js Optimizer

One disadvantage of keeping everything separate and using modules in this way is that it adds to the number of HTTP requests on the page. We can combat this by using the the [RequireJS Optimizer](http://requirejs.org/docs/optimization.html). The r.js script can be used a part of a build process and runs on both [node.js](http://nodejs.org/) and [Rhino](http://www.mozilla.org/rhino/). The Optimizer script can minify some or all of your dependencies with [UglifyJS](https://github.com/mishoo/UglifyJS) or Google's [Closure Compiler](http://code.google.com/closure/compiler/) and will concatenate everything into a single JavaScript file to improve performance. By following the documentation I was able to create a simple build script for my project and build the project with the following command:

```nohighlight
node ../../r.js -o app.build.js
```

This executes the app.build.js script with Node. We can compare the development and built versions of the project with the Network tab in Chrome's excellent [Developer Tools](https://developers.google.com/chrome-developer-tools/docs/overview).

Development Version:

<img alt="Webapp devel" border="0" height="357" src="/blog/2012/05/17/keeping-your-apps-neat-tidy-with/image-1.png" title="webapp-devel.png" width="600"/>

Optimized with the RequireJS r.js optmizer:

<img alt="Webapp built" border="0" height="356" src="/blog/2012/05/17/keeping-your-apps-neat-tidy-with/image-2.png" title="webapp-built.png" width="600"/>

It's great to be able to go from 8 HTTP requests and 360 KB in development mode to 4 HTTP requests and ~118 KB after by running a simple command with Node! I hope this post has been helpful and that you'll check out RequireJS on your next project.

 


