---
author: "Couragyn Chretien"
title: "JSforce: Salesforce Development without Java"
date: 2023-10-11
tags:
- jsforce
- javascript
- js
- java
- salesforce
- api
---

## JSforce: Salesforce Development without Java

Using Javascript with JSforce can get you working on a Salesforce project quickly if you don't have Salesforce expert on hand. It allows you to easily access Salesforce's API, which will allow you to focus on development instead of learning a new system.

### Reasons to use JSforce

#### Java isn't for everyone

Most developers I know have had some experience with Java, myself included. Whether they used it in a university course or had to jump on a Java project for a Hotfix. I've also found that the bulk of those devs aren't chomping at the bit to work on another Java project.

While Java can be a great language, JSforce's language Javascript has a wide and sometimes diehard following. NodeJS is currently the most widely used web framework out there, and it's almost impossible not to have written some front end JavaScript (if only an Alert()).

#### No Salesforce learning curve

Have you ever had a client ask for some Salesforce work, but you didn't have anyone on the team with exerience? Even if you had a Java expert on hand, experience with Salesforce's unique development environment is needed to have a resonable turnaround on any deliverables.

Developing in Salesforce can be compared to developing in Wordpress. It's easy enough to make surface level changes. But once you get under the hood and start actually working with the code it can be difficult to figure out and navigate all the "features" there that make things "easier". Even if you're a PHP (Wordpress) or Java (Salesforce) developer, working with these systems are a different beast.

JSforce lets you pull data from Salesforce, manipulate it with JS, then send it back.

### Using JSforce CLI

Here's an example on installation and some basic CRUD examples.

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