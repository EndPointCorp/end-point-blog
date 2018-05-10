---
author: Mark Johnson
gh_issue_number: 1008
tags: bcrypt, ecommerce, interchange, security, sysadmin
title: Interchange 5.8.2 Release with Bcrypt Encryption Support
---



The most recent release of Interchange contains support for adding encryption to user passwords with [bcrypt](http://bcrypt.sourceforge.net/). This provides for a significant improvement over the previously supported encryption options. Whether you are starting with a new user table, or have a long-established user table with any of the other supported encryption types, you can take advantage of this enhancement to Vend::UserDB.

In order to utilize bcrypt, you will need to have successfully installed the [Digest::Bcrypt](http://search.cpan.org/~jaitken/Digest-Bcrypt-1.0.1/lib/Digest/Bcrypt.pm) and [Crypt::Random](http://search.cpan.org/~vipul/Crypt-Random-1.25/lib/Crypt/Random.pm) modules. Once installed, it is recommended (though not required, ironically) you add these as Required modules to interchange.cfg to ensure Interchange can find them and will report back immediately if not:

```
Require module Digest::Bcrypt
Require module Crypt::Random
```

To use bcrypt, configure your UserDB directive with the following options:

- bcrypt—​set to 1
- cost—​desired cost between 1 and 31 (optional; current default is 13)
- bcrypt_pepper—​random string used to apply a unique padding pattern (also optional, but strongly recommended)

To encourage adoption of bcrypt, there are two mechanisms available that allow a user table already using another encryption type to convert to using bcrypt. The first option is to add the “promote” directive—​set to 1—​to your UserDB configuration. This will cause passwords stored by any other encryption type to update to bcrypt upon the next successful access of that user account. This causes no disruption to site operations or your users, but it does mean you have to allow full adoption of bcrypt to advance organically as your users return to your site over time.

The second option builds on “promote” by allowing the developer to construct a background process to slurp in the existing passwords stored by another encryption type and generate a bcrypt storage value of the *encrypted* password, by utilizing the construct_bcrypt() subroutine in Vend::UserDB. construct_bcrypt() takes a single hashref argument with a required key “password” and optional keys “type” and “profile”. In this use case, password holds the encrypted password extracted from the existing user table and type contains one of “sha1”, “md5”, “md5_salted”, or “crypt”, corresponding to the encryption algorithm used to produce the password originally. The profile key maps to the profile name assigned to control this user table in the UserDB directive. Normally, this will be either “default”, which controls the userdb table, or “ui”, which controls the access table. Note that the profile used *must* already be configured to use bcrypt, or construct_bcrypt() will die. If profile is omitted, defaults to “default”. It is anticipated the developer would construct an Interchange job to query all the users and encrypted passwords still stored by the previous algorithm, pass each into construct_bcrypt(), and update the source record’s password field with the return value from construct_bcrypt().

For any configuration of UserDB utilizing bcrypt, it is recommended to enable “promote”. Not only is it a painless way to begin the transition of your encrypted user table to use bcrypt, it also ensures continuing access for your users even if you advance with the second option. For a large user table, it may take weeks for your background process to complete the transition. In the mean time, any users who access the site before their passwords are updated will still have access to the site using promote. Lastly, over time you will likely want to increase the cost parameter of bcrypt to keep pace with hardware advances. By using promote, users returning to your site will have their passwords updated to use the current cost in addition to new users being stored at the current cost. In short, if you bcrypt, use promote.

Example configuration changes for UserDB using bcrypt for the access table. Replace:

```
UserDB  ui  crypt 1
```

with:

```
UserDB  ui  bcrypt         1
UserDB  ui  promote        1
UserDB  ui  cost           13
UserDB  ui  bcrypt_pepper  mrPIQ4$.qgJrbvD(5CStB.p8b8ABbpl+:0.`I`*J`)j{=7KY*b(M@QXXg+9B*-b
```

Of course, your bcrypt_pepper will be some suitable random string you generate and keep private. The above is just an example.

Also be aware that the password storage will be larger than any previous stored passwords, up to 63 characters in length. So be sure your user table’s password field is sized (or resized, if necessary) to hold at least 63 characters.

### Peppering your Padding

To provide additional support to protect weaker passwords against brute-force attacks, the process pads out password length to at least 72 characters. This padding is considerably more effective by adding a secret pepper that ensures the pattern cannot be reproduced without knowing the pepper value. This is, however, no substitute for enforcing good minimum standards on your passwords to ensure they are not weak in the first place, and does absolutely nothing to protect against a hacker guessing passwords through the front end.

Once a password hash is created with a particular pepper (which includes the possibility of no pepper) it is permanently dependent on that value. That is to say, the pepper should be settled on prior to introducing the use of bcrypt. If the pepper is changed, any hashes created and stored with the previous pepper (or no pepper) will become inaccessible. Even “promote” won’t help here because in order for promote to function, both encryption types (the original and the target) must be able to work against the supplied password. Once a new value of “bcrypt_pepper” is introduced, Vend::UserDB loses access to the old pepper and, thus, cannot use it to test the validity of the password proffered by the user against the existing stored data structure.

If it becomes unavoidable to change a pepper, a developer would have to create a new UserDB profile with the old pepper, write custom code to use the new profile to validate the password obtained from the user and, upon success, update the password field in the user table in the custom code with the new structure built with the profile holding the new pepper. This could be done using construct_bcrypt() but is in no way natively supported as a promotable option. Moreover, there is no mechanism to allow such an update to occur as a background process, as is available to migrate the other encryption types to bcrypt.


