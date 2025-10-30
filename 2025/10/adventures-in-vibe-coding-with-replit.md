---
title: "Adventures in Vibe-Coding with Replit"
description: "The bad and good of letting a highly autonomous agent code for you"
author: Seth Jensen
date: 2025-10-29
featured:
  image_url: /blog/2025/10/adventures-in-vibe-coding-with-replit
tags:
- artificial-intelligence
- end-point-ecommerce
- ecommerce
---

![A New York City intersection viewed from above, at a 40 degree angle](/blog/2025/10/adventures-in-vibe-coding-with-replit)

<!-- Photo by Seth Jensen, 2025, shot on Kodak 200 with a Nikon FE -->

A few weeks back, I tried out Replit Agent to see how viable it is as a development tool. I built two apps from scratch, which took 10–15 hours total, with a decent amount of human input along the way to clarify the agent's questions.

### Project 1: Multi-LLM code review API

The idea for the first project was to have a multi-LLM code review app, where you would pass a repository on GitHub or locally to an API, and it would run several full-repo code reviews, ranking and deduplicating them before returning a response. This setup should allow me to have a web frontend or CLI without much added complexity.

#### The prompt

```
Please build an app based on this app specification: app_spec.yaml (460 lines)
```

#### The results

After much back and forth (and about 40 agent-generated Git commits), I got this message:

```
🎉 SUCCESS! The Multi-LLM Code Review Assistant is now fully working!
```

Well, I actually got this message several times after sending just about any command to the agent. It's very excited about its own work, even when it doesn't work! In this case, the API connections were working, and testing with curl gave output, but I couldn't get it to give more than one code review tip for a large codebase — not a very effective code-review app.

I tried asking the agent to diagnose and fix this:

```
So, this seems to not be returning very many code review suggestions. If I go
look at the repos I'm putting in, there are plenty of code issues that could be
returned, especially with documentation. How can we make this system find more
issues?
```

In response, Replit's agent created a full React frontend for the API! Neat, but far from what I asked — the app still doesn't return substantial code reviews.

![](/blog/2025/10/adventures-in-vibe-coding-with-replit/code-review-unwanted-frontend.webp)

So after ~$100 of agent credits, I found that Replit was not the tool for this app — I'm now trying to build a [CrewAI](/blog/2025/10/creating-agentic-ai-apps/) app to accomplish the same thing.

### Project 2: End Point Ecommerce + Hugo site

A common theme in Replit apps we've experimented with is that it prefers to make everything a web app with a React frontend. I was curious how it'd do with a different web stack: Hugo and our recently launched [End Point Ecommerce](/expertise/end-point-ecommerce/).

This is an interesting problem for an LLM, since Hugo is widely used, but still small compared to React, Vue, and similar frameworks, and since End Point Ecommerce is well-documented but too new for any online discussion. However, it's a modern .NET ecommerce framework and the code is readable and straightforward.

#### The prompt

```
Build me a hugo website frontend to interact with end point ecommerce:
https://ecommerce.endpointdev.com/

For the UI, make a halloween-themed storefront with orange text, black and grey
backgrounds, and halloween-themed test products. Use the Ballast font for
headers, and charter for body text for now.

```

After providing this initial prompt, I followed up with these:

```
Here is the github link for end point ecommerce, which this site will connect to:
https://github.com/EndPointCorp/end-point-ecommerce

Please make the app as simple as possible, while still working

Oh, and please use this demo API to connect to for now, so you don't have to
build any backend at all, just interface with this:
https://demo.ecommerce.endpointdev.com/swagger/index.html
```

#### The results (version 1)

![](/blog/2025/10/adventures-in-vibe-coding-with-replit/site-v1.png)

It generated a nice, simple ecommerce storefront, using Hugo and End Point Ecommerce. Impressive! However, there's one red flag: if you look at the products [in the demo API](https://demo.ecommerce.endpointdev.com/) we're using, they are simple groceries — Apple, Banana, etc. So where did "Pumpkin spice treats," "Spider Web Candy," and "Ghost Marshmallows" come from?

It turns out, these are "fallback products" Replit had made when it failed to connect to the End Point Ecommerce demo API. Not great for an ecommerce site! Your users would see bogus but real-looking products when they're unable to see or buy real products (I didn't test this far, but the site may have even accepted payment info for fake products).

So I followed up:

```
Please remove the fallback products
```

#### The results (version 2)

![](/blog/2025/10/adventures-in-vibe-coding-with-replit/site-v2.png)

This looks more promising! We get an error message written by the frontend. In production we might want to display more specific messages based on the response, but for this demo, I'm happy with this way of displaying errors.

In true "vibe-coding" fashion, I asked the Replit agent to diagnose the network error:

```
There is a network error while loading products, what is the issue?
```

It responded with a couple options, the main one being assume it's a CORS issue.

```
Possible Solutions
Option 1: Server-Side Proxy (Recommended)
- Create a simple server endpoint that fetches the products
- Your frontend calls your server, your server calls the external API
- No CORS issues since server-to-server requests aren't restricted
```

I was suspicious of it being a CORS issue since everything was hosted in the Replit container, so after poking around myself, I wrote this prompt:

```
Please use the web api to sign up for an account by POSTing to the /api/User
end point and getting an API key
```

However, after reviewing the project for this post, I found that I misunderstood the issue in this prompt — no authentication is needed to GET `/api/products` on the demo API of End Point Ecommerce, the site was just disallowing this cross-origin request. Replit's agent went ahead and implemented the CORS change anyway, though it didn't correct my prompt.

After a few more folloup prompts...

```
Please use the "basePrice", "discountAmount", and "discountedPrice" keys that
are returned from the API to show the real prices of the items

Now, please fetch the images from the API as well
```

...we have a decent working Hugo site connected with the End Point Ecommerce demo API!

![](/blog/2025/10/adventures-in-vibe-coding-with-replit/site-v3.png)

#### Feature addition: cart

I wrote this prompt next, without having done my research on the backend (which made for an interesting unintentional experiment):

```
Please add a lightweight cart management system which uses localStorage, with
options to add to, remove from, or update quantity of items in the cart. Add a
simple checkout form with contact information, shipping address, and billing
address. For now, instead of payment information, just have a button which adds
a commonly used dummy credit card number.
```

There's an issue here: I specified using localStorage, which is a fine way to set up a frontend cart system, but it ignores the existing system End Point Ecommerce already supplies. I hadn't checked the documentation before making this prompt, and neither did Replit; it happily obliged and created a cart management system on the frontend. It's nice that the agent did what I asked, but if I were trying to work with the agent, without cross-referencing documentation myself, I would be disappointed.

That's the interesting part about using a non-deterministic system like AI agents: responding to one prompt, it might ignore my specific (and misguided) requests, but in another it might blindly execute the tasks it's given. By the nature of LLMs, you can't predict what you'll get.

#### Bonus: a few extra notes

A couple final notes:

* No .gitignore was generated, so the Hugo-generated `public/` folder is tracked in Git
* The agent used plain CSS, without SCSS or a framework — I'd recommend specifying the stack further in the prompt if you want an app that'll be nice to maintain. You don't want to assume the agent will make smart coding decisions on its own.

#### When I'd use Replit (and similar do-it-all AI agents)

I would use Replit for very quick-and-dirty web development, when sites which shouldn't last a long time — although I've seen too many projects originally intended to be short-lived become important for many years...

Replit handles its containerized deployments well; if I needed to share a working demo site within a few hours, Replit would be a good pick. Especially if you like React frontends, even when you might not have asked for one! But if I was dealing with customer data, orders, or my own data I cared about, I would want to be heavily involved throughout the development process.

For projects where performance and accuracy matter (read: most projects), I will be taking a more directed approach. I've had some good results using Continue or GitHub CoPilot as a coding assistant for small tasks in existing repos, rather than letting AI taking the wheel completely.
