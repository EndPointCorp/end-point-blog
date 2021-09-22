---
author: Patrick Lewis
title: Integrating the Estes Freight Shipping SOAP API as a Spree Shipping Calculator
tags:
- api
- ruby
- rails
- shipping
- spree
date: 2021-09-22
---

One of our clients with a Spree-based e-commerce site was interested in providing automated shipping quotes to their customers using their freight carrier [Estes](https://www.estes-express.com/). After doing some research I found that Estes provided a variety of SOAP APIs and determined a method for extending Spree with custom shipping rate calculators. This presented an interesting challenge to me on several levels: most of my previous API integration experience was with [REST](https://en.wikipedia.org/wiki/Representational_state_transfer), not [SOAP](https://en.wikipedia.org/wiki/SOAP) APIs, and I had not previously worked on custom shipping calculators for Spree. Fortunately, the Estes SOAP API documentation and some code examples of other Spree shipping calculators were all I needed to create a successful integration of the freight shipping API for this client.

## Estes API Documentation
The Estes [Rate Quote Web Service](https://www.estes-express.com/resources/digital-services/api/rate-quote-web-service-v4-0) API is the one that I relied on for being able to generate shipping quotes based on a combination of source address, destination address, and package weight. I found the developer documentation to be thorough and helpful, and was able to create working client code to send a request and receive a response relatively quickly. Many optional fields can be provided when making requests but I found that I only needed to use a small subset of these, as shown in the example code below.

The one aspect of the API that tripped me up a bit was their use of `CN` as the country code for Canada; Spree and most other codebases I have encountered use `CA` for Canada, so I had to add a small workaround for that in my client code when requesting shipping quotes to Canadian addresses. Another limitation I encountered is that the API expected to receive only 5-digit US and 6-character Canadian postal codes, so I had to do a bit of manipulation in my shipping calculator to account for that.

## Ruby SOAP Client
I researched Ruby SOAP clients and soon found [Savon](https://www.savonrb.com/), the "Heavy metal SOAP client", which proved to be very easy to integrate into my existing Rails/Spree application. I added the savon gem to my project's Gemfile and I was quickly able to instantiate a Savon client and configure it using the WSDL provided by Estes. After that, most of the integration work involved crafting a valid XML payload for my request and then parsing the response.

## Spree Shipping Calculators
The final piece of the puzzle was implementing the Savon client into a Spree shipping calculator class. This process allowed me to retrieve details about the current user's order and then return the calculated shipping estimates within the context of the Spree checkout pages. Looking at existing shipping calculator code helped set me on the right path here; in the end, it was just a matter of defining a new class that inherited from the base `Spree::ShippingCalculator` class and then defining the `#compute_package` method expected by Spree for returning the shipping cost of a given package.

## Code Example

```ruby
# app/models/spree/calculator/shipping/estes_calculator.rb
module Spree::Calculator::Shipping
  # Custom freight shipping rate API integration
  class EstesCalculator < Spree::ShippingCalculator
    ESTES_API_URL = 'https://www.estes-express.com/tools/rating/ratequote/v4.0/services/RateQuoteService?wsdl'.freeze

    def self.description
      'Estes Freight'
    end

    def compute_package(package)
      country_code = package.order.ship_address.country.iso
      return 0 unless country_code.in?(['US', 'CA', 'MX'])

      client = Savon.client(
        filters: %i[user password account],
        log: true,
        log_level: :debug,
        logger: Logger.new(Rails.root.join('log', 'savon.log')),
        pretty_print_xml: true,
        wsdl: ESTES_API_URL
      )

      country_code = 'CN' if country_code == 'CA' # Estes uses CN for Canada
      postal_code = package.order.ship_address.zipcode

      postal_code =
        if country_code == 'CN'
          postal_code.delete(' ').first(6)
        else
          postal_code.first(5)
        end

      xml = <<~XML
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:rat="http://ws.estesexpress.com/ratequote" xmlns:rat1="http://ws.estesexpress.com/schema/2019/01/ratequote">
                  <soapenv:Header>
                <rat:auth>
                  <rat:user>#{ENV['ESTES_USER']}</rat:user>
                  <rat:password>#{ENV['ESTES_PASSWORD']}</rat:password>
                </rat:auth>
            </soapenv:Header>
            <soapenv:Body>
                <rat1:rateRequest>
                  <rat1:requestID>#{package.order.number}</rat1:requestID>
                  <rat1:account>#{ENV['ESTES_ACCOUNT']}</rat1:account>
                  <rat1:originPoint>
                      <rat1:countryCode>US</rat1:countryCode>
                      <rat1:postalCode>10001</rat1:postalCode>
                  </rat1:originPoint>
                  <rat1:destinationPoint>
                      <rat1:countryCode>#{country_code}</rat1:countryCode>
                      <rat1:postalCode>#{postal_code}</rat1:postalCode>
                  </rat1:destinationPoint>
                  <rat1:payor>S</rat1:payor>
                  <rat1:terms>C</rat1:terms>
                  <rat1:baseCommodities>
                      <rat1:commodity>
                        <rat1:class>50</rat1:class>
                        <rat1:weight>#{package_weight(package)}</rat1:weight>
                      </rat1:commodity>
                  </rat1:baseCommodities>
                </rat1:rateRequest>
            </soapenv:Body>
          </soapenv:Envelope>
      XML

      response = client.call(:get_quote, xml: xml)
      quotes = response.body.dig(:rate_quote, :quote_info, :quote)

      if quotes.is_a?(Array)
        quotes.first.dig(:pricing, :total_price).to_f
      elsif quotes.is_a?(Hash)
        quotes.dig(:pricing, :total_price).to_f
      else
        0
      end
    rescue Savon::Error
      # Record shipping rate as 0 if an API error is caught, 0 amount will indicate need to show user an error message on the shipping rate page
      0
    end

    private

    def package_weight(package)
      weight = package.contents.sum { |content| content.line_item.weight }

      if weight < 5 # enforce minimum package weight
        5
      else
        weight.round
      end
    end
  end
end
```

## Conclusion

I was pleased that I was able to quickly build a custom shipping calculator in Spree that used the Estes Rate Quote API to provide accurate shipping estimates for large freight packages. The high quality documentation of the Estes API and the Savon SOAP Client gem made for a pleasant development experience, and the client was happy to gain the new functionality for their Spree store.