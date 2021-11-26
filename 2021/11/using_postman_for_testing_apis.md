---
title: "Using Postman for Testing APIs"
author: Couragyn Chretien
tags:
- testing
- postman
- api
date: 2021-11-26
---

![Postman](/blog/2021/11/using_postman_for_testing_apis/postman.png)

Postman is an easy to use tool that facilitates testing APIs. The GUI takes the pain out of using old school commnand lines tools and other time consuming practives. Postman is helpful during development, for collaborating, and integral in automated testing.

It's one of the biggest and longest running API tools out there, so there is a lot of documention and community forums to provide whatever assistance is need.

### Use in development

The days of manually testing APIs with curl are gone.

Instead we can use Postman to to create reusable API calls. Postman will remember information such as the header configuration and data contained in the body. The API call can be sent from the GUI client, and it will display the response in a human readable format.

Saved requests can be grouped in Collections. These can be imported and exported for collabrative use in a team. 

![Postman GUI](/blog/2021/11/using_postman_for_testing_apis/gui.png)

### Automated Testing

Full API testing can now be done with the click of a button. Investing time now into building up the Postman infastructure will save development time down the line.

Custom Test Suites can be written in JavaScript and run manually or by a script. Periodically running these will ensure your applications API experiences limited regression. Below is a few simple tests that can be run using Postmans Javascript pm object.

```javascript
// Post request
const postRequest = {
  url: 'https://endpointdev.com/post',
  method: 'POST',
  header: {
    'Content-Type': 'application/json'
  },
  body: {
    mode: 'raw',
    raw: JSON.stringify({ key: 'posting this text' })
  }
};
pm.sendRequest(postRequest, (error, response) => {
  console.log(error ? error : response.json());
});

// Get request
pm.sendRequest('https://endpointdev.com/get', (error, response) => {
  if (error) {
    console.log(error);
  }
  pm.test('response should be okay to process', () => {
    pm.expect(response).to.have.property('status', 'OK');
    pm.expect(response).to.have.property('code', 200);
    pm.expect(error).to.equal(null);
  });
});
```

These tests can be hooked into Your CI/CD Pipeline easily for truly automated testing. Postman integrates with Jenkins with help from Newman, Postmans command-line Collection Runner. For a step by step guide getting this up and running [go here](https://learning.postman.com/docs/running-collections/using-newman-cli/integration-with-jenkins/).

### Alternatives

Insomnia and Paw are two of the top alternatives to Postman. For the most part all have the same capabilities with slight differences.

![Insomnia](/blog/2021/11/using_postman_for_testing_apis/insomnia.png)

Insomnia, like Postman, has a free version and an upgraded paid version. The UI on Insomnia tends to be a bit easier on the eyes. Its lightweight nature allows it be run faster and be a bit more responsive than Postman typically is. The main downside is the inability to write testing for standard requests, rather it needs to be in Open API format.

![Paw](/blog/2021/11/using_postman_for_testing_apis/paw.png)

Paw is Apple to Postmans Android. It was originally a Mac only application and has only recently become available on other platforms. Like most Mac apps its UI is streamlined and will be very easy to pick up for any Mac users. The original Mac app performs better than the cross platform version, and it has many extensions to expand its capabilities. The main downside is that there is no free version.