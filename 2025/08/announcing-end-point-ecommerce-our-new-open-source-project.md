---
author: "Kevin Campusano"
title: "Announcing End Point Ecommerce, Our New Open Source Project"
date: 2025-08-21
github_issue_number: 2144
description: "A minimalist ecommerce system that's quick to set up and easy to understand. Meant for developers to own, adapt, customize, and extend."
featured:
  image_url: "/blog/2025/08/announcing-end-point-ecommerce-our-new-open-source-project/railing-blue-sky.webp"
tags:
- dotnet
- ecommerce
- open-source
---

![A white plastered railing from a low angle, behind which is a pure blue sky. The railing comes down and to the right from the top left corner of the image, then has a right angle in the center of the image, coming back up and to the right for another quarter of the image before stopping.](/blog/2025/08/announcing-end-point-ecommerce-our-new-open-source-project/railing-blue-sky.webp)

<!-- Photo by Seth Jensen, 2025. -->

Today we're pleased to announce a new open source project: End Point Ecommerce.

End Point Commerce is a minimalist ecommerce system that's quick to set up and easy to understand. It is meant for developers to own, adapt, customize, and extend.

You can learn more about it on [our landing page](https://ecommerce.endpointdev.com/). You can also fork it today on [GitHub](https://github.com/EndPointCorp/end-point-ecommerce). There are running demos here:

* [REST API](https://demo.ecommerce.endpointdev.com/swagger/index.html)
* [Admin Portal](https://admin.demo.ecommerce.endpointdev.com)
* [Web Store](https://demo.ecommerce.endpointdev.com)

Are you interested in using End Point Ecommerce for your ecommerce site? Feel free to [contact us](/contact/) and we can work together to help you deploy, customize, and maintain it.

![REST API](/blog/2025/08/announcing-end-point-ecommerce-our-new-open-source-project/epec_swagger.webp)

![Admin Portal](/blog/2025/08/announcing-end-point-ecommerce-our-new-open-source-project/epec_admin_portal.webp)

![Web Store](/blog/2025/08/announcing-end-point-ecommerce-our-new-open-source-project/epec_web_store.webp)

### Key features

- Built with [ASP.NET](https://dotnet.microsoft.com/en-us/apps/aspnet), [PostgreSQL](https://www.postgresql.org/), and [Authorize.net](https://www.authorize.net/)
- Multiple deployment strategies, including [Docker Compose](https://docs.docker.com/compose/)
- Code base designed to follow [Clean Architecture](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures#clean-architecture) and [Domain Driven Design](https://learn.microsoft.com/en-us/archive/msdn-magazine/2009/february/best-practice-an-introduction-to-domain-driven-design) concepts, without being dogmatic about it — simplicity trumps all
- Good test coverage with [xUnit](https://xunit.net/)
- Includes a backend admin portal for managing the store, a REST API for building user-facing store frontends, and a simple web frontend
- Limited functionality — implements the bare minimum of ecommerce use cases
- Product catalog, shopping cart, order submission, email delivery

### How we got here

We recently had the opportunity to help one of our clients migrate their ecommerce site. They were using an established ecommerce engine and were having various problems with it. Their requirements were simple, and they didn't need all the bells and whistles of big ecommerce solutions. They didn't want to deal with the overhead, bloat, and difficulty of finding maintainers.

During initial investigation and planning, we didn't find any options that were small and easy to set up, understand, and customize, so we decided to build them a new site from scratch.

We realize that there may be others out there in the same boat that we were. You want to set up a custom ecommerce site but you don't want to deal with the complexity of bigger off-the-shelf solutions. You want something which you can thoroughly understand quickly, and modify to your heart's content, as if it were your own code base that you developed from scratch.

### Who is this for?

This project is meant for .NET developers who want a solid and simple foundation to build and customize ecommerce sites. To that end, the feature set is very basic, the code base is very straightforward, and the documentation is very developer-oriented. The idea being that developers can quickly get up to speed with how everything works, develop ownership over the code base, and implement their bespoke use cases.

This project is not meant for non-technical folks. There is no installation wizard, no templating engine, no plugin framework, no no-code customization capabilities.

If you want to set up a simple online store, or develop a highly customized one from scratch, think of this as a way of skipping the first few steps of building the foundational architecture and basic functionality.

Please check it out! And do whatever you want with it!
