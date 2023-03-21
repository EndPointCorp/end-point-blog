---
author: Steve Yoman
title: COVID-19 Support for the Kansas Department of Health and Environment
github_issue_number: 1663
featured:
  epitrax: true
  image_url: /blog/2020/09/covid-19-support-kansas-dept-health/dashboard.jpg
tags:
- epitrax
- clients
- case-study
- rails
- vue
- emsa
date: 2020-09-14
---

### Kansas’s existing EpiTrax system

End Point has worked on Kansas’s disease surveillance systems since 2011. In 2018 we migrated them from their legacy TriSano application to the open source EpiTrax surveillance system created by Utah’s Department of Health. The new EpiTrax system had been in full production for about eight months when COVID-19 cases started to grow in the United States.

### COVID-19: Help needed

In March 2020, the Director of Surveillance Systems at the Kansas Department of Health and Environment (KDHE) asked us at End Point to create a web-based portal where labs, hospitals, and ad-hoc testing locations could enter COVID-19 test data. While systems existed for gathering data from labs and hospitals, they needed a way to quickly gather data from the many new and atypical sites collecting COVID-19 test information.

### Our approach

Since the portal was intended for people who were unfamiliar with the existing EpiTrax application, we were able to create a new design that was simple and direct, unconstrained by other applications. It required a self-registration function so users could access the system quickly and without administrative overhead, and users needed to understand how to use it without extensive training.

We at End Point agreed to create the portal and dashboard for test results reporters immediately, while planning for later development of additional administrative functions. We used Ruby on Rails and Vue.js to build the portal due to their usefulness for rapid development. The Vue.js front-end JavaScript framework allowed us to quickly put together the portal UI and integrate it with the Rails back-end web services.

Once approved, our team got to work setting up the environment, developing the portal application, and rigorously testing it.

Here are some screenshots of the application:

### Portal home page

![Kansas Reportable Disease Portal home page](/blog/2020/09/covid-19-support-kansas-dept-health/Home-Screen.jpg)

### User registration page

![Create New User Account page](/blog/2020/09/covid-19-support-kansas-dept-health/newuser.png)

### Dashboard

![Dashboard for searching and browsing cases](/blog/2020/09/covid-19-support-kansas-dept-health/dashboard.jpg)

### Reporters’ entry screens

![Forms collecting information about reporter and patient](/blog/2020/09/covid-19-support-kansas-dept-health/Reporter-Data-Entry.jpg)

![Forms collecting information about disease, speciment, and testing results](/blog/2020/09/covid-19-support-kansas-dept-health/form-part-2.png)

The portal was launched on April 30.

### Contact tracers support

After the EpiTrax portal for COVID-19 was up and running, Kansas made urgent plans to hire 400 contact tracers. We updated the EpiTrax portal to accommodate this new type of user, showing contact tracers only the data they are authorized to view, while providing them the ability to make limited contact record updates and to create tasks. The project is ongoing, and eventually will be used for all diseases.

### EpiTrax for Missouri

Late this Spring, after learning of Kansas’s use of the EpiTrax platform and the powerful capabilities that it provides to the Kansas public health system, the State of Missouri reached out to us at End Point to request their own EpiTrax implementation. End Point and Missouri quickly came to agreement, and since July we have been working together build out a full production EpiTrax surveillance system for them.

### Contact us!

To discuss an EpiTrax project, [contact](/contact/) us. Our expert team is ready to help you meet your requirements.
