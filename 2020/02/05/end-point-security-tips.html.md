---
author: "Charles Chang"
title: "End Point Security Tips: Securing your Infrastructure"
tags: security, windows, infrastructure
gh_issue_number: 1586
---

<div style="float: left"><img src="/blog/2020/02/05/end-point-security-tips/image-4.jpg" alt="phishingemail" align="left"></div>
[Photo](https://flic.kr/p/24YXTiY) from [comparitech.com](https://www.comparitech.com/blog/information-security/common-phishing-scams-how-to-avoid/)

### Implement Security Measures to Protect Your Organization & Employees

In this post, I’ll address what I believe are the three important initiatives every organization should implement to protect your organization and employees:

1. Train employees on security culture.
2. Implement the best technical tools to aid with organizational security.
3. Implement recovery tools in case you need to recover from a security breach.

### Habits of a Security Culture

Train everyone in your organization on these fundamentals:

1. The only time you should be requested to reset your password by email is when you initiate it. There are rare exceptions to this rule, such as when accounts are compromised and providers request all users reset their passwords, but those events should be publicly announced. Staff can confirm with security personnel before acting on such requests.
2. If you are asked to reset your password, it will typically be after you successfully logged into a website and the old one has expired.
3. If you receive an email and do not know the sender, do not trust the contents or open attachments. Get advice from security personnel if needed.
4. If you think the email is from your bank, keep in mind that banks do not ask their clients for private information via email.
5. If you think the social security office emailed you to obtain your personal information, keep in mind that they do not initiate or solicit private information via email.
6. Companies should not solicit private information unless you initiate first.
7. Online retailers should not ask for your private information unless you initiate first.

### A Security Concern: Going Phishing!

<div style="float: right; padding: 20px;"><img src="/blog/2020/02/05/end-point-security-tips/image-1.jpg" alt="phishing fraud" align="right" hspace="10"><p><a href="https://flic.kr/p/2gLaNqk">Photo</a> by <a href="http://www.epictop10.com/">Epic Top 10 Site</a></div>

One of the more common ways to steal someone’s private information is through phishing. Phishing is like fishing: you try to catch something. In this case, the ‘fish’ is your data. Someone with malicious intent sends you email to attempt to get you to click on the link, picture, content, etc. within the email. Once you click the link or content within the email, it might take you to a website to enter or reset your password, even ask for your social security number or other personal information. The person with malicious intent would use the information collect to open accounts, purchase items online or resell your personal data. The links within the phishing email might even redirect you to a fake website that mimics a real website to collect your personal data. The goal is to confuse the email recipient into believing that the email message is legit in its attempt to collect personal information from the user.

#### Phishing Exercises

<div style="float: left; padding: 20px;"><img src="/blog/2020/02/05/end-point-security-tips/image-2.jpg" alt="phishing attack" hspace="10"><p><a href="https://flic.kr/p/x9zZ4A">Photo</a> by <a href="https://www.flickr.com/photos/christiaancolen/">Christiaan Colen</a></p></div>

One way to help the staff better their understanding of a phishing email is to practice phishing exercises by setting up an experiment to see which users would click on your test phishing email. If the user clicks on the experiment phishing email, the email administrator would notify the compliance officer and he or she would re-train the staff on how to properly differentiate real emails from phishing emails. Phishing exercises make a great activity for the employees to avoid the email scams and exert more caution in the future.

### Essential Security Tools

#### Firewall

A firewall should be a mandatory technology for all consumers or businesses. This is basically your main door. The office or organization’s technology is what the firewall is protecting. When you sit in your office working on the computer, just imagine that you are in a fort surrounded by walls. If someone needs to come in, they must be given permission by a gatekeeper to enter the fort. The firewall is very similar. The firewall allows network traffic to go in and out of the office based on the configuration set by a network engineer. The engineer determines what network traffic comes into the office and goes out.

Companies typically test their firewall with penetration tests and network scans to determine if there are any security concerns after implementing the firewall. The testing of the firewall verifies that good security practices are implemented and the firewall is setup properly and securely.

Some hardware firewall devices to consider include:

- <a href="https://www.watchguard.com/wgrd-products/rack-mount/firebox-m270-m370/" target="_blank">WatchGuard</a>
- <a href="https://www.cisco.com/c/en/us/products/security/firewalls/index.html/" target="_blank">Cisco Firepower</a>
- <a href="https://www.ui.com/unifi-routing/unifi-security-gateway-pro-4/" target="_blank">UniFi Security Gateway Pro</a>

#### Network Assessment &amp; Internal Threat Protection

Why is security vulnerability testing necessary? Many organizations have legacy servers, or desktops/​laptops with operating systems that are no longer supported. For example, outdated Microsoft Windows XP and 7 can be compromised by malware while browsing the Internet due to [the BlueKeep vulnerability](https://www.pcworld.com/article/3400698/nsa-warns-that-bluekeep-vulnerability-in-windows-xp-and-windows-7-is-especially-dangerous.html). Systems that are not patched could expose your organization to be infected with malware such as ransomware which would hold your data ransom until you pay to unlock the data.

Security vulnerability testing typically results in a report outlining problematic areas such as outdated operating systems, private data that does not belong on a file server, such as social security or credit card number (personally identifying information, or PII). If PII is needed for the organization to operate, then higher security standards and an encryption system to store the private data is needed. The security vulnerabilities testing could also check if your environment is HIPAA or PCI DSS compliant if those security standards apply to you.

Some security vulnerability testing technology includes:

- <a href="https://www.rapidfiretools.com/products/network-detective/" target="_blank">Rapid Fire Tools Network Detective</a>
- <a href="https://www.rapidfiretools.com/products/cyber-hawk/" target="_blank">Rapid Fire Tools Cyberhawk</a>

#### Enterprise Antivirus Systems

Antivirus software is the last line of defense if malware enters your computer. The antivirus itself would not protect you 100% from being infected by malware or virus but if you have multiple layers of security in place, then the chances are much lower that your organization’s systems would not be compromised. A company called [AV-Comparatives assessed some of the popular antivirus software](https://www.av-comparatives.org/tests/business-security-test-2019-march-june/) in the market.

The battle with malware is endless. Case in point: The [WannaCry](https://techcrunch.com/2019/05/12/wannacry-two-years-on/) malware affected over 200,000 machines across the world and spread quickly. Security researchers quickly realized the malware was spreading like a computer worm, across computers and over the network, using the Windows SMB protocol.

New variants of viruses and malware are developed every day, so the antivirus companies are also daily hard at work developing a way to block and remove malware.

Some antivirus software includes:

- <a href="https://www.webroot.com/us/en/business/smb/endpoint-protection" target="_blank">Webroot Antivirus</a>
- <a href="https://www.symantec.com/products/endpoint-protection" target="_blank">Symantec Antivirus</a>

#### Web Filtering Technology

Web filtering technology blocks websites that are malicious or deemed not appropriate to visit from an organization’s network. For example, websites for gambling could be blocked to reduce employee distractions, but also to reduce access to sites popularly infected with malware, reducing the possibility of malware coming into your network.

There are many competitors out there in this competitive market, and some vendors offer free proof-of-concept testing with their product before you make a big investment. Take a look at:

- <a href="https://www.forcepoint.com/product/url-filtering/" target="_blank">Forcepoint Web Filtering</a>
- <a href="https://www.webtitan.com/webtitan-gateway/" target="_blank">Web Titan Gateway</a>

#### Data Loss Prevention

Employees’ and businesses’ private information is sensitive and should be protected. Businesses, whether audited or not, should always protect their employee private information. 20 years ago paper was used to store private information and locked in a file cabinet, but in 2020 most private information is stored digitally. How do companies keep private information from leaving their office?

Physically you probably can’t stop someone from walking out with private information, but digitally there is technology called digital loss prevention (DLP) that can help keep confidential information from leaving the office. For example, if someone in the office decides to copy private information onto USB storage, or tries to send a social security number or credit card information via email, this can often be prevented. Prepare your business with solutions tailored for regulations involving personal information using DLP software.

Some DLP solutions to consider include:

- <a href="https://www.forcepoint.com/product/dlp-data-loss-prevention" target="_blank">Forcepoint DLP</a>
- <a href="https://www.symantec.com/products/data-loss-prevention" target="_blank">Symantec DLP</a>

#### Email Filtering

Probably one of the easiest and oldest methods to infect or phish someone is via email. There are multiple mechanisms email filtering uses to stop malicious emails: SPF and DKIM, blacklists, etc. On top of these configurable items, email filtering software vendors often release updates throughout the day to block the latest known malware or spam based on heuristics.

Cloud email services such as Microsoft Office 365 are for many businesses superior to on-premise email servers due to having all the bells and whistles to proactively protect your email environment, such as spam & virus filtering, and email archiving for retention purposes. If you need email encryption to protect sensitive emails, this feature is also available.

The distinct advantage of using hosted email service is that the cost is predictable and includes maintenance, so your email administrators do not have to worry about updating the email server software or hardware.

Email filtering technology available includes:

- <a href="https://products.office.com/en-us/exchange/advance-threat-protection" target="_blank">Office 365 Advanced Threat Protection</a>
- <a href="https://www.forcepoint.com/product/email-security" target="_blank">Forcepoint Email Filtering</a>
- <a href="https://www.spamtitan.com/email-filtering-service/" target="_blank">Spam Titan</a>

#### Two Factor Authentication (2FA)

Companies like Duo (owned by Cisco) and Google’s two-factor authentication technology are great tools to implement to improve your overall security. Beyond the usual user name and password, your smartphone or a hardware token are used to authorize the access to a website, an application, or a network. This technology is now well-established and available in most online services, and can be added to your own custom business applications.

Some starting points:

- <a href="https://duo.com/product/multi-factor-authentication-mfa" target="_blank">Duo Multi-Factor Authentication</a>
- <a href="https://www.google.com/landing/2step/" target="_blank">Google Authenticator</a>

#### VPN (Virtual Private Network)

Virtual private network technology allows businesses to provide secure access to office systems or applications to employees who travel or work from a remote location. That is important so that data traveling to and from the source, and many details of traffic patterns, are encrypted, so that the data cannot be captured and decrypted. VPN solutions have been around for years and are an important tool to securely and safely protect data in transit.

#### Password Reset Systems

Why are self-service password reset systems necessary, and are they secure? They eliminate many manual password assignment mistakes, keep passwords private to the user alone, and allow an organization to integrate two-factor authentication to securely reset user passwords, such as Active Directory for Windows, or other single sign-on password. Onboarding is needed for each user, which is done by sending them an email with a link to register.

The password reset system could be an internal system only available to your organization. Another possibility is to access the system via VPN or even through a proxy server in the DMZ to allow password reset from anywhere.

Some password reset systems include:

- <a href="https://www.manageengine.com/products/self-service-password/" target="_blank">ManageEngine ADSelfService Plus</a>
- <a href="https://docs.microsoft.com/en-us/azure/active-directory/authentication/concept-sspr-howitworks" target="_blank">Azure AD Self-Service Password Reset</a>

### Recovery Tools

#### Data and System Backups/​Disaster Recovery

Data backup and disaster recovery practice is a critical component for a business to speed up the process of recovery if malware attacks your systems or if a system becomes inoperable.

If you are attacked by ransomware and all the critical systems and desktops are compromised and rendered useless, then the only way to recover is from backups. At that point, the disaster recovery preparation you made will be well worth what you invested into it. If you did not have an adequate backup or disaster recovery plan, your organization or company would have to start from scratch and rebuild all systems and desktops which could take weeks if not months to recover from. The lost wages, and possibly clients, due to unavailable systems and desktop to operate, probably would cost you far more than preparation does. The more options you have, the better the chances that you will get out of your bind and not prolong the situation.

Some backup solutions I have worked with have the flexibility to mix and match to fit your configuration needs:

- <a href="https://www.acronis.com/en-us/cloud/service-provider/backup/" target="_blank">Acronis Backup Solution</a>
- <a href="https://www.rubrik.com/product/overview/" target="_blank">Rubrik</a>
- <a href="https://azure.microsoft.com/en-us/services/backup/" target="_blank">Azure Backup</a>

Acronis Cloud Backup allows you to back up to local storage, the cloud, and off-premise, recover a system using a USB drive, back up Office 365 emails, or backup VMware or Hyper-V environments. It also allows you to recover a single file if needed.

### Additional Security Recommendations

#### SSL/TLS Certificates

What are SSL and TLS? SSL is outdated and replaced by TLS, but people often still use the familiar SSL name. They are an encryption system to keep sensitive information sent across the Internet encrypted so that only the intended recipient can access it.

When an SSL certificate is validated, the transmitted data is not only unreadable by anyone except for the intended server, but you are relatively well assured you are communicating with the organization you expected and not with a malicious intermediary. Read more details in [SSL Shopper’s Why SSL?](https://www.sslshopper.com/why-ssl-the-purpose-of-using-ssl-certificates.html) article.

SSL certificates were historically used primarily for higher-security web servers, but now are commonly used on almost all web servers. They are also used for other remote server access, B2B server-to-server communication, VPN access, email systems, etc.

### Recent Destructive Incidents

These incidents from just a few weeks in fall 2019 show that we have a long way to go in protecting our technology usage:

1. <a href="https://www.nbcnewyork.com/news/local/Long-Island-Schools-Hacked-District-Forced-to-Pay-88000-in-Ransom-558396441.html" target="_blank">Long Island Schools Hacked; District Forced to Pay $88,000 in Ransom</a>
2. <a href="https://www.nbcnewyork.com/news/local/NY-School-Delays-Start-of-Year-After-Ransomware-Attack-559322971.html" target="_blank">NY School Delays Start of Year After Ransomware Attack</a>
3. <a href="https://www.newsweek.com/tortoiseshell-hacker-hire-military-heroes-fake-website-1461320" target="_blank">Veterans Targeted by Hackers Through Fake Military Heroes Hiring Website</a>
4. <a href="https://www.zdnet.com/article/hackers-target-transportation-and-shipping-industries-in-new-trojan-malware-campaign/" target="_blank">Hackers Target Transportation and Shipping Companies in New Trojan Malware Campaign</a>
5. <a href="https://inc42.com/buzz/hacking-routers-webcams-printers-are-the-most-searched-keywords-on-the-dark-web/" target="_blank">Hacking of IoT – Internet of Things (webcams, security cams, printers, home routers)</a>

### Speak With Us!

Keeping up with security can be a full-time job. If you need professional consulting on security tools and implementing them, [contact](/contact) our team today.
