---
author: Evan Tann
title: Preventing Global Variables in JavaScript
github_issue_number: 526
tags:
- javascript
date: 2011-12-15
---

JavaScript’s biggest problem is its dependence on global variables
―Douglas Crockford, *JavaScript: The Good Parts*

Recently I built out support for affiliate management into LocateExpress.com’s Sinatra app using JavaScript and YUI.

<a href="/blog/2011/12/preventing-global-variables-in/image-0-big.png"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5686373444992788658" src="/blog/2011/12/preventing-global-variables-in/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 320px; height: 318px;"/></a>

I used a working page from the admin, Service Providers, as a starting point to get something up and running for affiliates quickly. By the time I finished, the Affiliates page worked great, but forms on the Service Provider page no longer populated with data.

### **Identifying a misbehaving global variable**

There were no errors in the console, and the forms on the Service Providers page remained broken even after restoring an old copy of service_providers.js. As it turns out, a global variable, edit_map, was defined within service_providers.js, and again in the copied affiliates.js. Credit for spotting the problem goes to Brian Miller.

The fix was as simple as moving edit_map’s declaration into the file’s YUI sandbox, so that version of edit_map wouldn’t be visible to any other pages in the admin.

### **Preventing global variables**

As projects grow and complexity increases, it becomes easier and easier to overlook global variables and thus run into this tough-to-debug problem. Douglas Crockford’s Javascript: The Good Parts covers several workarounds to using global variables.

Rather than declaring variables globally, like this:

```javascript
var edit_map = { 'business[name]' : 'business_name' };
```

the author recommends declaring them at the beginning of functions whenever possible:

```javascript
YUI().use("node", "io", "json",
function(Y) {
    var edit_map = { 'business[name]' : 'business_name' };
    ...
});
```

In all other cases, he suggests using Global Abatement, which prevents your global variables from affecting other libraries. For example,

```javascript
var LocateExpress = {};
LocateExpress.edit_map = { 'business[name]' : 'business_name' };

YUI().use("node", "io", "json",
function(Y) {
    ...
    return LocateExpress.edit_map;
});
```

<a href="https://www.amazon.com/JavaScript-Good-Parts-Douglas-Crockford/dp/0596517742"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5686371099560345650" src="/blog/2011/12/preventing-global-variables-in/image-1.gif" style="float:left; margin:0 10px 10px 0;cursor:pointer; cursor:hand;width: 180px; height: 236px;"/></a>

I highly recommend [JavaScript: The Good Parts](https://www.amazon.com/JavaScript-Good-Parts-Douglas-Crockford/dp/0596517742) to learn about the best JavaScript has to offer and workarounds for its ugly side. The author also wrote a very popular code-checker, JSLint, which could help debug this nasty problem by highlighting implicit global variables.
