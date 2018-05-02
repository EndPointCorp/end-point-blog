---
author: Steph Skardal
gh_issue_number: 936
tags: javascript, ruby, rails
title: JavaScript Namespacing with the Rails Asset Pipeline
---



Since the release of Rails 3 [a while back], I’ve had a lot of use with the [asset pipeline](http://guides.rubyonrails.org/asset_pipeline.html). There can be minor headaches associated with it, but ultimately, the process of combining, minifying, and serving a single gzipped JavaScript and CSS file is a great gain in terms of reducing requests to speed up your web application. It’s a behavior that I’ve wanted to emulate in other platforms that I’ve used (including [Interchange](http://www.icdevgroup.org/i/dev)).

One headache that might come up from the asset pipeline is that JavaScript functions from various parts of the application might have the same name, and may override existing functions of the same name. The last defined function will be the one that executes. I’ve come up with a common pattern to avoid this headache, described below:

### Set the Body ID

First, I set the body tag in my application layout file to be related to the controller and action parameters. Here’s what it looks like:

```nohighlight
<body id="<%= "#{params[:controller].gsub(/\//, '_')}_#{params[:action]}" %>">
...
</body>
```

If I was less lazy, I could create a helper method to spit out the id.

### Shared JS

I create a shared.js file, which contains JavaScript shared across the application. This has the namespace “shared”, or “app_name_global”, or something that indicates it’s global and shared:

```javascript
var shared = {
};
```

### Namespace JavaScript

Next, I namespace my JavaScript for that particular controller and action which contains JavaScript applicable only to that controller action page. I namespace it to match the body ID, such as:

```javascript
# for users edit page
var users_edit = {
...
};
# for product_show page
var products_show = {
...
};
```

### Add initialize method:

Next, I add an initialize method to each namespace, which contains the various listeners applicable to that page only:

```javascript
# for users edit page
var users_edit = {
    intialize: function() {
        //listeners, onclicks, etc.
    }, 
    ...
};
# for product_show page
var products_show = {
    intialize: function() {
        //listeners, onclicks, etc.
    }, 
    ...
};
```

### Shared initialize method

Finally, I add a method to check for the initialize method applicable to the current page and execute that, in the shared namespace:

```javascript
var shared = {
    run_page_initialize: function() {
        var body_id = $('body').attr('id');
        if(eval(body_id + '.initialize') !== undefined) {
            eval(body_id + '.initialize()');
        }
    }  
};
$(function() {
    shared.run_page_initializer();
});
```

### Dealing with shared code across multiple actions

In some cases, code might apply to multiple parts of the application and no one wants to repeat that code! I’ve set up a single namespace for one of the controller actions, and then defined another namespace (or variable) pointing to that first one in this case, shown below.

```javascript
# for users edit page
var users_edit = {
    intialize: function() {
        //listeners, onclicks, etc.
    }, 
    ...
};

# reuse users_edit code for users_show
var users_show = users_edit;
```

### Conclusion

It’s pretty simple, but it’s a nice little pattern that has helped me be consistent in my organization and namespacing and makes for less code repetition in executing the initialized methods per individual page types. Perhaps there are a few more techniques in the Rails space intended to accomplish a similar goal—I’d like to hear about them in the comments!


