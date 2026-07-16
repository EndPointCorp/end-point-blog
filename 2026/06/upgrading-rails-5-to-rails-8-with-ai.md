---
author: Edgar Mlowe
title: "Upgrading Rails 5 to Rails 8 with AI: What Broke After the Specs Went Green"
description: "A first-hand AI-assisted Rails 5.0 to Rails 8.1 fresh-app transplant: what broke after the specs went green, why the tests missed it, and how we verified the application's highest-risk workflows."
featured:
  endpoint: true
  image_url: /blog/2026/06/upgrading-rails-5-to-rails-8-with-ai/cover.webp
date: 2026-06-23
tags:
- artificial-intelligence
- ruby
- rails
- open-source
- troubleshooting
---

![An editorial illustration of an engineer crossing from a tangled legacy software landscape toward a cleaner modern system, with AI present as a small guide rather than the driver.](/blog/2026/06/upgrading-rails-5-to-rails-8-with-ai/cover.webp)

<!-- Illustration created with AI direction by Edgar Mlowe, 2026. -->

We moved our internal Timesheet app, a legacy Rails application, from Ruby 2.4.10 and Rails 5.0.1 to Ruby 3.3.6 and Rails 8.1.3, with AI assisting the work throughout. We did it as a fresh-app transplant: build a clean Rails 8 app, move the old code into it, and get it running. The backend RSpec suite went green. `bin/rails zeitwerk:check` eager-loaded the configured application code without complaint.

Then we brought up the real stack for the first time: a development server, a seeded database, the React frontend, a real browser. Every request behind login returned a 500. The calendar failed. Monthly totals crashed. The 18 Playwright end-to-end tests run against that same live stack, so they only went green after those failures were fixed. The green suite had not been wrong. It had been silent.

This post is about that gap. What broke in a direct Rails 5 to Rails 8 transplant, why a green suite missed it, and how we verified the application's highest-risk workflows after the migration. The app tracks hours, billing, reports, users, roles, and permissions, so quiet wrong answers matter more than loud crashes.

### Why a fresh-app transplant instead of an incremental upgrade

The standard advice is to upgrade one version at a time. The official Rails guides recommend it, and so does most consulting experience. We did not do that here, and it was a project-specific call, not a claim that transplants are safer in general.

The app was three major Rails versions behind, with many release series in between, and both Ruby 2.4.10 and Rails 5.0.1 had been end-of-life for years. The original developers were gone. A step-by-step path meant carrying old configuration and dead idioms through every intermediate upgrade. A transplant meant one larger jump into a clean Rails 8 baseline, at the cost of hitting every incompatibility at once.

We ran a throwaway spike first: fresh Rails 8 app, move the code in, see what breaks, then throw it away. That gave us a risk map before any real work started. The risk we cared about was silent behavior change in the areas that matter for a timesheet: hours, billing, reports, permissions, dates, and raw SQL.

A transplant is worth considering when the app is far behind, the intermediate versions hold no value to you, and you can afford to verify behavior end to end. Incremental should be the default when you are one or two versions behind, need to keep shipping, or cannot fully re-verify the app afterward.

### What actually broke

Here are the migration regressions, and why the automated suite did not catch them.

| Symptom | Root cause | Why the tests missed it | How it was found |
| --- | --- | --- | --- |
| Every logged-in request returned 500 | Dev config used a plain `Logger`. `activerecord-session_store` calls `#silence` on the Active Record logger on every session lookup, and a plain `Logger` does not provide it. The gem's old 1.x version had patched plain `Logger` to add it. The 2.x version in the new app does not. | The fault was in development-environment config. Specs run in the test env with a different logger. | Logging in to the running app |
| Calendar pages 500'd | Rails 7.0 renamed date formatting from `to_s(:db)` to `to_fs(:db)` and deprecated the old call. Rails 7.1 removed it, so on Rails 8 it raises an ArgumentError. | The calendar date helper had no spec of its own | Browser workflow check |
| Monthly and billing totals crashed | On Rails 5, Active Support's `sum` folded these interval objects together starting from the first element. The upgraded stack uses Ruby's built-in `sum`, which starts from integer `0`, so the first addition was `0 + Interval` and raised a TypeError. Fixed with an explicit identity: `sum(Interval.new)`. | The code that calculates the totals had no request spec | Browser check of report totals |
| Two reports 500'd | Rails 5 inlined these queries' `?` values as integer literals. Rails 8 sends them as untyped bind parameters, which PostgreSQL defaults to `text`, so the array came out `text[]` against `integer[]` columns, a pair with no overlap operator. Fixed by casting with `::int[]`. | One query had a spec and failed there. The second was in a report path with none. | Existing suite for the first, browser check for the second |
| The project search 500'd | Rails blocks raw SQL fragments in `order`. The results were ranked with a raw `ts_rank(...)` expression, now wrapped in `Arel.sql`. | No spec exercised that ordering | Browser search check |
| Three React admin pages rendered a raw object string, weeks later | `yajl-ruby` had quietly patched `JSON.dump`. Removing the gem broke `render json: JSON.dump(relation)`. Fixed with `render json: relation`. | The one spec that hit these endpoints checked the status code, not the body. A 200 with a garbage string still passed. | The pages broke after the gem was removed |

One note on that raw-SQL fix. `Arel.sql` does not sanitize anything. It marks a fragment as trusted. It was safe here only because the search phrase is stripped down to word characters and whitespace before it reaches the query. Wrapping arbitrary input in `Arel.sql` would just launder an injection.

The fixes themselves were tiny. That is what makes them worth showing: nothing this small should be able to break every login in an app.

The login failure was one word:

```ruby
- config.active_record.logger = Logger.new(File.join(Rails.root, 'log', 'activerecord.log'))
+ config.active_record.logger = ActiveSupport::Logger.new(File.join(Rails.root, 'log', 'activerecord.log'))
```

The old app's session store gem, `activerecord-session_store` 1.0, quietly patched the standard library's `Logger` so that every logger responded to `#silence`. The fresh app resolved that gem to 2.x, which had dropped the patch, and the gem calls `#silence` on the Active Record logger when it looks up a session. The plain `Logger` configured in this app's development environment did not have the method, so every logged-in request 500'd until that one word changed. The break came from a gem's major version bump, not from Rails itself. A transplant moves every dependency at once, and this is what that looks like. The specs were not careless. They run in the test environment by design, and this line lives in a file they never load. Running the app surfaced it in seconds.

The crashing totals were one argument, the explicit identity that `sum` used to supply implicitly:

```ruby
- subitems.sum { |item| Interval.new(item[:total]) }
+ subitems.sum(Interval.new) { |item| Interval.new(item[:total]) }
```

The identity also decides what an empty list sums to: a zero `Interval` now, where the old stack returned integer `0`. Any caller that can see an empty list is worth a check.

And the array-cast failure was six characters, in a query comparing a bound array against an `integer[]` column:

```ruby
- scope.where("array[?] && role_ids", role_ids)
+ scope.where("array[?]::int[] && role_ids", role_ids)
```

That one bit twice, in two different reports, which is why it is worth a grep for any other `array[?]` used against an integer-array column.

Most of that table is an old lesson: good test coverage is the first line of defense in a Rails upgrade. Specs for the calendar helper, the totals, the report queries, and the search ordering would have caught four of these failures before a browser was ever opened, and a fifth passed only because its one spec asserted the status code and not the body. Adding guard specs for the paths that broke was part of finishing the upgrade.

### What each verification layer proved

The checks were not one thing. Each layer ran in a different environment and proved something different. They have different blind spots.

| Layer | Environment or stack | What it exercised | What it did not prove |
| --- | --- | --- | --- |
| `bin/rails zeitwerk:check` | The app's code, eager-loaded in one process | Every configured class and file loads under Rails 8 naming and boot rules | That any request or workflow behaves correctly |
| Backend specs (145 RSpec examples) | Rails test environment, test database | The model and request behavior that had assertions | Paths with no specs, and development-only configuration |
| End-to-end tests (18 Playwright tests) | Development server, seeded database, real browser | A fixed set of scripted flows, real login included, on the live stack | Screens and flows outside those scripts |
| Browser checklist (74 checks) | Same live stack, disposable seeded database | High-risk workflows against visible expected results | Anything not on the checklist, and exact figures where no known-value fixture exists |

**`zeitwerk:check`** surfaces naming and load-time problems at startup instead of on the first request that reaches them. Ours passed while the app was still broken behind login. Loading is the floor, not the finish line.

**Backend specs.** The suite stood at 142 green examples when the runtime failures appeared, and at 145 by the end, after three regression guards were added for failures the browser work found. Green meant the covered behavior still worked. The runtime 500s all lived in paths that had no specs: the development logger, the calendar, the totals, and the project search.

**End-to-end tests.** The 18 Playwright tests drive a real browser through the development stack and log in for real. That is why they hit the login 500 too, and went green only after the fixes landed. Their green run was strong evidence for the flows they script and no evidence for the screens they skip.

### How the browser checklist worked

The last layer was a written checklist of 74 browser checks, run top to bottom against a disposable seeded database with known logins. The first live run had caught the loudest failures. The checklist caught the next round: a billing report crash, broken report PDFs, and more date-formatting callers, all on pages no automated test visited. It is a method, not exploratory clicking.

The checklist was written from business risk, not from the menu. The app tracks hours, billing, and permissions, so the checks concentrate on the failure modes that would cost the most: money and time math, access control, dates, and silent server errors. That is also why it includes negative checks, where the expected result is a refusal.

Three rules keep a run honest. Every check states a visible expected result: exact text, a URL, a count, never "looks fine." Every result records what was actually seen, plus a screenshot as evidence. Any 500 response or browser console error is an automatic fail, no matter how the page looks.

A representative sample:

- **Valid login.** Log in with valid credentials. Expect: lands on the calendar, nav shows the logged-in email. Evidence: screenshot.
- **Invalid password.** Log in with a wrong password. Expect: stays on the login page with an error message shown. Evidence: screenshot.
- **Permission wall.** As a non-admin, open an admin URL directly. Expect: access refused, the admin page does not render. Evidence: screenshot.
- **Calendar renders.** Open the calendar. Expect: current month and year label, a grid of day cells. Evidence: screenshot.
- **Day drill-down.** Click a day cell. Expect: navigates to that day's entries, matching the clicked date. Evidence: screenshot.
- **Entry deletion.** Note the entry count, delete one entry. Expect: the count drops by exactly one. Evidence: screenshot.
- **Every report type.** Generate each report type. Expect: each renders with rows. Evidence: screenshot per type.
- **Report totals.** On a generated report, compare the row values to the grand total. Expect: the rows sum to the shown total. Evidence: screenshot.
- **Search.** Search for a project by name. Expect: the list filters to matching results. Evidence: screenshot.
- **Error roundup.** Across the whole run, watch for any 5xx response or red console error. Expect: none, and list every one seen.

The operator can be a person or an AI driving the browser. The checklist, the expected results, and the evidence rule stay the same either way, so both kinds of run are judged against the same artifact. Several of the new backend guard tests exist only because a checklist run found the failure first.

### Regression, or already broken?

During manual testing I found failures that would have been easy to just fix on the branch. Before fixing, I checked the same path on the tagged Rails 5 version. In four cases, it failed there, too. Those were real bugs, but they were not upgrade regressions. I kept them off the upgrade branch and filed them on their own, so the diff stayed about the upgrade and nothing else.

That distinction, upgrade regression versus pre-existing bug versus unsupported assumption versus missing coverage, is what kept the branch reviewable. A reviewer can read the 29 commits and see only upgrade work.

### Where AI helped, and where it stopped

I used AI heavily, but the useful part was not that it wrote code. It was that it made exploring unfamiliar, obsolete code cheap. The pattern was always the same. It proposed, I verified, and none of its proposals merged without evidence.

- **Removed idioms.** One initializer extended Rails' PostgreSQL type map for the application's custom scheduling type using `alias_method_chain`, an old Rails extension pattern that no longer exists. AI explained the old idiom and drafted the replacement, a module hooked in with `prepend` and `super`. I kept the change only after confirming the scheduling fields still loaded, saved, and returned correctly.

```ruby
module CronSpecTypeRegistration
  def initialize_type_map(mapping = type_map)
    super
    oid = select_value("SELECT oid FROM pg_type WHERE typname = 'cron_spec'")
    if oid
      mapping.register_type(
        oid.to_i,
        ActiveRecord::ConnectionAdapters::PostgreSQL::OID::SpecializedString.new(:cron_spec)
      )
    end
  end
end
ActiveRecord::ConnectionAdapters::PostgreSQLAdapter.prepend(CronSpecTypeRegistration)
```

- **Old behavior.** It explained why `to_s(:db)`, `sum` without a starting value, and untyped array binds behaved differently on the upgraded stack. I confirmed each against the running app, not against the explanation.
- **Strategy.** I used it to compare transplant versus incremental and to run a pre-mortem before committing. I made the decision.

I also kept a few plain files in the repo: the working rules, how we were collaborating, and the current resume point. A fresh session could start with "read the notes and continue," which kept the work easy to pick back up.

The one time I trusted an assumption instead of testing it, it cost me. Early on I kept an old JSON library, `yajl-ruby`, because I assumed the API endpoints needed it. They did not. It was quietly patching `JSON.dump` so several admin endpoints serialized their query results as real arrays, and the suite stayed green the whole time. Weeks later I removed the gem, and three React admin pages started rendering a raw object string instead of a list. The fix was to stop leaning on the patched `JSON.dump` and let Rails encode the response with `render json: relation`. This lesson proved everything else here: an untested assumption is not a safe one, however green the suite looks.

### A method for risky Rails migrations

If I did another AI-assisted Rails upgrade like this, I would keep the same short method:

- Before touching the upgrade, check spec coverage on the highest-risk paths and fill the gaps. Most of what bit us was plain missing coverage.
- Reproduce a failure on the old version before calling it a regression.
- Treat load checks, unit tests, end-to-end tests, and browser checks as four separate kinds of evidence, not one.
- Turn manually found regressions into automated tests, highest-risk paths first.
- Require visible evidence for browser checks: an expected result and a screenshot, not "looks fine."
- Keep the commit history small and readable, so a reviewer can follow the upgrade one change at a time.

AI made the exploration cheap. The evidence is what made the result trustworthy.
