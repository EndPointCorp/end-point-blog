---
title: "Comparison of Lightweight CSS Frameworks"
author: Seth Jensen
tags:
- css
- design
date: 2022-01-13
github_issue_number: 1825
---

![The frame of a house in front of a mountain range](/blog/2022/01/comparison-of-lightweight-css-frameworks/house-frame.jpg)

<!-- Photo by Seth Jensen -->

Several months ago I was building a new website and needed a CSS framework. There are many new CSS frameworks around now, so I decided to do several small trial runs and compare them to find the most fitting for our site.

Initially I tried using Foundation, which this site is built on, but I ran into a problem: Foundation and other popular frameworks are powerful, but they have more features than I needed, and they take up too much disk space for a modest website. Foundation is about 6000 lines long and 200kB unminified. It can be shrunk by removing components you don't need, but the time it takes to slim a large CSS framework down to your needs can be more than it's worth, especially if you want to change any styling.

Instead of adapting a larger framework to my needs, I looked into lightweight CSS frameworks. These aim to provide boilerplate components, better styling for buttons, forms, tables, and the like, all at the cost of very little disk space.

I like to modify the source CSS as needed, so all of the sizes I list will be unzipped and unminified. They are also from my brief real-world testing on one machine, so your mileage may vary.

### Bulma

Bulma looked very attractive at first. It has sleek, modern design and is quite popular, with a good-sized community for support. But for our site, it was still too big. I only used a few components and layout helpers, a fraction of its 260kB — around 50kB bigger than Foundation, in my tests!

### mini.css

mini.css had some great things going for it, but got pushed out by even smaller options which I'll cover shortly. It took up about 46kB with all the bells and whistles.

The use of flex is a bonus, but it's a little too style agnostic for the website I was working on; I would have overridden a lot of its styling, making the overhead size even larger.

It has options for using SCSS or CSS variables, which I always like to see. I prefer SCSS's added features and variables, but if you would rather use vanilla CSS, mini.css has a plain option using CSS variables, which I don't see too often.

### Pure.css

Pure.css offers similar features to the other frameworks on this list, and weighing in at around 17kB, it competes well in size. However, I wasn't a big fan of its look, and with some odd omissions, notably, the absence of a `container` class for horizontally centering content, it was edged out by the competition.

### Skeleton

Skeleton has very clean styling and a good selection of minimal components. It's tiny, weighing in at 12kB. Unfortunately, it hasn't had a release since 2014, and uses `float` instead of Flexbox, which took it out of the running for building a more modern site.

### Milligram

Milligram feels like a spiritual successor to Skeleton: It covers a similar scope, and has a simple, clean design reminiscent of Skeleton's. In lieu of using classes, it usually applies styling directly to HTML tags. This is a choice I like, since I don't follow the Tailwind CSS approach of creating websites purely in HTML, with agnostic classes applied to the layout.

It also has an SCSS offering, so it's easy to drop components you don't want, making it even tinier!

The size and simplicity of Milligram made it win the bid. It has worked quite well, providing just enough framework to be useful for small websites, but getting out of the way so that you can do your own styling.

### Making the most of your lightweight framework

Hopefully this post will give you an idea of what each of these frameworks is like, but the best way to test them is by trying them yourself! These five were fairly quick to spin up and test out on the website I was working on, and doing the same will give you the best idea of what your website needs.

With frameworks that are only a few kilobytes, you can also read through the entire source. I tried to look through enough of each framework's CSS files to become familiar with its way of doing things. This eased the whole website-building process, and will help you find a framework that matches your style of web development.

Also see my colleague Afif's article [Building responsive websites with Tailwind CSS](/blog/2021/12/responsive-website-with-tailwindcss/) for an in-depth look at Tailwind CSS.
