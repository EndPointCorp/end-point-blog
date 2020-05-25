---
author: Árpád Lajos
title: "Thoughts on Project Estimation: The Star, the Planet, and the Habitable Zone"
tags: tips, project-management
gh_issue_number: 1508
---

<img src="/blog/2019/03/25/thoughts-on-project-estimation/planet_orbit.jpg" alt="planet in orbit" /><a href="https://www.flickr.com/photos/esoastronomy">Photo by ESO on Flickr</a> · <a href="https://creativecommons.org/licenses/by/2.0/">CC BY 2.0</a>

Whenever we are working on a feature, planning a milestone or a project, there is always a discussion about the cost and time needed. In most cases there are three main parties involved: the client, the manager, and the programmer(s). Let’s use the analogy of a star system, where the client is the star everything orbits around, the project is the planet, and the programmers are the biosphere. The closer we are to the star, the closer we are to the exact requests of the client.
 
Everything orbits around the star (the client), whose activity produces the energy, ensuring that there is any planet at all. If the planet (the project) is too close to the star, it will burn out quickly and evaporate. But if the planet is too far away, the relationship between the star and the planet, or the client and the project (from our perspective) will freeze out. There is a so-​called habitable zone, where the planet, or the project can benefit of the energy of the star. 

First the habitable zone should be found. This is a concept of the project which is close enough to the client’s desires, but still achievable, so biosphere can coexist with the star system, shaping the planet.
 
Whenever we create an estimation, we need to differentiate parts of the problem into two main categories. The first category is the subset of the problem where we can accurately foresee what is to be done and we can accurately estimate the needed time. The second category is the subset for problems where we have open questions. It’s good to offer the client alternatives: we could do a vague estimation for the problems where we have open questions, or we can do research to gather further knowledge and increase the subset of problems where we foresee the solution. In general:
 
```T = (T(Known) + T(Unknown) + T(Unforeseen)) * HR```
 
T(Known) is the total time we estimate for the problems for which we mostly already know the solution. T(Unknown) is the total time we estimate for problems we have open questions about, the answer of which directly affects the time we need. T(Unforeseen) is the total time to work on problems we cannot foresee before starting the project. HR is the Habitable Ratio we multiply the time by. For example, if HR = 1.3, then we estimate the time of the project to be 30% higher than what we think it’ll take. The reason we need such a ratio is that T(Unknown) and T(Unforeseen) in reality can be much higher than our estimation. If we estimate a time to the client which is around or less than the time we think we can successfully finish our work, then the work will potentially be a stressful rush. If we take longer than the estimation, we lose our hard earned reputation. In this case we will either be at the edge of the habitable zone towards the star, or even between the star and the habitable zone. It is the perfect recipe to burn out quickly.
 
On the other hand, if we exaggerate T, the client will think that costs will get out of control. In this case, even though we can surely fulfill the estimation, we are outside of the habitable zone. We are too far from the star, and will not get enough energy from our star to enable a biosphere to live on the planet.
 
So, the rules we would like to adhere to are:

- Make a reliable estimation.
- Be open when you cannot achieve the precision you would like for the estimation.
- Give alternatives when something takes too much energy, if possible.
- Pleasantly surprise the client by completing the work before the deadline, both in terms of agreed hours and end date, whenever we are able to.
- Be detailed about what and how was done, so if the work requires more time than we thought the client will understand the reason.

Communication is often not counted into the estimation and there could be other things we forget. Make sure to think about what you’re forgetting before you send an estimation. Asking colleagues for review can help you with your blind spots.
