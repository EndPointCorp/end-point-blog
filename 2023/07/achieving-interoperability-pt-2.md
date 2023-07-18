---
title: "Achieving Interoperability, Part II: Combating the Curse: Interoperability’s Quest for a Solution"
author: Jarrett Smolarkiewicz
tags:
- casepointer
date: 2023-07-13
---

### Expanding on Part I of the Achieving Interoperability Series

This piece marks the second article in the Achieving Interoperability series, which is designed to raise awareness of the complex and pressing challenges involved with standardizing healthcare data within the United States. Each part of the series is listed below:

* Part I: Pandora’s Box and the Problem of Healthcare Data Standardization
* Part II: Combating the Curse: Interoperability’s Quest for a Solution
* Part III: A New Hope: CasePointer’s Unique Standardization Approach

Part I introduced the problem of healthcare data standardization, and paralleled it with the myth of Pandora’s Box. Those not familiar with this story can find a brief summary under the section titled “In mythology” in the Wikipedia article named, “Pandora’s box”. Regardless of your familiarity, the most important piece of information to note is where Wikipedia states: 

“From this story has grown the idiom ‘to open a Pandora's box’, meaning to do or start something that will cause many unforeseen problems."

Decades ago, when healthcare providers, software engineers, public health officials, and others set out to provide a means of efficiently transmitting healthcare data across the variety of digital networks within the United States, they unintentionally unleashed a host of healthcare data standards that were designed to help, but have come to haunt and hinder the industry in the years since their inception. Part II of this series walks through the efforts and approaches that have been used to address these challenges, while Part III covers End Point’s involvement in developing an effective solution.

### Unintended Consequences

Upon opening the box entrusted to her care, Pandora wrestled with some regrets as to the resulting consequences of her actions. This is evident in versions of the story where, after all the troublesome things are released from the box, she quickly shuts it, accidentally trapping hope inside. The good news in the healthcare industry is that while we now live in a world where several healthcare data standards actively exist and make achieving interoperability more complicated, several groups of talented individuals are currently in hot pursuit of a definitive solution. In the story of healthcare data standardization, all hope is not lost.

### Applications Abound

As data standards have been introduced, adopted, and revised over the years, they have been integrated into the increasing number of industry software systems being utilized across the nation. While networks of hospitals and laboratories typically set up Electronic Health Record (EHR) platforms built by companies like Cerner or Epic to manage patient data, Public Health agencies require additional applications that can aid in the identification, tracking, and reporting of certain health conditions from those patient EHR’s. Different state and regional jurisdictions have taken different approaches to accomplish this. Many look to free software offered by the Centers for Disease Control and Prevention (CDC). Some partner with one or more consulting firms to implement the highly specialized networks of applications they require. Still others opt to develop, customize and maintain everything in-house. This has led to so many unique software installations, that when the need arises for them to communicate and transmit healthcare data with each other it seems all but impossible!

### The Quadratic Cost Problem

Getting so many diverse software systems to work together is extremely difficult due to a phenomena known as the Quadratic Cost Problem. This occurs as the need for bi-directional connections between individual software applications increases exponentially (instead of linearly), with each component added to a healthcare data system. The United States government is a hierarchy of Federal, State, Regional, Local, Tribal, and other specialized governing bodies that make decisions on which software they will use to protect the public health of their communities. Since these groups each have varying needs and do not always implement the same technology, when they have to work together to track and resolve health concerns they are faced with the staggering costs of building and supporting all the bi-directional connections that are a symptom of the Quadratic Cost Problem. If this concept still seems unclear, or you’re simply curious to learn more, a digital training and events firm known as TechChange breaks down this concept and more in a video called Standards and Interoperability in Digital Health: Explained (FULL). 

### Health Information Exchange Advantages

As government and healthcare collide, one attempt technology has made at bringing about order and harmony is through connecting the applications of each jurisdictional segment within a larger governing body to a centralized Health Information Exchange (HIE). An example of this would be an individual state public health organization connecting its own software to an HIE, along with the software currently in use by each local jurisdiction within that state. Each jurisdiction does not have to utilize the same software, but can communicate between platforms using its connection to the HIE vs. individual bi-directional connections to every other application used throughout the state. HIE’s also aim to leverage their centrality to overcome the Quadratic Cost Problem. Since it acts as a single hub connecting all other systems, an HIE is the only component that needs to be updated when changes occur in one of the other connected applications. As great as this all sounds, some drawbacks accompany HIE solutions. 

### Health Information Exchange Challenges

The individual applications connected to the central HIE must diligently ensure they maintain compatibility for this solution to prove effective. As with any complex software architecture, connections that work today can break tomorrow. When an HIE is upgraded to maintain its connectivity with another recently updated app in the ecosystem, the updates can inadvertently cause issues with other connected apps that had no prior problems. In addition to compatibility struggles, HIE’s rely on the presence of a universal set of standards to which they conform all other data in the workflow. An HIE scenario used in the TechChange video referenced earlier, assumes that the HIE implementation will seamlessly handle all healthcare data standards bundled together for an entire governing body. While this may seem intuitive and logical, it is unfortunately not the reality, given the numerous interoperability standards within the United States. These varying standards can also put the privacy and security of patient data being transmitted at risk. This brings about additional legal concerns with regard to HIPAA regulations. 

### Decades of Stagnation

Chapter four of the book: Patient Safety: Achieving a New Standard for Care, identified this concern by stating, “The fact that there is no standard means of representing the data for any of these datasets or requirements is astonishing and highlights the amount of unnecessary work performed by health care and regulatory organizations to prepare, transmit, and use what amount to custom reports.” Nearly 20 years after those words were written, and almost a decade after the FHIR standard was introduced, the variety of standards and systems has not narrowed to a set of standards that any HIE could use to universally coordinate healthcare data within the United States. Without a unified data standard, the power of the HIE falls flat.

### Hope on the Horizon

Thankfully, a new evolution of public health technology is emerging, known as CasePointer by End Point. This system unifies many components, including the EpiTrax application, which can handle all 170+ reportable health conditions known to public health within a single application. Data regarding occurrences of these conditions, which are identified by the National Notifiable Disease Surveillance System (NNDSS), are sent from the affected patient’s EHR to Public Health Agencies (PHA’s) utilizing the CasePointer platform. These PHA's then use the software tools for disease surveillance, contact tracing, outbreak management and most importantly to prevent the spread of disease within their communities. Once these cases reach a certain status, they must be reported by the PHA to the CDC. The CasePointer system standardizes the healthcare data involved in this process securely and efficiently. The system’s features greatly simplify the ever-increasing complexity that competing products like HIE’s have struggled to contain. CasePointer is already implemented in three states, with a fourth in progress as of this writing. The final part of the achieving interoperability series will provide a closer look into CasePointer’s unique approach at standardizing healthcare data, and becoming this country’s long-awaited hope in the Pandora’s box of Public Health.

### Become a Part of the Evolution

If this series has piqued your curiosity, and you’d like to learn more about CasePointer by End Point, or how our team is building the next evolution of customized healthcare data solutions, contact us at: ask@endpointdev.com We’d love to support your efforts to protect the well-being of people and communities you care about!

### Article Resources

* CDC Works 24/7. (2023, April 17). The Centers for Disease Control and Prevention. Retrieved April 18, 2023, from https://www.cdc.gov/ 
* EHR interoperability challenges and solutions. (2022, December 6). EHR in Practice. Retrieved April 7, 2023, from https://www.ehrinpractice.com/ehr-interoperability-challenges-solutions.html 
* Epi InfoTM | CDC. (2022, September 16). The Centers for Disease Control and Prevention. Retrieved April 14, 2023, from https://www.cdc.gov/epiinfo/index.html 
* Epic | . . .with the patient at the heart. (2023). Epic. Retrieved April 14, 2023, from https://www.epic.com/
* EpiTrax. (2023). End Point Dev. Retrieved April 14, 2023, from https://www.endpointdev.com/expertise/epitrax/ 
* HL7 Standards Product Brief - FHIR® (HL7 Fast Healthcare Interoperability Resources) | HL7 International. (2023). Health Level Seven International. Retrieved April 14, 2023, from https://www.hl7.org/implement/standards/product_brief.cfm?product_id=491 
* Home | Oracle Cerner. (2023). Oracle Cerner. Retrieved April 14, 2023, from https://www.cerner.com/ 
* National Academies Press (US). (2004). Health Care Data Standards. In Patient Safety - NCBI Bookshelf. https://www.ncbi.nlm.nih.gov/books/NBK216088/ 
* National Notifiable Diseases Surveillance System (NNDSS) - Healthy People 2030 | health.gov. (n.d.). Healthy People 2030. Retrieved April 14, 2023, from https://health.gov/healthypeople/objectives-and-data/data-sources-and-methods/data-sources/national-notifiable-diseases-surveillance-system-nndss#:~:text=The%20National%20Notifiable%20Disease%20Surveillance,state%2Dreportable%20and%20nationally%20notifiable 
* Privacy, Security, and Electronic Health Records. (n.d.). hhs.gov. Retrieved April 14, 2023, from https://www.hhs.gov/sites/default/files/ocr/privacy/hipaa/understanding/consumers/privacy-security-electronic-records.pdf 
* Public health agencies. (n.d.). APHL Association of Public Health Laboratories. Retrieved April 18, 2023, from https://ecr.aimsplatform.org/public-health-agencies/ 
* Secure Business Solutions. (2023). End Point Dev. Retri
