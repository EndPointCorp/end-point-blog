---
author: Kamil Ciemniewski
gh_issue_number: 1085
tags: angular, javascript
title: Polemics on opinions about AngularJS
---



Some time ago, our CTO, Jon Jensen, sent me a link to a *very* [interesting blog article about AngularJS](http://www.fse.guru/2-years-with-angular).

I have used the [AngularJS framework](https://angularjs.org/) in one of our internal projects and have been (vocally) very pleased with it ever since. It solves many problems of other frameworks and it makes you quite productive as a developer, if you know what you’re doing. It’s equally true that even the best marketed technology is no silver bullet in real life. Once you’ve been through a couple of luckless technology-crushes, you tend to stay calm—understanding that in the end there’s always some tradeoff.

We’re trying to do our best at finding a balance between chasing after the newest and coolest, and honoring what’s already stable and above all safe. Because the author of the blog article decided to point at some elephants in the room—it immediately caught our attention.

I must admit that the article resonates with me somewhat. I believe, though, that it also doesn’t in some places.

While I don’t have as much experience with Angular as this article’s author, I clearly see him sometimes oversimplifying, overgeneralizing, and being vague.

I’d like to address many of the author’s points in detail, so I will quote sections of the article. The author says:

>
> My verdict is: Angular.js is “good enough” for majority of projects, but it is not good enough for professional web app development.
> …
> When I say “professional web app” I mean the app, which is maintainable in a long run, performant in all reasonably modern browsers, has a smooth UX and is mobile-friendly.
>

The first example that meets those requirements is our internal project. Saying that Angular isn’t a good fit for author’s definition of “professional web apps” is IMHO a huge overgeneralization.

Jon Jensen shared with me the following thoughts on this:

>
> It is also worth asking what is meant by “maintainable in the long run”, since pretty much any web application will need a significant overhaul within 5 years or so, and heavy browser-based JavaScript apps are more likely to need a major overhaul sooner than that.
>
> That’s partly because front-end technology and browser competition is moving so quickly, but also because JavaScript frameworks are improving so rapidly. It’s impossible to predict whether a given framework will be maintained for 5 years, but even more impossible to say whether you would *want to* keep using it after that long.

Those questions make sense to me. The long run may not be so long for modern JavaScript apps.
Later the blog writer asks:

>
> Are there any use cases where Angular shines?
>
> - Building form-based “CRUD apps”.
> - Throw-away projects (prototypes, small apps).
> - Slow corporate monoliths, when performance does not matter and maintenance costs are not discussed (hm, but have you looked at ExtJS?)
>

This is true but is also constrained IMHO. Counter examples are to be found all over the Internet. The YouTube application for Sony’s PlayStation 3 is only one of them. One can use e.g. [https://www.madewithangular.com/](https://www.madewithangular.com/) to browse others.

>
> And what are no-no factors for angular?
>
> - Teams with varying experience.
> - Projects, which are intended to grow.
> - Lack of highly experienced frontend lead developer, who will look through the code all the time.
> - Project with 5 star performance requirements.
>

I agree with the last one. Other ones sprout from the fact that Angular is so liberal in how the app may be structured. In some cases it’s good, while in some bad—there’s always some tradeoff. I’d compare Angular to Sinatra and Ember to Rails. Both are intended to be used in different use cases. One isn’t superior to another without a context.

>
> It there any Working Strategy, if you are FORCED to work with angular?
>
> - Taking angular for fast prototyping is OK, hack it and relax.
> - After the prototype is proved to be the Thing-To-Go, kill the prototype. DO NOT GROW IT!
> - Sit and analyze the design mistakes you’ve made.
> - Start a fresh new project, preferably with other tech stack.
> - Port the functionality from the prototype to your MVP.
>

Agreed with #1. Maintainability isn’t trivial with Angular—it’s true. One reason is that with dependency injection there’s a possibility that with growing number of modules, some tries will depend on each other in a circular way:

A -> B -> C -> A

But it’s not inherent to Angular but to dependency injection itself and there are known strategies for dealing with that. Other reason is that it’s so liberal and yes—you have to always be alert, making sure the code grows in the good direction.

It’s also true that many teams who have previously been using other MV{C,P} frameworks—are converting to Angular. Why? I gave the answer in the first paragraph—there’s no silver bullet. If you want a truly [orthogonal](https://en.wikipedia.org/wiki/Orthogonality_(programming)) software you don’t grow it with just great tools—but with great people. And sometimes even having a star-level team isn’t enough because of the degree to which business requirements change.

Then:

>
> If you still need to grow your project and maintain it in the future:
>
> - Accept the fact that you will suffer in the future. The lowered expectations will help you stay happy sometimes.
> - Create a thorough guideline based on the popular things (this, this and that) covering all the use cases and patterns you can imagine.
> - Try to keep things as loosely coupled as possible with your OOD knowledge.
> - Choose either MVC or MVVM, but do not start by mixing approaches.
> - Include “refactoring” iterations in your dev process (good interval—each 3 months).
> - Analyze your usage patterns and use cases periodically.
> - Create a metaframework based on angular, tailored SPECIFICALLY for your project needs and your team experience!
>

Agreed with all of those. I’d agree with those really for any technology there’s out there.

Then the author says:

>
> Dependency injection lacks some functionality you will need sometime.
>

That intrigues me and I’ll look for similar opinions by others that explain in details *why* the writer thinks that dependency injection will leave me stuck without needed functionality someday.

Then:

>
> Directives are overloaded with responsibilities (ever wonder why and when you should use isolated scope? Yeah, that’s only the tip of the iceberg).
>

I don’t really think that’s a problem because a directive only has the amount of responsibility you make it have. One can use or abuse any technology so this point doesn’t really resonate with me.

Then:

>
> Modules are not real modules.
>
> - No CommonJS/AMD.
> - No custom lazy loading.
> - No namespaces.
>
> You can use modules only to specify the dependency graph and get rid of specifying the correct file order for injecting scripts (which is not a problem anyway if you are using component-based structure and, for example, browserify).
>

That’s only a half-truth. You can use e.g. RequireJS and have “real modules” with Angular—there’s even a good blog article describing how to do it: [https://www.sitepoint.com/using-requirejs-angularjs-applications/](https://www.sitepoint.com/using-requirejs-angularjs-applications/).

If you were to use just Angular-flavored modules one issue you might run into though could be name clashes. But then unless you want to use a dozen of 3rd party modules you find on GitHub—name clashes aren’t a real problem out there in the wild. And also if you do want to use those modules, you cannot expect to have a “maintainable” codebase over time anyway can you?

>
> $scope is “transparent” and inherited by default.
>
> Inheritance is known to be an antipattern in OOD. (Proof?)
> You MUST know the cases, when it can be useful.
>
> Angular forces you to get rid of this inheritance all the time.
>

I somewhat agree. Managing scopes is sometimes a pain.

>
> Bidirectional binding is unpredictable and hard to control (unless you know that you MUST control it).
>

That for me falls under the “use or misuse potential” category. I can’t see it causing any problem unless you create a huge nest of dependent variables and want then to debug if it goes wrong (there are cleaner ways to achieve the same results).

>
> Transparent scope and “referential hell” mean that you CANNOT KNOW what part of the system will be updated when you introduce a change using $scope.$apply().
>
> You have no guarantees.
>
> This is a design tradeoff.
>
> Do you know that each time you call $scope.$apply() you actually call $rootScope.$apply()?
>
> And this call updates all scopes and run all your watches?
>
> Moreover, $rootScope.$apply() is called each time when:
>
> $timeout handler is invoked (almost all debounce services are broken by design)
> $http receives a response (yeah, if you have a polling implemented on $http ...)
> any DOM handler is called (have you throttled your ng-mouseovers? They actually invoke ALL your $watches, and built-in digest phasing does not really help)
> If you know, that some change is localised (like, if you click the button, only the same $scope will be affected), then you MUST use $scope.$digest.
> But again, you will face nasty “$digest is already in progress” issue...*
>

This is a *huge* annoyance. He’s right about it.

Then:

>
> Yes, angular is complex and have a terrible learning curve.
> The worst thing is that you are learning framework for sake of learning framework.
>

I’d say quite the contrary is true. When we switched to Angular with the our internal app, no-one on the team had any experience with it. The team was ranging in experience—from “not much outside of jQuery” to some much more experienced with many JavaScript frameworks. Yet the team started producing much more almost right away. I also heard them saying that Angular is *much* easier than our previous setup—which was Backbone + KnockoutJS.

Then:

>
> 90% of those modules in the wild are broken by design.
>
> - They are not really performant
> - They do not scale
> - They misuse some of angular features
> - They are badly designed and forces bad practices
> - But hey, who cares? They do their job anyway, right?
>

This is true. I’d just add that it’s not really only inherent to Angular. If you’ve been a developer long enough you can recall probably hundreds of hours of fighting with someone else’s code which doesn’t work the way you’d expect it or was marketed as. The problem is there whether you’re trying some Angular modules, other JavaScript libraries and their plugins or other languages libraries too. You **always** have to be very careful when pulling in third party code into your application.

>
> - Those docs suck. They still suck.
> - There are no reference projects.
> - There is no reference project structure.
> - No one share their experience with you through the framework.
> - Yes, those practices can be overwhelming (I am looking at you, Ember). But it’s better to have overwhelming practices, than to have none.
> - Some encoded practices are questionable:
> - Blocking the UI while resolving all promises? Really?
> - No subrouting? Hmmm
>

I somewhat agree and somewhat disagree with those. There are reference projects on GitHub. The documentation was my friend really. Not having a rigid standard of doing things is good or bad only within a context.

I don’t want to come across as someone who thinks he has all the answers and knows more than others. This is just my perspective regarding the things enclosed in this article. I’d say mostly I agree with the author (with exceptions stated above). I’d also say that I cannot see any technology that would be entirely free of shortcomings.

I think it’s worth noting that Angular team seems to be aware of them. They’re already working on the next version: Angular 2. You can read some more about this project here: [http://ng-learn.org/2014/03/AngularJS-2-Status-Preview/](http://ng-learn.org/2014/03/AngularJS-2-Status-Preview/). There’s nothing perfect in this world, but the best thing we can do is to continuously follow the path of constant never-ending improvement.
