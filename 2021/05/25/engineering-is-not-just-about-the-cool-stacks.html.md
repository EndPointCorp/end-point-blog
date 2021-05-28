---
title: Engineering Is Not Just About the Cool Stacks
author: Afif Sohaili
tags: culture, training, programming
gh_issue_number: 1745
---

![](/blog/2021/05/25/engineering-is-not-just-about-the-cool-stacks/scaffolding.jpg)
[Photo](https://unsplash.com/photos/P6bOdzRk7TY) by [Di](https://unsplash.com/@gett_urban)

As a developer, I love finding new shiny pieces of tech that can help me develop web applications better. To me, it is one of the best parts of the job: Pick up a new programming language, a new database, a new standard, etc., and build cool things with it. But recently, I had the chance to reflect on my experience working on a boring stack at one of my previous workplaces, and it was actually a lot better than I expected.

### My journey

I used to work at a company where the teams are free to decide the tech stacks that best fit their requirements, so a wide range of modern tools were used there to solve the problems at hand. Within just 2 years of joining the company, I switched teams four times and touched everything from Java, Scala, Akka, Terraform, AWS ECS, Serverless, API Gateway, AWS Lambda, AWS DynamoDB, React, Gatsby, Vue, Nuxt, TypeScript, Flowtype, and many other tools that really helped advance my technical skills.

But in late 2018, my manager invited me to assist a “less popular” team in the company. The team handled a myriad of complex products that are quite old. The team’s tech stack was not the shiniest compared to the other teams in the company; the products are developed using Java, a language I generally do not prefer due to its verbosity. We just shipped JAR files to the platform’s marketplace, so there were no web services to maintain and hence it didn’t challenge or sharpen our operations skills. The frontend JavaScript code was largely built with jQuery as it came bundled with the platform we are building on top of.

As a developer who loves shiny tools, this team should have been a dreadful one to be in. But to my surprise, as I reflect upon it, it was actually the team that gave me the highest work satisfaction. It was satisfying because there were a lot of problems to solve, and most of the time the harder problems to solve are not the tech stack: **the apps work, and customers are paying**.

Instead of talking about moving from Java to Kotlin or from jQuery to React, our team spent the time brainstorming ideas on how to increase code quality, how to ensure discipline and follow good principles when crafting software, how to improve our developers’ workflow and processes, and how to best share knowledge and contexts that we had just acquired for future team members. Each problem solved gave me that dopamine boost that made me feel good.

Below are some of the things we did to solve these problems.

### Problem #1: Code quality

The products the team were handling had been suffering from some quality degradations in recent years, and these ultimately led to more bugs and regressions, which then leads to an increase in customer complaints, and that leads to us working under pressure, which then leads to even more quality degradations, and the vicious cycle repeats.

When this started to happen, what did we do?

**We slowed things down.** Instead of having individual engineers work on multiple tickets in parallel, we held more pair programming sessions and reduced the number of tickets in progress to help incorporate collaboration earlier and gain feedbacks on the implementation strategy sooner. At the same time, pairing sessions also helped get the newer engineers up to speed faster. We introduced more quality gates for pull requests to be able to be merged into `main`. We agreed as a team to scrutinize them harder, e.g. if you do not have tests among the changes, just consider the pull request rejected. We also required all team members to approve the changes. We worked with product managers to slow down shipping new features and instead having more bugs fixed. Hence, the health of the codebases got better and better and the products got more and more stable each day.

We also held a brown-bag meeting reinforcing SOLID design principles to everyone in the team. Knowledge sharing like this helps bring everyone onto the same page while pairing and reduce the long discussion threads on pull requests.

### Problem #2: Context-sharing

Members of a team come and go, and that is true for all teams. Complex apps like the ones we were maintaining are usually full of legacy decisions that the newer team members will not have the knowledge of if no deliberate efforts were made to ensure that those contexts get shared. So, we took steps to mitigate this by including the contexts in commit messages. We also encouraged writing our findings in the Jira tickets and in the pull request descriptions on GitHub, but we preferred Git commit messages for documenting decisions related to the commit, because Git is the system that is least likely to change. We might switch from Jira or from GitHub to some similar services, so contexts would be lost when that happens, but it is very unlikely that we would switch from Git for version control.

We also started a knowledgebase to contain information that should be shared within the team, including onboarding instructions, development gotchas, legacy contexts, etc. This helps distribute the knowledge to everyone and reduce blockers on specific team members. We also made a habit of documenting a discussion that happens offline, often in our internal communication channels or in our internal knowledgebase.

### Problem #3: Developers’ workflow

Improving our process was also a focus. One of the first things we did was rewrite our Jenkins CI/CD pipeline to adopt multibranch pipeline, allowing us to build and test feature branches before they were merged into the `main` branch.

We also automated several tasks that we identified as repetitive, from as small as notifying everyone that there is a new pull request open on GitHub, to automatically running compatibility checks for all of our products once the platform we were building on released a new beta version. We constantly looked for areas we could automate better and discussed them in our weekly retrospectives.

We also tuned our workflow to better organize our capacity around all the demands that we are getting: from our customers, our roadmaps, and our improvements bucket. We adopted Classes of Service (CoS) to achieve that. CoS is an approach in which you decide different treatments to different types of work. This means the capacity we have is flexible depending on the demand of each type of work.

For example, we introduced a collapsible task buffer called Intangible that holds work whose value customers do not experience directly, such as upgrading Node.js version, etc. It is collapsible in the sense that the developers in this CoS can be reassigned to other CoS should we deem more capacity is required there. Note that CoS (or any other system for that matter) is not without its pros and cons, so be sure to tweak it to fit your circumstances should you consider adopting it.

### Not all problems are tech, but all tech has problems.

Sometimes, we identify ourselves through our favorite tech stack.

_Hey, I’m a JavaScript developer._

_Hey, I’m a Ruby developer._

And that is not wrong per se, but this particular experience of mine serves as a reminder that the essence of software engineering goes deeper than just the tech — it is to solve problems through software. And that is what we do at End Point.

### Reference

* [SOLID Design Principles](https://devopedia.org/solid-design-principles) at Devopedia
* Classes of Service:
  * [On Classes of Service (CoS), a more pragmatic approach towards “squad formation”](https://medium.com/servicerocket-eng/on-classes-of-service-cos-a-more-pragmatic-approach-towards-squad-formation-ec93e3a80dfb) by Yuen-Chi Lian at ServiceRocket
  * [Predictability and Classes of Service](https://www.thoughtworks.com/insights/blog/predictability-and-classes-service) by Leonardo Campos at ThoughtWorks
