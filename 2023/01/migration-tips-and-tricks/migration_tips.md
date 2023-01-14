---
author: "Joshua Tolley"
title: "Data Migration Tips"
date: 2023-01-12
tags:
- postgres
- data-processing
- database
- migration
---

When you're in the business of selling software to people, you tend to get a
few chances to migrate data from their legacy software to your shiny new
system. We've collected a few tips that may help you learn from our successes,
as well as our mistak^Wparticularly educational experiences. 

### Customer Management

Your job is to satisfy your customers, and **your customers want to know how
the migration is progressing**. Give them an answer, even if it's just a
generalization. This may be a burn down chart, a calculated percentage, a nifty
graphic, or whatever, but something your project managers can show to their
managers, to know more or less how far along things are.

Your job is also to know your system; that's not the customer's job. They
shouldn't have to get their data into a specific format for you to make use of
it. **Be as flexible as possible** in the data format and structure
you'll accept. In theory, so long as your customer can provide the legacy data
in a machine-readable format, you should be able to use it. Let them focus on
getting the data out of their legacy system -- which is sometimes quite an
effort in itself! Real data is almost always messy data, and your customer will
probably want to take the opportunity to clean things up; make it as easy as
possible for them to do that, while still ensuring the migration proceeds
quickly and smoothly.

**Be careful about the vocabulary you use** with your customer. Your system and
the legacy system probably deal with the same kinds of data, and do generally
the same kinds of things. Of course, your software does it better than the
old'n'busted mess you're replacing, but in order to be better, your software
has to be different from what it's replacing. Different software means
different methods, different processes, and different concepts. You and your
customer might use the same words to mean totally different things, and unless
you're careful, those differences can remain hidden well into the
implementation process, coming to light just in time to highlight some horrible
mistake you've made. Try to avoid that. Talk with your customer to make sure
your team and their team share a common vocabulary. If your system's core
function is to track widgets, and their legacy system's function is also to
track widgets, make sure you understand the differences between your software's
concept of a widget and their legacy system's concept of a widget.

### Migration Scripting

For our products and our customers, we've found pretty much every migration
process is different, and each one is a custom programming job. Your team
should **decide at the beginning what steps the migration needs to include,
and what technologies it will use** in each step. Here at End Point, we often
like to work directly in the database, in SQL. Migrations are all about
manipulating data, and SQL is well suited for that task. With whatever
technology you use, decide how you'll use it, to manage the considerations
given here. You can change your mind later and refactor accordingly, but always
have a plan you're following.

**Design the migration as a sequence of processes**. That is, first you might
import one type of record, next another type of record that depends on the
previous one, followed by several further steps to import data from a third
source, clean it, map values from the legacy system to the new system, validate
the results, and create records in the destination database. Of course the
steps will vary from project to project, but the point is your migration will
probably include several steps which need to be run in a specific order, so
plan your development conventions accordingly. At End Point, we often like to
**put each step in a SQL file, and name each file beginning with a number**, so
you can run each script in order sorted by filename, and achieve the correct
result. We might have files called `01_import_products.sql`,
`02_import_customers.sql`, and `03_import_order_history.sql`.

It's also common to implement each step one at a time, and to need to run each
step several times as it's being developed. We find it very helpful to **wrap
each step in a transaction**. Often that means each SQL file begins with a
`BEGIN;` statement, and ends with `COMMIT;`. Often I'll leave out the `COMMIT`
until I'm finished working on a file. That way to work on the code I can open a
database session and run the migration script I'm working on, and when it
completes, it will leave me inside the open transaction where I can inspect the
results of my work. I make changes to the script, roll back the transaction,
and run the script again, for as many iterations as it takes. I only add a
`COMMIT` when I've tested the whole file and think it's ready for the next step
in testing.

I mentioned above that the customer may want to use this opportunity to clean
their data. You should want this, too. **Make sure the data you're feeding your
new system is as clean and well-structured as possible**. You may find, as we
do, that most of the work in your migrations is in validating the input data,
and that actually creating new records in your application is almost an
afterthought. That's OK. You may also find there are places where your
application, wonderful though it may be, could stand to be more strict about
the data it accepts. I've often discovered my application needs a uniqueness
constraint, or a foreign key, thanks to a migration I was working on.

### Data Migration History

I wish I could truthfully claim all our migrations go off flawlessly, but that
would be a lie. It's not unheard of to run into some corner case, a few weeks
or even months after the migration goes live, which wasn't migrated correctly.
It's certainly not uncommon for a customer or coworker to spot something that
strikes them as odd, after the migration goes live, only find later that
everything was in fact correct. In either case, it's important to **preserve a
history of the migration** to investigate these concerns. We accomplish this
with a few specific steps:

* **Create a database schema for the migration, and a table within that schema for each data file, or object type we're importing.** I call these tables "staging tables", where the incoming data is "staged" as it's cleaned and validated. Having a separate schema means these tables can remain in the production database long after the migration is complete, generally without interfering with anything.
* These staging tables should generally **use text fields, to be as forgiving and flexible as possible with the incoming data.** We can clean, parse, and reformat the data after it's imported.
* **Don't change the data in these staging tables; add to the data instead.** In other words, if you need to map a value from the legacy system to a different value for your new system, don't change the column you imported into the staging table; instead, add a new column to the staging table where you'll store the re-mapped value. If you need to parse a text field into a date (because you followed the instruction to use text fields!), don't change the type of an imported column; instead, add a new column of date or timestamp type, to store the parsed value. That way, when three months down the road someone discovers that some of the imported records have weird dates, you have all the information you need to determine whether the fault lies with the imported data or some step of the migration progress. Knowing exactly where the fault crept in leaves you that much more empowered to fix it.
* **Keep track of your migrated records' primary keys, in the legacy system and the new system.** Imagine you've just imported your client's legacy customer list into a staging table. This data includes the legacy system's primary key. Add a new column to the table for your new system's primary key, and populate it. Many of our systems use an integer sequence as a primary key, so we'd add a new integer column to the staging table, and fill it with the next values from the sequence. Following this principle will give you several important abilities:
** You can always connect a record in the legacy system with its corresponding record(s) in the new system. If you've imported a customer list in this fashion, then when you're importing the order data later, and each order points to a customer using a legacy customer primary key, you can easily find the correct customer primary key to use in your system.
** You can easily know if a record in your system comes from the migration, or from normal day-to-day business. You will probably use this every time you try to debug something with your migration.
** If you need to remove all imported records and re-import them, you can identify exactly which records those are. This should be only rarely needed.

Finally, **document the decision making process, in comments directly in your
code.** For instance, if you have a table of mappings from one value to
another, chances are good you arrived at the final version of that mapping
table only after some discussion with the customer. Chances are also good
someone's going to question it later on. It's helpful to keep a comment around,
something like, `# Joe Rogers verified this is the correct mapping in the
daily standup meeting, 23 Nov 2022`. This is especially common if you
eventually decide to ignore a certain class of records. `/* Rebecca says ignore
all records with type = "ARCHIVED", via group email 9 Jan 2023 */` is a very
helpful clue when someone comes around wondering where those records went.

### Teamwork

My remaining tips apply to almost any programming project. First, **use source
control, and commit your code to it often.** I can't count how often I've been
grateful the git repository had a backup of my work, or made my work accessible
to fill some unexpected need on some other system, nor can I count how many
times I've been stuck because someone else didn't commit their code so I
couldn't get at it when I needed it.  Let's not talk about how many times I've
caused someone else to get stuck in the same way... Of course, don't commit
your customer's data. But you should commit your code, and commit it often.

Finally, where possible, **work with someone else.** Two programmers reviewing
each other's code and collaborating on solutions are often far better than two
programmers working alone, or one programmer working twice as much.

Speaking of working out solutions together, I'd love your help improving this
list. What keys have you found are important for data migration projects? I
welcome your comments. And if you're looking for someone to handle a data
migration project for you, give us a call!
