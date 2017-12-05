---
author: Josh Tolley
gh_issue_number: 212
tags: books, java, pentaho
title: Pentaho Reporting 3.5 for Java Developers
---



I was recently asked to review a copy of Will Gorman's [Pentaho Reporting 3.5 for Java Developers](http://www.packtpub.com/pentaho-reporting-3-5-for-java-developers?utm_source=blog.endpoint.com&utm_medium=bookrev&utm_cont+ent=blog&utm_campaign=mdb_000670), and came to a few important realizations. Principle among these is that my idea of what "reporting" means includes far too little. Reporting includes much more than just creating a document with some graphs on it -- any document or presentation including information from a "data source" comprises a "report". This includes the typical sheaf of boardroom presentation slides, but also includes dashboards within an application, newsletters, or even form letters. I recently discovered that a local church group uses a simple reporting application to print its membership directory. In short, it's not just the analysts and managers that can use reporting.

The book gives the reader a tour of Pentaho's newest Pentaho Reporting system, which consists of a desktop application where users define reports, and a library by which developers can integrate those reports into their own applications. So as an example, not only can Pentaho Reporting publish weekly sales printouts, but it can also produce real-time inventory information in a J2EE-based web application or even a Swing application running on a user's desktop. Gorman describes, step-by-step, the process of building a report, integrating advanced data sources, working with graphics and visualizations, and building custom reporting components such as user-defined functions and custom report controls. Although this step-by-step description combined with Java's native verbosity occasionally make it difficult to read cover to cover, it provides a valuable reference and starting point for users wanting to implement advanced reporting features.

Shortly after having grasped the idea that "reporting", as a concept, was broader than I'd originally assumed, I got the idea that I'd like to know how to use Pentaho to replace a reporting system I worked on a while ago, which used Jython to gather data from a JMX server. Pentaho Reporting allows users to create data sources in languages other than Java, via the [Apache Bean Scripting Framework](http://jakarta.apache.org/bsf/), suggesting that my old Jython code might work mostly unchanged via Bean Scripting. Disappointingly, the book doesn't give an example of this technique, but since the Bean Scripting integration is still considered experimental (along with, apparently, several other data source types, contributed by the Pentaho community). Perhaps I'll figure this out one day, and make it the subject of a future blog post.

This fairly slight omission notwithstanding, I enjoyed the book and the ideas it suggested about places I might apply more interesting reporting. Thanks to PacktPub for the opportunity to review it.


