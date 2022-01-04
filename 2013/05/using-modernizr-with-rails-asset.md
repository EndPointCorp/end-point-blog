---
author: Mike Farmer
title: Using Modernizr with the Rails Asset Pipeline
github_issue_number: 796
tags:
- javascript
- rails
date: 2013-05-08
---

Like many web developers, I use [Google Chrome](https://www.google.com/intl/en/chrome/) to develop my front-end user interface. I do this because the [Chrome Developer Tools](https://developer.chrome.com/devtools) are very nice at letting me fix CSS styles and debug JavaScript. One downfall to using Google Chrome as my only view of my website while developing, however, is that I often find that I’ve used some feature of HTML or CSS that isn’t supported by other browsers. While this problem seems to come less often these days, I still find the occasional glitch. Most notably, this seems to happen with Microsoft’s Internet Explorer (IE) more than any other browser.

During a recent project, I finished up the UI so that everything looked and felt great. Then I popped open IE to see what sort of things I would need to fix. One feature of HTML that I didn’t know wasn’t supported by IE was that of placeholder text for form inputs. For example:

```html
<input type="text" name="user_name" placeholder="Enter your user name" />
```

This HTML generates a nice looking input box with the words “Enter your user name” already entered into the input field. When a user clicks on the field, the placeholder text disappears so that the user can begin to add their custom text. This is a popular solution for many web-sites so I was shocked to learn that IE up to version 10 doesn’t support this feature. My mind turned to horrid thoughts of writing custom javascript to handle placeholder text in input fields. It didn’t take long for me to think, surely someone has to have already fixed this.

Thankfully, someone had.

I found [placeholders.js](https://github.com/jamesallardice/Placeholders.js) on GitHub. It was a clean solution and it solved my problem by just adding it to my application. Since I’m using Rails 3.2, I just added the Placeholders.js file to the vendor/assets/javascript directory and then added it to the bottom of my app/assets/javascript/application.js manifest file like so:

```javascript
//= require Placeholders.js
```

Boom, suddenly all my placeholders were working flawlessly. But I was a little irritated with this solution. Why should all my non-IE users have to load this javascript file? And if I have more issues, there could be many of these little javascript solutions I need for things like gradients and rounded borders. And what about custom CSS that I had to write just for these features to work? Surely there must be a better way.

Enter [Modernizr](https://modernizr.com/).

From Modernizr’s web site, “Modernizr is a JavaScript library that detects HTML5 and CSS3 features in the user’s browser.” In short, Modernizer detects if certain features are available and then gives you a way to load custom assets to deal with those features, or the lack thereof. It introduced to me the concept of [polyfills](https://en.wikipedia.org/wiki/Polyfill). A polyfill is simply some code that helps you deal with browser incompatibilities. The nice JavaScript Placeholders.js file mentioned earlier is a polyfill.

Modernizr does two things to help you detect these compatibilities and deal with them. First, it adds some custom classes to your <html> tag that indicate what features are enabled and disabled in your browser. A <html> tag in IE might look something like this:

```html
<html class="js no-borderradius no-cssgradients">
```

While in Chrome it would look like this:

```html
<html class="js borderradius cssgradients">
```

This enables you to put together some CSS code to add extra styles for incompatible browsers. For example, some SASS to deal with a css gradient issues may look like this:

```css
.no-cssgradients gradient {
  background-image: blue url('assets/ie_gradients/blue_gradient.png') no-repeat;
}
```

This would then load a custom gradient image rather than using the CSS gradient for incompatible browsers.

The second thing Modernizr does for you is let you custom load assets based on compatibility. It does this using the [yepnope.js](http://yepnopejs.com/) library. You simply load your polyfills based on what compatibility is detected. This is exactly what I needed for my Placeholders.js file. I only wanted it to load for browsers that didn’t support the placehoder input attribute. I found a great [blog article on how to implement the Placeholders.js library using Modernizr](https://www.techrepublic.com/blog/australia/using-placeholder-text-in-html5-forms-across-all-browsers/1353) and started following the directions. [And here there be dragons](https://en.wikipedia.org/wiki/Here_be_dragons).

YepNope.js is essentially an assets loader. You load assets in Modernizr using the Modernizer.load function that wraps the YepNope functionality; like this:

```javascript
Modernizr.load({
  test: Modernizr.input.placeholder,
  nope: ['Placeholder.js'],
  complete: function(){Placeholders.init();}
});
```

Well, that doesn’t quite sit well with the other asset loader in my app, the Rails asset pipeline. So, to cut to the chase, here’s how you get the two to play nicely with each other.

First, place the Modernizr library (modernizr.js in this case) in the vendor/assets/javascript directory.

Second, place the following line at the top of your asset pipeline manifest js file (such as app/assets/javascripts/application.js):

```javascript
//= require modernizr
```

Third, DO NOT, put your polyfill in the asset pipeline manifest. If you do, it will load for all browsers thus defeating the whole point. I moved my Placeholders.js file from the vendor directory to the app/assets/javascripts/polyfills directory and made sure that I wasn’t loading this director in my manifest with a require_tree directive.

Fourth, add the following line to your config/application.rb if you want the polyfill to be compiled like the rest of your assets:

```ruby
config.assets.precompile += ['polyfills/Placeholders.js']
```

Fifth, you are now ready to use Modernizr to load your polyfill. I did so in my JavaScript app using CoffeeScript like so:

```javascript
# Polyfills
Modernizr.load
  test: Modernizr.input.placeholder
  nope: ['/assets/polyfills/Placeholders.js']
  complete: -> Placeholders.enable() if Placeholders?
```

Now my Placeholders.js library only loads when the browser doesn’t support input placeholders. Hooray! 

Note: One thing that tripped me up a little is that you can either use the development Modernizr library or you can [build your own](https://modernizr.com/download/) with just the functionality you want to detect. This corresponds directly to the test line in the load function options. Make sure if you build your own modernizr.js file that you include all the features you test. In my case, I had to include the “Input Attributes” option.
