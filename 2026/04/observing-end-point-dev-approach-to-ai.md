---
author: "Jesse Gardner"
title: "Observing End Point Dev's Approach to AI"
date: 2026-04-16
description: "A non-technical perspective on the use of AI in the workplace, expectations of improving efficiency, and a clear eyed view of the hype"
featured:
  image_url: /blog/2026/04/observing-end-point-dev-approach-to-ai/cover.webp
github_issue_number: 2178  
tags:
- artificial-intelligence
- vibe-coding
---

![A sweeping desert canyon stretches, framed by towering red sandstone formations and sparse desert scrub under a cloudless blue sky.](/blog/2026/04/observing-end-point-dev-approach-to-ai/cover.webp)<br>
Photo by Garrett Skinner, 2022.

When I joined End Point Dev in October of 2025, there was one clear directive among a wide-ranging set of responsibilities: AI is causing drastic changes in our industry, and we need to tackle it head-on.

As a non-engineer working in a software development consultancy, there is a double edged sword in focusing my work on AI. The downside, of course, is my lack of expertise in anything involving code. I’ve sold software for a majority of my career, but I haven’t been the one building it. A reasonable person could wonder: how would I have a useful perspective on the developments around AI?

To that there are a few answers. For starters, I don’t get bogged down in the “how” AI is working as much as I am interested in the results of its work. I’ve certainly learned context windows, token usage, rate limits, and other immediately useful information around utilizing AI.

I also get to be a guinea pig for End Point’s suite of AI services. Our team might be primarily technical users, but that does not mean our clients necessarily have that same background. I get to approach AI tools as an interested user, not a development wizard. 

With that said, these past six months have been an incredible learning experience within the space. I’ve experienced how AI can help with projects that would otherwise take ten times the amount of work, seen how development times can be improved with properly utilized generative AI, and observed healthy debate internally about where AI ought to be deployed.

### Time Sheet Analysis and AI Analysis

One of the most impressive aspects of the End Point culture is an emphasis on dutiful and detailed timesheet management. As I first stepped into the role, I gained access to the historical timesheet entries across the entire organization, which was a little overwhelming at first, if I’m being completely honest! For billable and non-billable work alike, whether from directors or part-time developers, there was a detailed record of work in 15-minute increments.

The application itself was novel—a lightweight yet powerful tool that organized this work by type and client and allowed multiple types of reporting for someone like me to get a quick lay of the land. Within a few hours of my first day on the job, I was able to get an overview of our top clients, what work was done with them, and which developers were involved.

This was directionally useful, but it was also a bit of context overload—a good problem to have.

So, I decided to keep my findings high-level. I got my overview and moved on, using these reports to pick a lane in the company and start swimming (Visionport). At the risk of mixing metaphors, I didn’t want to boil the ocean. A few months later, though, the allure of that timesheet data reentered my mind. There was so much valuable data there—beyond what I had looked at from that bird’s-eye view. AI is a great way to aggregate data, so I wondered: What else could be explored with the use of AI?

With a little help from my OpenClaw instance, JJ, a plan was devised. I downloaded a year’s worth of timesheet data for virtually every developer on our team, down to the nitty-gritty of each daily entry. I then fed this into my OpenAI pro account and gave it a fairly detailed prompt, asking it to locate patterns of work and opportunities to expand within our current clients. For good measure, I also asked it to organize the data to my specifications, creating a spreadsheet with the tech stack, percentage of hours worked by client for each employee, and other quality-of-life tracking.

As we all know, AI sometimes aims to please a bit too much, so before I acted on any of this data, I took it to the team. While there were certainly some clean upsell opportunities given by ChatGPT, it became clear that the real value was a common understanding for each of our clients between myself and the client rep—a conversation starter, if you will. The project led to an expedited process for me to know our clients, our common workloads, and a better relationship between me and my fellow End Pointers. A solid case for AI enabling real, human work.

### Traditional Software Engineering and Spec-Driven Development

There has been a healthy debate that I’ve witnessed from both my timesheet analysis and internal conversations here at End Point, and that has been the function of AI in a team of expert coders.

It’s no secret that AI has made tremendous progress in its ability to write large quantities of code, especially with the recent leaps in aptitude from the likes of GPT-5.3-Codex and Opus 4.6. Those most bullish on AI might claim that software engineers will be the first industry gobbled up by the ever-looming march of our sycophantic AI overlords. A step below that is an [emphatic push from Nvidia’s CEO](https://www.tomshardware.com/tech-industry/artificial-intelligence/jensen-huang-says-nvidia-engineers-should-use-ai-tokens-worth-half-their-annual-salary-every-year-to-be-fully-productive-compares-not-using-ai-to-using-paper-and-pencil-for-designing-chips) for their head developers to spend around two hundred and fifty thousand dollars on tokens, lest there be a problem with their productivity.

On the other side of the spectrum, there are those who believe that, while AI can sure as heck write code quickly, it can also cause more harm than good. As much as "vibe coders" have taken over, the myriad bugs and suboptimizations in their projects have given birth to a novel job title: the ["Vibe Code Cleanup Specialist."](https://www.indeed.com/career-advice/news/vibe-code-cleanup-specialist)

With these bullish opinions seemingly everywhere, I had to search for a counterargument within End Point itself. As the resident AI cynic at End Point, Senior Developer Gered King takes a very wary stance towards the involvement of AI in software development:

"While vibe-coding can certainly feel like magic when you first give it a try, as the saying goes, 'there is no such thing as a free lunch.' Under a very strict definition of 'vibe-coding' as it was originally coined by Andrej Karpathy, the vibe-coder is not even looking at the code at all. I think most today would agree without too much arm-twisting that this is likely a bad idea for anything that you eventually want to release into production. Languages like English can be incredibly ambiguous, and combined with the fact that LLMs are not deterministic, you could be really taking quite the gamble that you are crafting sufficiently detailed and unambiguous prompts to get an LLM to spit out quality results without looking at the code to see for yourself.

Even if we decide to take a less strict approach and agree to actually look at the code but still predominantly use AI assistance to write the majority of it for us, this can still lead to problems down the road. [Anthropic's own research is clear](https://www.anthropic.com/research/AI-assistance-coding-skills) that offloading parts of your coding to an AI leads to a statistically significant decrease in skills development and understanding. Struggling with problems is a big part of how we learn. If you constantly take the easy path or are otherwise taking shortcuts, you probably aren't learning a lot along the way!

Certainly, some of this AI-generated code is going to be of dubious quality, which further impairs our understanding of it. [CircleCI recently did an analysis](https://www.linkedin.com/pulse/what-28-million-workflows-reveal-ai-codings-biggest-risk-circleci-j9syc/) and found that their data across 28 million workflows from customers using their CI tools showed that in the last couple of years, where AI tools are seeing more and more adoption, only 5% of teams are measurably improving their output. The other 95% are barely seeing any difference at all, and in many cases, teams have even gotten slightly worse at shipping new software releases."

What Gered’s viewpoint represents, beyond the skepticism towards an industry enthralled with powerful tools, is a stalwart protection of human knowledge. I interpret his words as noting that coding is an art as much as a science, and that offloading too much of our problem-solving to AI comes with the risk of losing the ability to develop creative or optimal solutions to the sticky problems within software development.

As our company pushes toward a future where AI is not only prevalent but ever-improving, this skepticism is welcome and, in my humble opinion, critical.

### Spec-Driven Development with AI

While it’s foolish to proclaim that any sort of best practice around AI truly exists, a few truisms have emerged since the launch of ChatGPT in 2023. Chief among them is that AI produces dramatically better results when given clear, detailed specifications, and that unstructured "vibe coding" tends to produce unstructured results.

End Point has leaned into this reality. Over the past several months, our team has developed and begun using a framework for AI-assisted, spec-driven development, and the results have been nothing short of a revelation. Rather than treating AI as a replacement for engineering discipline, the approach doubles down on it: detailed project specifications, strict security standards baked into the framework’s core governance, rigorous testing requirements, and structured issue-driven execution with AI agents working within those guardrails rather than outside them.

A tremendous bonus we’ve found is the quality of documentation that AI agents produce alongside the code itself. When working within well-defined specifications, the agents generate thorough, consistent documentation as a natural byproduct—something that has historically been one of the easier things to let slip in traditional development.

CEO Ben Goldstein has been hands-on in developing and refining the framework in consultation with End Point team members and multiple AI systems, and End Point developers are actively using it on real projects. The shared experience has reinforced a central insight: the better the spec, the better the output.

#### Final Thoughts

Depending on where you look, generative AI is being touted as either the most important technological development in our lifetimes or a bubble that’s just waiting to burst. The beauty of working with the brilliant developers at End Point is that, regardless of how things shake out, preparations are being made.

Buried in the hype of AI’s progress is a question begging to be answered: Does *every* solution need to utilize AI? One of our leaders in AI, Edgar Mlowe, recently wrote about a [niche use case for LLMs](/blog/2026/03/why-i-am-focusing-on-intelligent-document-processing/), drilling into a specific need with a specific solution. When a clear solution isn’t present, though, can it be helped to avoid bringing in LLMs for a solution that simple automation is more appropriate to solve? In other words, is our industry becoming too AI-reliant, or is the emphasis on bringing the "Elephant Gun" drawn from a need to better familiarize us with working alongside LLMs?

This is why a healthy balance must be struck in how these models are leveraged, and why I find it so valuable and important that End Point is home to a range of opinions on AI—from the overt enthusiast to the hardened critic. My role requires a vantage point of all sides and helping craft solutions that leverage the full power of AI, without sacrificing that which makes End Point a special place: the human touch.