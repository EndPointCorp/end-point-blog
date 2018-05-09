---
author: Muhammad Najmi bin Ahmad Zabidi
gh_issue_number: 1307
tags: conference
title: Malaysia Open Source Conference (MOSC) 2017
---

A three days Malaysia Open Source Conference (MOSC) ended last week. MOSC is an open source conference which is held annually and this year it reaches its 10 years anniversary. I managed to attend the conference with a selective focus on system administration related presentations, computer security and web application development.

### The First Day

The first day’s talks were occupied with keynotes from the conference sponsors and major IT brands. After the opening speech and a lightning talk from the community, Mr Julian Gordon delivered his speech which regards to the Hyperledger project, a blockchain technology based ledger. Later Mr Sanjay delivered his speech on the open source implementation in the financial sector in Malaysia. Before lunch break we then listened to Mr Jay Swaminathan from Microsoft whom presented his talks on Azure based service for blockchain technology.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2017/05/25/malaysian-open-source-conference-mosc/image-0-big.jpeg" imageanchor="1"><img border="1" height="300" src="/blog/2017/05/25/malaysian-open-source-conference-mosc/image-0.jpeg" width="400"/></a><br/>
</div>

For the afternoon part of the first day I then attended a talk by Mr Shak Hassan on the Electron based application development. You can read his slides [here](https://docs.google.com/presentation/d/1YP2y0xOcLByONRauYI-xksxLmRulBrTPWVQK6extxaY/mobilepresent?slide=id.p). I personally used Electron based application for [Zulip](https://zulip.org/) so basically as a non web developer I already have a mental picture what Electron is prior to the talk, but the speaker’s session enlightened me more on what was happening at the background of the application. Finally for the first day before I went back I attended a slot delivered by Intel Corp on Yocto Project—​in which we could automate the process of creating a bootable Linux image to any platform—​whether it is an Intel x86/x86_64 platform or ARM based platform.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2017/05/25/malaysian-open-source-conference-mosc/image-1-big.jpeg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="300" src="/blog/2017/05/25/malaysian-open-source-conference-mosc/image-1.jpeg" width="400"/></a></div>

### The Second Day

The second day of the conference was started with a talk from Malaysia Digital Hub. The speaker, Diana, presented the state of Malaysian-based startups which are currently shaped and assisted by Malaysia Digital Hub and also the ones which already matured and able to stand by themselves.  Later, a presenter from Google—​Mr Dambo Ren—​presented a talk on Google cloud projects.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2017/05/25/malaysian-open-source-conference-mosc/image-2-big.jpeg" imageanchor="1"><img border="1" height="300" src="/blog/2017/05/25/malaysian-open-source-conference-mosc/image-2.jpeg" width="400"/></a></div>

He also pointed out several major services which are available on the cloud, for example—​the TensorFlow. After that I chose to enter the Scilab software slot. Dr Khatim who is an academician shared his experience on using [Scilab](http://www.scilab.org/)—​an open source software which is similar to Matlab—​to be used in his research and for his students. Later I entered a speaking slot with a title “Electronic Document Management System with Open Source Tools”.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2017/05/25/malaysian-open-source-conference-mosc/image-3-big.jpeg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="300" src="/blog/2017/05/25/malaysian-open-source-conference-mosc/image-3.jpeg" width="400"/></a></div>

Here two speakers from Cyber Security Malaysia (an agency within the Malaysia’s Ministry of Science and Technology) presented their studies on two open source document management software—​[OpenDocMan](http://www.opendocman.com/) and [LogicalDoc](https://www.logicaldoc.com/). The evaluation matrices were based from the following elements—​the access easiness, costs, centralized repo, disaster recovery and the security features. From their observation LogicalDoc managed to get higher scores compared to OpenDocMan.

Later after that I attended a talk by Mr Kamarul on his experience using R language and [R studio](https://www.rstudio.com/) in his university for medical-based research. After the lunch break then it was my turn on delivering a workshop. Basically my talk was targeted upon the entry level system administration, in which I shared pretty much my experiences using tmux/screen, git, [AIDE](http://aide.sourceforge.net/) to monitor file changes on our machines and [Ansible](https://www.ansible.com/) in order to automate common tasks as much as possible within the system administration context. I demonstrated the use of Ansible with multiple Linux distros—​CentOS, Debian/Ubuntu in order to show how Ansible would handle heterogeneous Linux distribution after the command execution. Most of the presented stuffs were “live” during the workshop, but I also created a slides in order to help the audience and the public to get the basic ideas of the tools which I presented. You can read about them [here](https://najmi.endpoint.com/talks/mosc-2017-najmi-workshop.pdf) [PDF].

### The Third Day (Finale)

On the third day I came into the workshop slot which was delivered by a speaker with his pseudonym—​Wak Arianto (not his original name though). He explained Suricata, a tool which has an almost similar syntax for pattern matching with the well known Snort IDS. Mr Wak explained OS fingerprinting concepts, flowbits and later how to create rules with [Suricata](https://suricata-ids.org/). It was an interesting talk as I could see how to quarantine suspicious files captured from the network (let’s say—​possible malware) to a sandbox for further analysis. As far as I understood from the demo and from my extra readings, flowbits is a syntax which being used to grab the state of the session which being used by Suricata that works primarily with TCP in order to detect. You can read an article about flowbits [here](https://redmine.openinfosecfoundation.org/projects/suricata/wiki/Flow-keywords). It’s being called a flowbits because it does the parsing on the TCP flows. I can see that we can parse the state of the TCP (for example, if it is established) based from the writings [here](https://redmine.openinfosecfoundation.org/projects/suricata/wiki/Suricata_Rules).

I have a chance to listen to FreeBSD developer’s slot too. We were lucky to have Mr Martin Wilke who is living in Malaysia and actively advocating FreeBSD to the local community. Together with Mr Muhammad Moinur Rahman—​another FreeBSD developer they presented the FreeBSD development ecosystem and the current state of the operating system.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2017/05/25/malaysian-open-source-conference-mosc/image-4-big.jpeg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="300" src="/blog/2017/05/25/malaysian-open-source-conference-mosc/image-4.jpeg" width="400"/></a></div>

Possibly we preserved the best thing at the last—​I attended a Wi-Fi security workshop which was presented by Mr Matnet and Mr Jep (both are pseudonyms). This workshop began with the theoretical foundations on the wireless technology and later the development of encryption around it.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2017/05/25/malaysian-open-source-conference-mosc/image-5-big.jpeg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="300" src="/blog/2017/05/25/malaysian-open-source-conference-mosc/image-5.jpeg" width="400"/></a></div>

The outline of the talks were outlined [here](http://lanyrd.com/2017/moscmy/sfqmcx/). The speakers introduced the frame types of 802.11 protocols, which includes Control Frame, Data Frame and Management Frame. Management Frame is unencrypted so the attacking tools were developed to concentrate on this part.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2017/05/25/malaysian-open-source-conference-mosc/image-6-big.jpeg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="300" src="/blog/2017/05/25/malaysian-open-source-conference-mosc/image-6.jpeg" width="400"/></a></div>

The Management Frames is susceptible to the following attacks:

- Deauthentication Attacks
- Beacon Injection Attacks
- Karma/MANA Wifi Attacks
- EvilTwin AP Attacks

Matnet and Jep also showed a social engineering tool called as “WiFi Phisher” in which it could be used as (according to the developer’s page in GitHub) a “security tool that mounts automated victim-customized phishing attacks against WiFi clients in order to obtain credentials or infect the victims with malwares”. It works together with the EvilTwin AP attacks by putting its role after achieving a man-in-the-middle position—​Wifiphisher will redirect all HTTP requests to an attacker-controlled phishing page. Matnet told us the safest way to work within the WiFi environment is either using 802.11w supported device (which is yet to be widely found—​at least in Malaysia). I found some infos on 802.11w that possibly could help to understand a bit on this protocol [here](https://www.cwnp.com/802-11w-management-frame-protection/).

### Conclusion

For me this is considered the most anticipated annual event where I could meet professionals from different backgrounds and keeping my knowledge up to date with the latest development of the open source tools in the industry. The organizer surely had done a good job by organizing this event and I hope to attend this event again next year! Thank you for giving me opportunity to talk within this conference (and for the nice swag too!)

Apart from MOSC I also planned to attend the annual Python Conference (Pycon) in which this year it is going to be special as it will be organized at the Asia Pacific (APAC) level. You can read more about Pycon APAC 2017 [here](https://pycon.my/category/pycon-apac-2017/) (in case you probably would like to attend this event).
