---
author: Liz Flyntz
title: 'Hue’s on First: How we used responsive bulbs to join software and hardware
  for a busy medical practice'
github_issue_number: 1376
tags:
- case-study
- design
- user-interface
- hardware
- architecture
date: 2016-03-14
---

<div class="separator" style="clear: both; text-align: center;"><img border="0" src="/blog/2016/03/hues-on-first/FastTrackoffice.jpg"/></div>

In 2014 we began working with a busy bariatric surgery office in Long Island to create a system that would allow the practice to better manage doctor paging and patient wait time. By placing a responsive, color-coded light bulb and tablet outside each examination room, the staff could see which rooms were empty, which were occupied by a patient waiting on a specific doctor, and in which a doctor-patient consultation was in process. Outside each room is a tablet with information including the patient number, the attending doctor’s name, and the wait time.

<div class="separator" style="clear: both; text-align: center;"><img border="0" src="/blog/2016/03/hues-on-first/FastTrackmapmonitor.jpg"/></div>

In addition to providing a comprehensive, granular paging service for doctors, Fast Track also provides feedback to the practice. This feedback includes average patient wait times per doctor, per time of day, and per procedure. This allows the practice to make necessary changes and increase patient satisfaction and peace of mind.

<div class="separator" style="clear: both; text-align: center;"><img border="0" src="/blog/2016/03/hues-on-first/FastTrackapp.jpg"/></div>

I asked Danny Divita, one of the main developers on this project, to tell us more about the [Hue](http://www2.meethue.com/en-us/)/ [FastTrack](http://www.fasttrackmed.com) interface.

*LF: Describe the project for which we used Hue bulbs. What were all the pieces that needed fitting together?*

DD: The Hue bulbs are being used for a bariatric clinic to alert the staff when pages are sent to of pages to specific rooms. Alongside the lights the API also has to work with a RF device-locating API. The RF API had to be coordinated with the Hue light API to coordinate changing colors, alerts, and states.

*LF: Why were Hue bulbs a good solution for the problem of creating an easy-to-understand, integratable visual alert system? Did you consider any alternatives?*

DD: From a cost perspective and ease of integration the bulbs were a good solution for this project. There are other solutions, but they are more costly and the integration would have taken longer.

*LF: How did you hear about Hue bulbs? Was the API easy to access and work with? How was using Hue’s testing environment?*

DD: The client suggested the bulbs during their research before having us develop their application. The API is extremely easy to work with and well documented. The Hue API has a built-in testing feature that made it easy to understand the API and develop around it.

*LF: What was the most difficult thing about integrating this technology? Can you think of any other commercial implementations of these bulbs? Specifically in the medical industry?*

DD: The most difficult aspect was trying to come up with a good alert (blinking) feature. The API has some built in alerts, but they are limited to a set timed interval. We had to develop around this to ensure the alerts stayed constant and did not time out. Another application for these lights in the medical field could be to indicate severity of a situation or condition. Because the lights can change color, the applications can signal the proper response for the staff.

*LF: Did you write any new software for this project? Is that work available to other developers?*

DD: We used a third party library that helps to manage stateless workflows. Our application expanded upon this library to design a workflow engine that manages paging the staff, Hue lights, and RF device locating.
