---
title: "Building a search suggestions feature with Node.js and Vue"
author: Greg Davidson
tags:
- nodejs
- vue
- javascript
- development
date: 2021-11-27
github_issue_number: 1804
---

![Old Dog](/blog/2021/11/search-suggestions-with-node-and-vue/banner.jpg)
[Photo](https://unsplash.com/photos/L1jHI4ThA44) by [Kasper Rasmussen](https://unsplash.com/@kaspercph) on Unsplash

### The backstory

Some time ago, I worked on a project to improve the usability of a search component for our clients. Similar to Google and other search interfaces, the user was presented with a number of suggested search terms as they typed into the search box. We wanted to add keyboard support and give the component a visual facelift. When the customer used the up, down, <kbd>Esc</kbd>, or <kbd>Enter</kbd> or <kbd>Return</kbd> keys, the component would allow them to choose a particular search term, clear their search, or navigate to the results for their chosen search term.

This is what the new and improved UI looked like:
![Search interface with suggested search terms](/blog/2021/11/search-suggestions-with-node-and-vue/search-suggestions-ui.jpg)

As developers, it can sometimes feel like we're stuck when working on older, well established projects. We gaze longingly at newer and shinier tools. Part of my objective while building this feature was to prove the viability of a newer approach (Node.js and Vue) to the other engineers on the project as well as the client.

The feature existed already but we wanted to improve the UX and performance. Having added several Vue-powered features to this site in the past, I was very comfortable with the idea and have written about that [previously](/blog/2017/12/enhancing-your-sites-with-vue/). It would also be very easy to roll back if needed since this project was limited in scope, and very easy to compare the new solution with the code it replaced.

### Picking a route and configuring it

This project was running on [Interchange](https://www.interchangecommerce.org/i/dev), nginx, and MySQL, but our approach would work in other stacks (e.g. with Apache). One key concept is that we're using nginx as a reverse proxy to route requests to our various apps, serve static files, etc. Using nginx in this way allows us to stitch together the different services for a given project. In this case I created an endpoint for the search suggestions endpoint in our nginx config file. This enabled requests made to `/suggestions/` to be passed along to our Node.js app. You can read more about [reverse proxying with nginx](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) if you like.

```nginx
# Node.js powered endpoint for search suggestions
location /suggestions/ {
    proxy_pass http://0.0.0.0:8741/;
}
```

If your project is running on Apache or another platform there will likely be a similar configuration option to route the requests to your Node.js app as I did.

### Node.js time

I wrote a little app with the [MySQL driver for Node.js](https://www.npmjs.com/package/mysql) and [Express](https://expressjs.com/). The app connects to MySQL and uses the nifty built-in connection pooling. It accepts POST requests from the site and responds with an array of search suggestion objects in JSON format.

### Enter Vue

For the front-end part of the feature I created Vue components for the search input and for the display of the results. As the customer types, results are fetched and displayed. Using the arrow keys navigates up and down and <kbd>Esc</kbd> clears out the search. Once the customer has the search they want they can either press <kbd>Enter</kbd> or click on the Search button.

It's worth mentioning that this search feature works without JavaScript. When you enter a search term and press <kbd>Enter</kbd> or click the Search button, you will get results. However, if you do have JavaScript enabled (and if our suggestions app is up and running) you'll get suggestions as you type. This is a good thing.

### Performance wins

The new endpoint returns results in less than 100ms — a 3x or 4x improvement over the Perl script it replaced. We get a response faster, meaning the experience is much more smooth for the user!

### Managing the Node.js process

We used [pm2](https://pm2.keymetrics.io/docs/usage/pm2-doc-single-page/) and [systemd](https://systemd.io/) to manage the Node.js processes and ensure they are started up when the server is rebooted. In my experience this has been very stable and has not required any babysitting by our operations folks.

### Great success!

Have you done anything similar in your projects? Do you have vintage/​legacy app that could benefit from learning some new tricks? Let us know!
