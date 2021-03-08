---
title: "Jamstack Conf Virtual 2020: Thoughts & Highlights"
author: Greg Davidson
tags: jamstack, html, css, javascript, conference, development
gh_issue_number: 1639
---

![Conference](/blog/2020/06/16/jamstack-conf-virtual-may-2020/conference.jpg)

### Welcome to Jamstack Conf Virtual 2020

Last week I attended [Jamstack Conf Virtual 2020](https://jamstackconf.com/2020/may/). It had originally been slated to take place in London, UK but was later transformed into a virtual event in light of the COVID-19 pandemic. The conference began at 2pm London time (thankfully I double-checked this the night before!)—​6am for those of us in the Pacific Time Zone.

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Up early for <a href="https://twitter.com/hashtag/jamstackconf?src=hash&amp;ref_src=twsrc%5Etfw">#jamstackconf</a> 😎☕️ <a href="https://t.co/ydjvrHWCZH">pic.twitter.com/ydjvrHWCZH</a></p>— Greg Davidson (@syncopated) <a href="https://twitter.com/syncopated/status/1265637434638778368?ref_src=twsrc%5Etfw">May 27, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Before getting too much further I wanted to mention that if you are not familiar with the Jamstack, You can read more about it at [jamstack.org](https://jamstack.org/).

To virtually participate in the conference we used an app called [Hopin](https://hopin.com/). I had not heard of it before but was impressed with how well it worked. There were over 3000 attendees from 130+ countries one of the times I checked. [Phil Hawksworth](https://www.hawksworx.com/) was the Host/​MC for the event and did a great job. There were virtual spaces for the stage, sessions, expo (vendors), and networking. If you opted to, the networking feature paired you with a random attendee for a video chat. I’m not sure what I expected going into it but I thought it was fun. I met a fellow developer from the Dominican Republic. The experience was very similar though more serendipitous than the hallway track or lunch line at an in-person conference.

![Phil Hawksworth welcoming the attendees](/blog/2020/06/16/jamstack-conf-virtual-may-2020/phil-welcome.png)

### Keynote

[Matt Biilmann](https://twitter.com/biilmann) opened the conference with a keynote address about the challenges we face as a developer community trying to improve access to accurate, timely and locally relevant information to a global audience. Many billions of users with all kinds of devices and varying levels of connectivity. He moved on to share how Netlify is trying to enable developers to “build websites instead of infrastructure” and “ensure all the best practices become common practices” through features like git-based deployments, build plugins, and edge handlers (more on those later).

### State of the Jamstack Survey results

![Laurie Voss reporting findings from the Jamstack Survey 2020](/blog/2020/06/16/jamstack-conf-virtual-may-2020/laurie-voss-talk.png)

[Laurie Voss](https://seldo.com/) [walked us through](https://slides.com/seldo/jamstack-survey-2020#/) the results of the [Jamstack Survey 2020](https://www.netlify.com/blog/2020/05/27/state-of-the-jamstack-survey-2020-first-results/). There were some interesting findings and surprises. Later on I read [Laurie’s post](https://seldo.com/posts/you-will-never-be-a-full-stack-developer/) (which Matt had mentioned in his talk) and found that very interesting as well.

### Fireside chat with Harper Reed

![Frances Berriman interviewed Harper Reed - fireside chat style](/blog/2020/06/16/jamstack-conf-virtual-may-2020/harper-phae-talk.png)

[Frances Berriman](https://fberriman.com/) chatted with [Harper Reed](https://harperreed.com/) and asked him about his application of Jamstack principles from years ago when he led the technology team for Barack Obama’s election campaign. He described the need to “get far with very limited resources” and spoke about experimenting with serving HTML from Google App Engine and Amazon S3. Using pre-built HTML allowed them to scale very efficiently and he opted to use message queues rather than interacting with the database to keep things very quick for users.

Another benefit Harper noted was how quickly and easily new team members could be onboarded. Folks who knew HTML, CSS and JavaScript would be up to speed and productive in no time. He admitted it’s more complicated today 😀. Speed is another benefit—he just loves when he comes across a super-fast web site (often mostly static).

### Lightning Launch: Netlify ⚡

[David Calavera](https://twitter.com/calavera) gave a demo of Netlify’s new Edge Handlers feature which lets developers add logic to their code at the edge (e.g. the CDN servers geographically closest to the user). He demonstrated how Edge Handlers make it possible to examine the headers of the request to tailor the response to that unique request. Check out the [video of his talk](https://www.youtube.com/watch?v=D44n8YVb5iI) to watch him live code an example. I believe [Cloudflare Workers](https://workers.cloudflare.com/) and Fastly’s [Edge Compute](https://www.fastly.com/products/edge-compute/serverless) are operating in a similar problem space. I plan to look into each of these offerings more thoroughly in future.

### Lightning Launch: Prismic ⚡

[Renaud Bressand](https://twitter.com/RenaudBressand) from Prismic demoed [Slicemachine](https://www.slicemachine.dev/)—​a new feature from Prismic which lets you combine [nuxt](https://nuxtjs.org/)/​Vue components with content managed in Prismic. It looked like a very compelling way of enabling better collaboration between developers and content creators.

### Lightning Launch: RedwoodJS ⚡

[Tom Preston-Werner](https://tom.preston-werner.com/) demoed his latest project [RedwoodJS](https://redwoodjs.com/). I had heard Tom speak about this on a few podcasts recently and it was nice to see him demo it for us. It looks interesting and feels reminiscent of [Rails](https://rubyonrails.org/). RedwoodJS simplifies wiring up your database to a [GraphQL](https://graphql.org/) API (they use [Prisma](https://www.prisma.io/) for this) and integrating it into a React application. Tom is also the creator of [Jekyll](https://jekyllrb.com/)—​a Jamstack-style tool which has been around for many years. It was nice to see several speakers give him some recognition for his work on that project.

### The COVID Tracking Project: 0 to 2M API requests in 3 months

![Erin Kissane presenting The COVID Tracking Project](/blog/2020/06/16/jamstack-conf-virtual-may-2020/kissane.png)

[Erin Kissane](http://incisive.nu/) gave an inspiring talk about her work on [The COVID Tracking Project](https://covidtracking.com). She described it as an “interim public data rescue project”. Erin and some friends, journalists and volunteers worked together to create the site. They started by scraping COVID data from each state’s web site and storing it in a Google Sheet. They used [Gatsby](https://www.gatsbyjs.com/), [Contentful](https://www.contentful.com/), and [Sass modules](https://css-tricks.com/introducing-sass-modules/) and hosted the site on Netlify. Using the Jamstack approach allowed the site to remain performant and continue to be responsive under some huge traffic spikes. Over time, they iterated on the design and continue to improve the site daily. I highly recommend checking out the [video of the talk](https://www.youtube.com/watch?v=ryngYoHXNfQ) when you get a chance.

### Jamstack for emerging markets

[Christian Nwamba](https://www.codebeast.dev/) described some of the challenges of building sites for users in Nigeria (low power devices, spotty connectivity, unreliable power). He shared that 55% of the most visited sites in Nigeria are global companies (Google, Facebook/​Instagram, Netflix, Stack Overflow etc.). Christian reviewed a large, popular banking site in Nigeria and noted its many shortcomings.

To demonstrate how the bank might do better he built [an app](https://proud-flower-060c1e01e.azurestaticapps.net/) for transferring money between friends &amp; family built in the Jamstack style and using serverless functions. The most interesting thing I picked up from this was his method of using serverless functions to protect the app secrets (API keys, etc.). The front end of the application did not need to concern itself with this—​the serverless functions kept the secrets safe and acted as a proxy between the frontend and the backend APIs. Be sure to take a look at [Christian’s code](https://github.com/christiannwamba/quickbank) if you are interested.

### Managing diabetes with Jamstack

[Jamie Bradley](https://jamiebradley.dev/) taught us about diabetes and the Jamstack app he built to help himself and others manage it. He built [HeySugar](https://heysugar.health/) with Gatsby and Sanity, hosted it on Netlify. He’s making it easier for others to deploy their own instances as well.

### Selling tickets without servers. Or frameworks. Or cookies.

[Jan van Hellemond](https://jvhellemond.nl/) has volunteered for years at a very popular conference in Europe ([Fronteers](https://fronteers.nl/congres) I think). In previous years tickets sold out in 6 minutes one year, and 30 seconds in another! Their ticket vendor was struggling to handle to the load and this caused them to oversell early bird tickets. Jan built a Jamstack site to sell their tickets and was very pleased with the performance. He used simple, single-purpose vanilla JavaScript components and simple, single-purpose API handlers (serverless functions).

![Jan presenting his Jamstack ticket selling app](/blog/2020/06/16/jamstack-conf-virtual-may-2020/tickets.png)

Jan prerendered as much as possible and seeded a relational database with the tickets available for sale. As the tickets were sold, they were marked sold with a database update. Webhooks were used as customers stepped through the checkout flow. Jan joked about deploying to production on a Friday afternoon because of how safe and simple the deployment process was. There were no services to restart, etc. because “it’s just files”. It was cool to see a practical example and that Jan used the basic building blocks of the web (HTML, JavaScript, CSS, old school links) successfully without reaching for a large JavaScript framework.

### The business side of the Jamstack

[Ana Rossetto](https://twitter.com/_anarossetto_) shared how her company has been having great success with the Jamstack. Previously, the agency had been building projects for clients with Drupal. She walked through a project she and the team built to encourage people to buy from small, locally-owned businesses. She was impressed with what they were able to create in a very short amount of time.

### Build plugin authors’ session

After the main talks there were several sessions. In the Hopin app, I was able to peek into some of these and the presenters and attendees were chatting (both text chat and video). This was very much like the experience of peeking into conference rooms at a physical venue and choosing whether to stay and participate or move on. After some wandering I chose to attend a session with three Netlify build plugin authors.

![Peter telling us about subfont](/blog/2020/06/16/jamstack-conf-virtual-may-2020/subfont.png)

[Peter Müller](https://mntr.dk/) built [Subfont](https://github.com/Munter/netlify-plugin-subfont) with a friend. He demonstrated how subsetting web fonts (i.e. only loading the characters &amp; glyphs you really need) can dramatically improve frontend performance. He compared the [WebPageTest](https://webpagetest.org/) results for Google Fonts with and without Subfont and Subfont was seconds faster! I have subset and locally hosted webfonts in several client projects here at End Point. It takes time and is a manual process. Peter’s plugin makes this excellent performance improvement relatively painless.

[David Darnes](https://darn.es/) demoed his build plugin to [turn Ghost content into Markdown files](https://github.com/daviddarnes/netlify-plugin-ghost-markdown). Very interesting and it seemed flexible enough to work with other tools as well.

[Gleb Bahmutov](https://twitter.com/bahmutov) presented the build plugin he created to run [Cypress](https://www.cypress.io/) tests as part of your Netlify build process. It was amazing to see how simple it was (single devDependency and single line in the netlify.toml config file).

### Videos from the conference

Netlify has already put all of the [Jamstack Conf Virtual 2020 talks](https://www.youtube.com/playlist?list=PL58Wk5g77lF8jzqp_1cViDf-WilJsAvqT) on YouTube so head over there and check those out if you’d like to. Thanks very much to the team at Netlify for organizing the conf, all of the speakers, vendors and attendees!
