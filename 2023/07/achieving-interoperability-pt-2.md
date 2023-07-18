---
title: "Achieving Interoperability, Part II: Combating the Curse: Interoperability’s Quest for a Solution"
author: Jarrett Smolarkiewicz
featured:
  casepointer: true
  image_url: /blog/2023/07/achieving-interoperability-pt-2/sunset.webp
github_issue_number: 1992
tags:
- casepointer
date: 2023-07-13
---

![A late sunset turns the clouds many shades of orange against a dim blue sky, above small town roofs and a few trees. Power lines cut across the top right side of the image.](/blog/2023/07/achieving-interoperability-pt-2/sunset.webp)

<!-- Photo by Seth Jensen, 2023. -->

This is the second article in the Achieving Interoperability series, which is designed to raise awareness of the complex and pressing challenges involved with standardizing healthcare data within the United States. Each part of the series is listed below:

* [Part I: Pandora’s Box and the Problem of Healthcare Data Standardization]()
* Part II: Combating the Curse: Interoperability’s Quest for a Solution
* [Part III: A New Hope: CasePointer’s Unique Standardization Approach]()

Part I introduced the problem of healthcare data standardization, and paralleled it with the myth of [Pandora’s Box](https://en.wikipedia.org/wiki/Pandora%27s_box): doing something that causes unforeseen problems.

Decades ago, when healthcare providers, software engineers, public health officials, and others set out to provide a means of efficiently transmitting healthcare data across the variety of digital networks within the United States, they unleashed a host of healthcare data standards that were designed to help, but have unintentionally come to haunt and hinder the industry in the years since their inception.

Part II of this series walks through the efforts and approaches that have been used to address these challenges, while Part III covers End Point’s involvement in developing an effective solution.

### Unintended Consequences

Upon opening the box entrusted to her care, Pandora wrestled with regrets due to the consequences of her actions. This is evident in versions of the story where, after all the troublesome things are released from the box, she quickly shuts it, accidentally trapping hope inside.

While in the healthcare industry several healthcare data standards exist and actively make interoperability more complicated, the good news is that several groups of talented individuals are currently in hot pursuit of a definitive solution. In the story of healthcare data standardization, all hope is not lost.

### Applications Abound

As data standards have been introduced, adopted, and revised over the years, they have been integrated into the increasing number of industry software systems used across the nation. While networks of hospitals and laboratories typically set up [Electronic Health Record (EHR)](https://www.healthit.gov/faq/what-electronic-health-record-ehr) platforms built by companies like Cerner or Epic to manage patient data, public health agencies require additional applications to aid in the identification, tracking, and reporting of certain health conditions from those patient EHRs.

States and regional jurisdictions have taken a variety of approaches to accomplish this. Many look to free software offered by the Centers for Disease Control and Prevention (CDC). Some partner with one or more consulting firms to implement the highly specialized networks of applications they require. Still others opt to develop, customize, and maintain everything in house. This has led to so many unique software installations that when the need arises for them to communicate with and transmit healthcare data to each other it seems all but impossible!

### The Quadratic Cost Problem

Getting so many diverse software systems to work together is extremely difficult due to a phenomena known as the quadratic cost problem. This occurs when the need for bi-directional connections between software applications increases exponentially (instead of linearly) with each component added to a healthcare data system.

The United States government is a hierarchy of federal, state, regional, local, tribal, and other governing bodies that decide which software they will use to protect the public health of their communities. Since these groups each have unique needs and do not always implement the same technology, when they have to work together to track and resolve health concerns they are faced with the staggering costs of building and supporting all the bi-directional connections which are a symptom of the quadratic cost problem.

If this concept still seems unclear, or you’re simply curious to learn more, a digital training and events firm known as TechChange breaks down this concept and more [on their YouTube channel](https://www.youtube.com/watch?v=KSEUh-wj7Y0).

### Health Information Exchange Advantages

As government and healthcare collide, one attempt technology has made to bring order and harmony is by connecting applications of each jurisdictional segment within a larger governing body to a centralized [Health Information Exchange (HIE)](https://www.healthit.gov/topic/health-it-and-health-information-exchange-basics/what-hie).

An example of this would be an individual state public health organization connecting its own software to an HIE, along with the software currently in use by each local jurisdiction within that state. Each jurisdiction does not have to use the same software, but can communicate between platforms using its connection to the HIE vs. individual bi-directional connections to every other application used throughout the state.

HIEs also aim to leverage their centrality to overcome the quadratic cost problem. Since it acts as a single hub connecting all other systems, an HIE is the only component that needs to be updated when changes occur in one of the other connected applications. As great as this all sounds, some drawbacks accompany HIE solutions. 

### Health Information Exchange Challenges

Individual applications connected to the central HIE must diligently make sure they maintain compatibility for this solution to prove effective. As with any complex software architecture, connections that work today can break tomorrow. When an HIE is upgraded to maintain its connectivity with another recently updated app in the ecosystem, the updates can inadvertently cause issues with other connected apps that had no prior problems.

In addition to compatibility struggles, HIEs rely on the presence of a universal set of standards to which they conform all other data in the workflow. An HIE scenario used in the TechChange video referenced earlier assumes that the HIE implementation will seamlessly handle all healthcare data standards bundled together for an entire governing body. While this may seem intuitive and logical, it is unfortunately not the reality, given the numerous interoperability standards within the United States. These varying standards can also put the privacy and security of patient data being transmitted at risk. This brings about additional legal concerns with regard to HIPAA regulations. 

### Decades of Stagnation

Chapter four of the book "[Patient Safety: Achieving a New Standard for Care](https://www.ncbi.nlm.nih.gov/books/NBK216088/)" identified this concern:

> “The fact that there is no standard means of representing the data for any of these datasets or requirements is astonishing and highlights the amount of unnecessary work performed by health care and regulatory organizations to prepare, transmit, and use what amount to custom reports.”

Nearly 20 years after those words were written, and almost a decade after the [FHIR](https://www.hl7.org/implement/standards/product_brief.cfm?product_id=491) standard was introduced, the variety of standards and systems has not narrowed to a set of standards that any HIE could use to universally coordinate healthcare data within the United States. Without a unified data standard, the power of the HIE falls flat.

### Hope on the Horizon

Thankfully, a new evolution of public health technology is emerging, known as [CasePointer](https://www.casepointer.com) by End Point. This system unifies many components, including the EpiTrax application, which can handle all 170+ [reportable health conditions](https://ndc.services.cdc.gov/) known to public health within a single application.

Data regarding occurrences of these conditions, which are identified by the [National Notifiable Disease Surveillance System (NNDSS)](https://health.gov/healthypeople/objectives-and-data/data-sources-and-methods/data-sources/national-notifiable-diseases-surveillance-system-nndss#:~:text=The%20National%20Notifiable%20Disease%20Surveillance,state%2Dreportable%20and%20nationally%20notifiable), are sent from the affected patient’s EHR to [Public Health Agencies (PHAs)](https://ecr.aimsplatform.org/public-health-agencies/) using the CasePointer platform. These PHAs then use the software tools for disease surveillance, contact tracing, outbreak management, and most importantly to prevent the spread of disease within their communities. Once these cases reach a certain status, they must be reported by the PHA to the CDC.

The CasePointer system standardizes the healthcare data involved in this process securely and efficiently. Its features greatly simplify the ever-increasing complexity that competing products like HIEs have struggled to contain. CasePointer is already implemented in three states, with a fourth in progress as of this writing. The final part of this series will provide a closer look into CasePointer’s unique approach at standardizing healthcare data, becoming a long-awaited hope in the Pandora’s box of public health.

### Become a Part of the Evolution

If this series has piqued your curiosity and you’d like to learn more about CasePointer by End Point, or how our team is building the next evolution of customized healthcare data solutions, contact us at [ask@endpointdev.com](mailto:ask@endpointdev.com). We’d love to support your efforts to protect the well-being of people and communities you care about!
