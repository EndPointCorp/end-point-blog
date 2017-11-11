---
author: Spencer Christensen
gh_issue_number: 996
tags: php, social-networks
title: Integrating Facebook SDK and HybridAuth PHP library
---



There are a few different libraries out there for integrating your site with Facebook and other social networking sites.  I recently added "Login with Facebook" for a client to their PHP site utilizing the [Facebook JavaScript SDK](https://developers.facebook.com/docs/facebook-login/v2.0).  The documentation on Facebook's site is pretty good (although it could use a few more examples).  Beyond just the login feature, this client also wanted to be able to offer a checkbox for "Post a message to Facebook about your order".  And the way they wanted it done required a PHP library to make calls to the Facebook Graph API directly.

I chose to use the [HybridAuth PHP library](https://github.com/hybridauth/hybridauth) which is a wrapper for integrating many different social networking sites using a plugin system (Facebook, Twitter, Google, other OpenID services, etc).  Likewise, the docs for HybridAuth were sufficient to get the examples up and running for me.  The problem was that none of the examples or documentation fit my scenario, where I already have the login set up and working with the JavaScript SDK but want to utilize the PHP library for posting to a user's feed.

When attempting to connect to Facebook with HybridAuth it kept attempting to log the user in again.  The main problem was that the access token received from the JavaScript SDK was not getting passed in correctly to HybridAuth, and so it was attempting to get a new access token.  The solution I finally got working seems a little dirty (not going through a standard method call or documented API), but it works.  Here is the snippet of PHP code to set the Facebook access token so that HybridAuth will use it instead of fetching a new one:

```php
    // Connect to Facebook and get the user's profile
    try {
        $hybridauth = new Hybrid_Auth( $config );

        // Set some session variables needed for HybridAuth
        Hybrid_Auth::storage()-&gt;set( 'hauth_session.facebook.is_logged_in', 1 );
        Hybrid_Auth::storage()-&gt;set( 'hauth_session.facebook.token.access_token', $_POST['fb_access_token'] );
        $hybrid_config = require $config;
        $fb_config     = $hybrid_config['providers']['Facebook'];
        $fb_app_id     = $fb_config['key']['id'];
        $_SESSION['fb_'. $fb_app_id .'_access_token'] = $_POST['fb_access_token'];
        $_SESSION['fb_'. $fb_app_id .'_user_id']      = $_POST['fb_uid'];

        // Now we connect to FB using the given access token for this user
        $adapter      = $hybridauth-&gt;getAdapter( "facebook" );
        $user_profile = $adapter-&gt;getUserProfile();
    }
    catch( Exception $e ) {
        return 'FB Connection Failed: <b>got an error!</b> error message=' . $e-&gt;getMessage() . ', error code='. $e-&gt;getCode();
    }
    ...
```

When a user successfully logs in with the JavaScript SDK, you will be given an authResponse object which contains, among other things, the user's Facebook ID and an access token.  I pass these two values to PHP using an HTTPS ajax call (POST as you can see above).  These two values are needed by HybridAuth and stored in certain session variables.  These must be set in the session before you call $hybridauth->getAdapter() method.  The order is important, otherwise HybridAuth won't use the access token you've set and will treat the user as not yet logged in.


