---
author: Greg Davidson
title: CSSConf US 2014 — Part One
github_issue_number: 988
tags:
- browsers
- conference
- css
- design
- html
date: 2014-05-28
---

### Geeks in Paradise

<img alt="IMG 2414" border="0" height="450" src="/blog/2014/05/cssconf-us-2014-part-one/image-0.jpeg" title="IMG_2414.jpg" width="600"/>

Today I was very lucky to once again attend [CSSConf US](https://2014.cssconf.com/) here in [Amelia Island, Florida](https://goo.gl/maps/uuQMK). [Nicole Sullivan](http://www.stubbornella.org/content/) and crew did an excellent job of organizing and curating a wide range of talks specifically geared toward CSS developers. Although I work daily on many aspects of the web stack, I feel like I’m one of the (seemingly) rare few who actually enjoy writing CSS so it was a real treat to spend the day with many like-minded folks.

### Styleguide Driven Development

Nicole Sullivan started things off with her talk on Style Guide Driven Development (SGDD). She talked about the process and challenges she and the team at [Pivotal Labs](https://pivotal.io/labs) went through when they redesigned the [Cloud Foundry Developer Console](https://docs.cloudfoundry.org/devguide/) and how they overcame many of them with the SGDD approach. The idea behind SGDD is to catalog all of the reusable components used in a web project so developers use what’s already there rather than reinventing the wheel for each new feature. The components are displayed in the style guide next to examples of the view code and CSS which makes up each component. The benefits of this approach include enabling a short feedback loop for project managers and designers and encouraging developers who may not be CSS experts to follow the “blessed” path to build components that are consistent and cohesive with the design. In Nicole’s project they were also able to significantly reduce the amount of unused CSS and layouts once they had broken down the app into reusable components.

[Hologram](http://trulia.github.io/hologram/) is an interesting tool to help with the creation of style guides which Nicole shared and is definitely worth checking out.

### Sara Soueidan — Styling and Animating Scalable Vector Graphics with CSS

[Sara](http://sarasoueidan.com/) talked to us about using [SVG](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics) with CSS and included some really neat demos. Adobe Illustrator, [Inkscape](https://inkscape.org/en/) and [Sketch 3](https://bohemiancoding.com/sketch/) are the commonly used tools used to create SVG images. Once you have your SVG image you can use the [SVG Editor](https://web.archive.org/web/20150218125407/http://petercollingridge.appspot.com/svg-editor) by Peter Collingridge or [SVGO](https://github.com/svg/svgo) (node.js based tool) to clean up and optimize the SVG code. After the cleanup and optimization you can replace the generic CSS class names from your SVG creation app with more semantic CSS class names.

There are a variety of ways to include SVG on a page and Sara went over the pros and cons of each. The method that seemed most interesting to me was to use an <object> tag which allowed for a fallback image for browsers that do not support SVG. Sara mapped out the subset of CSS selectors which can be used to target SVG elements, how to “responsify” SVGs and to animate SVG paths. Be sure to check out [her slides](https://docs.google.com/presentation/d/1Iuvf3saPCJepVJBDNNDSmSsA0_rwtRYehSmmSSLYFVQ/present#slide=id.p) from the talk.

### Lea Verou — The Chroma Zone: Engineering Color on the Web

Lea’s talk was about color on the web. She detailed the history of how color has been handled up to this point, how it works today and some of the interesting color-related CSS features which are coming in the future. She demonstrated how each of the color spaces have a geographical representation (e.g. RGB can be represented as a cube and HSL as a double-cone) which I found neat. RGB is very unintuitive when it comes to choosing colors. HSL is much more intuitive but has some challenges of its own. The new and shiny CSS color features Lea talked about included:

- filters
- blending modes
- CSS variables
- gray()
- color() including tint, shade and other adjusters
- the #rgba and #rrggbbaa notation
- hwb()
- named hues and <angle> in hsl()

Some of these new features can be used already via libs like [Bourbon](https://www.bourbon.io/) and [Myth](http://www.myth.io/). Check out the [Chroma Zone: Engineering Color on the Web](http://leaverou.github.io/chroma-zone/) slides to learn more.

### C$$

I will write up more of the talks soon but wanted to thank [Jenn Schiffer](https://web.archive.org/web/20140207090237/http://madeby.jennschiffer.com/) for keeping us all laughing throughout the day in her role as MC and topping it off with a hilarious, satirical talk of her own. Thanks also to [Alex](https://alexsexton.com/) and [Adam](http://ajpiano.com/) for curating the music and looking after the sound.
