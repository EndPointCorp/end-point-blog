---
author: Steph Skardal
gh_issue_number: 143
tags: conference, rails, spree, cms, magento
title: Spree at RailsConf
---

Last week at [RailsConf 2009](https://conferences.oreilly.com/rails2009), the Spree folks from End Point conducted a [Birds of a Feather](https://conferences.oreilly.com/rails2009/public/schedule/stype/Bof) session to discuss Spree, an End Point sponsored open source rails ecommerce platform. Below is some of the dialog from the discussion (paraphrased).

Crowd: “How difficult is it to get Spree up and running from start to finish?”

Spree Crew: “This depends on the level of customization. If a customer simple needs to reskin the site, this shouldn’t take more than a week (hopefully much less than a full week). If the customer needs specific functionality that is not included in core functionality or extensions, you may need to spend some time developing an [extension](https://web.archive.org/web/20090513101129/http://wiki.github.com/schof/spree/extensions).”

Crowd: “How difficult is it to develop extensions in Spree?”

Spree Crew: “Spree extension work is based on the work of the [Radiant](http://radiantcms.org/) community. Extensions are mini-applications: they allow you to drop a pre-built application into spree to override or insert new functionality. Documentation for extensions is available at the [spree github wiki](https://web.archive.org/web/20090513101129/http://wiki.github.com/schof/spree/extensions). We also plan to release more extensive Spree Guides documentation based on [Rails Guides](http://guides.rubyonrails.org/) soon.”

Spree Crew: “How did you hear about Spree?”

Crowd: “My client and I found it via search engines. My client thought that Spree looked like a good choice.”

Spree Crew: “What other platforms did you consider before you found spree?”

Crowd: “Magento”, “Substruct”, “My client considered Magento, but I know several people that have developed with Magento and have found it difficult to override core functionality.”

Spree Crew: “What types of functionality were missing from Spree that you’d like to see developed in the future?”

Crowd: “My client wanted checkout split into multiple steps instead of the new single page checkout. I was able to implement this by overriding the Spree checkout library and checkout views.”, “My client needed complex inventory management.”, “My client needed split shipping functionality.”

Crowd: “What is the plan for Spree with regards to CMS development?”

Spree Crew: “There has been some discussion on the [integration of a CMS into Spree](https://web.archive.org/web/20121016021052/http://groups.google.com/group/spree-user/search?q=cms). No one in the Spree community appears to be currently working on this. Contributions in this area are welcome. Also, Yehuda Katz is giving a talk on [mountable apps](https://conferences.oreilly.com/rails2009/public/schedule/detail/7785)—​the Spree community would like to investigate the implications this has for Spree.”

Crowd: “What are the next steps for localization, especially multilingual product descriptions?”

Spree Crew: “This is on the radar for future Spree development. It is not currently in development, and again, contributions in this area are welcome.”

From the discussion, I took away that some of the desired features for Spree are inventory management, split shipping functionality, cms integration, and improved localization. I hope that the application of Spree continues to contribute to it’s progress. The Spree Crew also hopes to showcase some of the sites referenced above at the spree site.
