---
title: "Domain Move Considerations"
date: 2023-11-30
---

![Photo taken of and from the Mormon Row Homestead at Grand Teton National Park. Photo is taken facing WNW, and has an old home and barn in the foreground with the Teton Mountain Range in the background. ](/blog/2023/11/domain-move-considerations/mormon-row-and-tetons.webp)

<!-- Photo by Josh Ausborne, 2019 -->


In 2021 [we moved to a new Internet domain](/blog/2021/10/moving-to-endpointdev-dot-com/). We had been on endpoint.com for 26 years, so a lot of things were tied to that domain!

As we expected, there were a lot of little details to deal with. We found the switch to be a bit overwhelming until we started listing things out, at which time we realized that a divide-and-conquer approach would make it achievable.

A domain move is not an extremely common experience for a company to go through, but it’s not unheard of, either, due to acquisitions, mergers, or rebranding like ours. So we want to share our notes from our move to endpointdev.com in case they are helpful to others considering their own move.

How long did we reserve for the move, in calendar time? We planned to work on it over 6 months, but in the end we were done in about 3 months.

### Make a schedule

Look at your calendar. Mark any major company or personal events that you do not want any infrastructure disruption around. Block out busy periods, major holidays and vacations, etc. This will help you be realistic about how much time various people can spend on this, and how you can minimize problems for the company by choosing when to break things, or at least risk breaking them.

Start by noting your timeline for starting and your drop-dead end date to be off the old domain.

Is this something that you want or need to do all at one time, with a massive cutover of all services? Or do you expect to move services piecemeal? As we have helped clients move domains, we have done both types of moves.

Plan to divide tasks among the team to preserve sanity and enlist the experience of many people instead of just a few. That shares important knowledge among more people, which is good in any case.

As you settle on a schedule, make sure everybody involved is aware of it. Post it in a shared document all the relevant people have access to, and put important milestones on a shared calendar.

### Internal messaging

Messaging internally is just as important as messaging externally.

Your own staff may think that the domain has moved everything when it has only moved some. Consider making an internally available status page.

### New domain

As soon as possible, get the new domain registered and start using it as a secondary domain. You want to minimize the length of time you use a placeholder name, or have to add the qualifier “or whatever domain we get” every time you mention it. That will also help you see whether you find it nice to say all the time, how often it is misunderstood in speaking, how easy it is to type, etc. If you’re going to have second thoughts about the new domain you’ve chosen, have them early while you can still choose a different one and see if it works better.

### Identify all services

It’s important to brainstorm with your transition team to identify the list of services that need to be updated, as you could lose the ability to do so after transitioning away from the old domain. These services may include email, websites, ticketing systems, and proof of ownership of logins to SaaS (software as a service) accounts, among other things.

As you start building your list, you may be surprised to find out how many different services and providers you are using. This is a good time to start closing any accounts that you don’t use anymore, as well.

Examples of some services that companies use:

- Website hosting
- Domain registrar accounts and contacts
- Google Workspace (G Suite), Microsoft Office 365, or other email services
- GitHub (Note that you will lose the GitHub contribution stats associated with the old email address if you delete it from your account.)
- GitLab
- Bitbucket
- Slack
- Microsoft Teams
- Zoom
- Skype
- Atlassian (Jira, Trello)
- Asana
- Monday.com
- Redmine
- PagerDuty
- Adobe Creative Cloud
- Windows, Apple iCloud accounts
- Shippers such as USPS, FedEx, UPS, DHL
- Vendor purchasing accounts
- Website and server monitoring services
- Payment accounts such as company credit cards, Apple, PayPal, Google Pay
- Vendor account logins and contacts (Dell, Microsoft, Apple)
- Payroll service
- Retirement savings such as 401(k)
- Office rental invoicing and payments
- Office services such as water/food delivery



### Staff self-service

Have your staff update their own accounts on their own for as many as possible of the services that they use.

Some sites will allow you to add a secondary address, promote it to primary, then delete the old one.

### Infrastructure

Make a list of every hostname in your DNS zone, whether it’s public-facing or internal, where it is hosted (SaaS, which cloud service, on-premises), and how its hostname can be changed.

You should create new DNS entries in the new domain for all of your hosts well in advance of the cutover date. When reviewing your DNS entries, it is as good a time as any to review your existing entries and to do a bit of spring cleaning. We found numerous entries that were no longer needed, and we were able to purge them rather than migrate them into the new domain.

Update reverse DNS entries for all hosts.

### Email

Email is the lifeblood of business nowadays. It is how businesses interact with each other: invoicing, payments, sales requests, notifications, reminders, business partner requests, account login resets, etc. For most businesses everything would grind to a halt if email stops working.

Monitor outbound mail relay to see if any internal systems are sending notifications to old domain
Notify outsiders (customers, clients, business partners) of new domain
Notify them well in advance of the shutdown date
Some infrequently contacted clients might continue to use the old email address for months, and if the new owner of the domain doesn’t have email set up there, or if it doesn’t send “bounce” messages back when delivery fails, senders may have no idea you’re not receiving their mail.

### Websites

Change website URLs, email address, redirects
Main website
Blog (posts and comments)
Google Analytics: use domain move function. SEO is crucial for many businesses.

### Social media

Update your company social media accounts on Twitter, LinkedIn, Facebook, Instagram, YouTube, etc. If you move too quickly then you can get ahead of any marketing efforts that you may be making, but if you move too slowly then you might find yourself locked out of accounts or miss out on opportunities to take advantage of those same marketing efforts.

### Lessons learned

Use a separate infrastructure domain for cloud services. This means that your servers might be located in a different domain than your main marketing domain. For End Point, we use endpointdev.com as our marketing domain, but our infrastructure servers are known by names in epinfra.net. This, in theory, would allow us to easily change our marketing domain yet again (though this is *not* something that is on the horizon!) without having to go and change the domain in which our servers reside. Even if you never move to a new domain, putting your infrastructure on a separate domain now is a good idea, to separate marketing and public-facing services from internal hostnames.

Consider typing convenience for infrastructure names! epinfra.net is way easier to type correctly than endpoint.com was, and much better than the longer endpointdev.com. You’ll be typing this domain name a *lot*, so it’s worth taking a few minutes to find one that is easy to type.

Everything you can move earlier, which doesn’t affect the public, do so. The less you have to do up against a deadline, the better.

One lesson that we learned during our domain change is related to the fact that we use [Google Workspace](https://workspace.google.com/) for our mail services, etc., and our domain change involved having to login using the new domain. We had some staff who used Google’s Single Sign On (SSO) for services such as Trello. When the users logged into the account using the new domain name, Trello/Atlassian automatically created a new account for them at the new domain name, and users completely lost access to their old Trello accounts that were using the old domain. This caused us some issues later on because we had to go back through all Trello boards and cards, add all the new users, then remove all of those accounts, now dead and never to be used again, from everywhere. That was very tedious.

Another thing that we’ve found two years after The Great Migration is that the old domain still seems to live on in configuration files in various places. We found recently that we still had a virtual host configured on one of our web servers that was listening for requests for a host in the endpoint.com domain. We also found that many of our custom scripts and configurations reference endpoint.com in their comments. I’m never surprised when I stumble across the old domain in some obscure place. In fact, I kind of laugh about it now, as if I just found an Easter egg.

### Conclusion

When you finally decide to make your transition to a new domain, be sure to make lists and plan things out. Then be methodical in your work. Migrating can be a challenging task, but can be necessary for a full marketing rebrand and is doable.

