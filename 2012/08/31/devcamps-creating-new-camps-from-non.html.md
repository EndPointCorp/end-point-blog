---
author: Brian Gadoury
gh_issue_number: 686
tags: camps, git, hosting
title: 'DevCamps: Creating new camps from a non-default Git branch'
---



I recently set up part of a new Rails project [DevCamps installation](http://www.devcamps.org/) with a unique Git repo setup and discovered a trick for creating camps from a Git branch other than master. Admittedly, the circumstances that led to me discovering this trick are a bit specific to this project, but the trick itself can be useful in other situations as well.

The Git repo specified in local-config had a master branch with nothing in it but the standard "initial commit." This relatively new project uses a simplifed [git-flow workflow](http://jeffkreeftmeijer.com/2010/why-arent-you-using-git-flow/) and as such, all its code was still in the "develop" branch. 

In my case, this empty-ish master branch meant there were no tracked files in __CAMP_PATH__/public directory. This meant that Git did not create that directory when the repo is cloned by `mkcamp`. This meant that apache2 would refuse to start. Camping without a web server makes my back hurt, so I snooped around a little bit...

I discovered two things:

1. You can tell `git clone` which branch to checkout initially by passing it a '--branch $your_non_default_branch' switch 
1. The `mkcamp` command will happily pass that switch (as well as any other spicy options you include) along to the `git clone` system command it executes. To do that, just add it to your camp type's local-config file as part of the 'repo_path_git' config variable. For example:

repo_path_git:git@github.com:somegituser/somegitrepo.git --branch develop 

Note that this option means your fresh new camp won't have a 'master' branch checked out. This might confuse some users, but we all know the 'master' branch is nothing but a tracking branch with some convention mixed in. A simple `git checkout master` will create that expected master branch easily enough. It's probably worth giving your devs a heads up about this, lest they think something wonky is afoot with mkcamp.

Now, there are people out there that may try to find fault with my solution. These detractors, these misanthropes, these malingering sluggards might cry "Why don't you just commit an empty __CAMP_PATH__/public/.gitkeep" to your master branch?" Well, I like a clean git history. So, to those people I would say, "David, that's messy and silly and wouldn't make a very good blog article at all. I'm embarrassed for you for even bringing it up, *David.*"


