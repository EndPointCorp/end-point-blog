---
author: "Charles Chang"
title: "End Point Security Tips: Securing your Infrastructure"
tags: security, windows, infrastructure
gh_issue_number: 1561
---


 <div style="float: left"><img src="/blog/2020/02/05/endpointsecuritytips/image-4.jpg" alt="phishingemail"  align="left"></div>
 [Photo](https://flic.kr/p/24YXTiY) from [comparitech.com](https://www.comparitech.com/blog/information-security/common-phishing-scams-how-to-avoid/)


### Implement Security Measures to Protect Your Organization & Employees

In this post, I’ll address what I believe are the three important initiatives every organization should implement to protect your organization and employees:

1. Train employees on security culture.
2. Implement the best technical tools to aid with organizational security.
3. Implement recovery tools in case you need to recover from a security breach.

### Habits of a Security Culture
Train everyone in your organization on these fundamentals:

1. The only time you would be requested to reset your password is when you initiate it. This is true for any password. 
2. If you are ask to reset your password, typically after you successfully logged into a website, etc will they ask you to reset if needed.
3. If you receive an email and do not know the sender, do not click the email but delete right away.
4. If you think the email is from your bank, keep in mind banks do not ask their clients for private information via email.
5. If you think the social security office email you to obtain your personal information, keep in mind social security office do not initiate or solicit private information via email.
6. Companies would not solicit private information unless you initiate first.
7. Online retailer would not ask for your private information unless you initiate first.
8. Websites would not ask to reset your password without warning; generally, they would expire the password or delete your account over time if not used.

### A Security Concern: Going Phishing!
   <div style="float: right; padding: 20px;"><img src="/blog/2020/02/05/endpointsecuritytips/image-1.jpg" alt="phishing fraud" align="right" hspace="10"><p><a href="https://flic.kr/p/2gLaNqk">Photo</a> by <a href="http://www.epictop10.com/">Epic Top 10 Site</a></div>One of the more common ways to steal someone’s private information is through phishing.There are few other ways which someone could steal your personal information, but phishing is one of the more common ways. Phishing is like fishing; you try to catch something. In this case, the ‘fish’ is your data. Someone with malicious intent would send you an email and attempt to influence you to click on the link, picture, content etc. within the email. Once you click the link or content within the email, it might take you to a website to enter or reset your password, even ask for your social security number, or personal information. The person with malicious intent would use the information collect to open accounts, purchase items online or resell your personal data. The links within the phishing email might even redirect you to a fake website that mimics a real website to collect your personal data. The goal is to confuse the email recipient into believing that the email message is legit and attempts to collect personal information from the user. 

#### Phishing Exercises
<div style="float: left; padding: 20px;"><img src="/blog/2020/02/05/endpointsecuritytips/image-2.jpg" alt="phishing attack" hspace="10"><p><a href="https://flic.kr/p/x9zZ4A">Photo</a> by <a href="https://www.flickr.com/photos/christiaancolen/">Christiaan Colen</a></p></div>One way to help the staff better their understanding of a phishing email is to practice phishing exercises by setting up an experiment to see which users would click on your test phishing email. If the user clicks on the experiment phishing email, the email administrator would notify the compliance officer and he or she would re-train the staff on how to properly differentiate real emails from phishing emails. Phishing exercises is a great activity for the employees to avoid the email scams and exert caution in the future. 

### Essential Security Tools

#### Firewall
A firewall should be a mandatory technology for all consumers or businesses. This is basically your main door. The office or organization’s technology is what the firewall is protecting. When you sit in your office and working on the computer, just imagine that you are in a fort surrounded by walls. If someone needs to come in, they are given permission to enter the fort. The firewall is very similar. The firewall allows network traffic to go in and out of the office based on the configuration set by a network engineer. The engineer would determine what network traffic comes into the office and out. He is basically the gatekeeper. Many companies typically test their firewall with penetration and network scans to determine if there are any security concerns after implementing the firewall. The testing of the firewall is typically done to make sure security best practices are implemented and test the configuration to see if the firewall is setup properly and securely. 

##### Firewall Devices:
- <A href=https://www.watchguard.com/wgrd-products/rack-mount/firebox-m270-m370/ target=_blank>WatchGuard</a>
- <A href=https://www.cisco.com/c/en/us/products/security/firewalls/index.html/ taget=_blank>Cisco Firepower</a>
- <A href=https://www.ui.com/unifi-routing/unifi-security-gateway-pro-4/>UniFi® Security Gateway Pro</a>

#### Network Assessment & Internal Threat Protection
Why is security vulnerability testing necessary? For one, many organizations might have legacy servers, or desktops/laptops that are no longer supported by Microsoft and thus might cause the Windows XP or Windows 7 to be compromise through malware while browsing the internet. The National Security Agency is warning users that a recent vulnerability affecting Windows 7 and Windows XP systems is potentially “wormable,” meaning that it could be exploited and weaponized by malware<sup>1</sup>. The danger with systems that are not patched could expose your organization to be infected with malware such as ransomware which would hold your data ransom until you pay to unlock the data. If ransomware hits, your computer will be rendered useless. 

The security vulnerability testing would generate a report outlining problematic areas such as outdated Windows XP or 7. The security test would also search for private data that should not belong on a file server such as social security or credit card number. If PI information is needed for the organization to operate, then an encryption system to store the private data would be needed. The security vulnerabilities testing could also check if your environment is HIPAA or PCI compliant if that service is needed.

##### Security Vulnerability Testing Technology:
- <A href=https://www.rapidfiretools.com/products/network-detective/ target=_blank>Rapid Fire Tools Network Detective</a>
- <A href=https://www.rapidfiretools.com/products/cyber-hawk/ target=_blank>Rapid Fire Tools Cyberhawk</a>


<sup>1</sup> <sup><a href=https://www.pcworld.com/article/3400698/nsa-warns-that-bluekeep-vulnerability-in-windows-xp-and-windows-7-is-especially-dangerous.html target=_blank>https://www.pcworld.co/article/3400698/nsa-warns-that-bluekeep-vulnerability-in-windows-xp-and-windows-7-is-especially-dangerous.html</a></sup>

#### Enterprise Antivirus Systems
Antivirus software should be a mandatory technology running on all servers, or computers. Basically, this is the last line of defense if a malware or viruses enter your computer. The antivirus itself would not protect you 100% from being infected by malware or virus but if you have multiple layers of security in place, then the chances are much lower that your organization’s technologies would not be compromised. A company called<sup>2</sup> AV-Comparatives did an assessment on some of the popular antivirus software’s out in today’s market. The success rates range from 98% to 100%. The 2% difference could potentially compromise your network. It only takes one malware or virus to enter your network and becomes destructive.

The constant battle with malware and virus is endless. Case in point, the wannacry malware affected 200,000 machines across the world and spread quickly. <sup>3</sup>Security researchers quickly realized the malware was spreading like a computer worm, across computers and over the network, using the Windows SMB protocol. 

New variants of viruses and malware are developed everyday thus the antivirus companies are hard at work developing a way to remove malware and viruses everyday. Basically, you could only prevent it, but not stop it since malware and viruses are constantly evolving. 

##### Antivirus Softwares:
- <A href=https://www.webroot.com/us/en/business/smb/endpoint-protection target=_blank>Webroot Antivirus</a>
- <A href=https://www.symantec.com/products/endpoint-protection target=_blank>Symantec Antivirus</a>


<sup>2</sup> <sup><a href=https://www.av-comparatives.org/tests/business-security-test-2019-march-june/ target=_blank>https://www.av-comparatives.org/tests/business-security-test-2019-march-june/</a></sup><br>
<sup>3</sup> <sup><a href=https://techcrunch.com/2019/05/12/wannacry-two-years-on/ target=_blank>https://techcrunch.com/2019/05/12/wannacry-two-years-on/</a></sup>


#### Web Filtering Technology
Web Filtering technology basically block websites that are malicious or deemed not appropriate to visit during work hours. For example, websites such as gambling could be blocked by the web filtering technology. Websites is another way malicious virus and malware could be deployed and enter your network. By blocking these malicious sites, the possibilities of a virus or malware coming into your network could be prevented. Forcepoint (formally WebSense) has a web filtering technology and one of the leaders in the industry to block malicious websites. There are other competitors out there in this competitive market, and some vendors offer free proof of concept testing with their product before you make a big investment in their product.

##### Web Filtering Technology:
- <A href=https://www.forcepoint.com/product/url-filtering/ target=_blank>Forcepoint Web Filtering</a>
- <A href=https://www.webtitan.com/webtitan-gateway/ target=_blank>Web Titan Gateway</a>

#### Data Loss Prevention
Employees’ and businesses’ private information is sensitive in nature and should be protected at all cost. Business that are audited or not should always protect their employee private information. 20 years ago, paper was used to store private information and locked in a cabinet. Fast forward to 2019, most if not all private information is stored digitally. How do companies protect their private information from leaving their office? Physically, probably can’t stop someone from leaving the office with the private information, but digitally, there are some technology out there that would stop a credit card number from leaving the office. If someone in the office decides to copy private information onto a USB key, this could be prevented. If someone sends social security or credit card information via email to another recipient, this would be prevented. Prepare your business with built-in expertise for regulations involving PII, and PHI/HIPAA, with DLP software. 

##### Data Loss Prevention Technology:
- <A href=https://www.forcepoint.com/product/dlp-data-loss-prevention target=_blank>Forcepoint DLP</a>
- <A href=https://www.symantec.com/products/data-loss-prevention target=_blank>Symantec DLP</a>

#### Email Filtering 
Probably one of the easiest and oldest methods to infect or phish someone’s information is via email. How does the email filtering stop malicious links and attachments? Well, there are multiple mechanism email filtering use to stop malicious emails. SPF and DKIM records, Public IP and DNS, blacklists, etc. On top of these configurable items, the vendor that developed the email filtering would release updates throughout the day to block the latest known malware or spam based on heuristics. 

Cloud email services such as Microsoft Office 365 are superior to on-premise email servers due to having all the bells and whistle to proactively protect your email environment and provides many important email services such as a spam filter, antivirus filter, and email archiving for retention purposes. Microsoft 365 email service cost is affordable compared to an on-premise email systems which requires a separate system to filter spam and viruses. If you need email encryption to protect sensitive emails, this feature is also available. 

The distinct advantage using Microsoft 365 email service is that your email administrator do not have to worry about updating the email server, or update the hardware firmware and drivers which is necessary to maintain the email system over time. The Microsoft cloud email service would always provide you with the latest tools and technology to combat spam and viruses. This advantage allows the email administrator to easily manage the email systems since the email is a critical part of communication for all businesses.

##### Email Filtering Technology:
- <A href=https://products.office.com/en-us/exchange/advance-threat-protection target=_blank>Office 365 Advanced Threat Protection</a>
- <A href=https://www.forcepoint.com/product/email-security target=_blank>Forcepoint Email Filtering</a>
- <A href=https://www.spamtitan.com/email-filtering-service/ target=_blank>Spam Titan</a>

#### Two Factor Authentication
Companies like Duo (owned by Cisco) and Googles’ two factor authentication technology are great tools to implement to improve your overall security. Basically, your smartphone is unique to you so the phone would be used to authorize the access to a website, an application or a network. If someone attempts to compromise your account with a known working password, the two-factor authentication running on your phone would be the final layer of protection to prevent un-authorize access. This technology is the latest trend most companies are adapting to improve overall infrastructure security. Keep in mind two factor authentication are available for most mainstream technology but not all. If you would like us to determine which solution best fits your environment, please contact us for more information.

##### Two Factor Authentication:
- <A href=https://duo.com/product/multi-factor-authentication-mfa target=_blank>Duo Multi-Factor Authentication</a>
- <A href=https://www.google.com/landing/2step/ target=_blank>Google Authenticator</a>

#### VPN (Virtual Private Network)
Virtual Private Network technology allows businesses to provide a secure access to office systems or applications to employees who travels, or work from a remote location. VPN allow secured, encrypted access to internal networks initiated by an employee. Why is VPN important? Well for one the data traveling to and from the source is encrypted meaning that the data would be impossible to capture and decrypt. Confidential information, and personal data will be well protected with VPN. VPN solution has been around for years and it’s a must have technology to securely and safely protect all data. 

#### Password Reset Systems
Why are self service password reset systems necessary and is it secure? The reason to have a password reset systems is to be able to eliminate manual mistakes, and the system allows an organization to integrate two factor authentication to securely reset a staff’s Active Directory password (Windows password). The two factor authentication used to reset the password would be unique to the user. The user in your organization would need to register their phone number within the two factor authentication system and thus allow a safe way to reset your password without the need of an IT staff to intervene. Onboarding will be needed for each user which is done by sending them an email with a link to register. 

The password reset system could be an internal system only available to your organization. Another possibility is to access the system via VPN or even through a proxy server in the DMZ to allow password reset from anywhere. If setting up a proxy server in the DMZ, your security practice to secure the server in the DMZ should be implemented. 

##### Password Reset Systems:
- <A href=https://www.manageengine.com/products/self-service-password/ target=_blank>ManageEngine ADSelfService Plus</a>
- <A href=https://docs.microsoft.com/en-us/azure/active-directory/authentication/concept-sspr-howitworks target=_blank>Azure AD Self-Service Password Reset</a>

### Recovery Tools

#### Data and System Backups/Disaster Recovery
Data backup and disaster recovery practice is a critical component for a business to speed up the process of recovery if virus or malware attacks your systems or if a system becomes inoperable. If a ransomware attack occurs, and all the critical systems and desktops are compromised and rendered useless, then the only way to recover is from backups. If your system becomes inoperable due to human error or system issues, then the disasters recovery you practice would come in handy. These are all protective measures your organization could implement to prevent and provide options if issues occur from ransomware attacks. 

Basically, ransomware would take your desktop or server hostage and then affect other systems within your network/office. To build back your environment post-ransomware attacks, you would need the backups or disaster recovery plan to recover. If you did not have an adequate backup or disaster recovery plan, your organization or company would have to start from scratch and rebuild all systems and desktops which could take weeks if not months to recover.

One of the better affordable backup solutions I worked with is Acronis Cloud Backup Solution which have the flexibility to mix and match to fit your configuration needs. Acronis Cloud Backup allows you to back up to a local storage, backup to the cloud and have a copy off-premise, recover a system using a USB key, backup office 365 emails, or backup VMware or Hyper V environment. It would also allow you to recover a single file if needed.

The cost of backup will not be felt until something happens. Let’s say you did not have a backup solution and ransomware attacks your system. If this occurs, it might be days, or weeks before your organization is able to operate normally. The lost wages, and possibly clients, due to unavailable systems and desktop to operate, probably would cost you more money or even customers, if you cannot recover quickly. In technology, the more options you have, the chances are better that you will get out of a bind easier and not prolong the situation. 

##### Backup Solutions:
- <A href=https://www.acronis.com/en-us/cloud/service-provider/backup/ target=_blank>Acronis Backup Solution</a>
- <A href=https://www.rubrik.com/product/overview/ target=_blank>Rubrik</a>
- <A href=https://azure.microsoft.com/en-us/services/backup/ target=_blank>Azure Backup</a>

### Additional Security Recommendations

#### SSL Certificates 
What is a SSL certificate? <sup>4</sup> The primary reason why SSL is used is to keep sensitive information sent across the Internet encrypted so that only the intended recipient can access it. When an SSL certificate is used, the information becomes unreadable to everyone except for the server you are sending the information to. 

The SSL certificate usage have been around for a long time. The practice of using SSL is more common in today’s world to protect and encrypt data at all cost. SSL certificate are commonly used on web servers but you could find SSL usage for simple server access, SFTP servers, B2B server to server communication, VPN access, email systems, etc. 

When it comes to online transactions, in order to accept credit card information on your website, you must pass certain audits that show that you are complying with the Payment Card Industry (PCI) standards. One of the requirements is properly using an SSL Certificate. Other areas where you could implement a SSL certificate include VMware vSphere ESXi host to vCenter communication. The cost is small to obtain a SSL certificate for each system compared to better your overall security. 


<sup>4</sup><sup><a href=https://www.sslshopper.com/why-ssl-the-purpose-of-using-ssl-certificates.html target=_blank>
https://www.sslshopper.com/why-ssl-the-purpose-of-using-ssl-certificates.html</a></sup>

### Recent Destructive Incidents

A few incidents that occurred recently has shown that we have a long way in protecting our technology usage. A few articles below will detail the incident. 

1. 08/27/19:  <A href=https://www.nbcnewyork.com/news/local/Long-Island-Schools-Hacked-District-Forced-to-Pay-88000-in-Ransom-558396441.html target=_blank>Long Island Schools Hacked; District Forced to Pay $88,000 in Ransom</a> 
2. 09/03/19:  <A href=https://www.nbcnewyork.com/news/local/NY-School-Delays-Start-of-Year-After-Ransomware-Attack-559322971.html target=_blank>NY School Delays Start of Year After Ransomware Attack</a> 
3. 09/25/19:  <A href=https://www.newsweek.com/tortoiseshell-hacker-hire-military-heroes-fake-website-1461320 target=_blank>Veterans Targeted by Hackers Through Fake Military Heroes Hiring Website</a> 
4. 09/23/19:  <A href=https://www.zdnet.com/article/hackers-target-transportation-and-shipping-industries-in-new-trojan-malware-campaign/ target=_blank>Hackers Target Transportation and Shipping Companies in New Trojan Malware Campaign</a> 
5. 09/25/19: <A href=https://inc42.com/buzz/hacking-routers-webcams-printers-are-the-most-searched-keywords-on-the-dark-web/ target=_blank>Hacking of IoT – Internet of Things (webcams, security cams, printers, home routers)</a> 



### Conclusion

Keeping up with security can be a full-time job. If you need professional consulting on security tools and implementing them, [contact](https://www.endpoint.com/contact) our team today. 






