---
author: Phin Jensen
gh_issue_number: 1170
tags: company, conference, remote-work, clients
title: "End Point’s 20th anniversary meeting"
---

End Point held a company-wide meeting at our New York City headquarters for two days on October 1 and 2. We had an excellent two days of presentations, discussions, and socializing with each other.

In addition to our main Manhattan office we have an office in Tennessee, and many of us work throughout the world from home offices. Because of this, we usually work together through text chat, phone, video call, and other remote means. Everyone traveling to New York City for this gathering was a great chance to get to know each other more personally.

The meeting itself was prefaced by a meetup at the Metropolitan Museum of Art, which turned out to be an fun game of hide-and-seek, trying to find each other throughout the museum's exhibits.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/10/23/end-points-20th-anniversary-meeting/image-0-big.png" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/10/23/end-points-20th-anniversary-meeting/image-0.png"/></a></div>

### We're 20 years old!

This gathering was a special occasion because this year we are celebrating our 20th anniversary as a company! Day one of our meetings began with introductory comments by End Point's founders, Rick Peltzman, CEO, and Ben Goldstein, President. Together with Jon Jensen, CTO, they took a look back at where we've been, where we are now, and where we're going.

Rick had this message for our clients and friends in August, the month the company was founded:

> Hello and happy birthday to us! This week marks End Point’s 20th anniversary. Congratulations to all our friends, clients, business partners, advisers, and especially our gifted engineers over these many years that have been the core of what makes this company successful.
>
> We started as a two-person company out of New York, building simple websites in the infant stages of the oncoming internet boom. We now are 55 people strong and counting, throughout the world. Our skillsets have expanded to include dozens of technologies and services. And we’re extremely proud of the emergence of our Liquid Galaxy division. End Point is no longer your father’s internet company!
>
> Along the way we weathered stock market crashes and bubble bursts, three U.S. presidents, amazing triumphs and heartbreaking human events. Still, through it all, End Point has adapted, grown, and has always lived up to its core principles: providing excellent support, deep knowledge of all things internet, and great client relationships.
>
> Thank you again for helping us thrive, improve, and position ourselves for an even more exciting next 20 years!

### Remote work tips

Moving on, two of our company directors, Ron Phipps and Richard Templet, took the floor to tell us about some remote work hacks, or tips and techniques, they use. Ron recommends using multiple monitors to increase productivity, dedicating one monitor to tools for time tracking, chat, calendar, etc. so they're always in sight and easy to access. Ron summarized how he records his time by writing notes down *before* starting the work, then refining the description and recording the time spent as he goes.

Ron also talked about the value of using voice or video calls with Google Hangouts or Skype to break through communication logjams. We use lots of good tools including email, IRC, Flowdock, Trello, Redmine, and Google Calendar, but they are inefficient for rapid, in-depth conversations. When there's confusion or misunderstanding in a discussion, speaking together in real-time makes it much easier to clear things up. Using the phone also helps us establish better relationships with each other and our clients, which, in turn, improves our work together.

Some other tips from Ron: Keep notes and download apps for whatever tools your team or projects are using. Use separate browsers or browser profiles for work and personal stuff. When traveling, relying solely on WiFi is a bad idea. Bringing a 50-100 foot Ethernet cable and an extra router has saved a few of our employees before.

Richard shared some tips as well:

- Keep some things offline so your work doesn't shudder to a halt whenever the network cuts out.
- Taking notes with pen and paper works without power or a network, helps you get things into your head, and is much simpler than using an app or website.
- Bringing a backup power supply or battery when traveling can save you from a bad situation.
- Whenever working at home, setting up a spot that is *your office* helps cut down on outside distractions.
- Use screen or tmux on remote servers so you don't lose work when the network drops.
- Pair or team programming can do miracles for productivity! Use a shared screen or tmux session while talking on the phone with a headset.

<a data-flickr-embed="true" href="https://www.flickr.com/photos/end-point/22344461751/" title="DSC_4275"><img alt="DSC_4275" src="/blog/2015/10/23/end-points-20th-anniversary-meeting/image-1.jpeg" style="max-width: 100%; margin-bottom: 1em;"/></a>

### Perusion history

Greg Hanson and Mike Heins then reviewed the history of their company Perusion which merged with End Point in July 2015. Greg and Mike met when Greg was looking for someone to create a website for his computer hardware store and later they went into the consulting business together.

Perusion started with just a few clients, getting business by word of mouth. Their first big client was Vervanté, an on-demand publishing firm built on Interchange. Vervanté started small but has grown to a large business supporting thousands of authors.

We have written up more about Perusion in the blog post [Perusion has joined End Point!](/blog/2015/07/31/perusion-has-joined-end-point)

### Stance

Piotr Hankiewicz and Greg Davidson talked about their work with Stance, a company founded in 2009 that creates and sells stylish socks. Most of the work we've done has been on the "product wall," which was challenging because of the sheer number of products and many ways to filter them. We started working with Stance in 2014, when they wanted help replacing their Magento site and redesigning it to be more responsive. We use Snapshot.js to very efficiently sort and filter large datasets. It also lets us keep the number of AngularJS models low, which keeps the site fast.

The product wall has around 3000 SKUs, and we've built a complex JavaScript system which makes it possible to sort and filter. It's even possible to filter the products by a combination of many things: color, size, thickness, price, collection, etc. There's a search function which is also integrated with the site.

<a data-flickr-embed="true" href="https://www.flickr.com/photos/end-point/21712970854/" title="IMG_4839"><img alt="IMG_4839" src="/blog/2015/10/23/end-points-20th-anniversary-meeting/image-1.jpeg" style="max-width: 100%; margin-bottom: 1em;"/></a>

### Carjojo

Josh Williams and Patrick Lewis talk about Carjojo. Carjojo is a company to help consumers find detailed information and history on cars they're interested in buying.

Josh works on the back-end of their site, creating a REST API with Django and TastyPie. TastyPie makes it very easy to write functions that return data from the database, although it becomes very complicated when it comes to return datasets that are more complicated than TastyPie is built to handle.

The front-end is handled by Patrick, who creates a modern Angular-based JavaScript web application. There are two main parts of the front-end; one for filtering cars when you have a more general idea of what kind of car you're looking for, and the other for when you have a more specific idea of what you're looking for. They will both result in a detail page for a vehicle.

This architecture lends itself to a simple development process: It starts with the web designer, who gives Patrick a mockup of a page he wants created. Patrick implements the front-end app code, figures out what data is necessary to make the page work, and then Josh works on the backend to implement functions to return that data.

### Code quality and testing

Kamil Ciemniewski and Marina Lohova talked about testing code. They started by talking about the difference between core testing (functionality of a program), compatibility testing (across browsers and devices), and usability testing.

Automated testing is a great way to make sure everything's working. It is very useful for catching things that the developer may not catch if they're testing manually. Automated testing can also easily cover odd scenarios, such as null values and empty search results (and other "fuzzing" of input data).

Kamil also talked about the importance of preventing bugs versus fixing them when they happen. It's much better for everyone involved if a bug is prevented or avoided rather than caught after it's been found. It means the user can do what they want to, the client feels like they are getting what they're paying for, and the developer feels satisfied with their work.

These are some ways to help prevent bugs coming up:

- Use declarative syntax rather than imperative.
- Always be clear about types.
- Break code into small chunks.
- Create terse code that is easy to read and documents itself.
- Stick to standard libraries when possible.
- Learn common programming paradigms.

Having clear communication with the client is also an important part of testing, as they're really the only ones qualified to judge the quality of the product they envisioned.

<a data-flickr-embed="true" href="https://www.flickr.com/photos/end-point/22307819166/" title="DSC_4263"><img alt="DSC_4263" src="/blog/2015/10/23/end-points-20th-anniversary-meeting/image-1.jpeg" style="max-width: 100%; margin-bottom: 1em;"/></a>

### Agile development methodologies

Wojciech Ziniewicz and Brian Gadoury talked about Agile theory and practice. First, they briefly covered "waterfall development," which starts with defining requirements, then goes on to design, development, testing, and then maintenance. In reality, requirements change, design needs revision, development takes longer than expected, testing may be skipped or skimped on, and maintenance is never perfect.

The Agile Manifesto was written in 2001, and emphasizes a focus on adapting to change, a simpler process, and tight feedback loops. "Agile development" has become a collection of management and development methodologies. It’s intended to be light on the process overhead, iterative and incremental, and to be helpful when done right.

There are now many flavors of Agile, such as Extreme Programming (XP), Scrum, Crystal, Kanban, Lean, DSDM, etc.

XP focuses on things like short development cycles and many checkpoints. It relies on great communication and tools to help with frequent small releases, like good devops. It also requires pair programming. According to a [study done](http://collaboration.csc.ncsu.edu/laurie/Papers/XPSardinia.PDF) by the University of Utah and North Carolina State University, pair programmers spend 15% more time on problems, but the resulting code has 15% fewer defects. 96% of programmers in the study said they enjoy pair programming more than solo programming. Pair programming also makes knowledge-sharing easy.

Scrum involves short "sprints", usually one or two weeks long, and along the way a daily standup meeting which is a short, disciplined meeting where you discuss what you've done since the last meeting, any blockers to your work, and what you are and will be doing in the near future.

One interesting agile technique is planning poker, which involves using playing cards to create estimates for work, with the numbers representing a difficulty for the project. Everyone will flip their cards over at the same time, and people with high or low estimates are given a chance to explain their justification. The [Dunning-Kruger effect](https://en.wikipedia.org/wiki/Dunning%E2%80%93Kruger_effect) is a very good reason to use this, as it helps people see when they're estimating too low or when team members think something will be much easier than the person making the estimate thinks. There is a nice plugin to Google Hangouts for doing planning poker remotely.

Test driven development (TDD) is another good agile technique. TDD involves writing tests before code, running the test (it'll fail), writing code to fix the test problems, then testing again to confirm it's all working as expected. It can get in the way sometimes, but usually ends up making you write better code.

Several agile methodologies encourage measuring velocity: finding the rate of progress to measure the capacity of your team by putting points on tasks and then assigning points on new tasks based on how points were assigned for completed tasks. In other words, rather than using points to represent time, use them to represent difficulty and improve the team's speed at completing tasks over time.

### Continuous Integration

Zdeněk Maxa talked about another Agile technique, Continuous Integration (CI). CI is a method used in software development where developers commit and push to the code base frequently. A CI server automatically runs unit tests and/or builds the software packages and reports on the success or any problems introduced by recent commits or merges. CI tests and builds are usually done at least once a day, if not after every single push. This kind of rapid re-alignment can work wonders in helping avoid last-minute conflict merges and provide quality assurance.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/10/23/end-points-20th-anniversary-meeting/image-1.png" imageanchor="1"><img border="0" src="/blog/2015/10/23/end-points-20th-anniversary-meeting/image-1.png" style="margin-top: 1em; margin-bottom: 1em; max-width: 100%;"/></a></div>

### Project estimation

David Christensen talked about project estimation. Successful agreements for new projects come through good communication, scoping, and estimation. Difficulty estimation is fairly similar to engineering; sometimes it can be easy, for example when the project involves things we’ve done many times, when people who know the area of work well have time to work on it. Some estimates are more difficult, when things like unclear objectives, uncertainty, or lack of experience in the field get in the way.

Depending on the circumstance, it can be useful to put together a very broad estimate with a wide range, so that the customer has a rough idea of the size of the project and can decide whether to pursue it at all. Such a rough estimate is much quicker and simpler than putting lots of time into project analysis, only to find out the project is far outside of the budget range.

A large project that requires a more exact estimate may call for a smaller paid discovery project, which involves a deeper investigation into the project and ferreting out hidden pitfalls and risks. It can be incredibly useful for when a more exact estimate of time and/or cost is needed.

David says we need to avoid unrealistic engineer optimism and be honest about estimates. Overpromising leads to unhappy clients and unhappy management. Clients need to make informed decisions, and giving them only a best-case scenario isn’t good for that. To that end, we can solicit input from more experienced people and those who are subject matter experts in relevant areas.

<a data-flickr-embed="true" href="https://www.flickr.com/photos/end-point/22370682871/" title="DSC_0629"><img alt="DSC_0629" src="/blog/2015/10/23/end-points-20th-anniversary-meeting/image-2.jpeg" style="max-width: 100%; margin-bottom: 1em;"/></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>

### Electrical problem in the building!

Our day had some extra excitement when our office building was evacuated due to an electrical problem that may have posed a fire risk. We split up for short walks around the neighborhood, until Ben Witten found us a great temporary meeting place at [Rise New York](http://thinkrise.com/), a co-working space focused on helping financial startups work together. The rest of the afternoon our meeting continued there, a comfortable and convenient place just down the street from our office!

Continue reading about [day 2 of our meeting](/blog/2015/11/02/end-points-20th-anniversary-meeting)!
