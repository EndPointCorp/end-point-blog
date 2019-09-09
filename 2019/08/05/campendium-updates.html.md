---
title: "Campendium v2019: A Summary of Recent Updates"
author: Steph Skardal
tags: rails, solr, sunspot, react, maps, javascript, user-interface, ruby, clients
gh_issue_number: 1547
---

This year has brought a handful of exciting changes for [Campendium](https://www.campendium.com/), one of End Point’s long-time clients, by yours truly. Created by campers for campers, Campendium has thousands of listings of places to camp, from swanky RV parks to free remote destinations, vetted by a team of full-time travelers and reviewed by over 200,000 members. I thought I would take some time to summarize these recent updates.
 
### Maps and Clustering

![Campendium map clustering of campground locations](/blog/2019/08/05/campendium-updates/map-clusters.png)

Campendium uses [Mapbox](https://www.mapbox.com/) for map rendering to display campgrounds and locations throughout North America. One of the new features added this year was [clustering](https://docs.mapbox.com/mapbox-gl-js/example/cluster/) of campground locations, where campgrounds are grouped together and presented in a “cluster” with a size relative to how many campgrounds are in the cluster. 

If a user is searching for campgrounds in a broad location, they can see where campgrounds might be more densely grouped by location. Once a user zooms in zoom in a couple of clicks, the campgrounds are no longer clustered and individual campgrounds locations can be seen. While working on this update, we spent a good amount of our time tweaking and troubleshooting the optimal clustering behavior to provide the most benefit to those searching for a campground. [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/api/) works in parallel with [ReactJS](https://reactjs.org/), and runs with a Ruby on Rails back-end.

![Campendium map non-clustering of campground locations after zooming in](/blog/2019/08/05/campendium-updates/map-non-clusters.jpg)

### Advanced Filtering

![Campendium advanced filtering](/blog/2019/08/05/campendium-updates/map-filtering.jpg)

Another exciting was the introduction of advanced filtering in the search interface, presented in combination with map display. Users can filter campgrounds by category (e.g. Public Land, RV Parking, Parking, Dump Station), filter by price (with a slider), hookups, campground policy (e.g. age or pet restrictions), discounts, recreation, and facilities. All of this search filtering is driven by [Sunspot](https://github.com/sunspot/sunspot), a Ruby on Rails gem for working with the popular [Solr](https://lucene.apache.org/solr/) search engine. Results can be sorted by user provided reviews, price or distance from a specific GPS location. Here, much care was given to provide the best user interface for presenting this valuable functionality.


### “Supporters Only” Features

![Campendium Supporters only, Subscriptions](/blog/2019/08/05/campendium-updates/supporters.jpg)

Another recent update to Campendium includes functionality to offer user subscriptions. Registered users can sign up to support Campendium on a monthly or annual basis, and subscriptions are set to auto-renew at the end of their subscription period. This paid support hides advertisements throughout the site (advertisements are controlled by a third party), and advanced filtering on cell reception. There are plans to expand supporter features in the future. Ruby on Rails combined with [StripeJS](https://stripe.com/docs/stripe-js/reference) is used to manage subscription payments, and Ruby on Rails also serves as a backend for [In-App Purchases](https://developer.apple.com/in-app-purchase/) of subscriptions from the App store. 

### Always Responsive and Latency-Aware

Because a large portion of the Campendium visitors are on the road, it’s important to have both a responsive design and to build for bandwidth limitations for users. Throughout the development of these new features, responsive and mobile friendly designs were implemented leveraging [Sass](https://sass-lang.com/), sometimes requiring help from the rest of the knowledgeable [End Point team](/team)!

Many of the pages throughout the site are fully cached including the homepage, search result pages, and campground detail page, and cookies are used to indicate user status. In some cases, user submitted campground images are lazy-loaded to mitigate bandwidth limitations.

![Mobile, responsive design for Campendium](/blog/2019/08/05/campendium-updates/mobile.jpg)

### What’s Next?

While I didn’t go into much technical depth on these updates, I am happy that the updates represent a broad spectrum of full-stack development skills featuring nginx, Ruby on Rails, 3rd party integration including StripeJS, MapboxGL and IAP (Apple), a JavaScript framework with ReactJS, and working with Ruby gems to leverage other tools, for example, Solr (Sunspot) and Sass.

In the future, Campendium plans to continue using these tools to see a more interactive, social campground detail page, and has plans to expand outside of North America. You can visit Campendium [here](https://www.campendium.com/), or find them on Instagram [here](https://www.instagram.com/campendium/?hl=en) to follow their exciting announcements! 
