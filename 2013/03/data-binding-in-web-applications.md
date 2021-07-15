---
author: Kamil Ciemniewski
title: Data binding in web applications
github_issue_number: 766
tags:
- javascript
- jquery
- open-source
- user-interface
date: 2013-03-06
---

Ever since JavaScript was introduced the world of web programming has constantly been visited by creative minds, ready to solve burning problems web developers were experiencing.

Navigating through some of the oldest web-dev articles, we still can feel the pain of manipulating the DOM, the-vanilla-way and creating ever so clever hacks to make the code work on all of the web browsers.

Then, the JS-frameworks epidemy started to disseminate. As web developers—​we started to have some powerful tools. The productivity of average nerdy Joe raised immediately as he started using Prototype.js, Mootools or jQuery.

### Evolution of UI programming for browsers

And so was the start of our global evolution, towards making the Web—​our main means of interacting with *users*. Few with big enough imagination were already seeing HTML, CSS & JS as the future standard of creating user interfaces for data-rich applications. Of course, there were toolkits like ExtJS which aimed at nothing but this—​but who would have known back then, that we will be able to build apps for **smartphones** the way we are building ones for the web?

I have my little observation in life — all *hot stuff* in the world of technology, has their *phases*. That is:

- they don’t exist, but the problems they solve do and they are **painful**
- they show up, and there is massive excitement
- people discover new pains brought on by these solutions
- next pain and the beginning of the “next big thing”

At the beginning it was painful to write all the *vanilla* JS code without shooting yourself in your own foot (well let’s just say it—​JS is Pandora’s Box of pain). Then you realize you’ve got your sweet & cool jQuery with which you can rapidly impress your boss/clients/friends.

Your next surprise is that jQuery isn’t enough—​ever wondered why frameworks like Backbone.js were created?

### Data binding

Here is the challenge for you: write GMail web interface clone using **just** jQuery. Here is the spoiler: you’d get lost in managing your app’s *state*—​and syncing UI to reflect it. In fact—​even small *todo* app in vanilla jQuery could end up being quite complicated. That’s just not the way other folks are dealing with UI programming. A long time ago they were—​but they got smarter. We can learn from their mistakes.

When I was beginning my journey into the world of professional programming, I was given a job of creating small business app with C# and Windows Forms. Despite the fact that in the world of desktop apps you have to be mindful of much more things than in the web/browsers world (like updating your UI only on the main thread), the whole experience was pretty much the same as with vanilla jQuery:

1. create inputs
1. subscribe to its events
1. write the code that updates inner state based on the state of those inputs/controls

This quickly gets very cumbersome as the needs grows. You could have a requirement that one set of inputs is dependent on another, which results in hours of coding and more hours in debugging.

The way *smart devs* are tackling this issue is called *data binding*. This simply means that you *tell* specific portion of UI to be *bound* to some value from your business layer.

One nice example of the framework that employs data binding is Apple’s Cocoa. The XCode even has nice visual tools to bind controls values with the data model. Another example of the framework that uses data binding extensively is WPF (Windows Presentation Foundation). The concept widely used there is the MVVM pattern (Model-View-ViewModel). Which basically says that you have your *view model* object and UI which is bound to the view model and all you have to do is to manage the view model.

That’s the core concept here: **managing objects is much easier than managing UI**

### Data binding on web

As the need came with more and more amazing web apps—​we now have quite a nice choice when it comes to employing data binding:

[Angular.js](https://angularjs.org/)

Angular.js is one of the most impressive front-end JS frameworks there are. It has view templates mechanism allowing you to specify your binding statements directly there.

[Ember.js](https://emberjs.com/)

Ember.js gains popularity every day. Just like Angular.js, it has its own nice templating language (handlebars) which allows you to have your binding statements in the markup too.

[Knockout.js](http://knockoutjs.com/)

If you don’t want to use any of those frameworks, that’s a great library that implements **just** the data binding part.

It uses the concept I described before: the MVVM pattern. You are simply defining your view model and telling your UI where it has to get values from and that’s it.

[Backbone.js](http://backbonejs.org/)

But what if you’d like to use Backbone.js? It’s true that it’s amazing and is one neat piece of technology you can use to build your next ‘cool app’. There is one caveat though: you have to set up all the niceties that comes along with Angular.js or Ember.js yourself, including all the sweetness of data binding.

### Backbone.js + Knockout.js

Here is a simple way of using Knockout.js with Backbone.js:

- for every Backbone.js view, define complementary view model
- put ‘ko.applyBindings’ at the end of your ‘render’ method
- do not use any logic in your view templates—​rely solely on data binding

So for example:

**# app/views/photos.coffee**

```python
module.exports = class PhotosView extends Backbone.View
   template: require "./templates/photos/index"

   initialize: () ->
       @view = new PhotosViewModel()
       @render()

   render: () ->
       $(@el).html(@template())
       ko.applyBindings(@view, @el)

   setData: (photos) =>
       @view.photos(photos)

class PhotosViewModel
   constructor: ->
       @photos = ko.observableArray []
```

**# app/views/templates/photos/index.eco**

```html
<ul data-bind="foreach: photos">
   <li><img data-bind="attr: {src: $data.get('url')}"/></li>
</ul>
```

Now—​with this, you can manipulate the photos array however you like, and the UI will get auto-updated on its own. But this idea shines the most when it comes to implementing forms with it. Take a look at the following example:

**# app/views/company.coffee**

```python
module.exports = class EditCompanyView extends Backbone.View
   template: require "./templates/companies/edit"

   initialize: () ->
       @view = new EditCompanyViewModel()
       @render()

   render: () ->
       $(@el).html(@template())
       ko.applyBindings(@view, @el)

   setData: (company) =>
       @view.company(company)

class EditCompanyViewModel
   constructor: ->
       # let’s instantiate it with default company for bindings to work
       @company = ko.observable(new Company())
       @companyName = ko.computed
           read: => @company.get('name')
           write: (value) => @company.set('name': value)
       @companyState = ko.computed
           read: => @company.get('state')
           write: (value) => @company.set('state': value)
       @companyWebsite = ko.computed
           read: => @company.get('url')
           write: (value) => @company.set('url': value)
       @saveCompany = () =>
           @company.save()
```

**# app/views/templates/companies/edit.eco**

```html
<form data-bind="submit: saveCompany">Name:
   <input data-bind="value: companyName"/>
   State:
   <input data-bind="value: companyState"/>
   Website:
   <input data-bind="value: companyWebsite"/>

   <button type="submit">Submit</button>
</form>
```

### Other solutions

These are quite contrived examples to give you an idea of how it can be done. The beauty of Backbone is that it allows you to structure your code however you’d like. And there are plenty of other solutions for this. Most notable:

- [http://kmalakoff.github.com/knockback/](http://kmalakoff.github.com/knockback/)
- [http://rivetsjs.com/](http://rivetsjs.com/)
- [https://github.com/DreamTheater/Backbone.DataBinding](https://github.com/DreamTheater/Backbone.DataBinding)
