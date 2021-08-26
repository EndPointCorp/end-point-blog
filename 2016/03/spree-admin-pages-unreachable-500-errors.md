---
author: Kent Krenrich
title: Spree Admin pages unreachable (500 errors)
github_issue_number: 1213
tags:
- spree
- ecommerce
date: 2016-03-17
---

I was notified a few minutes ago by one of our Spree clients that their admin interface was unreachable due to errors.

Digging into the logs, I discovered SocketErrors (DNS lookup failures) were behind the 500 errors. Digging deeper, I discovered the SocketErrors were coming from a Spree file attempting to access “alerts.spreecommerce.com”. I confirmed in my browser that alerts.spreecommerce.com fails to resolve.

[This Git commit](https://github.com/spree/spree/commit/d9bd19468d34ee12cc5ce0f73509748ca569957f) discusses the removal of the class, but if you haven’t stayed current and you’ve left the “Check for alerts” box checked, you may need to do some manual editing of your stored preferences to get the UI to load again.

```ruby
Spree::Preference.where(key: "spree/app_configuration/check_for_spree_alerts").first.update_attributes(value: false)
```

It does appear that your app will need to restart to pull in this change.

I’m not sure what the chances are your particular config key might vary, so please use the above with caution.
