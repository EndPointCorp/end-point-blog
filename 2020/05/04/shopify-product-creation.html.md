---
author: "Patrick Lewis"
title: "Shopify Admin API: Importing Products in Bulk"
tags: shopify, ecommerce, ruby, rails
gh_issue_number: 1626
---

![Cash Register](/blog/2020/05/04/shopify-product-creation/banner.jpg)
[Photo](https://flic.kr/p/qJhs9) by [Chris Young](https://www.flickr.com/photos/mrvjtod/), used under [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/), cropped from original.

I recently worked on an interesting project for a store owner who was facing a daunting task: he had an inventory of hundreds of thousands of [Magic: The Gathering](https://en.wikipedia.org/wiki/Magic%3A_The_Gathering) (MTG) cards that he wanted to sell online through his Shopify store. The logistics of tracking down artwork and current market pricing for each card made it impossible to do manually.

My solution was to create a custom Rails application that retrieves inventory data from a combination of APIs and then automatically creates products for each card in Shopify. The resulting project turned what would have been a months- or years-long task into a bulk upload that only took a few hours to complete and allowed the store owner to immediately start selling his inventory online. The online store launch turned out to be even more important than initially expected due to current closures of physical stores.

### Application Requirements

The main requirements for the Rails application were:

* Retrieving product data for MTG cards by merging results from a combination of sources/APIs
* Mapping card attributes and metadata into the format expected by the Shopify Admin API for creating Product records
* Performing a bulk push of products to Shopify

There were some additional considerations like staying within rate limits for both the inventory data and Shopify APIs, but I will address those further in a follow-up post.

### Retrieving Card Artwork and Pricing

I ended up using a combination of two APIs to retrieve MTG card data: [MTGJSON](https://mtgjson.com/) for card details like the name of the card and the set it belonged to, and [Scryfall](https://scryfall.com/) for retrieving card images and current market pricing. It was relatively easy to combine the two because MTGJSON provided Scryfall IDs for all of its records, allowing me to merge results from the two APIs together.

### Working With the Shopify Admin API in Ruby

The [Shopify Admin API](https://shopify.dev/docs/admin-api) deals in terms of generic [Product](https://shopify.dev/docs/admin-api/rest/reference/products/product) records with predefined attributes like `title` and `product_type`. The official [shopify_api](https://github.com/Shopify/shopify_api) Ruby gem made it very easy to connect to my client’s Shopify store and create new products by creating `Shopify::Product` objects with a hash of attributes like so:

```ruby
  attrs = {
    images: [{ src: scryfall_card.image_uris.large }],
    options: [
      {
        name: 'Card Type'
      },
      {
        name: 'Condition'
      }
    ],
    product_type: 'MTG Singles',
    tags: card.setCode,
    title: card.name,
    variants: [
      {
        inventory_management: 'shopify',
        inventory_quantity: 1,
        option1: 'Foil',
        option2: 'Like New',
        price: scryfall_card.prices.usd_foil
      }
    ]
  }

  Shopify::Product.new(attrs).save
```

The actual production code is a bit more complicated to account for outliers like cards with multiple “faces” and cards that come in both regular and foil variants, but the example above shows the basic shape of the attributes expected by the Shopify API.

### Pushing 50,000 Products to Shopify

After I completed testing with individual products and confirmed the ability to take a specific card and turn it into a Shopify product with artwork and pricing pre-populated it was time to perform the full upload of all 50,000+ cards in the MTGJSON database. I decided to use [Sidekiq](https://sidekiq.org/) and create jobs for each card upload so that I could rate limit the workers to stay within rate limits for both the Scryfall and Shopify APIs, and also have persistence that would allow me to pause/resume the queue or retry individual failed jobs.

The Sidekiq approach to queueing up all of the card uploads worked great; I was able to use the Sidekiq dashboard to monitor the queue of 50,000 jobs as it worked its way through each card, and was able to see the Shopify products being created on the store in real time. Once the inventory was in place in Shopify the store owner was able to start updating his inventory levels and make cards available for sale via the Shopify Admin.

### Conclusion

 A custom Ruby application using the Shopify API is a powerful solution for online storefronts that need to retrieve a large number of inventory data from external sources. I was pleased with how this project turned out; it was rewarding to create a custom application that leveraged several APIs and automated a task that would have been extremely repetitive, and probably impossibly time-consuming, to do manually. It was encouraging to do my first upload of a card and see it show up on the Shopify store with artwork, pricing, and card details pre-populated.

 The development model used for this project could be applied to stores in a wide variety of markets. This project used external APIs to retrieve product information but that data source could easily be replaced with a spreadsheet, CSV file, or some other export file containing bulk information on products to be sold.
