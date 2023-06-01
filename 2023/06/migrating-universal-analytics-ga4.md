---
title: Migrating from Universal Analytics to GA4
author: Juan Pablo Ventoso
date: 2023-06-01
tags:
- google
- analytics
---

![Birds migration](/2023/06/migrating-universal-analytics-ga4/birds-migration.jpg)

<!-- Image: Migration by Aivar Ruukel, 2014. Attribution 2.0 Generic (CC BY 2.0), obtained from https://flic.kr/p/pEy1Er -->

Most public-facing websites rely on [Google Analytics](https://marketingplatform.google.com/about/analytics/) to track their traffic, analyze the user’s characteristics and behavior, and run reports based on that information to improve marketing strategies, engage their public and ultimately, increase the user’s loyalty.

### Universal Analytics vs. Google Analytics 4

Until 2020, Google relied on [Universal Analytics](https://support.google.com/analytics/answer/2790010), a system that offered a set of reports that were mainly based on page visits and content visualization. But in October 2020, Google announced that the new [GA4](https://developers.google.com/analytics/devguides/collection/ga4) was launched, using an event-centered approach for metrics. That allows several improvements in the way the data is collected and analyzed, like taking into account several platforms and devices as a source for the data (for example, combining website traffic with mobile app usage and activity on social networks).

Another improvement is privacy: Among the new features, anonymous IP addresses are now the default setting for GA4. The user's IP address will be still registered and used to group data when doing the initial collection, but it won't be retained after, and only the location metadata will be used for reporting.

In present, both versions are co-existing - but not for long! On [July 1](https://blog.google/products/marketingplatform/analytics/prepare-for-future-with-google-analytics-4/), GA4 will be the one option available, and Universal Analytics will disappear completely. That means we have a month (or less, depending on when you’re reading this!) to add a GA4 property and export the existing data from the Universal Analytics property.

One thing to consider is that the historical data will still be available under our Universal Analytics account for at least six months, but no new traffic will be processed.

### Migrating from UA to GA4

First, a few considerations:

- We should do this process on the [Google Analytics website](https://analytics.google.com/analytics/web). We cannot do it through the mobile app.
- We should repeat this process for every account that we need to migrate.
- We need access to our website’s source code in case we need to update the existing GA tag.

Once we navigated to the Analytics website, we need to do the following steps:

- Go to the Settings item on the lower left
- Select the account we want to migrate
- Select the existing Universal Analytics property
- Click the GA4 Setup Assistant link
- Create a new GA4 property with the assistant's help

![Screenshot of Google Analytics GA4 Setup Assistant](/2023/06/migrating-universal-analytics-ga4/google-analytics-ga4-setup-assistant.jpg)

If you already have a Google tag on the website that can be reused for GA4, you won't need to make any changes to your source code, and you will be all set. If your tag is not compatible, or Google can't detect it properly, the assistant will provide you a new tag. In that case, you will need to install the Javascript snippet that contains the tag on your website.

The snippet will look similar to the one below:

```javascript
<!-- Global Site Tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=xxxxxxxxxxxxxxx"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'xxxxxxxxxxxxxxx');
</script>
```

After finishing the wizard, you will have the new GA4 property connected to your account. Now you can navigate to it and start the second Setup Assistant, that will allow you to customize your property and import the existing data from Universal Analytics:

- Click on the "Set up conversions" option on the main screen of the assistant
- Choose the option "Import from Universal Analytics"
- Select which goals should be imported into events on the GA4 property
- Click "Import selected conversions"

![Screenshot of Google Analytics Setup Assistant](/2023/06/migrating-universal-analytics-ga4/google-analytics-setup-assistant.jpg)

That's it! Once the import finishes, the existing goals will appear as [conversion events](https://support.google.com/analytics/answer/9267568) on the GA4 property. If the Google tag was set up properly, the traffic information should start flowing to the new property, showing real time information about your traffic, and the conversion events should be registering specific user actions:

![Screenshot of Google Analytics GA4 Account enabled](/2023/06/migrating-universal-analytics-ga4/google-analytics-ga4-account-example.jpg)


We have done several migrations to GA4 for clients that were using Analytics during the past months. If you haven’t done it yet and need any assistance with the process, don’t hesitate to [contact us](https://www.endpointdev.com/contact/)!