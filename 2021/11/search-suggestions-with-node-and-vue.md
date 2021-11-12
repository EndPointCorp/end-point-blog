---
title: "Buildng a Search Suggestions Feature with Node.js and Vue"
author: Greg Davidson
tags:
  - nodejs
  - vue
  - html
  - css
  - javascript
  - development
---

![Old Dog](/blog/2021/11/search-suggestions-with-node-and-vue/banner.jpg)
[Photo](https://unsplash.com/s/photos/old-dog) [Michael](https://unsplash.com/@michael75) on [Unsplash](https://unsplash.com)

### The Backstory

Some time ago, I worked on a project to improve the usability of a search component for our clients. Similar to Google and other search interfaces, the user was presented with a number of suggested search terms as they typed into the search box. We wanted to add keyboard support and give the component a visual facelift. When the customer used the up or down, <kbd>Esc</kbd>,  
r <kbd>Enter</kbd> or <kbd>Return</kbd> keys, the component would allow them to choose a particular search term, clear their search or navigate to the results for their chosen search term.

This is what the new and improved UI looked like:
![Search interface with suggested search terms](/blog/2021/11/search-suggestions-with-node-and-vue/search-suggestions-ui.jpg)

### Teaching an Old Dog New Tricks

As developers, it can sometimes feel like we're stuck while working on older, well established projects. We gaze longingly at newer and shinier tools or greenfield projects. I wanted to write about a technique where I've had some success sneaking more modern tech safely into older codebases.

### The Feature

Part of my objective while building this feature was to validate a newer approach (using node.js and vue) idea with the other engineers on the project as well as the client. The feature existed already but we wanted to improve the UX and performance. Having added several vue-powered features to this site in the past I was very comfortable with that and [had written about that](https://www.endpoint.com/blog/2017/12/26/enhancing-your-sites-with-vue) earlier. It would be very easy to roll back if needed and this project was very limited in scope and impact. It would also be very easy to compare the new solution with the code it replaced.

### Existing Stack

In my case the project was running on Interchange but this technique could be applied on any other stack.

### Pick a Route and Configure It

This project was running on [Interchange](https://www.interchangecommerce.org/i/dev), nginx and MySQL but would work in other stacks (e.g. with Apache). One key concept is that we are using nginx as a reverse proxy to route requests to our various apps, serve static files etc. Using nginx in this way allows us to stitch together various services for a given project. In this case I created an endpoint for the search suggestions endpoint in our nginx config file. This enabled requests made to `/suggestions/` to be passed along to our node app. You can read more about [reverse proxying with nginx](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) if you like.

```nginx
# node.js powered endpoint for search suggestions
location /suggestions/ {
    proxy_pass http://0.0.0.0:8741/;
}
```

If your project is running on Apache or another platform there will likely be a similar configuration option to route the requests to your node app as I did.

### Node Time

I wrote a little app with the [mysql driver for node](https://www.npmjs.com/package/mysql) and [express](https://expressjs.com/). The app connects to MySQL and uses the nifty built-in connection pooling. It accepts POST requests from the site and responds with JSON (an array of search suggestions objects)

### Enter Vue

For the front-end piece of the feature I created vue components for the search input and for the display of the results. as the customer types results are fetched and displayed. Using the arrow keys navigate up and down, <kbd>Esc</kbd> clears out the search etc. Once the customer has the search they want they can either press <kbd>Enter</kbd> or click on the Search button.

### Progressive Enhancement

It's worth mentioning that the this search feature works without JavaScript. When You enter a search term and press <kbd>Enter</kbd> or click the Search button and you will get results. However, if you do have JavaScript enabled (and if our suggestions app is up and running) you'll get suggestions as you type. This is a good thing.

### Performance Wins

The new endpoint returns results less than 100ms &mdash; a 3 or 4x improvement over the existing perl script it replaced. We get results quicker and can show them to customers more quickly as a result!

### Managing the Node.js Process

We used [pm2](https://pm2.keymetrics.io/docs/usage/pm2-doc-single-page/) and [systemd](https://systemd.io/) to manage the node processes and ensure they are started up when the server is rebooted. In my experience this has been very stable and has not required any babysitting by our devops folks.

### Great Success

Have you done anything similar in your projects? Do you have vintage/legacy app that could benefit from learning some new tricks? Let us know!
