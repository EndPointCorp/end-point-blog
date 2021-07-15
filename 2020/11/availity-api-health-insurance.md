---
author: Patrick Lewis
title: 'Availity: An API for Health Insurance'
github_issue_number: 1689
tags:
- ruby
- rails
date: 2020-11-16
---

![Stethoscope](/blog/2020/11/availity-api-health-insurance/banner.jpg)
[Photo](https://flic.kr/p/25e3v5L) by [Sergio Santos](https://www.flickr.com/people/143707811@N07/), used under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/), cropped from original.

I have been working on a tele-therapy application for a client in the health care industry over the past few months and had the opportunity to do some interesting work in the area of health insurance coverages and claims.

I was tasked with creating an integration of the [Availity](https://www.availity.com/) API for insurance coverages which provides the ability to make requests for details about a patient’s health insurance coverage and returns responses containing information like the patient’s primary care doctor, their copay amounts, and their deductibles.

The ability to query this health insurance information from an API in an automated fashion helps streamline the process of billing clients by validating their health insurance details and also determining what a patient’s financial responsibility will be for their online therapy sessions. Availity provides information for over 11,000 insurance companies; a [full list of supported payers](https://apps.availity.com/public-web/payerlist-ui/payerlist-ui/#/) is available on their site via a web interface and a downloadable CSV file.

Availity provides both REST and SOAP APIs in addition to a batch processing system that functions over SFTP. For the purposes of this article I will be focusing on the REST API which was the primary focus of my work for this project.

The [developer documentation](https://developer.availity.com/partner/documentation) for the REST API was mostly self-serve; after signing up for an account on the Availity site I was able to rely on their publicly available documentation for all of the API details that I needed to start making requests.

Unfortunately, the development process for integrating the SOAP API was not nearly as smooth; the [SOAP APIs](https://developer.availity.com/partner/) link on Availity’s main developer portal page currently comes up blank, and I had to register a separate account in order to create a support request to obtain documentation on the SOAP API. Even with that documentation in hand, I found it difficult to determine things like the correct WSDL to use, and the process for generating X12 strings was much more complicated than making a more traditional REST request with a parameter hash. The large majority of payers supported by Availity are covered by the REST API, but there are some that are only supported by SOAP API requests and necessitate this more difficult process.

The application we were developing featured a Rails backend, so I used the Ruby [rest-client](https://github.com/rest-client/rest-client) gem when making requests to the Availity REST API.

The request payload was surprisingly small. Most payers only require this combination of patient/provider details when making a request:

* Patient birth date
* Payer ID (Assigned by Availity to the health insurance company in the payer list linked above)
* Member ID (The patient’s membership ID with their insurer)
* Provider NPI
* Service type

Here is an excerpt of the API client code I created for making requests to the API:

```ruby
module Availity
  class Client
    extend Limiter::Mixin

    # Rate limit API requests to 100 per second
    # https://developer.availity.com/partner/node/503
    limit_method :coverages, rate: 100, interval: 1

    BASE_URL = 'https://api.availity.com/availity/v1'

    # ...

    def coverages(payer_id:, member_id:, patient_birth_date:, patient_first_name:, patient_last_name:)
      url = "#{BASE_URL}/coverages"

      params = {
        payerID: payer_id,
        memberId: member_id,
        providerNpi: '123456789',
        patientBirthDate: patient_birth_date,
        patientFirstName: patient_first_name,
        patientLastName: patient_last_name,
        serviceType: '30'
      }

      headers = {
        Authorization: "Bearer #{token}",
        params: params
      }

      RestClient::Request.execute(
        method: :get,
        url: url,
        headers: headers,
        log: @log
      )
    end
  end
end
```

The insurance coverage API then returns a link to a fairly long JSON response with a variety of information on the patient’s health insurance plan. I added an additional class to parse that response for specific details such as name of primary care doctor, total and remaining deductibles for the year, copay amounts, etc.

In addition to this insurance coverage API, Availity provides various other [API end points](https://developer.availity.com/partner/node/503) related to health care claims and costs that could be equally valuable to the development of applications in the health care industry.
