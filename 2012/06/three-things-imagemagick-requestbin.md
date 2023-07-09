---
author: Steph Skardal
title: 'Three Things: ImageMagick, RequestBin, Responsivness'
github_issue_number: 662
tags:
- browsers
- mobile
date: 2012-06-28
---

It’s been a while since I wrote a **Three Things** blog article, where I share tidbits that I’ve learned that don’t quite make it into a full blog post, but are still worth sharing!

### Image Stacking via Command Line

I recently needed to stack several images to CSS spritify them. I did some quick searching and found the following ImageMagick command line functionality:

```
convert add.png add_ro.png -append test.png
convert add.png add_ro.png +append test.png
```

The -append argument will stack the images vertically, and +append will stack the images horizontally.

### RequestBin

Recently, I needed to quickly examine the contents sent during a payment transaction. [Richard](/team/richard-templet/) pointed me to [RequestBin](https://github.com/Runscope/requestbin) a neat and quick tool for examining the contents of an external request. I was testing the Elavon payment gateway integrated in an application using [Piggybak](https://github.com/piggybak/piggybak). In my code, I made the following change:

```ruby
class ElavonGateway < ViaklixGateway
  self.test_url = 'https://demo.myvirtualmerchant.com/VirtualMerchantDemo/process.do'
  self.live_url = 'https://www.myvirtualmerchant.com/VirtualMerchant/process.do'
+ self.test_url = 'http://requestb.in/abc1def2'
```

I ran through a single checkout, then visited the RequestBin inspect URL to examine the variables passed to the payment gateway, to see the following data (the text overwrites itself in Chrome):

<img border="0" height="400" src="/blog/2012/06/three-things-imagemagick-requestbin/image-0.png" width="372"/><br>
[RequestBin](https://github.com/Runscope/requestbin) example output.

### A Responsiveness Tool

I’ve been working on responsiveness for a couple of sites recently. One of my clients pointed out [responsivepx](http://responsivepx.com/), which allows you to toggle the width of your browser to review various responsive layouts.
