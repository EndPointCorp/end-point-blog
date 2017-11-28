---
author: Brian Gadoury
gh_issue_number: 832
tags: database, mysql, postgres, ruby, rails
title: 'SFTP virtual users with ProFTPD and Rails: Part 2'
---



In [Part 1 of "SFTP virtual users with ProFTPD and Rails"](/blog/2012/12/20/sftp-virtual-users-with-proftpd-and), I introduced [ProFTPD](http://www.proftpd.org/)'s virtual users and presented my annotated proftpd.conf that I used to integrate virtual users with a Rails application. Here in Part 2, I'll show how we generate virtual user credentials, how we display them to the user, as well as our SftpUser ActiveRecord model that does the heavy lifting. 

Let's start at the top with the SFTP credentials UI. Our app's main workflow actually has users doing most of their uploads through a sweet [Plupload widget](http://www.plupload.com/). So, by default, the SFTP functionality is hidden behind a simple button sitting to the right of the Plupload widget:

<div class="separator" style="clear: both; text-align: center;"><img border="0" src="/blog/2013/07/10/sftp-virtual-users-with-proftpd-and/image-0.png"/></div>

The user can click that button to open the SFTP UI, or the Plupload widget will open it automatically if the user tries to upload a file through the widget that is too big. Either way, it uses a jQuery UI function to slide the SFTP UI open. Before it makes the jQuery call, an Ajax request is made to request a new SFTP virtual user username and password. When that request returns, we populate those two textboxes. At that point, that virtual user exists as a new row in the sftp_users database table. At this point in the workflow, the user will be able to login using those credentials, and upload their files.

<div class="separator" style="clear: both; text-align: center;"><img border="0" src="/blog/2013/07/10/sftp-virtual-users-with-proftpd-and/image-1.png"/></div>

Let's go look at our shiny new virtual user in the sftp_users table:

```nohighlight
-[ RECORD 1 ]-+-----------------------------------
id            | 1
user_id       | 3
username      | user13A84C76
passwd        | {sha1}5kT0WDb/5H6C8M92dTeiKQO0Kg0=
uid           |
sftp_group_id |
homedir       | /home/sftp/uploads/3/user13A84C76
shell         |
created_at    | 2013-07-08 17:24:24.780753
```

The id and user_id fields are ignored by ProFTPD (they're just standard primary/foreign key integers.) The username can be anything, so we just use "user" plus a random-enough hex string. The way we configured ProFTPD in Part 1 means our virtual users have absolutely nothing to do with normal system users, so the uid, sftp_group_id and shell fields can be empty. 

The homedir has three components: "/home/sftp/uploads" must exist and be writable by the effective UID that is running your Rails app. The directory named "3" is the value from the user_id field. (Adding that additional level lets us associate these virtual users with actual web app users should we need to debug, etc.) Lastly, each *virtual* user gets its own directory underneath that. In this example, ProFTPD will create the "3" and "3/user13A84C76" directories when that virtual user logs in. The format of the value in the passwd field is highly dependent upon your proftpd.conf settings for SQLAuthTypes. The format shown here matches the proftpd.conf shown in Part 1 of this article, if you're a copying and pasting type. The created_at field is ignored by ProFTPD, but it's handy info to have.

Let's look at the relevant methods implemented by our SftpUser ActiveRecord model.

```ruby
  def hash_password(password)
    "{sha1}" + Base64.strict_encode64(Digest::SHA1.digest(generate_password))
  end

  def generate_username
    'user' + SecureRandom.hex(4).upcase
  end

  def generate_password
    SecureRandom.hex(8).downcase
  end
```

Admittedly, there's no deep wizardry going on there. The critical piece is that the password gets hashed in the format that ProFTPD expects. Our hash_password method handles that for us here. (You can do whatever you want for the username and the raw password.) As a caveat, upgrading from Ruby 1.8.7 to 1.9.3 required replacing the Base64.encode64 call with Base64.strict_encode64.

Ok, that's the end of Part 2. We now have a new virtual user with credentials that can be used to login via SFTP. We've displayed those credentials to the user using jQuery UI and Ajax. Each virtual user gets its own chrooted home directory that is created only if and when they log in. The next steps in the workflow will be discussed in Part 3: How the user signals they are done uploading via SFTP, using Resque to make the Rails app process the files uploaded by the user, preventing upload overlap and re-entrant problems, and cleaning up after a virtual user's files are successfully processed offline by the Rails app.


