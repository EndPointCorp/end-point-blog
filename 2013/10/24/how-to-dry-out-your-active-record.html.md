---
author: Kamil Ciemniewski
gh_issue_number: 866
tags: database, ruby, rails, sql
title: How to DRY out your Active Record queries with Squeel
---



Active Record alone isn’t enough when it comes to having a data-access code-base that is DRY and clean in real world Rails applications. You need a tool like the [squeel](https://github.com/activerecord-hackery/squeel) gem and some good practices in place.

### Using JOIN with Active Record is cumbersome

Having JOINs in composable data-access Rails code, quickly makes the code ugly and hard to read.

Consider this snippet of code taken directly from Rails guides, that gives developer a full control over the joining part of the query:

```ruby
Client.joins('LEFT OUTER JOIN addresses ON addresses.client_id = clients.id')
```

That’s 77 characters for something as simple as a left outer join.

Now—​when using Rails, we almost always have properly defined associations in our models, which allows us to put in code something like this:

```ruby
Category.joins(:posts)
```

That’s much better—​there’s not much code and you immediately know what it does. It isn’t “left outer join” but is useful nevertheless. You could do more with that feature. For example you could join with multiple associations at once:

```ruby
Post.joins(:category, :comments)
```

Also—​join with nested associations:

```ruby
Post.joins(comments: :guest)
```

Which produces:

```sql
SELECT posts.* FROM posts
INNER JOIN comments ON comments.post_id = posts.id
INNER JOIN guests ON guests.comment_id = comments.id
```

Another example from the Rails guides shows that you can join multiple nested associations as well:

```ruby
Category.joins(posts: [{comments: :guest}, :tags])
```

Producing:

```sql
SELECT categories.* FROM categories
INNER JOIN posts ON posts.category_id = categories.id
INNER JOIN comments ON comments.post_id = posts.id
INNER JOIN guests ON guests.comment_id = comments.id
INNER JOIN tags ON tags.post_id = posts.id
```

Specifying conditions on nested associations works nicely according to the guides too:

```ruby
time_range = (Time.now.midnight - 1.day)..Time.now.midnight
Client.joins(:orders).where(orders: {created_at: time_range})
```

And indeed this looks pretty **sweet**.

### The ugly side of the Active Record JOIN mechanism

If the real world would consist only of the use cases found in docs—​we wouldn’t need to look for any better solutions.

Take a look at the following example that might occur:

```ruby
@tags = params[:tags]
Post.joins(comments: [{guest: :tags}]).
     where(comments: {guest: {tags: {code: @tags}}})
```

Now try to look at this code and answer the question:

“what does this code do?”.

### Squeel—​The missing query building DSL

The last example could be easily stated using squeel as:

```ruby
@tags = params[:tags]
Post.joins{comments.guest.tags}.
     where{comments.guest.tags.code << my{@tags}}
```

Isn’t that simpler and easier to read and comprehend?

#### What about queries you wouldn’t do even in Active Record?

If you were to produce a query with e.g. left outer join—​you’d have to resort to writing the joining part in a string. With squeel you can just say:

```ruby
Person.joins{articles.outer}
```

#### Can I do the same with subqueries?

Surely you can, take a look here:

```ruby
awesome_people = Person.where{awesome == true}
Article.where{author_id.in(awesome_people.select{id})}
```

Which produces the following SQL query:

```sql
SELECT "articles".* FROM "articles"
WHERE "articles"."author_id" IN 
  (SELECT "people"."id" FROM "people"  WHERE "people"."awesome" = 't')
```

#### But if I were to use SQL functions—​I’d have to write queries in strings, no?

No! Take a look here:

```ruby
Person.joins{articles}.group{articles.title}.
       having{{articles => {max(id) => id}}}
```

Producing:

```sql
SELECT "people".* FROM "people"
INNER JOIN "articles" ON "articles"."person_id" = "people"."id"
GROUP BY "articles"."title"
HAVING max("articles"."id") = "articles"."id"
```

### Why use a DSL to generate SQL?—​Composability

At this point many hard-core database experts sit with a wry face, frowning at the idea of having an ORM and DSL for accessing the database.

I won’t go into reasons as to why their concerns are valid or not. I’ll just say that I completely understand and feel most of them.

Here though, is an argument **for** using those DSLs: you simply can’t compose SQL strings easily, mixing and matching many of them in order to have a DRY and maintainable code base.

You can’t compose:

```sql
SELECT "people".* FROM "people"
WHERE "people"."active" IS TRUE
```

With:

```sql
SELECT "people".* FROM "people"
WHERE "people"."sex" = 'female'
```

But with a DSL like squeel you can easily define:

```ruby
def self.active
  where{active == true}
end

def self.females
  where{sex == 'female'}
end
```

And then in your controller say:

```ruby
def index
  @people = Person.active.females
end
```

And nothing would stop you from reusing those methods to build nice looking and easy to comprehend queries.

### More to read

I encourage you to visit the [squeel GitHub pages](https://github.com/activerecord-hackery/squeel). The documentation is well written and very easy to grasp.


