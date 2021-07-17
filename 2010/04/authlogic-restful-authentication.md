---
author: Steph Skardal
title: Authlogic and RESTful Authentication Encryption
github_issue_number: 289
tags:
- ecommerce
- rails
- rest
- api
date: 2010-04-19
---

I recently did a bit of digging around for the migration of user data from RESTful authentication to Authlogic in Rails. My task was to implement changes required to move the application and data from RESTful Authentication to Authlogic user authentication.

I was given a subset of the database dump for new and old users in addition to sample user login data for testing. I didn’t necessarily want to use the application to test login functionality, so I examined the repositories [here](https://github.com/technoweenie/restful-authentication) and [here](https://github.com/binarylogic/authlogic) and came up with the two blocks of code shown below to replicate and verify encryption methods and data for both plugins.

## RESTful Authentication

```ruby
user = User.find_by_email('test@endpoint.com')

key = REST_AUTH_SITE_KEY
actual_password = "password"
digest = key

REST_AUTH_DIGEST_STRETCHES.times { digest = Digest::SHA1.hexdigest([digest, user.salt, actual_password, key].join('--')) }

# compare digest and user.crypted_password here to verify password, REST_AUTH_SITE_KEY, and REST_AUTH_DIGEST_STRETCHES
```

Note that the stretches value for RESTful authentication defaults to 10, but it can be adjusted. If no REST_AUTH_SITE_KEY is provided, the value defaults to an empty string. Also note that RESTful authentication uses the SHA-1 hash function by default.

## Authlogic

```ruby
user = User.find_by_email('test2@endpoint.com')

actual_password = "password"
digest = "#{actual_password}#{user.salt}"

20.times { digest = Digest::SHA512.hexdigest(digest) }

# compare digest and user.crypted_password here to verify password
```

Note that the stretches value for Authlogic defaults to 20, but it can be adjusted. Also note that Authlogic uses the SHA-512 hash function by default.

After I verified the encryption of both old user passwords encrypted with RESTful Authentication and new user passwords encrypted Authlogic, I added the verified REST_AUTH_SITE_KEY and REST_AUTH_DIGEST_STRETCHES values to RAILS_ROOT/config/initializers/site_keys.rb and confirmed that the changes implemented in the tutorial described [here](https://web.archive.org/web/20100722161801/http://www.binarylogic.com/2008/11/23/tutorial-easily-migrate-from-restful_authentication-to-authlogic/) were implemented. The Spree User model already contains the model changes below discussed in the tutorial. As users log in to the application, user authentication is performed against the RESTful authentication crypted password. After a successful login, the password is re-encrypted by Authlogic.

```ruby
# app/models/user.rb
class User < ActiveRecord::Base
  acts_as_authentic do |c|
    c.act_like_restful_authentication = true
  end
end
```

Prior to this task, I hadn’t poked around the user authentication code in Rails or Spree. Hopefully, this experience will prepare me for the next time I encounter user migrations with encrypted passwords.
