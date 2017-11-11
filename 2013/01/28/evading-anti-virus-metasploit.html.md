---
author: Brian Buchalter
gh_issue_number: 753
tags: security
title: Evading Anti-Virus Detection with Metasploit
---



This week I attended a free, technical webinar hosted by [David Maloney](https://twitter.com/TheLightCosine), a Senior Software Engineer on [Rapid7's](http://www.rapid7.com/company/) Metasploit team, where he is responsible for development of core features for the commercial Metasploit editions. The webinar was about evading anti-virus detection and covered topics including:

- Signatures, heuristics, and sandboxes
- Single and staged payloads
- Executable templates
- Common misconceptions about encoding payloads
- Dynamically creating executable templates

After [Kaspersky Lab broke news of the "Red October" espionage malware package last week](https://threatpost.com/en_us/blogs/rocra-espionage-malware-campaign-uncovered-after-five-years-activity-011413), I thought this would be an interesting topic to learn more about. In the post, Kaspersky is quoted saying, "the attackers managed to stay in the game for over 5 years and evade detection of most antivirus products while continuing to exfiltrate what must be hundreds of terabytes by now."

### Separating Exploits and Payloads

Vocabulary in the world of penetration testing may not be familiar to everyone, so let's go over a few terms you may see.

- Vulnerability: A bug or design flaw in software that can be exploited to allow unintended behavior
- Exploit: Software which takes advantage of a vulnerability allowing arbitrary execution of an attacker's code
- Payload: Code delivered to a victim by an exploit
- Signature: Set of rules or pattern match against code
- Sandbox: Protected segments in OS, where code can be run safely

Metasploit by design, separates the payload from the exploit. Payloads can come in two types. A single-stage payload includes all code intended for use in the attack. A staged payload has a small initial exploit which then connects back to a server using shell commands to download subsequent payloads. This is an important distinction because many anti-virus products have signatures for common first-stage exploits, but not for the much wider universe of secondary payloads. By building first-stage exploits that can evade detection, additional payloads can be installed and remain resident without detection.

### A Unique Exploit for Every Target

To have unique initial exploits that will not have anti-virus signatures, Metasploit Pro includes tools to bundle exploits inside otherwise randomly generated executables. These tools create C code which assign variables in random orders and with random values. Functions are created at random to manipulate and perform calculations on these variables. The functions are then called randomly, building a random call tree, making it very difficult to develop a signature because the execution flow and memory maps are all random.

Of course, eventually, we want the random calculations to stop and the exploit to execute so a payload can be downloaded and executed. Amazingly, one of the key ways to hide the payload from the anti-virus is simply to wait to decode the encoded (obfuscated) exploit until after the anti-virus has completed its scan of the executable. Anti-virus vendors are keenly aware that their products hurt end user performance and so the amount of time which they can sandbox and scan an executable is limited. If the initial payload's random functions take a sufficient time, then the anti-virus releases the file from the sandbox. This delay is configurable and is very effective, allowing the exploit to be decoded and executed without detection.

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2013/01/28/evading-anti-virus-metasploit/image-0-big.png" imageanchor="1" style="margin-left:1em; margin-right:1em"><img border="0" height="225" src="/blog/2013/01/28/evading-anti-virus-metasploit/image-0.png" width="400"/></a></div>

### The Next Generation of Exploits

It's been 8 months since these randomization generators were released with Metasploit Pro and anti-virus companies are starting to catch up. Still, only 8 of the 44 scanners used at [VirusTotal](https://www.virustotal.com/about/) detected one of these exploits bundled with randomized code. The next generation of generators are designed to avoid using shell code entirely, further reducing anti-virus products' ability to detect malicious behavior. Instead of shell code, system calls are starting to be used directly, pulling payloads directly into memory. Since anti-virus depends heavily on scanning writes to the file system, this also reduces the exploits surface area. PowerShell version 2.0 seems to be the vehicle of choice for these next generation of exploits and thus far has gone completely unnoticed by anti-virus vendors (according to David anyway).

### Additional Resources

- Evading Anti-virus Detection with Metasploit: [video](http://information.rapid7.com/evading-anti-virus-detection-with-metasploit-video-page.html), [slides](http://information.rapid7.com/rs/rapid7/images/Evading%20Antivirus%20Metasploit%20Webcast.pdf)
- [The Odd Couple: Metasploit and Antivirus Solutions](https://community.rapid7.com/community/metasploit/blog/2012/12/14/the-odd-couple-metasploit-and-antivirus-solutions)
- [Why Encoding Does not Matter and How Metasploit Generates EXE’s](http://www.scriptjunkie.us/2011/04/why-encoding-does-not-matter-and-how-metasploit-generates-exes/)
- [Facts and myths about antivirus evasion with Metasploit](http://schierlm.users.sourceforge.net/avevasion.html)
- [Using Metasm To Avoid Antivirus Detection (Ghost Writing ASM)](http://www.pentestgeek.com/2012/01/25/using-metasm-to-avoid-antivirus-detection-ghost-writing-asm/)


