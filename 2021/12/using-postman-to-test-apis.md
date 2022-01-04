---
title: "Using Postman to Test APIs"
author: Couragyn Chretien
github_issue_number: 1807
tags:
- testing
- api
- json
date: 2021-12-16
---

![Photo of large rusty iron chain with blurry sea in background](/blog/2021/12/using-postman-to-test-apis/20071221_144412000-sm.jpg)

<!-- photo by Josh Ausborne -->

Postman is an easy-to-use tool that facilitates testing APIs. The GUI avoids the pain of old-school command-line tools and other time-consuming practices. Postman is helpful during development, for collaborating, and integral in automated testing.

It's one of the most popular and longest-running API tools out there, so there's a lot of documentation and community forums to provide whatever assistance is needed.

![Postman logo](/blog/2021/12/using-postman-to-test-apis/postman.png)

### Use in development

The days of only manually testing APIs with curl are gone.

Instead we can use Postman to create reusable API calls. Postman will remember information such as the header configuration and data contained in the body. The API call can be sent from the GUI client, and it will display the response in a human-readable format.

Saved requests can be grouped in Collections. These can be imported and exported for collaborative use in a team.

![Postman GUI screenshot](/blog/2021/12/using-postman-to-test-apis/gui.png)

### Automated Testing

Full API testing can be done with the click of a button. Investing time now into building up the Postman infastructure will save development time down the line.

Custom Test Suites can be written in JavaScript and run manually or by a script. Periodically running these will ensure your application's API experiences limited regression. Below are a few simple tests that can be run using Postman's Javascript `pm` object.

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
```

```javascript
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

These tests can be hooked into your CI/CD pipeline easily for truly automated testing. Postman integrates with Jenkins with help from Newman, Postman's command-line Collection Runner. For a step-by-step guide getting this up and running see their [Integrating with Jenkins](https://learning.postman.com/docs/running-collections/using-newman-cli/integration-with-jenkins/) documentation.

### Alternatives

Insomnia and Paw are two of the top alternatives to Postman. They have mostly the same capabilities with slight differences.

![Insomnia logo](/blog/2021/12/using-postman-to-test-apis/insomnia.png)

Insomnia, like Postman, has a free version and an upgraded paid version. The UI tends to be a bit easier on the eyes. Its lightweight nature allows it to run faster and be a bit more responsive than Postman typically is. The main downside is the inability to write testing for standard requests—it needs to be in OpenAPI format.

![Paw logo](/blog/2021/12/using-postman-to-test-apis/paw.png)

Paw is Apple to Postman's Android. It was originally a Mac-only application and has only recently become available on other platforms. Like most Mac apps its UI is streamlined and will be very easy to pick up for any Mac users. The original Mac app performs better than the cross-platform version, and it has many extensions to expand its capabilities. The main downside is that there is no free version.

### Reference

- [Postman](https://www.postman.com/)
- [Insomnia](https://insomnia.rest/)
- [Paw](https://paw.cloud/)
