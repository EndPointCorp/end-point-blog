---
author: Steph Skardal
gh_issue_number: 690
tags: analytics, ecommerce, piggybak, rails
title: Cannot parse Cookie header in Ruby on Rails
---



Yesterday I resolved a client emergency for a Ruby on Rails site that continues to leave me scratching my head, even with follow-up investigation. In short, the emergency came up after an email marketing campaign was sent out in the morning, and resulted in server (HTTP 500 Status Code) errors for every customer that clicked on the email links. Despite the fact that Rails exception emails are sent to the client and me, the errors were never reaching the exception email code, so I was unaware of the emergency until the client contacted me.

Upon jumping on the server, I saw this in the production log repeatedly:

```
ArgumentError (cannot parse Cookie header: invalid %-encoding (...)):
ArgumentError (cannot parse Cookie header: invalid %-encoding (...)):
ArgumentError (cannot parse Cookie header: invalid %-encoding (...)):
```

The URLs that the production log was complaining about had a bunch of Google Analytics tracking variables:

- utmcmd=Email
- utmcct=customeremail
- utmccn=New Site Sale 70% off
- etc.

After a user visits the site, these variables are typically stored as cookies for Google Analytics tracking. Upon initial investigation, the issue appeared to be triggered from any Google campaign variable that contained a '%' character.

After follow-up investigation today, the more complete story looks like this:

1. Email blast sent
1. User clicks on link in email. That link goes to the email marketing company first for tracking, then is redirected to the website.
1. According to the email marketing campaign (after chatting with them today), Google Analytics tacks on their own tracking here, which is the source of the non-parseable URLs.
1. Rack receives the request and tries to parse the query, utilizing the Ruby URI module:

```ruby
def self.decode_www_form_component(str, enc=Encoding::UTF_8)
    if TBLDECWWWCOMP_.empty?
      tbl = {} 
      256.times do |i|
        h, l = i&gt;&gt;4, i&amp;15 
        tbl['%%%X%X' % [h, l]] = i.chr
        tbl['%%%x%X' % [h, l]] = i.chr
        tbl['%%%X%x' % [h, l]] = i.chr
        tbl['%%%x%x' % [h, l]] = i.chr
      end  
      tbl['+'] = ' '
      begin
        TBLDECWWWCOMP_.replace(tbl)
        TBLDECWWWCOMP_.freeze
      rescue
      end  
    end  
    raise ArgumentError, "invalid %-encoding (#{str})" unless /\A[^%]*(?:%\h\h[^%]*)*\z/ =~ str
    str.gsub(/\+|%\h\h/, TBLDECWWWCOMP_).force_encoding(enc)
  end 
```

1. The argument error on line 18 trickles up the pipeline in [rack](http://rack.github.com/), and is not handled elegantly, so a rack-originated server (HTTP 500 Status Code) error is triggered. Again, the '%' character in the URL appears to be the problem here likely based on the regexp match on line 18 — the error is not triggered when the Google variable does not contain a '%' character.
1. Customer sees server error page and is unhappy :(

At the time of the emergency we tried solving the problem on multiple avenues:

- Investigated removal of Google Analytics tracking URLs from email blast links, but this wouldn't help all the customers who already received the emails.
- Remove CGI parameters or sanitize them via nginx.
- Make web application changes to ignore or handle the ArgumentError.

Ultimately, I ended up added a begin/rescue statement to the rack code to skip escaping URLs where decode_www_form_component was raising an error:

```ruby
def unescape(s, encoding = Encoding::UTF_8)
  begin
    URI.decode_www_form_component(s, encoding)
  rescue
    Rails.logger.warn "DECODING on #{s.inspect} with #{encoding.inspect} FAILING."
  end 
end 
```

While this is a reasonable fix, I'm still puzzled for a number of reasons:

- The email marketing company (via chatting) claims that Google Analytics is tacking on the tracking variables, however, there is only one redirect from the email marketing company to the website. I don't understand the mechanism for which Google Analytics tracking variables are added to the URL, and if this process can be cleaned up to ensure proper URL encoding.
- I'm not sure if the issue happens immediately upon a customer landing on the site, or after a cookie is stored.
- At the moment, I'm not able to reproduce this issue in development mode, which makes it difficult to troubleshoot on my development instance.
- When I use the URI module directly in a console, no ArgumentError is raised:

```ruby
&gt;&gt; URI.decode_www_form_component("url_with_google_campaign_variables")
&gt;&gt; #happy dance
```

My best advice at this point is to tell the client not to use '%' character in the Google Campaign ID, but I'm still putting all the pieces together in the virtual code map in my head. I think a fix is more likely needed on the Ruby and rack side to handle URL parameters with the '%' character, and to elegantly handle situations where the URI.decode_www_form_components method dies.


