---
author: Ben Ironside Goldstein
title: "Announcing End Point Timesheet, our open source time-tracking tool"
description: "End Point is open-sourcing Timesheet, the time-tracking and reporting application we have built and used internally for years."
date: 2026-10-26
tags:
- company
- open-source
- ruby
- rails
---

Today we’re open-sourcing [End Point Timesheet](https://github.com/EndPointCorp/Timesheet-App), the flexible time-tracking and reporting application we built and have used internally for years.

Timesheet supports more than simply recording hours. It helps teams organize work across clients and projects, manage access, monitor available hours, and turn time entries into useful operational and billing reports.

Its features include:

- Calendar and daily views for entering, editing, and reviewing time
- Searchable project hierarchies and quick access to frequently used projects
- Project managers, recurring hour budgets, and “hours in the bank” tracking
- Reports by date range, project, or user, including billing reports, saved presets, and PDF output
- Users, teams, groups, roles, and fine-grained permissions
- Tools for viewing another user’s calendar, switching roles, and managing approvals

The application has a React frontend, a Rails JSON API, and PostgreSQL. The complete development stack can be started with one Docker Compose command and includes demo data, making it straightforward to explore locally.

## Preparing the application for release

Getting an established internal application ready for the public took more than moving its code to GitHub.

The backend was still running Ruby 2.4 and Rails 5.0, both of which had stopped receiving security updates years ago. Edgar Mlowe led an upgrade to Ruby 3.3.6 and Rails 8.1.3, preserving the familiar user experience while updating the framework, dependencies, APIs, configuration, and database behavior underneath it.

The existing automated test coverage was useful but incomplete, so a green test suite alone could not prove that the application still worked correctly. Edgar supplemented the backend specs and Playwright end-to-end tests with a 74-check browser testing process covering the workflows where errors would matter most: time calculations, billing, reports, permissions, dates, and project management.

AI served as a development teammate throughout this work. Because the application’s original developers were no longer available, it helped Edgar interpret unfamiliar legacy patterns, investigate changed behavior, propose updates, and develop the browser checklist. Each result was still verified against the running application, and regressions found through browser testing were protected with additional automated tests. Edgar describes that process in more detail in [Upgrading Rails 5 to Rails 8 with AI: What Broke After the Specs Went Green](https://www.endpointdev.com/blog/2026/08/upgrading-rails-5-to-rails-8-with-ai/).

Preparing the repository also included adding an MIT license, creating a reproducible Docker-based development environment, adding demo seed data, improving setup documentation, cleaning out obsolete and internal-only code, supporting CI preview environments, and tightening authorization around sensitive timesheet data.

## Why open source?

Open source software has long been central to how we work at End Point. We use it every day, contribute to it, and believe that useful work should be shared when it can benefit others.

Timesheet represents many years of development and real-world use. By releasing it, we hope other organizations can learn from it, adapt it to their needs, and help make it better.

[Explore End Point Timesheet on GitHub.](https://github.com/EndPointCorp/Timesheet-App)
