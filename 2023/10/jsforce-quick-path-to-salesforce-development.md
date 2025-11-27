---
author: "Couragyn Chretien"
title: "JSforce: A Quick Path to Salesforce Development"
date: 2023-10-21
featured:
  image_url: /blog/2023/10/jsforce-quick-path-to-salesforce-development/desert-sky.webp
description: An overview of JSforce, including using it for CRUD actions
github_issue_number: 2016
tags:
- javascript
- salesforce
- api
---

![A completely clear blue sky is broken by a desert mountain with exposed light rock, covered partly by striking green trees and bushes. Above the mountain is a half-moon.](/blog/2023/10/jsforce-quick-path-to-salesforce-development/desert-sky.webp)

<!-- Photo by Seth Jensen, 2023. -->

Using JavaScript with JSforce can get you working on a Salesforce project quickly if you don't have a Salesforce expert on hand. It provides easy access to Salesforce's API, which will allow you to focus on development instead of learning a new system.

### No Salesforce learning curve

Apex is a platform-specific language created so that developers can interact with Salesforce classes/​objects and write custom code. Apex allows you to do some cool things such as directly triggering custom Apex code based on an action in Salesforce.

The problem with Apex is that it is its own world, with its own IDEs, deployment processes, etc. There's a steep learning curve to getting up to speed with the Apex ecosphere.

JSforce is a wrapper/​abstraction of the Salesforce API. It allows you to do a lot, like search, perform CRUD actions, and even send emails. These functions aren't as streamlined as their built-in Apex counterpart, but JSforce allows any JS developer to jump right into the code without wasting costly training time.

### Using JSforce CLI

Below are some examples of connecting and performing basic CRUD operations.

#### Connecting

Installation:

```plain
$ npm install jsforce -g
```

Connection:

```plain
$ jsforce
> login('user@example.org', 'password123');
{ id: '00550000000vwsFAAQ',
  organizationId: '00D500000006xKGEAY',
  url: 'https://login.salesforce.com/id/00D500000006xKGEAY/00550000000vwsFAAQ' }
>
```

#### GET

```js
conn.sobject("Account").retrieve("0017000000hOMChAAO", function(err, account) {
  if (err) { return console.error(err); }
  console.log("Name : " + account.Name);
  // ...
});
```

#### POST

```js
conn.sobject("Account").create({ Name : 'My Account #1' }, function(err, ret) {
  if (err || !ret.success) { return console.error(err, ret); }
  console.log("Created record id : " + ret.id);
  // ...
});
```

#### PUT

```js
conn.sobject("Account").update({
  Id : '0017000000hOMChAAO',
  Name : 'Updated Account #1'
}, function(err, ret) {
  if (err || !ret.success) { return console.error(err, ret); }
  console.log('Updated Successfully : ' + ret.id);
  // ...
});
```

#### DELETE

```js
conn.sobject("Account").destroy('0017000000hOMChAAO', function(err, ret) {
  if (err || !ret.success) { return console.error(err, ret); }
  console.log('Deleted Successfully : ' + ret.id);
});
```

For a deeper dive into setup and uses of JSforce check out [this post](/blog/2020/03/salesforce-integration-with-node/) by my coworker Dylan Wooters. 