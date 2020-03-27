---
author: "Dylan Wooters"
title: Salesforce Integration with Node.js
tags: nodejs, javascript, integration
gh_issue_number: 1612
---

![Patterned roof](/blog/2020/03/27/salesforce-integration-with-node/fulton-ceiling.jpg)

<small>Photo by Dylan Wooters, 2020</small>

Salesforce is huge. It is currently the dominant customer relationship management (CRM) provider, accounting for [around 20%](https://www.forbes.com/sites/louiscolumbus/2019/06/22/salesforce-now-has-over-19-of-the-crm-market/#75a6cdf9333a) of market share. Businesses are using Salesforce not only as a traditional CRM solution, but also for novel purposes. Salesforce can serve as a backend database and admin portal for custom apps, or as a reporting tool that pulls data from various systems.

This growth leads to increasing demand for Salesforce integrations. The term “Salesforce integration” may conjure up images of expensive enterprise software or dense API documentation, but it doesn’t have to be that way. You can work with Salesforce easily using Node.js and the npm package [JSforce](https://jsforce.github.io/). An example of a project that might benefit from this kind of Node.js integration is an e-commerce website where order data is loaded to and from Salesforce for order fulfillment, tracking, and reporting.

In this post we’ll cover how to connect to Salesforce using JSforce, the basics of reading and writing data, as well as some advanced topics like working with large amounts of data and streaming data with [Socket.IO](https://socket.io/).

### Setting Up

You’ll first want to [install Node.js](https://nodejs.org/en/download/) on your local machine, if you haven’t done so already.

Next, create your Node app. This will vary with your requirements. I often use [Express](https://expressjs.com/) to build a REST API for integration purposes. Other times, if I am routinely loading data into Salesforce, I will create Node scripts and schedule them using cron. For the purposes of this post, we will create a small Node script that can be run on the command line.

Create a new directory for your project, and within that directory, run `npm init` to generate your package.json file. Then install JSforce with `npm install jsforce`.

Finally, create a file named script.js, which we will run on the command line for testing. To test the script at any time, simply navigate to your app’s directory and run `node script.js`.

At the top of the script, require `jsforce`, as well as the Node IO libraries `fs` and `path`. Then define an asynchronous function that will serve as our script body. This is where all of your Salesforce code will go.

```javascript
var jsforce = require('jsforce');
var fs = require('fs');
var path = require('path');

run();
async function run() {
    // salesforce code goes here...
}
```

### Connecting to Salesforce

I usually store my Salesforce credentials and instance URL as a JSON object in a separate file, which I gitignore. This ensures that sensitive data does not appear in Git. Below is the content of my salesforce-creds.json file. You’ll want to add your Salesforce username and password and update the instance URL, if necessary.

```json
{
    "username": [your username],
    "password": [your password],
    "url": "https://na111.salesforce.com"
}
```

To connect to Salesforce simply retrieve the credentials from the file and use them with the JSforce Connection class to login. Be sure to wrap all JSforce code in a try-catch block, to catch any errors coming back from Salesforce.

```javascript
let creds = JSON.parse(fs.readFileSync(path.resolve(__dirname, './salesforce-creds.json')).toString());
let conn = new jsforce.Connection({
    loginUrl: creds.url
});
try {
    await conn.login(creds.username, creds.password);
    console.log('Connected to Salesforce!');
    // now you can use conn to read/write data...
    await conn.logout();
} catch (err) {
    console.error(err);
}
```

### Reading, Writing, and Deleting Data

Once connected, the easiest way to query data from Salesforce is to use the JSforce query function, and pass in an [SOQL](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql.htm) statement. This offers the most flexibility, as you can run queries for child and parent objects. Using SOQL, we can query all accounts and their contacts (children) in a single statement. Note, however, that there are [limitations on relationship queries](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql_relationships_query_limits.htm). You can only go down one level, from parent to child, but you can go up multiple levels from child to parent.

Writing and deleting data is simple with JSforce using the `sobject` class and the corresponding create/update/delete function. In the example below, we will query for accounts and contacts using SOQL, and then isolate and update a specific contact using `sobject().update`.

```javascript
let soql = `select id, name,
    (SELECT Id, FirstName, LastName, Email_Verified__c, Enrollment_Status__c from Contacts)
    FROM Account`;
let accounts = await conn.query(soql);
let cooper = accounts.records
    .filter(x => x.Name === 'Twin Peaks Sheriff Dept.')[0].Contacts.records
    .filter(y => y.FirstName === 'Dale' && y.LastName === 'Cooper')[0];
console.log(cooper);

// Console output:
// {
//     attributes: {
//         type: 'Contact',
//         url: '/services/data/v42.0/sobjects/Contact/0033h000001sDzDAAU'
//     },
//     Id: '0033h000001sDzDAAU',
//     FirstName: 'Dale',
//     LastName: 'Cooper',
//     Email_Verified__c: true,
//     Enrollment_Status__c: 'Pending'
// }

cooper.Enrollment_Status__c = 'Accepted';
let ret = await conn.sobject('Contact').update(cooper);
if (ret.success) {
    console.log('Contact updated in Salesforce.');
}
```

### Working with Large Amounts of Data

You may need to read and write large amounts of data, for example if you are using Salesforce for reporting and loading data to and from other systems.

#### Event-driven Querying

The record limit for standard promise-style SOQL querying, as in our example above, is 2000 records. To query more than that, it is best to shift to the event-driven style of querying. This will ensure that all records are successfully retrieved from Salesforce. You can use the `maxFetch` property to set the upper limit of records returned. By default, `maxFetch` is set to 10,000.

```javascript
let contacts = [];
let soql = 'SELECT Id, FirstName, LastName, Email_Verified__c, Enrollment_Status__c from Contact';
let query = await conn.query(soql)
    .on("record", (record) => {
        contacts.push(record);
    })
    .on("end", async () => {
        console.log(`Fetched Contacts. Total records fetched: ${contacts.length}`);
    })
    .on("error", (err) => {
        console.error(err);
    })
    .run({
        autoFetch: true,
        maxFetch: 5000
    });
```

#### Loading Data with the Bulk API

Loading a large amount of data into Salesforce is best accomplished through the [Bulk API](https://jsforce.github.io/document/#bulk-api) via JSforce. There are a couple good reasons for this approach.

The Bulk API has better performance over other methods when working with large collections of objects.

The standard JSforce `sobject` create/update/delete functions have a 200 object limit. For operations on large collections, you must divide the total by 200, resulting in many separate API calls. By contrast, the Bulk API only uses a single API call. Since Salesforce imposes [API limits](https://developer.salesforce.com/docs/atlas.en-us.salesforce_app_limits_cheatsheet.meta/salesforce_app_limits_cheatsheet/salesforce_app_limits_platform_api.htm), this makes the Bulk API a better choice.

Running a bulk operation is simple using the `bulk.load` method, which takes three parameters: the Salesforce object type, the operation type, and an array of objects. The method returns an array of objects with success/errors fields, as well as the id of the newly created object, if successful.

If you’re working with thousands of objects, it’s good to set the pollTimeout property manually to one minute or more, to avoid Salesforce connection timeouts. Also note that the possible values for operation type are: ‘insert’, ‘update’, ‘upsert’, ‘delete’, or ‘hardDelete’.

```javascript
// set poll timeout to one minute for larger datasets
sfConnection.bulk.pollTimeout = 240000;

// normally you will have thousands of Accounts, this is just an example
let accounts = [{
        Name: 'Saul Goodman, LLC'
    },
    {
        Name: 'Los Pollos Hermanos Inc'
    },
    {
        Name: 'Hamlin, Hamlin & McGill'
    }
];
let results = await conn.bulk.load('Account', 'insert', accounts);
console.log(results);

// Console output:
// [
//     { id: '0013h000006bdd2AAA', success: true, errors: [] },
//     { id: '0013h000006bdd3AAA', success: true, errors: [] },
//     { id: '0013h000006bdd4AAA', success: true, errors: [] }
// ]

if (accounts.length === results.filter(x => x.success).length) {
    console.log('All account successfully loaded.');
}
```

### WebSocket Streaming with Socket.io

Say you are building a web application for reporting, and the app contains a dashboard with data on all of your contacts in Salesforce. You want the dashboard to be updated whenever the data in Salesforce changes, and you also want this to happen without refreshing the web page.

To accomplish this, you can stream real-time data from Salesforce using JSforce and the [Socket.IO library](https://socket.io/), which makes working with WebSockets quite simple.

The first step in this process is creating a [PushTopic](https://developer.salesforce.com/docs/atlas.en-us.api_streaming.meta/api_streaming/code_sample_java_create_pushtopic.htm) in Salesforce. This is basically a trigger that emits a notification anytime an object is created, updated, etc. in Salesforce. I created a PushTopic for Contacts by running the following Apex code in the Salesforce developer console.

```javascript
PushTopic pushTopic = new PushTopic();
pushTopic.Name = 'UserChange';
pushTopic.Query = 'SELECT Id, FirstName, LastName, Email_Verified__c, Enrollment_Status__c FROM Contact';
pushTopic.ApiVersion = 48.0;
pushTopic.NotifyForOperationCreate = true;
pushTopic.NotifyForOperationUpdate = true;
pushTopic.NotifyForOperationUndelete = true;
pushTopic.NotifyForOperationDelete = true;
pushTopic.NotifyForFields = 'Referenced';
insert pushTopic;
```

Then, back in your Node app, install Express and Socket.IO.

Next, you’ll want to create a very basic Express server that will listen for updates from the Salesforce PushTopic, and emit them to your reporting site. Start by installing Express and Socket.IO.

```
npm install express
npm install socket.io
```

Then delete the `run` function in your script.js file, which contained the code from the samples above, and replace it with the following:

```javascript
async function run() {
    // listen with express
    server.listen(3000, function() {
        console.log('listening on *:3000');
    });

    // connect to Salesforce
    let creds = JSON.parse(fs.readFileSync(path.resolve(__dirname, './salesforce-creds.json')).toString());
    let conn = new jsforce.Connection({
        loginUrl: creds.url
    });
    try {
        await conn.login(creds.username, creds.password);
    } catch (err) {
        console.error(err);
    }

    // when the client connects, emit streaming updates from salesforce to client
    io.on("connection", (socket) => {
        console.log('A socket connection was made!');
        let eventHandler = (message) => {
            console.log('New streaming event received from Salesforce:', message);
            socket.emit('UserChange', message);
        };
        conn.streaming.topic('UserChange').subscribe(eventHandler);
    });
}
```

Here is a step-by-step description of what is occurring in the code sample above:

- The Express server is set to listen for connections on port 3000.
- We connect to Salesforce and login.
- Socket.IO is set to listen for incoming connections from clients.
- A function called `eventHandler` that emits Salesforce streaming messages to the client is defined.
- When a connection is made, `eventHandler` is attached to the Salesforce streaming topic as a callback, using the live Salesforce connection.

If you follow the nice little [tutorial from Socket.IO](https://socket.io/get-started/chat/) and create the sample chat webpage, you can actually test the Salesforce streaming updates. In the chat page, add this script, which will log messages coming back from Salesforce.

```html
<script>
    var socket = io();
    socket.on('UserChange', function(msg) {
        console.log(msg);
    });
</script>
```

Then update a contact in Salesforce, changing the contact’s first name. If everything works correctly, you should see the client connect via Socket.IO in the Node logs, and also see a streaming message from Salesforce logged in the browser’s console window.

### Summary

Node.js and JSforce provide a straightforward and elegant way to interact with Salesforce. Whether you have an existing Node API that needs to work with Salesforce, or you are building a new application that is powered by Salesforce data, consider the recipes above as stepping stones for completing your project.

