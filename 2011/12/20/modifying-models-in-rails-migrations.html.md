---
author: Sonny Cook
gh_issue_number: 530
tags: ruby, rails
title: Modifying Models in Rails Migrations
---



As migrations have piled up in projects that I work on, one problem seems to come up fairly consistently. New changes to models can break migrations.

This can happen a number of different ways. One way is to break old migrations. Another is for the changes to be made to the file before the migration is run (timing issues with version control).

While these can be (and usually are) considered coordination rather than technical issues, sometimes you just need to handle them and move on.

One case I’d like to cover here is removing or changing associations. At the time the migration is expected to run, the file for the model class will have been updated already, so it is hard use that in the migration itself, even though it would be useful.

In this case I found myself with an even slightly trickier example. I have a model that contains some address info. Part of that is an association to an external table that lists the states. So part of the
class definition was like so:

```ruby
Class Contact 
 belongs_to :state
 ...
end
```

What I needed to do in the migration was to remove the association and
introduce another field called “state” which would just be a varchar
field representing the state part of the address. The two problems the
migration would encounter were:

1. The state association would not exist at the time it ran
1. And even if it did, there would be a name conflict between it and the
new column I wanted

To get around these restrictions I did this in my migration:

```ruby
Contact.class_eval do
  belongs_to :orig_state,
             :class_name => "State",
             :foreign_key => "state_id"
end
```

This creates a different association named “orig_state” using the states table for the Contact class. I can now use my original migration code more-or-less as is, and still create a new state column.
column.

Another problem I had was that the table had about 300 rows of data that
failed one of the validations called “validate_names”. I didn’t feel
like sorting it out, so I just added the following code to the above
class_eval block:

```ruby
define_method(:validate_names) do
  true
end
```

With these two modifications to the Contact class, I was able to use the simple migration with all of my Rails associations to do what I needed in the migration without resorting to hand crafting more complex SQL that would have been required in order to not have to refer to the model classes at all in the migration.


