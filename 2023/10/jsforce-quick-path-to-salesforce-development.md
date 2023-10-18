---
author: "Couragyn Chretien"
title: "JSforce: Quick Path to Salesforce Development"
date: 2023-10-11
tags:
- jsforce
- javascript
- js
- Apex
- salesforce
- api
---

## JSforce: Quick Path to Salesforce Development

Using JavaScript with JSforce can get you working on a Salesforce project quickly if you don't have a Salesforce expert on hand. It allows you to easily access Salesforce's API, which will allow you to focus on development instead of learning a new system.

For a deeper dive into setup and uses of JSforce checkout [this post by Dylan Wooters](https://www.endpointdev.com/blog/2020/03/salesforce-integration-with-node/).

### Reasons to use JSforce

#### Apex is a niche language

Salesforce is written in Apex, and language similar to Java. In my experience most developers haven't delved too deep into Apex aside from Salesforce specialists.

JavaScript, JSforce's language has a wide and sometimes diehard following. NodeJS is currently the most widely used web framework out there, and it's almost impossible not to have written some front end JavaScript (if only an Alert()).

According to [Statista](https://www.statista.com/statistics/793628/worldwide-developer-survey-most-used-languages/), Apex is used by 0.66% of developers worldwide (#45), while JavaScript is used by 63.63% (#1).


#### No Salesforce learning curve

Have you ever had a client come forward with some Salesforce work but you didn't have anyone with exerience available? Even if you had a Salesforce expert on hand, experience with Salesforce's unique development environment is needed to have a resonable turnaround on any deliverables.

Developing in Salesforce can be compared to developing in Wordpress. It's easy enough to make surface level changes. But once you get under the hood and start actually working with the code it can be difficult to figure out and navigate all the "features" there that make things "easier". Even if you're a PHP (Wordpress) or Apex (Salesforce) developer, working within these systems are a different beast.

JSforce lets you pull data from Salesforce, manipulate it with JS, then send it back.

### Using JSforce CLI

Below are some examples for connecting and performing basic CRUD operations.

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