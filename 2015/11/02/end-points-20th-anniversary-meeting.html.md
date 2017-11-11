---
author: Phin Jensen
gh_issue_number: 1170
tags: company, conference
title: "End Point’s 20th anniversary meeting, part 2"
---

Friday, October 2nd, was the second and final day of our company meeting. (See the earlier [report on day 1 of our meeting](http://blog.endpoint.com/2015/10/end-points-20th-anniversary-meeting.html) if you missed it.) Another busy day of talks, this day was kicked off by Ben Goldstein, who gave us a more detailed rundown of End Point's roots.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/11/02/end-points-20th-anniversary-meeting/image-0.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/11/02/end-points-20th-anniversary-meeting/image-0.jpeg"/></a></div>

### The History of End Point

Ben and Rick met in the second or third grade (a point of friendly dispute), and from the early days of their friendship were both heavily influenced by each other's parents. Their first business enterprise together was painting houses in the summer to earn money for college.

After attending college, Ben worked with Unix and dabbled with the World Wide Web when it was brand new. Rick worked on Wall Street for a while, then decided he had had enough of that and worked briefly in real estate, then left to pursue more creative interests.

Ben showed Rick some simple websites he had been working on and Rick said *that* is what they should do: they should start a business building websites together. Soon they made the big decision and End Point was officially incorporated on August 8, 1995. Their earliest clients were all found by word of mouth, with the first website being made for one of Ben's cousins.

At first they made only static websites. But Ben had worked with Oracle databases and knew some scripting languages, so the possibility of making dynamic data-driven web applications on the server seemed within reach. They met someone who had been scanning wine labels and putting the data into a Mini SQL (msql) database. Ben wrote some Perl scripts and soon had created End Point's first dynamic website.

Rick met an employee of Michael C. Fina, a company that did wedding registries and wanted to move to the web. Ben got started working on that in 1998. Around the same time, he found the open source MiniVend web application framework, exactly what he needed for a project like that which would be much more than a few CGI scripts.

Once End Point's early dynamic websites went into production, Ben wanted to grow more solid hosting and support services. After working with a few independent consultants who were a little too fly-by-night, he went to Akopia for help. Akopia had just acquired MiniVend and renamed it to Interchange. They brought Mike Heins, the creator of MiniVend, on board, and were building out a support and hosting business around Interchange.

Before long, Akopia was acquired by Red Hat, and Ben met Jon Jensen there while getting his help with Interchange and Linux questions. Later when Red Hat was phasing out its Interchange consulting group, Ben offered Jon a job, and Jon introduced Ben and Rick to his co-worker Mark Johnson who was expert at all things database, Perl, and Interchange. Rick and Ben hired both Jon and Mark in 2002, and End Point continued to grow with new clients and soon more employees as well.

The story continues with End Point moving into PostgreSQL support, Ruby on Rails development, AFS support, the creation of Spree Commerce, programming with Python &amp; Django, Java, PHP, Node.js, AngularJS, Puppet and Chef and Ansible, and a major move into the Liquid Galaxy world. By then things are documented a little better thanks to wikis and blogs, so Ben was able to keep to the highlights.

A lot happens in a business in 20 years!

<a data-flickr-embed="true" href="https://www.flickr.com/photos/end-point/22374541691/" title="20151002_185637"><img src="/blog/2015/11/02/end-points-20th-anniversary-meeting/image-1.jpeg" style="max-width: 100%;"/></a>

### Using Trello

Next Josh Ausborne talked about how we make our lives easier by tracking tasks with Trello, a popular software as a service offering. At End Point we use Trello as one way to keep track of what we're working on in a project, along with other systems for certain projects or preferred by our various clients.

Most work tracking systems store data about progress and status, but Trello's strength is that it provides a nice way to look at things as a whole and to streamline collaboration. Trello is simple and easy to use, comes with just enough features to be helpful but not to overwhelm, has great apps for Android and iOS, and costs nothing to use for almost all functionality.

Using Trello is simple. It's made up of "boards", each of which contain lists of "cards". Each card can be used to represent a task or small project. People can be assigned to a card, watch it for notifications, comment, create checklists, upload images, share links, and more.

Cards are organized into lists, where they can be organized by status, priority, person, or any way else you choose. A popular arrangement is a "Kanban"-style board with one list each for "Ideas", "To do", "Blocked", "Doing", and "Done/Review". Nearly everything can be organized or moved with simple drag-and-drop gestures.

### Automated Hosting

Lele Calò and Richard Templet talk about automated versus manual infrastructure management. In the beginning of the web era, system administrators did everything by hand. They soon moved on to a “shell for-loop” style of system administration, but many things were still done by hand and often incompatible between systems. That’s where automation comes in. With tools like Puppet, Chef, Salt, and Ansible, it becomes easy to automate much of the configuration across many servers, even of different operating system distributions and versions.

So what should automation be used for? Mainly repetitive tasks that don’t require human touch. A lot of things in server setup and update deployment are easily done once, but become tedious very quickly.

What does End Point use automation for? We use it in our web hosting environment for initial operating system setup on new servers, managing changes to SSH public key lists and iptables firewall rules, and deploying monitoring configurations. For certain applications, we automate building, deploying, and updating entire systems with consistent configuration across many hundreds of nodes. We use Puppet, Chef, and Ansible for various internal and customer projects.

For those who are looking to get started, Lele and Richard recommended starting with automation on new servers. It's very simple and safe to experiment there, as there isn't anything yet to lose. Later once you're confident in what you're doing you can start to carefully spread your automation to existing servers.

<a data-flickr-embed="true" href="https://www.flickr.com/photos/end-point/22145874720/" title="DSC_4216"><img height="424" src="/blog/2015/11/02/end-points-20th-anniversary-meeting/image-1.jpeg" style="max-width: 100%;" width="640"/></a>

### Command Line Tools

Kannan Ponnusamy and Ram Kuppuchamy showed us some of their favorite Unix command-line tools. Here are some of the cool things I liked.

You can use ^ (caret) to correct typos in the previous command, like so:

```
user@host $ cd Donloads
cd: no such file or directory: Donloads
user@host $ ^on^own
cd Downloads
user@host:~/Downloads $
```

Use ! ("bang") commands to access commands and arguments in the history:

- !! - entire previous command
- !* - all arguments of previous command
- !^ - first argument of previous command
- !$ - last argument of previous command
- !N - command at position N in history
- !?keyword? - most recent command with pattern match of keyword
- !-N - command at Nth position from last in history

Using Ctrl-R will do a reverse search of your command history, letting you see and edit old commands. If you press Ctrl-O on a historic command, it will execute it and put the following command from the history into the prompt. Additional presses of Ctrl-O will continue down the history.

The ps --forest option creates a visual ASCII art tree of the process hierarchy. Likewise, Git has git log --graph, which shows a visual representation of the repository history. Try using git log --oneline in addition to --graph to make it a little more concise.

tee $filename lets you pipe to STDOUT and a file at the same time. For example, crontab -l | tee crontab_backup.txt will print the crontab and put it in a text file.

ls -d */ will list all directories in the current directory.

These are just a few of the neat things they showed us. See their [blog post about these and other Unix commands](http://blog.endpoint.com/2015/11/favourite-unix-command-line-tools.html).

<a data-flickr-embed="true" href="https://www.flickr.com/photos/end-point/21741059554/" title="20151002_200437"><img height="360" src="/blog/2015/11/02/end-points-20th-anniversary-meeting/image-1.jpeg" style="max-width: 100%" width="640"/></a>

### ROS in the Liquid Galaxy

Wojciech Ziniewicz and Matt Vollrath gave us a preview of their talk “ROS-driven user applications
in idempotent environments” to be presented at [ROSCon 2015 in Hamburg, Germany](http://roscon.ros.org/2015/) a few days later. The Liquid Galaxy project recently transitioned away from ad-hoc services and protocols to ROS (Robot Operating System) and their [presentation slides](http://roscon.ros.org/2015/presentations/ROS_driver_user_applications_in_idempotent_environments.pdf) give a good idea of how much was involved in that process.

### State of the Company

Next, Rick gave a talk on the current state of the company, which he summarized with one word: Transition. End Point is a company that has been changing since its inception in 1995, and now is no exception. A major transition over the last year or so has been growing to a head-count of 50 people. While we are in many ways similar to when we were, say, 30 people, more people requires different approaches for management and coordination.

A larger End Point presents us with both opportunities and challenges. However, the core values of our company have remained the same and are part of what make us what we are.

<a data-flickr-embed="true" href="https://www.flickr.com/photos/end-point/22176971989/in/photolist-zMGM92" title="20151002_200115"><img src="/blog/2015/11/02/end-points-20th-anniversary-meeting/image-1.jpeg" style="max-width: 100%;"/></a>

### Personal Tech Security

Marco Matarazzo and Lele Calò next spoke to us on personal tech security. Why should you secure your personal or work devices? One obvious reason is to prevent disclosure of sensitive data. But just as important is not losing important data or becoming a conduit for attacks on other systems and networks.

So how should you approach security? It's important to think of usability vs. security. A door with 100 locks on it may be more secure than one with two, but getting in and out of it, even with the proper keys, would be far too difficult. So security should be adapted for the scenario. Securing a personal laptop with pictures, music, and games should be approached differently from a work device with passwords and SSH or GnuPG keys.

For members of our hosting team and employees who work with clients that require it, we have certain more stringent security policies they must follow. Some things are considered common sense, such as shredding or burning business-related papers and being careful with access to work environments.

In public places, make sure shared networks have proper encryption. Do not use untrusted computers, such as public computers at libraries or internet cafes, for work or any personal sites you need to log into. Be careful to not leave any work data behind, whether on an old backup disk or computer you get rid of, or on scraps of paper or notepads.

Keep all of your devices safe physically and in software! Apply operating system and other software updates promptly, and reboot at least a few times a week to let everything get fully updated. That includes laptops, desktops, phones, tablets, etc. And don't forget external drives! Keep automatic password-protected screen locks on your devices, encrypt your data and swap partitions, as well as phones and removable devices.

Backup your data to a safe place, and remember to share your passwords with someone trusted who may need them in case of an emergency.

Make sure your private SSH keys are password-protected, and ensure you're asked for confirmation when using them. Avoid common and unsafe passwords, like '12345' and 'password', although 'pizza1' is perfectly fine :). Use PGP to encrypt private messages and confidential data at rest.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/11/02/end-points-20th-anniversary-meeting/image-1.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/11/02/end-points-20th-anniversary-meeting/image-1.jpeg"/></a></div>

### “Brain bowl” challenge

We finished our meetings with a little friendly competition led by Jon Jensen. We were divided into ad-hoc teams by Ron Phipps, and were presented with trivia questions to see which team could answer correctly first. Some of the questions included:

- Who created the World Wide Web? In what year?
- What is now wrong with the term “SSL certificate”?
- What do HIPAA and PCI-DSS stand for?
- The Agile Manifesto says its authors have come to value what things over what other things?
- Where does the word “pixel” come from?
- Where did the Unix command “tee” that Kannan mentioned get its name?
- What does the name UTF-8 stand for?
- How many bytes are in a terabyte? In a tebibyte?

Then we had some questions about programming languages we work with, such as which of Python's built-in types are immutable, or what values are boolean false in Ruby, Perl, and JavaScript.

We ended with a programming problem that required HTML parsing and number-crunching. The task was the same for all teams, but each team used a different toolset: Node.js, Ruby, Perl, Python, or bash + classic Unix text tools sed, awk, sort, cut, etc. The Perl, Python, and bash/Unix teams came up with working and impressive solutions at about the same time.

### Company party

We ended the day with a party nearby at Spin where we played ping-pong and had dinner and socialized and met significant others who were also visiting New York City.

It was great to get everyone together in person!

<a data-flickr-embed="true" href="https://www.flickr.com/photos/end-point/22145792200/" title="DSC_4301"><img src="/blog/2015/11/02/end-points-20th-anniversary-meeting/image-2.jpeg" style="max-width: 100%;"/></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>
