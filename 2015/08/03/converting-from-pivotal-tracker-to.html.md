---
author: Josh Lavin
gh_issue_number: 1146
tags: perl, tips, tools
title: Converting from Pivotal Tracker to Trello for project management
---



For larger client projects, I find it helpful to maintain a list of tasks, with the ability to re-order, categorize, and mark tasks as completed. Add in the ability to share this list with coworkers or project owners, and you have a recipe for a better record and task-list for development.

I had been using [Pivotal Tracker](http://www.pivotaltracker.com/) for this purpose, but I found a lot of its features were too complicated for a small team. On the simpler side, [Trello](https://trello.com/) offers project "boards" that meet many needs for project management. Plus, you can accomplish a lot with the free level of Trello.

### No import

After being convinced that switching from Pivotal to Trello was the right move for my current project, I was dismayed to find that Trello offers no Import functionality, at least that I could find for front-end users. (They do have an API, but I didn't relish taking time to learn this.) I could easily export my Pivotal project, but how to get those tasks into Trello cards?

### One idea

In my search of Trello for an import feature, I found a feature called *Email-to-board*. Trello provides a custom email address for each Board you create, allowing you to send emails to this address, containing information for a new Trello card. (This email address is unique for each board, containing random letters and numbers, so only the Board owner can use it.)

What if I wrote a quick script that processed a Pivotal CSV export file, and sent an email to Trello for each row (task) in the file? The script might send out quite a few emails, but would it work? Time to try it.

### Perl to the rescue

I started cooking up a simple [Perl](https://www.perl.org/) script to test the idea. With the help of some [CPAN](https://metacpan.org/) modules to easily process the CSV file and send the emails, I landed on something that worked. After running the script, each row in the CSV export became an email to my Trello board, containing the item's title, description, estimate (difficulty level), and list of tasks required to complete it.

The script should work for most exports from Pivotal Tracker, and I have published it to my [GitHub account](https://github.com/jdigory), in case it is helpful for others who decide to move to Trello.

**[Find the pivotal2trello script on GitHub.](https://github.com/jdigory/pivotal2trello)**

If you happen to try it, let me know if you experience any problems, or have any suggestions!


