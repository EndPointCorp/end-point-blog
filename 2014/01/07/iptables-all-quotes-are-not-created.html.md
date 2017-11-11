---
author: Richard Templet
gh_issue_number: 910
tags: iptables, security, sysadmin
title: 'IPTables: All quotes are not created equal'
---



We have been working on adding comments to our iptables rules to makes it a lot easier to know what each rule is for when reviewing the output of /sbin/iptables -L. If you aren't familiar with the comment ability in iptables it is pretty straight forward to use. You just add this to an existing or new rule:

```nohighlight
-m comment --comment "testing 1 2 3"
```

I had the displeasure of learning this weekend, while updating a system, that though it is a pretty easy addition to make the quotes you use do make a difference. As you can see in the example above, it uses double quotes. The culprit of my displeasure was the dreaded single quote.

When the server rebooted I noticed that iptables didn't start as expected so I tried to start it using service iptables start and was greeted with this error: 

```nohighlight
iptables: Applying firewall rules: Bad argument `1'
Error occurred at line: 30
```

I loaded up the /etc/sysconfig/iptables file in vim and started to try to figure out what had changed on line 30. I reviewed the rule and it looked pretty straight forward.

```nohighlight
-A INPUT  -s 1.2.3.4 -p tcp -m multiport --dports 22,80 -j ACCEPT -m comment --comment 'testing 1 2 3'
```

Why was it freaking out over the 1 in the comment? I knew we had done comments before with spaces in them before without having any issues. So what was the deal? Well knowing in other instances that the type of quote mattered after a few minutes of scratching my head I decided to try changing them from single quotes to double quotes on a hunch. After adjusting the quotes, I ran service iptables start and much happiness was had as it started. I moved on with the other systems I needed to get done and called it a night.

Today I decided to circle back and get a better idea on why the single quotes were causing the problem so I started testing different setups. My first test was to remove the quotes completely and see if that worked. It failed as expected which was good to see. My second test was to switch back to single quotes and remove all spaces. This did work but didn't generate the results I was expecting. What I ended up with in iptables -L was output that looked like this:

```nohighlight
ACCEPT     tcp  --  1.2.3.4         0.0.0.0/0           multiport dports 22,80 /* 'testing' */ 
```

I didn't notice it at first but notice how the single quotes actually made it into the comment itself? This means that iptables didn't actually parse the quotes at all. It took them just as characters in my comment. After realizing this it was clear why my comment 'testing 1 2 3' was causing iptables to throw an error:it was seen as 'testing 1 2 3', spaces and single quotes themselves included, instead of "testing 1 2 3" as a unique string, spaces included and double quotes excluded. Changing single quotes to double quotes did the trick and iptables finally was seeing it as a complete unique string.


