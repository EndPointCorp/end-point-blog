---
author: Seth Jensen
title: Converting to Hugo
date: 2021-08-23
tags:
- company
- design
- html
---

![A view of Manhattan from the Empire State Building](/blog/2021/08/converting-to-hugo/manhattan-view.jpg)

<!--Photo by Seth Jensen-->

We recently converted the End Point website from [Middleman](https://middlemanapp.com/) to [Hugo](https://gohugo.io). I’ll go into more detail shortly, but the general result has been *much* better build times with less configuration and better support for local development.

### Background

In 2017 we converted this website from a Rails app to a static site. With tons of high-quality static site generator options, we could implement the shiny features used by our [rails site in 2009](/blog/2009/10/new-end-point-site-rails-jquery-flot/) with less overhead and quicker load times.

We also wanted to move away from Blogger to [self-hosting](/blog/2017/11/using-github-for-blog-comments/) our blog. We ended up switching to Middleman, a static site generator written in Ruby, and had a mostly positive experience. Ruby was a good fit switching from Rails, and (if I remember correctly) Middleman had pretty competitive performance.

With over 1000 blog posts at the time, as well as lots of other pages, our site was quite slow to build—3.5 minutes when building with the full blog.

Middleman had a nice development server, but due to some server-side rewrites, we couldn't use it. Instead, we got around the build times by writing a simple Ruby script to generate an HTML preview, letting our blog authors see what their post would look like, more or less. This worked okay, but was not 100% accurate and made copy-editing and formatting slower than it needed to be for us "Keepers of the Blog".

We started hiding most of the blog from Middleman while building to save time, but build times were still 40 seconds or more. With our patience for long build times waning, as well as Middleman losing most of its support, we decided to get in the market for a new site generator.

### Shopping around

Before we (🚨 spoiler alert 🚨) settled on Hugo, we tried using [Zola](https://www.getzola.org/), a site generator written in Rust and boasting tiny build times. Zola is a small project, and would have worked fairly well, but it had several downsides.

- Initial build times were very promising, but slowed down more than expected after adding our 1500+ blog posts. We still ended up with very respectable build times; less than 15 seconds.
- As far as I could tell, Zola would have required an `_index.md` file in every section and subsection, to hold section settings or to make it a transparent section, passing its files to the parent section. I didn't like the sound of having a couple hundred extra markdown files for every blog year and month.
- At the time of writing, Zola doesn't support custom taxonomy paths. That means we would have our blog tags at `www.endpoint.com/tags/`, instead of our existing (and preferred) `www.endpoint.com/blog/tags/`. This has been [discussed](https://zola.discourse.group/t/custom-path-for-taxonomy-pages/82) on Zola forums, but seems to have stalled. This wasn't a complete dealbreaker, but it was disappointing.

### Making the switch to Hugo

We wanted to see if there was another option which solved our issues with Zola. I decided to try Hugo. It's written in Go and is one of the most popular static site generators.

I partially converted the site and blog, and found that Hugo solved our main concerns with Zola:

- Build times were close to twice as fast as Zola.
- You can dump as many subdirectories as you want in each section, and they'll still belong to the section but retain the original directory structure.
- Hugo supports custom taxonomy paths through its [permalinks](https://gohugo.io/content-management/urls/).

> We were also able to shave off a lot of build time by analyzing our [template metrics](https://gohugo.io/troubleshooting/build-performance/)—this is one of my favorite features in Hugo.

#### Local development

So far, we've had extremely smooth local development. Hugo (like Zola) requires only a single executable, so it's extremely easy to get started or update. This was a huge improvement from Middleman, which required a heap of Ruby gems and plugins. Now every blog author can easily clone our repo, run the development server, and edit their post directly, with the full site building in anywhere from ~10 seconds all the way down to ~2 seconds, depending on the author's machine.

For blog authors, we were using a fork of an abandoned Middleman plugin. With Hugo, we're using their taxonomies, which have been fairly easy to set up. We were also able to use Hugo's built-in Chroma highlighter, instead of loading highlight.js on every blog page.

#### Some drawbacks

We're loving the wonderfully fast build times and easy local development. I like the templating fairly well, and the simple configuration is wonderful. But Hugo does have several issues and missing features I'd like to see.

One place Zola wins over Hugo is the ability to easily print the [entire context](https://www.getzola.org/documentation/templates/overview/) in a big JSON object. It's a bit hard to navigate, but in my experience much easier and clearer than Hugo, where I have to either try using `printf` to display the context's variables, or search through the documentation. This was one of my favorite ways to quickly debug and learn about the inner workings of Zola, and would be very welcome in Hugo as well, without needing to know Go formatting [width](https://pkg.go.dev/fmt) and the full shape of Hugo's context object beforehand.

Documentation is another area where Hugo struggles sometimes. Pages often don't feel interconnected and examples are often lacking. Here's a few examples I encountered in the docs:

* The Hugo Pipes page [SASS/​SCSS](https://gohugo.io/hugo-pipes/scss-sass/) shows how to transform Sass files to CSS, but did not link to the very useful [Page Resources](https://gohugo.io/hugo-pipes/scss-sass/) page. It turned out I just needed to link to `{{ $style.RelPermalink }}`, but as a new user it wasn't clear that the CSS file was considered a `Resource`. Having more links to related pages or more examples could save a lot of headaches for newbies.
* [Lookup Order](https://gohugo.io/templates/lookup-order/#hugo-layouts-lookup-rules) says under the `Layout` section that it "can be set in page front matter," but I had to look under [Front Matter](https://gohugo.io/content-management/front-matter/) to see that `layout` is the key name. A small change, and didn't take long to experiment and find out, but especially since YAML is case sensitive, having a link to the actual front matter key would be better.
* Enabling custom outputs on a per-taxonomy basis does not seem to be possible. We want to generate Atom feeds for our blog tags, but not for our blog authors, both of which are taxonomies. As far as I can tell, we have to enable them both and live with the cruft of unnecessary blog author feeds.

### Onward and upward!

It may look (mostly) the same, but on our end it's never been easier to write blog posts or update the website, thanks to Hugo and all its contributors!

