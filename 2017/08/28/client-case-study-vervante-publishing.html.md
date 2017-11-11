---
author: Greg Hanson
gh_issue_number: 1322
tags: case-study, clients, ecommerce, interchange
title: 'Client Case Study: Vervante - Publishing, Production and Fulfillment Services'
---

  

## A real-life scenario

The following is a real-life example of services we have provided for one of our clients.  

[Vervante Corporation](https://store.vervante.com/c/affil/index.html) provides a print on demand and order fulfillment service for thousands of customers, in their case, "Authors". Vervante needed a way for these authors to keep track of their products. Essentially they needed an [Inventory management system](https://en.wikipedia.org/wiki/Inventory_management_software). So we designed a complete system from the ground up that allows Vervante's authors many custom functions that simply are not offered in a pre-built package anywhere. 

This is also a good time to mention that **you should always view your web presence, in fact your business itself, as a process**, not a one time "setup". Your products will change, your customers will change, the web will change, **everything** will change. **If you want your business to be successful, you will change.** 

## Some Specifics

While it is beyond the scope of this case study to describe all of the programs that were developed for Vervante, it will be valuable for the reader to sample just a few of the areas to understand how diverse a single business can be. Here are a few of the functions we have built from scratch, over several years to continue to provide Vervante, their authors, and even their vendors with efficient processes to achieve their daily business needs. 

## Requirements

1. Author Requirement -  First, in some cases, the best approach to a problem is to use someone else's solution! Vervante's authors have large data files that are converted to a product, and then shipped on demand as the orders come in. So we initially provided a custom file transfer process so that customers could directly upload their files to a server we set up for Vervante. Soon Vervante's rapid growth outpaced the efficacy of this system, so we investigated and determined the most efficient and cost-effective approach was to incorporate a 3rd party service. So we recommended a well known file transfer service and wrote a program to communicate with the file transfer service API. Now a client can easily describe and upload large files to Vervante. 

<div class="separator" style="clear: both; text-align: center;"><object class="BLOG_video_class" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,40,0" height="266" id="BLOG_video-f735687e5d91b6e5" width="320"><param name="movie" value="https://www.youtube.com/get_player"/>
<param name="bgcolor" value="#FFFFFF"/>
<param name="allowfullscreen" value="true"/>
<param name="flashvars" value="flvurl=https://redirector.googlevideo.com/videoplayback?requiressl%3Dyes%26id%3Df735687e5d91b6e5%26itag%3D5%26source%3Dblogger%26app%3Dblogger%26cmo%3Dsecure_transport%253Dyes%26cmo%3Dsensitive_content%253Dyes%26ip%3D0.0.0.0%26ipbits%3D0%26expire%3D1508990116%26sparams%3Drequiressl,id,itag,source,ip,ipbits,expire%26signature%3D99FD6C851283A8BC063EB63455AA30622B1A8437.3D4F2FF3F744A46AD71889580CB2708476EA61F4%26key%3Dck2&iurl=https://video.google.com/ThumbnailServer2?app%3Dblogger%26contentid%3Df735687e5d91b6e5%26offsetms%3D5000%26itag%3Dw160%26sigh%3DIi_vgaZOeZV9xdyNjeqlp9MvQPM&autoplay=0&ps=blogger"/>
<embed allowfullscreen="true" bgcolor="#FFFFFF" flashvars="flvurl=https://redirector.googlevideo.com/videoplayback?requiressl%3Dyes%26id%3Df735687e5d91b6e5%26itag%3D5%26source%3Dblogger%26app%3Dblogger%26cmo%3Dsecure_transport%253Dyes%26cmo%3Dsensitive_content%253Dyes%26ip%3D0.0.0.0%26ipbits%3D0%26expire%3D1508990116%26sparams%3Drequiressl,id,itag,source,ip,ipbits,expire%26signature%3D99FD6C851283A8BC063EB63455AA30622B1A8437.3D4F2FF3F744A46AD71889580CB2708476EA61F4%26key%3Dck2&iurl=https://video.google.com/ThumbnailServer2?app%3Dblogger%26contentid%3Df735687e5d91b6e5%26offsetms%3D5000%26itag%3Dw160%26sigh%3DIi_vgaZOeZV9xdyNjeqlp9MvQPM&autoplay=0&ps=blogger" height="266" src="https://www.youtube.com/get_player" type="application/x-shockwave-flash" width="320"/></object>
</div>

[View File Save Process](https://drive.google.com/file/d/0B_fTO4RaXomtd3REUWR3U1hERmM/view) 
1. Storage Requirement -  The remote storage of these large files caused Vervante a dramatic inefficiency as relates to access times, as they worked daily on these files to format, organize, and create product masters. So we needed to provide Vervante with a local server to act as a file server that was on their local network (LAN), where it could be rapidly accessed and manipulated. This was a challenge, as Vervante did not have IT personnel on site. So we purchased an appropriate server, set up everything in our offices, and shipped the complete server to them! They plugged the server into their local network, and with a long phone call, we had the server up and running and remotely managed.

1. Author Requirement -  On the website, the authors first wanted to see what they had in inventory. Some customers provided Vervante with some product components that needed to be included with a complete product, while others relied on Vervante to build all components of their products. They also requested a way to set minimum inventory stock requirements.

So we built an interface that would allow authors to:

(a) See their current stock levels for all products,

(b) View outstanding orders for these items,

(c) Set minimum inventory levels that they would like to have maintained at the fulfillment warehouse.

<div class="separator" style="clear: both; text-align: center;margin-top:20px;"><a href="/blog/2017/08/28/client-case-study-vervante-publishing/image-0-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="441" data-original-width="1211" height="233" src="/blog/2017/08/28/client-case-study-vervante-publishing/image-0.png" width="640"/></a></div>

For example a finished product may consist of a book, a CD, and a DVD. A customer may supply the CD and require Vervante to produce the book and the DVD "on demand" for the product. We created a system that tracked all items at a "base" item level, and then allowed Vervante to "build" products with as many of these "base" items as necessary, to create the final product. The base items could be combined to create an item, and two or more items could be combined to produce yet another item. It is a recursive item inventory system, built from scratch specifically for Vervante. 

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2017/08/28/client-case-study-vervante-publishing/image-1.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="437" data-original-width="1227" src="/blog/2017/08/28/client-case-study-vervante-publishing/image-1.png"/></a></div>

1. Vervante Vendor (fulfillment warehouse) Requirement -  Additionally, the *fulfillment warehouse* that receives, stores, builds and ships end user products, needed access to this system. They had several needs including:

        - Retrieving pending orders for shipment
        - Creating packing / pick slips for the orders
        - Create shipping labels for orders
        - Manage returns
        - Input customer supplied inventory
        - Input fulfillment created inventory

In our administrative user interface for the fulfillment house, we developed a series of customer specific processes to address the above needs. Here is a high level example of how a few of the items on the list above are achieved: 

        - The fulfillment house logs into the user admin first thing in the morning, and prints the outstanding orders.
        - The "orders" are formatted similar to a packing slip, and each slip has all line items of the order, and a bar code imprinted on the slip.
        - This document is used as a "pick" slip, and is placed in a "pick" basket. The user then goes through the warehouse, gathers the appropriate items, and when complete the order is placed on a feed belt to the shipper location.
        - When the basket lands in front of the shipper, that person checks the contents of the basket against the slip, and then uses a bar code scanner to scan the order. That scan triggers a query into our system that returns all applicable shipping data into an Endicia or UPS system. 
        - A shipping label is created, and the shipping cost and tracking information is returned to the our system.
        - Additionally the inventory is decremented accordingly when the order receives a shipping label and tracking number.

1. Requirements: administrative / accounting -   Vervante also needed an administrative / accounting arm, designed to control all of the accounting functions such as:

        - Recording customers' fulfillment charges
        - Recording customers' sales (Vervante sells product for the customers as well as fulfilling outside orders)
        - Determining fulfillment vendor fees and payments
        - Tracking shipping costs
        - Monthly billing of all customers
        - Monthly payments for all customers.
        - Interface with in-house accounting systems and keeping systems in sync
        - Tracking and posting outside order transactions

The above described processes are just a few of the processes that we developed from scratch, and matched to Vervante's needs. It is also a tiny portion of their system. 

## Last, but not least

Oh, and one other interesting fact: When Vervante first came to us several years ago, they had fewer than 20 customers. Today, they provide order fulfillment and print on demand services for nearly 4000 customers. So when we say to plan ahead for growth, we have experience in that area. 


