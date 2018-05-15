---
author: Greg Davidson
gh_issue_number: 811
tags: conference, css, design, graphics, html, javascript, open-source, testing, tips, tools
title: "CSS Conf 2013 — When Bootstrap Attacks!"
---

<img alt="Cssconf 2013" border="0" height="234" src="/blog/2013/06/03/css-conf-2013-when-bootstrap-attacks/image-0.png" style="display:block; margin-left:auto; margin-right:auto;" title="cssconf-2013.png" width="373"/>

I attended the inaugural [CSS Conf](https://web.archive.org/web/20130629170825/http://cssconf.com/speakers.html) last week at Amelia Island, Florida. The conference was organized by [Nicole Sullivan](http://www.stubbornella.org/), [Brett Stimmerman](http://brett.stimmerman.com/), [Jonathan Snook](https://snook.ca/), and [Paul Irish](https://www.paulirish.com/) and put on with help from a host of volunteers. The talks were presented in a single track style on a wide range of CSS-related topics; there was something interesting for everyone working in this space. I really enjoyed the conference, learned lots and had great discussions with a variety of people hacking on interesting things with CSS. In the coming days I will be blogging about some of the talks I attended and sharing what I learned, so stay tuned!

### When Bootstrap Attacks

[Pamela Fox](http://www.pamelafox.org/) had the opening slot and spoke about the experiences and challenges she faced when upgrading [Bootstrap](https://getbootstrap.com/2.3.2/) to V2 in a large web app ([Coursera](https://www.coursera.org/)). What she initially thought would be a quick project turned into a month-long “BOOTSTRAPV2ATHON”. Bootstrap styles were used throughout the project in dozens of PHP, CSS and JavaScript files. The fact that Bootstrap uses generic CSS class names like “alert”, “btn”, error etc made it very difficult to grep through the codebase for them. The Bootstrap classes were also used as hooks by the project’s JavaScript application code.


### Lessons Learned

Fox offered some tips for developers facing a similar situation. The first of which was to prefix the Bootstrap CSS classes (e.g. .tbs-alert) in order to decouple Bootstrap from the customizations in your project. Some requests have been made to the Bootstrap team on this front but the issue has not been addressed yet. In the meantime, devs can add a task to their build step (e.g. [Grunt](https://gruntjs.com/), the asset pipeline in Rails etc) to automate the addition of prefixes to each of the CSS classes.

Another tip is to avoid using Bootstrap CSS classes directly. Instead, use the “extend” functionality in your preprocessor (Sass, Less, Stylus etc) of choice. For example:

```
  .ep-btn {
    @extend .btn
      &:hover {
          @extend .btn:hover
      }
  }
```

This way your project can extend the Bootstrap styles but keep your customizations separate and not closely coupled to the framework.

The same logic should also be applied to the JavaScript in your project. Rather than using the Bootstrap class names as hooks in your JavaScript code, use a prefix (e.g. js-btn) or use HTML5 data attributes. Separating the hooks used for CSS styles from those used in JavaScript is very helpful when upgrading or swapping out a client-side framework like Bootstrap.

### Test All Of The Things

Pamela wrapped up the talk by explaining how testing front end code would ease the pain of upgrading a library next time. There are many testing libraries available today which address some of these concerns. She mentioned [mocha](https://mochajs.org/), [Chai](http://www.chaijs.com/), [jsdom](https://github.com/jsdom/jsdom) and [Selenium](https://docs.seleniumhq.org/) which all look very helpful. In addition to testing front end code she offered up the idea of “diffing your front end” in a visual way. This concept was very interesting to someone who ensures designs are consistent across a wide array of browsers and devices on a daily basis.
<img alt="Diff your front end" border="0" height="341" src="/blog/2013/06/03/css-conf-2013-when-bootstrap-attacks/image-1.png" style="display:block; margin-left:auto; margin-right:auto;" title="diff-your-front-end.png" width="559"/>

[Needle](https://github.com/python-needle/needle) is a tool which allows you to do this *automatically*. Once you develop a test case, you can run Needle to view a visual diff of your CSS changes. I think this is an excellent idea. Pamela also noted that the combination of [Firefox screenshots](https://support.mozilla.org/en-US/questions/940991) and [Kaleidoscope](https://www.kaleidoscopeapp.com/) could be used manually in much the same way.

Many thanks to [Pamela](https://twitter.com/pamelafox) for sharing this! The slides for this talk can be viewed [here](http://slides.com/pamelafox/when-bootstrap-attacks#/) and the talk was recorded so the video will also be available sometime soon.
