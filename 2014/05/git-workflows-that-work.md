---
author: Spencer Christensen
title: Git Workflows That Work
github_issue_number: 978
tags:
- git
- tips
date: 2014-05-02
---



<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/05/git-workflows-that-work/image-0-big.png" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/05/git-workflows-that-work/image-0.png"/></a></div>

There was a [significant blog post some years ago](http://nvie.com/posts/a-successful-git-branching-model/).  It introduced a “successful” workflow for using Git.  This workflow was named Gitflow.  One of the reasons this blog post was significant is that it was the first structured workflow that many developers had been exposed to for using Git.  Before Gitflow was introduced, most developers didn’t work with Git like that.  And if you remember when it was introduced back in 2010, it created quite a buzz.  People praised it as “the” way to work with Git.  Some adopted it so quickly and full heartedly that they dismissed any other way to use Git as immature or childish.  It became, in a way, a movement.

I start with this little bit of history to talk about the void that was filled by Gitflow.  There was clearly something that drew people to it that wasn’t there before.  It questioned the way they were working with Git and offered something different that worked “successfully” for someone else.  I supposed many developers didn’t have much confidence or strong feelings about their use of Git before they heard of Gitflow.  And so they followed someone who clearly did have confidence and strong feelings about a particular workflow.  Some of you may be questioning your current Git workflow now and can relate to what I’m describing.  However, I’m not going to prescribe a particular workflow for you as “the” way to do it.

Instead, let’s talk about the purpose of a workflow.  Let’s reword that so we’re clear- the purpose of a software development workflow using Git.  What is the purpose?  Let’s back up and ask what is the purpose of software?  [The purpose of software is to help people.](https://www.codesimplicity.com/post/the-purpose-of-software/)  Period.  Yes it can help servers, and networks, and robots, and telephones, etc.  But help them do what?  Help people.  They are tools to help us (people) do things better, faster, simpler, etc.  I submit to you that the purpose of a software development workflow using Git should be the same.  It should help people release software.  Specifically, it should help match the software development process with business expectations for the people responsible for the software.  That list of people responsible for the software should include more than just the developers.  It also includes operations engineers, project managers, and certainly business owners.

Does your Git workflow help your business owners?  Does it help your project managers or the Operations team?  These are questions you should be thinking about.  And by doing so, you should realize that there is no “one size fits all” workflow that will do all that for every case.  There are many different workflows based on different needs and uses.  Some are for large complex projects and some are extremely simple.  What you need to ask is- what will best help my team/project/organization to develop, release, and maintain software effectively?  Let’s look at a few workflow examples and see.

### GitHub Flow

 

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/05/git-workflows-that-work/image-1-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/05/git-workflows-that-work/image-1.jpeg"/></a></div>

 

GitHub’s own workflow, [their internal workflow](http://scottchacon.com/2011/08/31/github-flow.html), is quite different from what everyone else does who uses GitHub.  It is based on a set of simple business choices:

- Anything in the master branch is deployable
- To work on something new, create a descriptively named branch off of master (ie: new-oauth2-scopes)
- Commit to that branch locally and regularly push your work to the same named branch on the server
- When you need feedback or help, or you think the branch is ready for merging, open a pull request
- After someone else has reviewed and signed off on the feature, you can merge it into master
- Once it is merged and pushed to ‘master’ on the origin, you can and should deploy immediately

They release many times per day to production using this model.  They branch off master for every change they make, hot fixes and features are treated the same.  Then they merge back into master and release.  They even have automated their releases using an irc bot.

### Skullcandy’s workflow

<div class="separator" style="clear: both; text-align: center;"><a href="http://1.bp.blogspot.com/-AX-_EhIL6v0/U2Po8uyGNcI/AAAAAAAAAUo/5EYh2pZhwd8/s1600/git_workflow_skullcandy+(1).jpg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/05/git-workflows-that-work/image-2.jpeg"/></a></div>

When I worked for Skullcandy we used a workflow loosely based on the GitHub Flow model, but altered a bit.  We used a Scrum Agile methodology with well defined sprints of work and deliverables at the end of each sprint.  The workflow followed these business choices:

- A userstory or defect in our tracking system represented a single deliverable, and a Git branch was created for each userstory or defect.  We used a naming convention for branches (skdy/schristensen/US1234-cool-new-feature, for example).  Yes, you can use ‘/’ characters in branch names.
- Everything branches off master.  Features and hot fixes are treated the same.
- After code review, then the branch was merged into a QA branch and deployed to the QA environment where business owners tested and approved the changes.
- The QA branch is just another branch off master and can be blown away and recreated when needed at any time.
- We released once a week, and only those changes that have been approved by the business owners in QA got merged into master and released.
- Since branch names and items in our issue tracking system were tied together we could easily verify the status of a change, the who, when, and what, and why of it, and even automate things- like auto merging of approved branches and deployment, auto updating tickets in the tracking system, and notifying developers of any merge issues or when their branch got released.

 

### Master only workflow

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/05/git-workflows-that-work/image-3-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/05/git-workflows-that-work/image-3.jpeg"/></a></div>

Not every team or project is going to work like this.  And it may be too complicated for some.  It may be appropriate to just work on master without branching and merging.  I do this now with some of the clients I work with.

- Each feature or hot fix is worked on in dev environment that is similar to production, that allows business owner direct access for testing and approval.  Changes are committed locally.
- Once approved by the business owner, commit and push changes to master on origin, and then deploy to production immediately.

You may not be working for a business, and so the term “business owner” may not fit your 
situation.  But there should always be **someone** who approves the changes as acceptable for release.  That person should be the same one who requested the change in the first place.

### Gitflow

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/05/git-workflows-that-work/image-4-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/05/git-workflows-that-work/image-4.jpeg"/></a></div>

 

On the other end of the spectrum from a master only workflow, is Gitflow.  Here there are at least three main branches: develop (or development), release, and master.  There are other branches as well for features and hot fixes.  Many of these are long running.  For example, you merge develop into the release branch but then you continue working on develop and add more commits.  The workflow looks like this:

- All work is done in a branch.  Features are branched off develop.  Hot fixes are treated different and are branched off master.
- Features are merged back into develop after approval.
- Develop is merged into a release branch.
- Hot fixes are merged back into master, but also must be merged into develop and the release branch.
- The release branch is merged into master.
- Master is deployed to production.

### Backcountry workflow

When I worked for Backcountry.com we used a similar workflow, however we used different names for the branches.  All development happened on master, feature branches were branched off and then merged back into master.  Then we branched master to create a new release branch.  And then we merged the release branch into a branch called “production”.  And since master is just a branch and doesn’t have to be special, you could use a branch named whatever you want for your production code.

### Guidelines

There are many other examples we could go over and discuss, but these should be enough to get you thinking about different possibilities.  There are a few guidelines that you should consider for your workflow:

- Branches should be used to represent a single deliverable request from the business- like a single user story or bug fix.  Something that can be approved by the business that contains everything needed for that single request to be released- and nothing more!
- The longer a feature branch lives without getting merged in for a release, the greater risk for merge conflicts and challenges for deployment.  Short lived branches merge and deploy cleaner.
- Business owner involvement in your workflow is essential.  Don’t merge, don’t deploy, don’t work without their input.  Otherwise pain and tears will ensue (or worse).
- Avoid reverts.  Test, test, test your branch before a merge.  When merging use `git merge --no-ff`, which will ease merge reverts if really needed.
- Your workflow should fit how you release.  Do you release continually, multiple times a day?  Do you have 2 week sprints with completed work to release on a regular schedule?  Do you have a business Change Control Board where all released items must get reviewed and approved first?  Does someone else run your releases, like the Operations team or a Release manager?  Your branching and merging strategy needs to make releasing easier.
- Complicated workflows drive people crazy.  Make it simple.  Review your workflow and ask how you can simplify it.  In actively making things more simple, you will also make them easier to understand and work with as well as easier for others to adopt and maintain.

These should help you adjust your software development workflow using Git to fulfill its purpose of helping people.  Helping ***you***.

### Further Reading

There is a lot more you can read about on this topic, and here are several good places to start:

- [https://www.codesimplicity.com/post/the-purpose-of-software/](https://www.codesimplicity.com/post/the-purpose-of-software/)
- [http://scottchacon.com/2011/08/31/github-flow.html](http://scottchacon.com/2011/08/31/github-flow.html)
- [http://nvie.com/posts/a-successful-git-branching-model/](http://nvie.com/posts/a-successful-git-branching-model/)
- [http://www.kdgregory.com/index.php?page=scm.git](http://www.kdgregory.com/index.php?page=scm.git)
- [https://sandofsky.com/blog/git-workflow.html](https://sandofsky.com/blog/git-workflow.html)
- [https://stackoverflow.com/questions/2428722/git-branch-strategy-for-small-dev-team](https://stackoverflow.com/questions/2428722/git-branch-strategy-for-small-dev-team)
- [https://git-scm.com/book/en/Git-Branching-Branching-Workflows](https://git-scm.com/book/en/Git-Branching-Branching-Workflows)
- [https://www.atlassian.com/git/workflows](https://www.atlassian.com/git/workflows)


