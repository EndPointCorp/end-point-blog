---
author: "Selvakumar Arumugam"
title: "Why Upgrading Software Libraries is Imperative"
tags: software, update
gh_issue_number: 1638
---

![](/blog/posts/2020/06/10/why-upgrading-software-libraries-is-imperative/image-0.jpg)

[Image](https://unsplash.com/photos/PlBsJ5MybGc) by [Tolu Olubode](https://unsplash.com/@toluobde) on [Unsplash](https://unsplash.com)

Applications primarily run on front- and back-end programming languages, including necessary library dependencies. Operating Systems and programming languages can be periodically updated to run on the latest version, but what about the many libraries being used in the app’s front and backend? As we all know, it can be quite a daunting task to maintain and individually update a long list of software dependencies like the examples later in this post. Still, it is important to keep them updated. This post dives into our experience upgrading a complex app with a full software stack and lots of dependencies. We’ll examine the benefits of upgrading, what you will need, and how to go about such an upgrade as simply as possible below.

The app in question contained decade-old software and included extensive libraries when we received it from our client. The app used languages including Java, Scala, Kotlin, and JavaScript along with many libraries. The initial plan was to upgrade the complete software stack and libraries all at once due to the gap between versions. This proved to be more difficult than expected due to a host of deprecated and removed functionalities as well as interdependence of a few of the libraries.

### Conflict approach: “Don’t update unless you have to”
While this can be sustainable in the short term, it quickly becomes less applicable in the long run. One important purpose of updates is to (hopefully) protect from new vulnerabilities and cyber attacks. Scenarios arise where particular library fixes are implemented on the latest version, yet require upgrading other libraries to the latest version in a chain. Because upgraded libraries need extensive testing and preparation for new issues, this directly impacts whether the app attempts to resolve an issue. Therefore, smaller and more frequent updates are more sustainable in the long run. Larger and more infrequent upgrades will not only result in unexpected errors, but also require regression testing to deliver a bug-free update. The following reasons justify the necessity of software and library upgrades:

* They apply timely security patches to reduce vulnerabilities and defend from cyberattack
* You can identify deprecated functionality earlier and use alternatives
* They can apply fixes for known bugs in the library
* They’re based on the latest versions of software or library, encouraging stability

In addition, staying on the latest major version yields the benefit of applying minor and patch releases seamlessly without risk. Most software and libraries use semantic versioning, formatted as MAJOR.MINOR.PATCH (examples below).

* MAJOR version - Incompatible API changes
* MINOR version - Add functionality with backward compatiblity
* PATCH version - Bug fixes with backward compatibility

So being on the latest major versions of libraries makes applying minor and patch releases without breaking existing functionalities of the app.

### Benefits
The benefits of keeping software and libraries updated include bug fixes, new features, boosted performance, as well as better stability, compatibility, and security measures. We can often ignore upgrades in projects because we don’t perceive significant effects in appearance or usage. But on closer inspection, frequent updates deliver advantages which clearly demonstrate the importance of upgrading software libraries.

### Real-time difficulties
In real-life scenarios, bug fixes and performance optimization of an app often take a higher priority than upgrading libraries. In many cases, this results in a discrepancy between the app’s version and the current version. This discrepancy can lead to the following issues when upgrading libraries:

* Unexpected error handling in new releases
* Unexpected unsupported library dependency errors
* Need for complete end-to-end testing due to major version of library upgrade
* Lack of demonstration of work being done can lead to a lack of confidence from client
* Difficulty in estimating workload due to major unexpected errors

The following passages offer guidance in how to adequately prepare for these issues.

### Get prepared
Much can be learned from a major upgrade on both a business and technical level, so being prepared for such an endeavor is imperative. First, a complete list of libraries from the entire app should be compiled. This list should include the latest and current version of the library in the app. Reviewing the changelog of both versions will help identify potential incompatibilities or problems. Visiting the “issue report page” of the library to monitor any version-specific issues is also recommended. Once you’ve adequately prepared the libraries for upgrading, you can use any method of your choosing to upgrade and maintain the list. Once the roadmap is established, upgrading can commence and compatibility issues that arise can be dealt with in real time. Finally, thorough end-to-end testing is necessary once the upgrade process is complete.

Below are some examples of software lists you might have for a project (we left out the latest versions for brevity in this post, but it’s helpful to have a column for those too!).

##### Programming software & servers

<table><tbody>
<tr><th>Software</th><th>Current</th><th>Release date</th></tr>
<tr><td>Ubuntu</td><td>12.04.5</td><td>2017-04-28</td></tr>
<tr><td>nginx</td><td></td></tr>
<tr><td>Jetty Java Servlet container</td><td>9.2.3</td><td>2014-09-05</td></tr>
<tr><td>JVM/Java</td><td>1.7 </td><td></td></tr>
<tr><td>Scala</td><td>2.11</td><td>2014-04-21</td></tr>
<tr><td>Kotlin</td><td>0.9.223</td><td>2014-10-23</td></tr>
<tr><td>Lucene</td><td>4.10.0</td><td>2014-09-03</td></tr>
<tr><td>PostgreSQL</td><td></td><td></td></tr>
</tbody></table>

##### Java libraries

<table><tbody>
<tr><th>Software</th><th>Current</th><th>Release date</th></tr>
<tr><td>joda-convert</td><td>1.3.1</td><td>2013-03-01</td></tr>
<tr><td>joda-time</td><td>2.2</td><td>2013-03-01</td></tr>
<tr><td>play-json</td><td>2.11</td><td></td></tr>
<tr><td>httpclient</td><td>4.1.2</td><td>2011-07-10</td></tr>
<tr><td>httpcore</td><td>4.1.2</td><td>2011-07-22</td></tr>
<tr><td>httpmime</td><td>4.1.2</td><td>2011-07-29</td></tr>
<tr><td>commons-codec</td><td>1.3</td><td>2005-10-01</td></tr>
<tr><td>jooq</td><td>3.1.0</td><td>2013-06-30</td></tr>
<tr><td>jooq-codegen</td><td>3.1.0</td><td>2013-06-30</td></tr>
<tr><td>jooq-meta</td><td>3.1.0</td><td>2013-06-30</td></tr>
<tr><td>jtds</td><td>1.3.0</td><td>2012-10-27</td></tr>
<tr><td>servlet-api</td><td>3.1</td><td>2013-04-25</td></tr>
<tr><td>play-json-joda</td><td>2.11-2.6.9</td><td>2018-03-01</td></tr>
<tr><td>lucene-core</td><td>4.10.0</td><td>2014-09-02</td></tr>
<tr><td>lucene-memory</td><td>4.10.0</td><td>2014-09-02</td></tr>
<tr><td>lucene-queries</td><td>4.10.0</td><td>2014-09-02</td></tr>
<tr><td>lucene-queryparser</td><td>4.10.0</td><td>2014-09-02</td></tr>
<tr><td>lucene-highilghter</td><td>4.10.0</td><td>2014-09-02</td></tr>
<tr><td>lucene-analyzers-common</td><td>4.10.0</td><td>2014-09-02</td></tr>
<tr><td>postgresql</td><td>9.2-1003-jdbc4</td><td>2013-05-27</td></tr>
<tr><td>jsoup</td><td>1.7.3</td><td>2013-11-11</td></tr>
<tr><td>jetty-util</td><td>9.2.5.v20141112</td><td>2014-11-12</td></tr>
<tr><td>tika-core</td><td>1.16</td><td>2017-07-07</td></tr>
<tr><td>commons-fileupload</td><td>1.3</td><td>2013-03-24</td></tr>
<tr><td>commons-beanutils</td><td>1.6</td><td>2005-11-08</td></tr>
<tr><td>commons-collections</td><td>2.1</td><td>2005-11-08</td></tr>
<tr><td>commons-digester</td><td>2.1</td><td>2010-09-24</td></tr>
<tr><td>commons-io</td><td>1.1</td><td>2005-11-24</td></tr>
<tr><td>commons-lang</td><td>1.0.1</td><td>2005-11-24</td></tr>
<tr><td>commons-logging</td><td>1.0.3</td><td>2005-11-17</td></tr>
<tr><td>commons-validator</td><td>1.0.2</td><td>2005-11-24</td></tr>
<tr><td>slf4j-api</td><td>1.6.4</td><td>2011-10-31</td></tr>
<tr><td>slf4j-nop</td><td>1.6.4</td><td>2011-10-31</td></tr>
</tbody></table>

##### JavaScript libraries

<table><tbody>
<tr><th>Software</th><th>Current</th><th>Release date</th></tr>
<tr><td>angular</td><td>1.2.11</td><td>2014-02-03</td></tr>
<tr><td>jQuery</td><td>1.10.2</td><td>2013-07-03</td></tr>
<tr><td>calendar</td><td>1.51</td><td>2005-03-07</td></tr>
<tr><td>calendar-en</td><td></td><td></td></tr>
<tr><td>calendar-setup</td><td>1.25</td><td>2005-03-07</td></tr>
<tr><td>fckeditor</td><td>-</td><td></td></tr>
<tr><td>dom-drag</td><td></td><td>2001-10-28</td></tr>
<tr><td>jt_</td><td></td><td></td></tr>
<tr><td>jt_DialogBox</td><td>2007-08-23</td><td></td></tr>
<tr><td>jt_AppDialogs</td><td>2005-04-09</td><td></td></tr>
<tr><td>dialog_box</td><td></td><td></td></tr>
<tr><td>ng-grid</td><td>2.0.7</td><td>2013-06-07</td></tr>
<tr><td>ng-grid-flexible-height</td><td>2.0.7</td><td>2013-06-07</td></tr>
<tr><td>ng-grid.css</td><td>2.0.7</td><td>2013-06-07</td></tr>
</tbody></table>

### Recommendations
Once the app’s software stack and libraries are up to date it’s important to regularly update. The complete upgrade experience can be a rigorous and involved process that includes juggling numerous issues and intensive testing. From a client’s perspective, a major upgrade project often doesn’t obviously demonstrate improvement to appearance or function. Because it is not recommended to keep outdated software and major upgrades (such as the one described above) are tedious, the following update options are preferable in order to keep software libraries as up-to-date as possible:

* *Interval Based:* Particular interval periods are implemented to check versions of softwares and libraries. This minimizes frequency of errors while ensuring a minimal gap between the current and latest software version.
* *Module Based:* Whenever work is performed on any module for new features or bug fixes, software and libraries versions are reviewed. This allows for relevant libraries to be updated, tested, and deployed along with development changes within the module.

### Conclusion
Even if new features and improvements are not pertinent to the new release, frequent upgrades to software and libraries are crucial in order to ensure the most secure and debugged versions. With security as the highest priority, these upgrades are not only imperative, but unavoidable. Please feel free to share your methods of upgrading software libraries in a comment!
