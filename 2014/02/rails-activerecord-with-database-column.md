---
author: Kent Krenrich
title: Rails ActiveRecord with Database Column Defaults
github_issue_number: 922
tags:
- database
- rails
date: 2014-02-07
---

I had an interaction with a coworker recently that made me take stock of what occasions and situations I use database column defaults. I realized that far and away my primary use is for booleans. I commonly set a default on my boolean columns when I’m defining a new migration. I do this primarily to minimize the potential for three states—​true, false, and null—​when I usually want a boolean to be limited to either true or false.

Alongside the distillation down to the classically defined values, another perk of defaults in general is that Rails uses the table’s definition within the database to pre-fill attributes that are not included in the initialization params for an object. For example, a table with columns defined as follows:

```ruby
create_table :my_objects do |t|
  t.string :column_one, default: 'foo'
  t.string :column_two
end
```

Will result in:
```ruby
$> m = MyObject.new
  => #<MyObject id: nil, column_one: "foo", column_two: nil>
```

Note that column_two has no default and so is initialized to nil. But column_one is set to "foo" because no other value was supplied. This behavior can be quite handy for boolean attributes such as :published or :unread. Published can be a good example of a value that would start as false while unread is a good candidate to start out true.

It’s worth mentioning that defaults aren’t absolutely enforced. It is still your prerogative to override should you so choose. For example:

```ruby
$> m = MyObject.new(column_one: nil)
  => #<MyObject id: nil, column_one: nil, column_two: nil>
$> m.save
  => true
$> m
  => #<MyObject id: 1, column_one: nil, column_two: nil>
```

I mentioned my primary use for defaults is pairing them with booleans. Considering that overriding a default could defeat the purpose of having that default, pairing the default with a non-null constraint is one additional level of security you can provide yourself. For example, you can modify the original table definition as follows:

```ruby
create_table :my_objects do |t|
  t.boolean :column_one, default: true, null: false
  t.string :column_two
end
```

Attempting to save an occurrence of the above object with column_one set to nil would raise a database-specific error. If you don’t want to rescue an error, you can go one step further and add a validation to your Rails object.
```ruby
class MyObject < ActiveRecord::Base
  validates :column_one, inclusion: {in: [true, false]}
end
```

It’s probably worth noting the use of an inclusion validation instead of a presence validation. Using presence would disallow setting the boolean to false.

Personally, I usually stick with:

```ruby
t.boolean :column_one, default: <pick one>, null: false
```

I don’t find much need for the model validation since if I explicitly add the following line of code:
```ruby
my_object.boolean_column = nil
```

I’m confident that I won’t be doing it by accident. That only leaves the potential for:
```ruby
my_object.boolean_column = some_method
```

where some_method may have the potential to return a null value. I find that almost exclusively any method I assign to a boolean will be of the form “some_method?” which by convention should return either true or false. Again, strictly the two values I’m interested in representing.

In conclusion, though I don’t find myself using them on every project, I am happy to have this particular tool available in my repertoire for those not uncommon occasions where I can draw a benefit.
