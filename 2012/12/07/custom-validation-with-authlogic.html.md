---
author: Marina Lohova
gh_issue_number: 731
tags: rails
title: 'Custom validation with authlogic: Password can''t be repeated.'
---



I recently worked on a small security system enhancement for one of my projects: the user must not be able to repeat his or her password for at least ten cycles of change. Here is a little recipe for all the [authlogic](https://github.com/binarylogic/authlogic) users out there.

We will store ten latest passwords in the users table.

```ruby
def self.up
    change_table :users do |t|
      t.text    :old_passwords
    end
  end
```

The database value will be serialized and deserialized into Ruby array.

```ruby
class User
  serialize :old_passwords, Array
end
```

If the crypted password field has changed, the current crypted password and its salt are added to the head of the array. The array is then sliced to hold only ten passwords.

```ruby
def update_old_passwords
  if self.errors.empty? and send("#{crypted_password_field}_changed?")
    self.old_passwords ||= []
    self.old_passwords.unshift({:password =&gt; send("#{crypted_password_field}"), :salt =&gt;  send("#{password_salt_field}") })
    self.old_passwords = self.old_passwords[0, 10]
  end
end
```

The method will be triggered after validation before save.

```ruby
class User
  after_validation :update_old_passwords
end
```

Next, we need to determine if the password has changed, excluding the very first time when the password is set on the new record.

```ruby
class User &lt; ActiveRecord::Base
  def require_password_changed?
    !new_record? &amp;&amp; password_changed?
  end
end
```

The validation method itself is implemented below. The idea is to iterate through the stored password salts and encrypt the current password with them using the authlogic mechanism, and then check if the resulting crypted password is already present in the array.

```ruby
def password_repeated?
  return if self.password.blank?
  found = self.old_passwords.any? do |old_password|
    args = [self.password, old_password[:salt]].compact
    old_password[:password] == crypto_provider.encrypt(args)
  end
  self.errors.add_to_base "New password should be different from the password used last 10 times." if found
end
```

Now we can plug the validation into the configuration.

```ruby
class User &lt; ActiveRecord::Base
  acts_as_authentic do |c|
    c.validate :password_repeated?, :if =&gt; :require_password_changed?
  end
end
```

Done!


