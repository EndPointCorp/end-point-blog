---
author: "Dan Briones"
title: "What is SharePoint?"
tags: tools
gh_issue_number: 1608
---

![Web servers](/blog/2020/03/25/what-is-sharepoint/servers.jpg)

[Image](https://unsplash.com/photos/M5tzZtFCOfs) by [Taylor Vick](https://unsplash.com/@tvick)

People often ask me about SharePoint, Microsoft’s browser-based collaboration platform which allows users to upload and share all kinds of documents, images, messages, and more. The product has nearly two decades of history and there are still many who don’t know much about it.

The SharePoint platform has grown over those years, but its capabilities have expanded in such a way that it can be quickly dismissed from consideration out of fear of the complexity of its implementation and the cost of deployment. These fears may be unfounded, however. Especially if you are already on Office 365, SharePoint may be included in your plan.

SharePoint was designed as a framework to create and share content on the web without the need to write code. Its purpose was to allow everyone in the organization to collaborate without any specific programming skills. This framework grew over time, adding many different types of content allowing for interactions with other frameworks increasing the effectiveness of any organization’s work product or intellectual property and communications.

### Flavors of SharePoint

There are two ‘flavors’ of SharePoint. You can use Microsoft’s cloud-based service or you can host your own on-premises server farm. But I suspect Microsoft’s preference is to wrangle organizations into the cloud, as seen in Microsoft’s SharePoint 2019 online documentation which casually omits references to the on-premises server product. Microsoft offers an inexpensive per-user SharePoint cloud service license for those organizations that don’t want to use Office 365’s other offerings.

On the other hand, on-premises SharePoint Server licensing is very expensive, especially if you wish to design for high availability and create a well-balanced SharePoint server farm. This requires CALs (Client Access Licenses) as well. But the cloud licensing model is very attractive in pricing, especially if you are planning to move your organization’s Exchange email into the Office 365 offering because SharePoint licensing is included in the top two Business tiers and all the Enterprise licensing plans.

### Intranets

Over the years I have helped many small- to medium-sized businesses create their intranets using both on-prem SharePoint servers and the SharePoint Online offering, mostly to leverage document management features and their content search capabilities. SharePoint is very good at indexing all Microsoft Office formats, data and metadata, allowing for the inclusion of custom extended tags that can be applied to files and folders to further categorize them and make them easy to organize and find. It also indexes content and metadata from readable PDF format.

Because the environment is highly customizable or “brandable”, companies quickly expand on its use once they are introduced to its basic capabilities. I’m often surprised by how creative non-technical staff can be as they come up with new ways to use the platform.

SharePoint is also a secure way to share documents on a variety of devices including mobile, via the web, leveraging Active Directory or SAML compliant single-sign on (SSO) services like Okta, OneLogin, or Duo for authentication. The framework has its own content permission group capabilities that are simple to manage without giving content-managers access to AD or auth servers. This framework is attractive because it provides, without much training, the ability for employees to create and share content with granular permissions, manage data and custom lists, and create individual web pages or entire sites within the Portal.

### SharePoint Sites

Let’s discuss SharePoint Sites. SharePoint allows users with permissions to create individual pages or entire “Team Sites” to organize and secure content with permissions that the site creator can define. The ability to create content and assign these permissions within the organization or with external partners or customers can be delegated by an administrator to team leaders who wish to control their own content. However, global administrators retain the control to secure the company’s data and intellectual property via built-in tools, policies, auditing, and alerts. There is also a reporting system for compliance reporting.

Sites can contain an assortment of content types. Team managers can simply pick from a list of available components, including document and photo libraries, and custom lists that are created much like Excel tables to hold data for distribution, such as employee directories, product lists, and inventory items. Sites can also contain other shared resources such as Wikis, calendars, tasks, issue tracking, and OneNote notebooks. Sites can contain components you can create yourself with Visual Studio leveraging the API. Each site can also hold its own set of usage statistics and workflow management for teams to optimize and hone both performance and effectiveness of the data shared. In my experience sales, finance, and HR teams benefit the most from these ready-made components, but all manner of teams can find useful tools on this platform.

### Power Apps, Power Automate (Flow)

Each SharePoint release adds to its predecessor’s core functionality. One such example is “Power Apps”, an add-on service that allows using external data sources capable of interacting with the built-in lists and library components without coding, by establishing connectors and forming mobile content pages.

Another called “Power Automate” (formerly known as “Flow”) can reduce repetitive tasks by using a simple visual designer for scripting actions that respond to triggered events. This varied set of tools also integrates seamlessly with not just the base Office products like Word, Excel, and PowerPoint, but also with Teams and OneNote and even other major services like Exchange and Dynamics. This increases the collaboration options for a mobile workforce regardless of the device or OS they use. This is a very powerful tool for organizations needing to collaborate across different platforms and around the world.

### Mobile

There are currently native mobile apps that are free on iOS and Android for mobile access to SharePoint content. This provides an additional layer of security and also compartmentalizing for Mobile Device Management (MDM) systems that run business content in a separate and encrypted container for work on these devices. This may include systems like IBM’s Maas360, SOTI MobiControl, Citrix XenMobile, AirWatch by VMware or Microsoft’s own Microsoft Intune.

With all these out-of-the-box capabilities, SharePoint is perfect for intranet portals, group sites that can be created and managed without any programming experience or knowledge. But if you have the skill set, the entire framework and all its capabilities are created upon a well-documented and time-tested API, with which a person can easily expand with web components that can be created via Visual Studio, Microsoft’s own IDE (Integrated Development Environment), and in several programming languages, allowing integration with other Microsoft API frameworks like MS SQL Server, Exchange, and Dynamics.

### Keeping up with content changes

All this functionality and capability sometimes intimidates some businesses. It would seem that you could easily overwhelm your users. To combat that, the whole system, at every level, allows users to “follow” content. This is functionality that has been in the platform since inception and is one of my favorite features. For every page, every site or component at any level, users have the ability to subscribe to content. You can follow with one click any document and be notified in your portal homepage or via notifications of actions taken or content changed. This means that you can allow people to be as connected as they feel they need to be. Nobody needs to suffer from information overload or out-of-control mobile notifications.

### We can help!

If you are already a Microsoft Office 365 subscriber, odds are you already have access to this incredible tool without any additional cost. How can you leverage this for your business? Visit the following content, or [contact us](/contact) at End Point for additional information.

- [The SharePoint Community](https://techcommunity.microsoft.com/t5/sharepoint/ct-p/SharePoint)
- [SharePoint Developer Network](https://developer.microsoft.com/en-us/sharepoint)
- [SharePoint online training](https://support.office.com/en-us/article/sign-in-to-sharepoint-online-324a89ec-e77b-4475-b64a-13a0c14c45ec?ui=en-US&rs=en-US&ad=US)
