---
author: Steph Skardal
gh_issue_number: 665
tags: browsers, mobile
title: 'Code School: Journey into Mobile Review'
---



Yesterday, I took the [Journey into Mobile](http://www.codeschool.com/courses/journey-into-mobile) course over at [Code School](http://www.codeschool.com/), an online training program with a handful of web technology courses. I just started a large mobile project for [Paper Source](http://www.paper-source.com/), so this was good timing. Because a paid membership to Code School is required to participating in the training, I won't share too many of the course details here. But I'll share a few tidbits that will hopefully interest you in taking the course or learning more about mobile development.

The course was divided into 5 high level lessons (or levels):

- Relative Font Size
- Fluid Layouts
- Adaptive Design
- Responsiveness Adventures
- Responsive Media

The first two topics covered working with proportional font sizes and content regions, and how to convert your existing layout to proportions (percentage or ems) to create a fluid layout which included proportional font sizes. In the Adaptive Design lesson, the CSS3 supported @media query was introduced. I've used the media query on the responsive design for [The Best Game Apps](http://www.thebestgameapps.com/) and will be using it for Paper Source. Some examples of @media queries include:

```css
@media (min-width: 655px) and (max-width: 1006px) {
  # styles specific to browser width 655-1006 pixels
}
@media only screen and (device-width: 768px) {
  # styles specific to browser width 768 pixels
}
@media (min-device-width: 320px) and (max-device-width: 655px) {
  # styles specific to browser width 320-655 pixels
}
@media (min-device-width: 450px) and (orientation:landscape) {
  # styles specific to browser width 450 pixels and landscape orientation
}
```

For each of the above @media queries, specific "break points" are determined to adjust styles as certain elements break as the browser width changes. For example, if elements begin to overlap as the screen narrows, the browser width at which this begins to happen is one break point, and new styles are defined for that width.

The last two levels of the training course covered Responsiveness Adventures and Responsiveness Media. Responsive design also leverages the @media query to design responsively for changing browser widths. One interesting topic covered in the Responsive Media lesson was how [Retina Images](http://blog.cloudfour.com/how-apple-com-will-serve-retina-images-to-new-ipads/) are addressed on devices where the pixel density is 1.5-2 times regular pixel density. This was a topic I hadn't come across in mobile development. The lesson presented a couple of options for dealing with Retina images, including use of the @media query and picture HTML tag.

Overall, it was a decent course with a good overview. I would recommend it to anyone planning to get involved in mobile development.


