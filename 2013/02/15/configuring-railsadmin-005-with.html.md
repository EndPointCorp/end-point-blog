---
author: Marina Lohova
gh_issue_number: 761
tags: javascript, rails
title: Configuring RailsAdmin 0.0.5 with CKeditor 3.7.2
---



If you like adventures, read on! Because recently I went trough a really tough one with RailsAdmin 0.0.5 and Ckeditor 3.7.2 in production mode. I only needed to enable the WYSIWYG editor for one of the fields in admin, yet it turned out to be a bit more than just that.

After I installed ckeditor gem, created the custom config file as described in [Ckeditor gem readme](https://github.com/galetahub/ckeditor/blob/master/README.md) and added ckeditor support to the field as suggested by [RailsAdmin configuration tutorial](https://github.com/sferik/rails_admin/wiki/Text), both frontend and backend in production mode were broken in pieces with JavaScript errors. So what did I do wrong?

### The problem with frontend

After careful investigation it turned out that ckeditor files were not loading on the frontend, but my custom ckeditor configuration file was. And because CKEDITOR was not defined anywhere, the following code in my config.js failed:

```javascript
CKEDITOR.editorConfig = function( config )
 {
   config.toolbar = 'Basic';
   config.toolbar_Basic =
   [
     ['Source', 'Bold', 'Italic', 'NumberedList', 'BulletedList', 'Link', 'Unlink']
   ];

   config.enterMode = CKEDITOR.ENTER_BR;
   config.shiftEnterMode = CKEDITOR.ENTER_BR;
   config.autoParagraph = false;
 }
```

as I was getting

```javascript
ReferenceError: CKEDITOR is not defined
```

Duh! I found a lot of complaints about [ckeditor gem production mode loading issues](https://github.com/galetahub/ckeditor/issues/87) due to the incorrect work with asset pipeline, as well as a [solution that required update to 3.7.3](https://github.com/galetahub/ckeditor/pull/191), but at this point I did not need any ckeditor on the frontend, so I decided to put a sanity check into custom config file that would be useful to have anyway. None of the README’s provided sample custom config file or considerations regarding loading order, so I had to improv on this one:

```javascript
if (typeof(CKEDITOR) != 'undefined') {
  CKEDITOR.editorConfig = function( config )
  {
   config.toolbar = 'Basic';
   config.toolbar_Basic =
   [
     ['Source', 'Bold', 'Italic', 'NumberedList', 'BulletedList', 'Link', 'Unlink']
   ];

   config.enterMode = CKEDITOR.ENTER_BR;
   config.shiftEnterMode = CKEDITOR.ENTER_BR;
   config.autoParagraph = false;
  }
}
```

All JavaScript errors were gone on the frontend and the website looked good again.

### The problem with RailsAdmin

RailsAdmin version 0.0.5 was still acting up, and none of WYSIWYG fields were rendered exposing the naked textarea boxes. At this point I could not upgrade RailsAdmin gem in the hope that the error will go away because of the regression issues, so I looked deeper into the problem. Only to find more JavaScript errors on pages.

RailsAdmin rendered Ckeditor-enhanced textareas with the following markup:

```html
<textarea cols="48" data-options="{"jspath":"/assets/ckeditor/ckeditor.js","
base_location":"/assets/ckeditor/","options":{"customConfig":"/assets/ckeditor/config.js"}}"
data-richtext="ckeditor" id="testimonial_content" name="testimonial[content]" rows="3">
```

Please, note the explicit hard-coded call to “/assets/ckeditor/config.js”. During asset precompilation Ckeditor gem would compile the source from vendor/assets/ckeditor folder into the special resource package that looked like this:

```bash
$ ls public/assets/ckeditor/
application.js
application.js.gz
application-1f3fd70816d8a061d7b04d29f1e369cd.js
application-1f3fd70816d8a061d7b04d29f1e369cd.js.gz
application-450040973e510dd5062f8431400937f4.css
application-450040973e510dd5062f8431400937f4.css.gz
application.css
application.css.gz
ckeditor-b7995683312f8b17684b09fd0b139241.pack
ckeditor.pack
filebrowser
images
plugins
skins
lang
```

and, apparently, plain ckeditor.js was just not there. In order to provide the necessary source files I had to explicitly add them to the precompile array for the production environment in config/environments/production.rb:

```ruby
config.assets.precompile += %w( ckeditor/* )
```

### Happy end

The necessary files showed up after I ran rake assets:precompile task, and the ckeditor fields rendered beautifully in admin.

It's very important to always stick to the newest version of gems possible, but in times when this option is not allowed, maybe, this article will help!


