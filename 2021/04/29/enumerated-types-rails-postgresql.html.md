---
author: "Patrick Lewis"
title: "Enumerated Types in Rails and PostgreSQL"
tags: ruby, rails, postgres
gh_issue_number: 1735
---

![enumeration](/blog/2021/04/29/enumerated-types-rails-postgresql/banner.jpg)
[Photo](https://flic.kr/p/euTck) by [Jared Tarbell](https://flickr.com/people/generated/), used under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/), cropped from original.

Enumerated types are a useful programming tool when dealing with variables that have a predefined, limited set of potential values. An example of an enumerated type from [Wikipedia](https://en.wikipedia.org/wiki/Enumerated_type) is “the four suits in a deck of playing cards may be four enumerators named Club, Diamond, Heart, and Spade, belonging to an enumerated type named suit”.

I use enumerated types in my Rails applications most often for model attributes like “status” or “category”. Rails’ implementation of enumerated types in [ActiveRecord::Enum](https://api.rubyonrails.org/classes/ActiveRecord/Enum.html) provides a way to define sets of enumerated types and automatically makes some convenient methods available on models for working with enumerated attributes. The simple syntax does belie some potential pitfalls when it comes to longer-term maintenance of applications, however, and as I’ll describe later in this post, I would caution against using this basic 1-line syntax in most cases:

```ruby
enum status: [:active, :archived]
```

The Rails implementation of enumerated types maps values to integers in database rows by default. This can be surprising the first time it is encountered, as a Rails developer looking to store status values like “active” or “archived” would typically create a string-based column. Instead, Rails looks for an numeric type column and stores the index of the selected enumerated value (0 for active, 1 for archived, etc.).

This exposes one of the first potential drawbacks of this minimalist enumerated type implementation: the stored integer values can be difficult to interpret outside the context of the Rails application. Although querying records in a Rails console will map the integer values back to their enumerated equivalents, other database clients are simply going to return the mapped integer values instead, leaving it up to the developer to look up what those 0 or 1 values are supposed to represent.

A larger problem that arises from defining an enum as an array of values is that the values are tied to the order of elements in an array. This means any change to the order or length of the array can have unwanted consequences on the mapped values.

```ruby
# don't do this; the index of active is changed from 0 to 1, archived from 1 to 2
enum status: [:abandoned, :active, :archived]
```

At a minimum, I would recommend using this hash-based syntax for defining enumerated types with explicit integer mapping:

```ruby
enum status: {
  active: 0,
  archived: 1
}
```

This provides the benefit of documenting which integers are mapped to which enumerated values, and also provides more flexibility for future adjustments. For example, a new status value can now be added to the enumerated type without disrupting any of the existing records:

```ruby
enum status: {
  abandoned: 2,
  active: 0,
  archived: 1
}
```

For Rails applications with PostgreSQL databases, it’s possible to go one step further and get most of the best of both worlds: the efficiency of using predefined enumerated types while still maintaining the ability to store meaningful string values at the database level. This is made possible by combining Rails enums with [PostgreSQL Enumerated Types](https://www.postgresql.org/docs/current/datatype-enum.html).

This technique requires using a migration to first define a new enumerated type in the database, and then creating a column in the model’s table to use that PostgreSQL type:

```ruby
class AddEnumeratedStatusToDevices < ActiveRecord::Migration[5.2]
  def up
    execute <<-SQL
      CREATE TYPE device_status AS ENUM ('abandoned', 'active', 'archived');
    SQL

    add_column :devices, :status, :device_status
    add_index :devices, :status
  end

  def down
    remove_index :devices, :status
    remove_column :devices, :status

    execute <<-SQL
      DROP TYPE device_status;
    SQL
  end
end
```

The corresponding model code to use this new enumerated type looks similar to before, but now the values are mapped to strings:

```ruby
class Device < ApplicationRecord
  enum status: {
    abandoned: "abandoned",
    active: "active",
    archived: "archived"
  }
end
```

This combination of Rails and PostgreSQL enumerated types has become my preferred approach in most situations. One limitation to be aware of with this approach is that PostgreSQL enumerated types can be extended with [ALTER TYPE](https://www.postgresql.org/docs/current/sql-altertype.html), but existing values cannot be removed. There is a small bit of additional development overhead introduced with the need to manage the enumerated type at both the Rails and the PostgreSQL level, but I like having the option of querying records by the string values of attributes, and the use of a PostgreSQL enumerated type provides for more efficient database storage than simply using a string type column.
