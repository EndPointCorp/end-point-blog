---
author: Steph Skardal
gh_issue_number: 429
tags: ecommerce, interchange
title: Product Personalization for Ecommerce on Interchange with Scene7
---

One of the more challenging yet rewarding projects [Richard Templet](/team/richard_templet) and I have worked on over the past year has been an ecommerce product personalization project with [Paper Source](http://www.paper-source.com/). I haven't blogged about it much, but wanted to write about the technical challenges of the project in addition to shamelessly self-promote (a bit).

<a href="/blog/2011/03/15/ecommerce-product-personalization/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584675341866725922" src="/blog/2011/03/15/ecommerce-product-personalization/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 291px;"/></a>

Personalize this and many other products at [Paper Source](http://www.paper-source.com/).

Paper Source runs on [Interchange](http://www.icdevgroup.org/i/dev) and relies heavily on JavaScript and jQuery on the customer-facing side of the site. The "personalization" project allows you to personalize Paper Source products like wedding invitations, holiday cards, stationery, and business cards and displays the dynamic product images with personalized user data on the fly using Adobe's [Scene7](http://www.scene7.com/). The image requests are made to an external location, so our application does not need to run Java to render these dynamic personalized product images.

### Technical Challenge #1: Complex Data Model

To say the data model is complex is a bit of an understatement. Here's a "blurry" vision of the data model for tables driving this project. The tables from this project have begun to exceed the number of Interchange core tables.

<a href="/blog/2011/03/15/ecommerce-product-personalization/image-1-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584409144732666786" src="/blog/2011/03/15/ecommerce-product-personalization/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 393px;"/></a>

A snapshot of the data model driving the personalization project functionality.

To give you an idea of what business needs the data model attempts to meet, here are just a few snapshots and corresponding explanations:

<table cellpadding="10" cellspacing="0" width="100%">
<tbody><tr style="background-color:#DDE4DF;">
<td><a href="/blog/2011/03/15/ecommerce-product-personalization/image-2-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584409146406906498" src="/blog/2011/03/15/ecommerce-product-personalization/image-2.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 177px;"/></a></td>
<td>At the highest level, there are individual products that can be personalized.</td>
</tr>
<tr>
<td><a href="/blog/2011/03/15/ecommerce-product-personalization/image-3-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584409146577494946" src="/blog/2011/03/15/ecommerce-product-personalization/image-3.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 329px; height: 400px;"/></a></td>
<td>Each product may or may not have different color options, or what we refer to as colorways. The card shown here has several options: gravel, moss, peacock, night, chocolate, and black. Clicking on each colorway here will update the image on the fly.</td>
</tr>
<tr style="background-color:#DDE4DF;">
<td><a href="/blog/2011/03/15/ecommerce-product-personalization/image-4-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584409157309960914" src="/blog/2011/03/15/ecommerce-product-personalization/image-4.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 44px;"/></a></td>
<td>In addition to colorways, each product will have corresponding paper types and print methods. For example, each product may be printed on white or cream paper and each product may have a "digital printing" option or a letterpress option. Colorways shown above apply differently to digital printing and letterpress options. For example, letterpress colorways are typically a subset of digital printing colorways.</td>
</tr>
<tr>
<td><a href="/blog/2011/03/15/ecommerce-product-personalization/image-5-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584409159508590450" src="/blog/2011/03/15/ecommerce-product-personalization/image-5.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 367px; height: 400px;"/></a>
</td>
<td>Each card has a set of input fields with corresponding fonts, sizes, and ink colors. The input fields can be input fields or text boxes. All cards have their own specific set of data to control the input fields – one card may have 4 sections with 1 text field in each section while another card may have 6 sections with 1 text field in some sections and 2 text fields in other sections. In most cases, inks are limited between card colorways. For example, black ink is only offered on the black colorway card, and blue ink is only offered on the blue colorway card.</td>
</tr>
<tr style="background-color:#DDE4DF;">
<td><a href="/blog/2011/03/15/ecommerce-product-personalization/image-6-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584409708544273634" src="/blog/2011/03/15/ecommerce-product-personalization/image-6.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 243px;"/></a></td>
<td>Each card also has a set of related items assigned to it. When users toggle between card colorways, the related item thumbnails update to match the detail option. This allows users to see an entire suite of matching cards: a pink wedding invite, RSVP, thank you, and stationery or a blue business card, matching letterhead stationery, and writing paper shown here.</td>
</tr>
<tr>
<td><a href="/blog/2011/03/15/ecommerce-product-personalization/image-7-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584412106643372322" src="/blog/2011/03/15/ecommerce-product-personalization/image-7.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 259px;"/></a>
</td>
<td>In addition to offering the parent product, envelopes are often tied to the products. In most cases, there are default envelope colors tied to products. For example, if a user selected a blue colorway product, the blue envelope would show as the default on the envelopes page.
</td>
</tr>
<tr style="background-color:#DDE4DF;">
<td>
<a href="/blog/2011/03/15/ecommerce-product-personalization/image-8-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584412113568036130" src="/blog/2011/03/15/ecommerce-product-personalization/image-8.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 291px;"/></a></td>
<td>In addition to managing personalization of the parent products, the functionality also meets the business needs to offer customization of return address printing on envelopes tied to products. For example, here is a personalized return address printing tied to my wedding invitation.</td>
</tr>
</tbody></table>

### Technical Challenge #2: Third Party Integration with Limited Documentation

There are always complexities that come up when implementing third-party service in a web application. In the case of this project, there is a fairly complex structure for image requests made to Scene7. In the case of dynamic invitations, cards, and stationery, examples of image requests include:

<table cellpadding="10" cellspacing="0" width="100%">
<tbody><tr style="background-color:#DDE4DF;">
<td><a href="/blog/2011/03/15/ecommerce-product-personalization/image-9-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584680200259449346" src="/blog/2011/03/15/ecommerce-product-personalization/image-9.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 200px; height: 200px;"/></a>
</td>
<td>https://a248.e.akamai.net/f/248/9086/10h/origin-d7.scene7.com/is/image/?layer=0&
anchor=-50,-50
&size=2000,2000&layer=1&src=is{PaperSource/A7_env_back_closed_sfwhite}&
anchor=2900,-395
&rotate=-90&op_usm=1,1,8,0&resMode=sharp&qlt=95,1&pos=100,50&size=1800,1800&
layer=3&src=fxg
{PaperSource/W136-122208301?&imageres=150}&anchor=0,0&op_usm=1,1,1,0&pos=500,315&
size=1732,1732
&effect=0&resMode=sharp&fmt=jpg</td>
</tr>
<tr>
<td><a href="/blog/2011/03/15/ecommerce-product-personalization/image-10-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584680200854096066" src="/blog/2011/03/15/ecommerce-product-personalization/image-10.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 200px; height: 200px;"/></a>
</td>
<td>https://a248.e.akamai.net/f/248/9086/10h/origin-d7.scene7.com/is/image/?layer=0&
anchor=-50,
50&size=2000,2000&layer=1&src=is{PaperSource/4bar_env_back_closed_fig}&anchor=0,0&
pos=115,375
&size=1800,1800&layer=2&src=fxg{PaperSource/4barV_white_background_key}&anchor=0,0&
rotate=-90&
pos=250,1757&size=1733,1733&layer=3&
src=fxg{PaperSource/ST57-2011579203301?&$color_fig=true&$color_black=false&$
color_chartreuse
=false&$color_espresso=false&$color_moss=false&$color_peacock=false
&$ink_0=780032
&$ink_2=780032&$ink_1=780032&imageres=150}&anchor=0,0
&op_usm=2,1,1,
0&pos=255,513&size=1721,1721&resMode=sharp&effect=0&fmt=jpg</td>
</tr>
<tr style="background-color:#DDE4DF;">
<td>
<a href="/blog/2011/03/15/ecommerce-product-personalization/image-11-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584680197021988386" src="/blog/2011/03/15/ecommerce-product-personalization/image-11.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 200px; height: 200px;"/></a>
</td>
<td>https://a248.e.akamai.net/f/248/9086/10h/origin-d7.scene7.com/is/image/?layer=0&anchor=-50,- 50&size=2000,2000&layer=1&src=is{PaperSource/4bar_env_back_closed_night}&anchor=0,0&pos =115,375&&size=1800,1800&layer=2&src=fxg{PaperSource/4bar_white_sm}  &anchor=0,0&rotate=-90&pos=250,1757&size=1733,1733&layer=3&src=fxg{PaperSource/W139-201203301?}  &anchor=0,0&op_usm=2,1,1,0&pos=255,513&size=1721,1721&resMode=sharp&effect=0&fmt=jpg</td>
</tr>
</tbody></table>

Each argument is significant to the dynamic image; background envelope color, card colorway, ink color, card positioning, envelope positioning, image quality, image format, and paper color are just a few of the factors controlled by the image arguments. And part of the challenge was dealing with the lack of documentation to build the logic to render the dynamic images.

### Conclusion

As I mentioned above, this has been a challenging and rewarding project. Paper Source has sold personalizable products for a couple of years now. They continue to move their old personalized products to use this new functionality including many stationery products moved yesterday. Below are several examples of Paper Source products that I created with the new personalized functionality.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td><a href="/blog/2011/03/15/ecommerce-product-personalization/image-12-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584416706343268178" src="/blog/2011/03/15/ecommerce-product-personalization/image-12.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 286px; height: 400px;"/></a></td>
<td><a href="/blog/2011/03/15/ecommerce-product-personalization/image-13-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584416705363612082" src="/blog/2011/03/15/ecommerce-product-personalization/image-13.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 287px; height: 400px;"/></a></td>
</tr>
<tr>
<td><a href="/blog/2011/03/15/ecommerce-product-personalization/image-14-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584416699907318978" src="/blog/2011/03/15/ecommerce-product-personalization/image-14.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 290px;"/></a></td>
<td><a href="/blog/2011/03/15/ecommerce-product-personalization/image-15-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584416695253858626" src="/blog/2011/03/15/ecommerce-product-personalization/image-15.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 291px;"/></a></td>
</tr>
<tr>
<td><a href="/blog/2011/03/15/ecommerce-product-personalization/image-16-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584416692143788562" src="/blog/2011/03/15/ecommerce-product-personalization/image-16.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 291px;"/></a></td>
<td><a href="/blog/2011/03/15/ecommerce-product-personalization/image-17-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5584417135000411794" src="/blog/2011/03/15/ecommerce-product-personalization/image-17.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 290px;"/></a></td>
</tr>
</tbody></table>
