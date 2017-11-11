---
author: Kent Krenrich
gh_issue_number: 1228
tags: database, ruby, rails
title: Randomized Queries in Ruby on Rails
---

I was recently asked about options for displaying a random set of items from a table using Ruby on Rails. The request was complicated by the fact that the technology stack hadn’t been completely decided on and one of the items still up in the air was the database. I’ve had an experience with a project I was working on where the decision was made to switch from MySQL to PostgreSQL. During the switch, a sizable amount of hand constructed queries stopped functioning and had to be manually translated before they would work again. Learning from that experience, I favor avoidance of handwritten SQL in my Rails queries when possible. This precludes the option to use built-in database functions like rand() or random().

With the goal set in mind, I decided to look around to find out what other people were doing to solve similar requests. While perusing various suggested implementations, I noticed a lot of comments along the lines of “Don’t use this approach if you have a large data set.” or “this handles large data sets, but won’t always give a truly random result.”

These comments and the variety of solutions got me thinking about evaluating based not only on what database is in use, but what the dataset is expected to look like. I really enjoyed the mental gymnastics and thought others might as well.

Let’s pretend we’re working on an average project. The table we’ll be pulling from has several thousand entries and we want to pull back something small like 3-5 random records. The most common solution offered based on the research I performed works perfectly for this situation.

```
records_desired = 3
count = [OurObject.count, 1].max
offsets = records_desired.times.inject([]) do |offsets|
  offsets << rand(count)
end
while count > offsets.uniq!.size && offsets.size < records_desired do
  offsets << rand(count)
end
offsets.collect {|offset| OurObject.offset(offset).first}
```

Analyzing this approach, we’re looking at minimal processing time and a total of four queries. One to determine the total count and the rest to fetch each of our three objects individually. Seems perfectly reasonable.

What happens if our client needs 100 random records at a time? The processing is still probably within tolerances, but 101 queries? I say no unless our table is Dalmations! Let’s see if we can tweak things to be more large-set friendly.

```
records_desired = 100
count = [OurObject.count - records_desired, 1].max
offset = rand(count)
OurObject.limit(records_desired).offset(offset)
```

How’s this look? Very minimal processing and only 2 queries. Fantastic! But is this result going to appear random to an observer? I think it’s highly possible that you could end up with runs of related looking objects (created at similar times or all updated recently). When people say they want random, they often really mean they want unrelated. Is this solution close enough for most clients? I would say it probably is. But I can imagine the possibility that for some it might not be. Is there something else we can tweak to get a more desirable sampling without blowing processing time sky-high? After a little thought, this is what I came up with.

```
records_desired = 100
count = records_desired * 3
offset = rand([OurObject.count - count, 1].max)
set = OurObject.limit(count).offset(offset).pluck(:id)
OurObject.find(ids.sample(records_desired))
```

While this approach may not truly provide more random results from a mathematical perspective, by assembling a larger subset and pulling randomly from inside it, I think you may be able to more closely achieve the feel of what people expect from randomness if the previous method seemed to return too many similar records for your needs.
