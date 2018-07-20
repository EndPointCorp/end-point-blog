---
author: Sonny Cook
gh_issue_number: 530
tags: rails, ruby, database
title: Modifying Models in Rails Migrations
---

One problem that has haunted me in the past was making modifications to the model in migrations. Specifically, stuff like removing or changing associations. At the time the migration is expected to run, the file for the model class will have been updated already, so it is hard use that in the migration itself, even though it would be useful.

In this case I found myself with an even slightly trickier example. I have a model that contains some address info. Part of that is an association to an external table that lists the states. So part of the class definition was like so:

```
Class Contact {
 belongs_to :state
 ...
}
```

What I needed to do in the migration was to remove the association and introduce another field called “state” which would just be a varchar field representing the state part of the address. The two problems the migration would encounter are:

1. the state association would not exist at the time it ran
1. and even if it did, there would be a name conflict between it and the
new column I wanted

to get around these restrictions I did this in my migration:

```
Contact.class_eval {
      belongs_to :orig_state,
                 :class_name => "State",
                 :foreign_key => "state_id" }
```

This loads the association association code into the context of the Contact class and gives me a new handle to work with, so I am free to create a “state” column without worrying about the names colliding.

Another problem I had was that the table had about 300 rows of data that failed one of the validations called “validate_names”. I didn’t feel like sorting it out, so I just added the following code to the above class_eval block:

```
define_method(:validate_names) { true }
```

This overrides the method for the validation in the class while the migration is running. I can sort out the invalid data later.
