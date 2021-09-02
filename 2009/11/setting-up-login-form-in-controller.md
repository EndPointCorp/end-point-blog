---
author: Ron Phipps
title: Setting up a login form in a controller other then the Users controller in
  CakePHP, don’t forget the User model
github_issue_number: 227
tags:
- community
- php
date: 2009-11-25
---

I ran into an issue today while setting up a login form on the front page of a site that would post to the login action of the User controller. The issue was that when the the form was posted the App controller beforeFilter was called, the User controller beforeFilter was called, but the login action of the User controller was never reached and a blank template with the normal debugging output was shown. No errors were being output and there wasn’t much to go on. Ultimately what ended up being the problem was that in the Home controller where the form was being served from we did not have the following to include the User model:

```
var $uses = array('User');
```

Surprisingly within our view we were able to setup forms to work with the User model. When the auth component was checking for the user data in the post it did not find any data, and stopped processing the request. This was not a graceful way for the auth component or CakePHP to handle the request, an error message would have helped track down the issue.
