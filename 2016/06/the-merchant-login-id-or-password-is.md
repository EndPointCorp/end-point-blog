---
author: Matt Galvin
title: The merchant login ID or password is invalid or the account is inactive, and
  to how to fix it in Spree
github_issue_number: 1232
tags:
- payments
- spree
- ecommerce
date: 2016-06-02
---

Authorize.net has disabled the RC4 cipher suite on their test server. Their production server update will follow soon. So, in order to ensure your, or your client’s, site(s) do not experience any interruption in payment processing it is wise to place a test order in the Authorize.net test environment.

The projects I was testing were all [Spree](https://spreecommerce.com/) Gem (2.1.x). The Spree Gem uses the [ActiveMerchant ](https://github.com/activemerchant/active_merchant)Gem (in Spree 2.1.x it’s ActiveMerchant version 1.34.x). Spree allows you to sign into the admin and select which server your Authorize.net payment method will hit- production or test. There is another option for selecting a “Test *Mode*” transaction. The difference between a test **server** transaction and a test **mode** transaction is explained quite succinctly on the [Authorize.net documentation](http://developer.authorize.net/hello_world/testing_guide/). To summarize it, test **server** transactions are never sent to financial institutions for processing but are stored in Authorize.net (so you can see their details). Transactions in test **mode** however are not stored and return a transaction ID of zero.

I wanted to use my Authorize.net test account to ensure my clients were ready for the RC4 Cypher Suite disablement. I ran across a few strange things. First, for three sites, no matter what I did, I kept getting errors saying my Authorize.net account was either inactive or I was providing the wrong credentials. I signed in to Authorize.net and verified my account was active. I triple checked the credentials, they were right. So, I re-read the Spree docs thinking that perhaps I needed to use a special word or format to actually use the test server (“test” versus “Test” or something like that).

Below is a screenshot of the test payment method I had created and was trying to use.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2016/06/the-merchant-login-id-or-password-is/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2016/06/the-merchant-login-id-or-password-is/image-0.png"/></a></div>

Since I kept getting errors I looked through the Spree code, then the [ActiveMerchant Gem](https://github.com/activemerchant/active_merchant) that Spree is using.

Below, you can see that the ActiveMerchant is deciding which URL to use (test or live) based on the value of **test?** (line 15).

[active_merchant/lib/active_merchant/billing/gateways/authorize_net.rb](https://github.com/activemerchant/active_merchant/blob/master/lib/active_merchant/billing/gateways/authorize_net.rb)

```ruby
require 'nokogiri'

module ActiveMerchant #:nodoc:
  module Billing #:nodoc:
    class AuthorizeNetGateway < Gateway
      include Empty

      self.test_url = 'https://apitest.authorize.net/xml/v1/request.api'
      self.live_url = 'https://api2.authorize.net/xml/v1/request.api'

      # etc.

      def url
        test? ? test_url : live_url
      end
```

How and where is this set? Spree passes the ActiveMerchant Gem some data which the ActiveMerchant Gem uses to create Response objects. Below is the code where ActiveMerchant handles this data.

[active_merchant/lib/active_merchant/billing/response.rb](https://github.com/activemerchant/active_merchant/blob/master/lib/active_merchant/billing/response.rb)

```ruby

module ActiveMerchant #:nodoc:
  module Billing #:nodoc:
    class Error < ActiveMerchantError #:nodoc:
    end

    class Response
      attr_reader :params, :message, :test, :authorization, :avs_result, :cvv_result, :error_code, :emv_authorization

      # etc.

      def test?
        @test
      end

      def initialize(success, message, params = {}, options = {})
        @success, @message, @params = success, message, params.stringify_keys
        @test = options[:test] || false
        @authorization = options[:authorization]
        @fraud_review = options[:fraud_review]
        @error_code = options[:error_code]
        @emv_authorization = options[:emv_authorization]

        @avs_result = if options[:avs_result].kind_of?(AVSResult)
          options[:avs_result].to_hash
        else
          AVSResult.new(options[:avs_result]).to_hash
        end

        @cvv_result = if options[:cvv_result].kind_of?(CVVResult)
          options[:cvv_result].to_hash
        else
          CVVResult.new(options[:cvv_result]).to_hash
        end
      end
    end
```

[active_merchant/lib/active_merchant/billing/gateway.rb](https://github.com/activemerchant/active_merchant/blob/master/lib/active_merchant/billing/gateway.rb)

```ruby
# Are we running in test mode?
def test?
  (@options.has_key?(:test) ? @options[:test] : Base.test?)
end
```

Now that I was more familiar with ActiveMerchant, I wanted to verify that Spree was passing the data as intended

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2016/06/the-merchant-login-id-or-password-is/image-1-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2016/06/the-merchant-login-id-or-password-is/image-1.png"/></a></div>

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2016/06/the-merchant-login-id-or-password-is/image-2-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2016/06/the-merchant-login-id-or-password-is/image-2.png"/></a></div>

I could see in [spree/core/app/models/spree/gateway.rb](https://github.com/spree/spree/blob/8bfa0824d2a7f6cfa6efc9bd4e32d1d564f6270b/core/app/models/spree/gateway.rb) that Spree was setting ActiveMerchant::Billing::Base.gateway_mode equal to the server param as a symbol. I verified it with some logging.

```ruby
def provider
	gateway_options = options
	gateway_options.delete :login if gateway_options.has_key?(:login) and gateway_options[:login].nil?
	if gateway_options[:server]
		ActiveMerchant::Billing::Base.gateway_mode = gateway_options[:server].to_sym
	end
	@provider ||= provider_class.new(gateway_options)
end
```

At this point I was satisfied that Spree was sending a server param. I also knew Spree was setting Active Merchant’s Base.gateway_mode as intended. I then reviewed [active_merchant/lib/active_merchant/billing/gateway.rb
](https://github.com/activemerchant/active_merchant/blob/master/lib/active_merchant/billing/gateway.rb) once more

```ruby
# Are we running in test mode?
def test?
	(@options.has_key?(:test) ? @options[:test] : Base.test?)
end
```

and [active_merchant/lib/active_merchant/billing/base.rb](https://github.com/activemerchant/active_merchant/blob/v1.34.0/lib/active_merchant/billing/base.rb)

```ruby
def self.test?
	self.gateway_mode == :test
end
```

So, that’s it! We know from the exceptions I raised that Spree is sending a test key and a test_mode key. They seem to be the same value but with different keys (I’m guessing that’s a mistake), and they both just seem to indicate if the test **mode** checkbox was checked or not in the Spree admin. However, Base.test? is the **server** selection and comes from whatever anyone enters in the server input box in the Spree admin. So, we just need to update the ternary operator to check if @options\[:test\] (test *mode*) **or** Base.test? (test *server*) is true.

Since this is Spree, I created a decorator to override the test? method.

app/models/gateway_decorator.rb

```ruby
ActiveMerchant::Billing::Gateway.class_eval do
  def test?
    @options.has_key?(:test) && @options[:test] || ActiveMerchant::Billing::Base.test?
  end
end
```

Lastly, I placed some test orders and it all worked as intended.

## Summary

Authorize.net is disabling the RC4 Cypher suite. If your site(s) uses that, your payment processing may be interrupted. Since the test environment has been updated by Authorize.net, you can see if your site(s) is compliant by posting test transactions to the test environment. If it works, then your site(s) should be compliant and ready when Authorize.net applies the changes to the production server.

Spree 2.1.x  (and perhaps all other Spree versions) ALWAYS send the test key, so the ActiveMerchant Gem will always just use the boolean value of that key instead of ever checking to see what the server was set to. Further, this fix makes things a little bit more robust in my opinion by checking if test mode OR the test server was specified, rather than **only checking** which server (gateway_mode) was specified **if the test key was absent**.

Alternatively, you could probably make Spree only pass the test key if the value was true.  Either way, if you are trying to send test orders to the test environment for a Spree site of at least some versions and have not implemented one of these changes, you will be unable to do so until you add a similar fix as I have described here. If you need any further assistance, please reach out to us at [ask@endpoint.com](mailto:ask@endpoint.com?subject=Blog Post Question).
