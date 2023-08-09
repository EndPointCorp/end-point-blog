---
title: "Achieving Healthcare Data Interoperability"
author: Jarrett Smolarkiewicz
github_issue_number: 1973
tags:
- casepointer
- epitrax
- emsa
date: 2023-07-28
featured:
  casepointer: true
  image_url: /blog/2023/07/achieving-healthcare-data-interoperability/a_stream_running_between_houses_and_a_road.webp
---

![An impressionist watercolor scene of two red-roofed farm houses with a tree-lined path leading forward on the left side of the image. The brushstrokes are very loose.](/blog/2023/07/achieving-healthcare-data-interoperability/a_stream_running_between_houses_and_a_road.webp)

<!-- Image: Johan Barthold Jongkind, A Stream Running between Houses and a Road, 19th century. Public domain under CC0. -->

### Background

For many years, healthcare providers, public health experts, and software developers have been hard at work on standards and methods for interconnecting systems to share vast and ever-expanding patient and lab data.

In the late 1980s the non-profit organization Health Level Seven International released the HL7 data standard. That was updated many times up to the year 2007 with [HL7 v2.5.1](https://www.hl7.org/implement/standards/product_brief.cfm?product_id=144) which is still widely used today.

New healthcare data standards have emerged, including [HL7 v3](https://www.hl7.org/implement/standards/product_section.cfm?section=14), the Consolidated Clinical Document Architecture ([C-CDA](https://www.hl7.org/implement/standards/product_brief.cfm?product_id=492)), the Fast Healthcare Interoperability Resource ([FHIR](https://www.hl7.org/implement/standards/product_brief.cfm?product_id=491), pronounced "fire"), and more. These are not yet as broadly adopted as HL7 v2.5.1.

Under the Health Insurance Portability and Accountability Act of 1996 ([HIPAA](https://www.hhs.gov/sites/default/files/ocr/privacy/hipaa/understanding/consumers/privacy-security-electronic-records.pdf)), most of this data is classified as PII (personally identifiable information) and/or PHI (personal health information) and must be kept secure and protected at all times, so that it will not be accessed without proper authorization or patient consent.

### The data dilemma

Healthcare data systems now routinely communicate in many ways, but there are sometimes incompatibilities when patient data travels from one system to another.

The U.S. Centers for Disease Control (CDC) encourages and sometimes incentivizes, but does not mandate, adoption and implementation of common standards. So each jurisdiction's public health agency (PHA), lab, and vendor may be using different and only partially overlapping standards.

Different labs, doctors, and public health workers use varying conventions for things like facility names and lab codes, which presents problems for interpreting and reporting data. For example, “KU MAIN” may be recognized as the main campus of the University of Kansas Medical Center in nearby communities or states, while providers elsewhere may not recognize this code, or may mistake it for a similarly named facility in their area. The University of Kansas Health System consists of a large network of satellite facilities that span the states of Kansas and Missouri, rather than just one location in a single state. This may create additional confusion about which state jurisdictions should be involved.

This semantic category is called a vocabulary, and if two systems use incompatible vocabulary, one of them, or an intermediary, must have a mapping from the terms in one vocabulary to another.

The syntactic category of challenge is called a grammar, and covers the kinds of message types and actions a system works with.

An article published in December 2022 by Dr. Naheed Ali identifies “inconsistent data and lack of standardized data structure” as the number one issue to be overcome regarding the [Electronic Health Record (EHR)](https://www.healthit.gov/faq/what-electronic-health-record-ehr) interoperability challenges facing healthcare professions today:

> One of the biggest EHR interoperability challenges in healthcare interoperability is managing inconsistent data from multiple sources. Information stored in different databases can have a variety of formats and data types that are not easily compatible with one another. A single record may contain different information about a patient's medical history or treatment plan, making it more difficult for different systems to interpret correctly.  
> —Dr. Naheed Ali, [EHR Interoperability Challenges and Solutions](https://www.ehrinpractice.com/ehr-interoperability-challenges-solutions.html)

### Cooperating for a healthier future

Although great strides have been made to digitize healthcare data and improve interoperability, much remains to be done. Newer standards (like HL7 FHIR, released in 2014) face an uphill battle for industry adoption to become as widely utilized as HL7 v2.5.1 (from 2007) and C-CDA (from 2011).

While networks of hospitals and laboratories typically set up EHR platforms built by companies like Cerner or Epic to manage patient data, public health agencies require additional applications to aid in the identification, tracking, and reporting of reportable health conditions from those patient EHRs.

Public health services in the United States are provided by various federal, state, tribal, territorial, regional, municipal, and other bodies that decide which software they will use to support their communities. Some look to software offered by the CDC or software firms to provide the application functions they require. Others contract with consulting firms to develop custom software. Still others opt to develop and maintain everything in house.

Getting so many diverse software systems to work together is difficult due to a phenomenon known as the quadratic cost problem. This occurs when the need for bi-directional connections between software applications increases exponentially, instead of linearly, with each component added to a system.

An organization called TechChange explains this concept and more in their video [Standards and Interoperability in Digital Health: Explained](https://www.youtube.com/watch?v=KSEUh-wj7Y0).

The book [Patient Safety: Achieving a New Standard for Care](https://www.ncbi.nlm.nih.gov/books/NBK216088/) identifies in chapter 4 this concern:

> The fact that there is no standard means of representing the data for any of these datasets or requirements is astonishing and highlights the amount of unnecessary work performed by health care and regulatory organizations to prepare, transmit, and use what amount to custom reports.

Nearly 20 years after those words were written, and almost a decade after the FHIR standard was introduced, the variety of standards and systems has not narrowed. Change is difficult.

### Health Information Exchanges

One architectural attempt to simplify data sharing is by connecting applications of each jurisdictional segment within a larger governing body to a centralized [Health Information Exchange (HIE)](https://www.healthit.gov/topic/health-it-and-health-information-exchange-basics/what-hie).

An example of this would be an individual state public health organization connecting its own software to an HIE, along with the software currently in use by each local jurisdiction within that state. Each jurisdiction does not have to use the same software, but can communicate by using its connection to the HIE rather than individual bi-directional connections to every other application used throughout the state.

This sounds like just what is needed, and likely is for some use cases.

But HIEs generally work at the syntactic (grammar) level. Many HIEs have agreements with the facilities they serve, that they will not change the content of messages in any way. Unfortunately that means most HIEs essentially work as a passthrough.

They thus are helpless when it comes to the wide variety of nonstandard content semantics that they encounter, and have no way of correcting vocabularies, so they pass on junk data.

Even a small, steady volume of unusable messages can at best clog up manual review queues and overwhelm already overworked staff, and at worst give a false sense that all data are being ingested and reported on, when they are not.

Something like an HIE that is capable of semantic (vocabulary) inspection, translation, and rule-based routing, customizable per reporter for the jurisdiction's changing needs, is called for.

### The CasePointer software suite

We at End Point are solving the interoperability problem for our client jurisdictions’ public health disease surveillance with [CasePointer](https://www.casepointer.com), a new suite of proven open source software. It interoperates with many other systems, including HIEs, and is configurable to map varying local data conventions into a single system that routes messages and reporting as needed.

#### EpiTrax disease surveillance system

We began in 2008 to work with software for public health using the open-source TriSano disease surveillance system.

In 2017, the Utah Department of Health and Human Services (DHHS) released a new open source disease surveillance application called [EpiTrax](/expertise/epitrax/) to replace their use of TriSano. EpiTrax is a more capable, comprehensive, and supportable application that supports [all 170+ reportable health conditions](https://ndc.services.cdc.gov/) identified by the [National Notifiable Disease Surveillance System (NNDSS)](https://health.gov/healthypeople/objectives-and-data/data-sources-and-methods/data-sources/national-notifiable-diseases-surveillance-system-nndss).

As open source software, we and others can use it, extend its capabilities, and contribute back to a shared source code repository.

Today EpiTrax serves as the central application within the CasePointer suite.

#### EMSA preprocessing powerhouse

The separate application [Electronic Message Staging Area (EMSA)](/expertise/emsa/) was also designed by the team at Utah DHHS to work in tandem with EpiTrax. EMSA ingests electronic case and lab reports (eCRs & ELRs) from various reporters and allows public health organizations to create extremely powerful custom configurations capable of message inspection, semantic (vocabulary) mapping and transformation, and routing, tailored to each jurisdiction's needs and preferences.

Once these EMSA rules are set up, the healthcare data can flow continuously while automatically being pre-processed by EMSA according to its matching jurisdiction with minimal manual intervention by the area's public health agency. PHA staff can focus on their primary objective: investigating and tracking disease to protect the health of their community.

Investigators can customize their individual dashboards within EpiTrax to analyze, sort, trace, and process the data prepared by EMSA in the way that is most efficient for them. Working together, these two powerhouse applications provide the cost and time saving benefits that public health organizations around the country need.

#### NMI automatic CDC reporting

Once a public health case reaches a certain status within EpiTrax, certain data must be reported per current requirements of the CDC. Historically, this has been a manual and tedious process for investigators involving referencing a text file with the latest CDC guidelines as they process these reports.

More recently, the [NNDSS Modernization Initiative (NMI)](https://www.cdc.gov/nndss/about/history.html) by the CDC has provided options for a much more automated method of reporting the necessary case data. This is a critical part of the process for PHAs, as they receive funding for their organization based on their ability to meet CDC reporting requirements and interoperability standards.

The NMI module is integrated into the CasePointer workflow to ensure that once data reporting has been configured for a case, any updates will be automatically sent to the CDC without additional manual processing.

#### CasePointer Disease Reporting Portal

During COVID-19, nontraditional reporters such as pharmacies, university health centers, community drive-up testing centers, and others not part of our state clients' formal public health infrastructure, needed to be able to submit test results to the state.

We developed a specialized disease reporting portal, initially focusing on COVID-19, to accept simple batch uploads of test results and, based on changing policy, to forward test data to the disease surveillance system. This separate system had no access to the main EpiTrax disease surveillance system, or to any other reporters' data.

### Bringing it all together

CasePointer provides two prominent strengths:

* First, its ability to map the endless local conventions used by those reporting the data into a unified standard for the rest of the workflow.
* Second, the customizability and agility of the CasePointer applications are unique among available disease surveillance solutions.

CasePointer puts the ability to customize data collection and surveillance in the hands of the public health experts. New fields can be added into an investigation form with the click of a button. The ability to quickly pivot and document disease information is critical in a quickly changing public health landscape.

### Join the evolution of public health technology

Such highly configurable, unified, robust tools can be a game changer for public health jurisdictions in need of an affordable, extensible solution that meet all their needs. CasePointer can even work to further streamline systems that are already integrated with an HIE.

Within the United States, four states have already partnered with us to implement EpiTrax. We are helping them reduce unnecessary manual data processing costs, more effectively manage caseloads, and further automate their data workflows.

If this piqued your curiosity, visit [our CasePointer website](https://www.casepointer.com/) and [contact us](https://www.casepointer.com/contact/) to learn more about CasePointer and how our team is evolving public health support with customized data solutions.

We would love to support your efforts to protect the well-being of people and communities you care about!
