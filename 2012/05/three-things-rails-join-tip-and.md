---
author: Steph Skardal
title: 'Three Things: Rails, JOIN tip, and Responsiveness'
github_issue_number: 612
tags:
- browsers
- css
- rails
- tips
date: 2012-05-11
---



Here’s another entry in my *Three Things* series, where I share a few small tips I’ve picked up lately.

### 1. Rails and Dramas

Sometimes I think that since Rails allows you write code efficiently, [a few] members of the Rails community have time to overdramatize incidents that otherwise would go relatively unnoticed :) Someone with a good sense of humor created [this website](https://web.archive.org/web/20120531143155/http://rubydramas.com/) to track these dramas. While it’s probably a waste of time to get caught up on the personal aspects of the drama, some of the dramas have interesting technical aspects which are fiercely defended.

### 2. JOIN with concat

Recently I needed to perform a JOIN on a partial string match in MySQL. After some investigation, I found that I had use the CONCAT method in a conditional (in an implicit inner JOIN), which looked like this:

```sql
SELECT * FROM products p, related_items ri WHERE concat(p.sku, '%') = ri.id
```

In modern MVC frameworks with ORMs, databases are typically not designed to include data associations in this manner. However, in this situation, data returned from a third party service in a non-MVC, ORM-less application was only a substring of the original data. There may be alternative ways to perform this type of JOIN, and perhaps my fellow database experts will comment on the post with additional techniques ;)

### 3. Responsiveness

Responsive web design is all the rage lately from the increase in mobile web browsing and tablets. [Here](http://mattkersley.com/responsive/) is a fun tool that that the ecommerce director at [Paper Source](https://www.papersource.com/) pointed out to me recently. The website allows you to render a single URL at various widths for a quick review of the UI.


