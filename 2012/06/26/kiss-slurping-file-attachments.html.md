---
author: Steph Skardal
gh_issue_number: 659
tags: rails
title: 'KISS: Slurping up File Attachments'
---

I've been heavily involved in an ecommerce project running on Rails 3, using [Piggybak](http://www.piggybak.org/), [RailsAdmin](https://github.com/sferik/rails_admin), [Paperclip]() for file attachment management, [nginx](http://nginx.org/) and [unicorn](http://unicorn.bogomips.org/). One thing that we've struggled with is handling large file uploads both in the [RailsAdmin import](/blog/2012/02/01/railsadmin-import-part-2) process as well as from the standard RailsAdmin edit page. Nginx is configured to limit request size and duration, which is a problem for some of the large files that are uploaded, which are large purchasable, downloadable files.

To allow these uploads, I brainstormed how to decouple the file upload from the import and update process. Phunk recently worked on integration of [Resque](https://github.com/defunkt/resque), a popular Rails queueing tool which worked nicely. However, I ultimately decided that I wanted to go down a simpler route. The implementation is described below.

### Upload Status

First, I created an UploadStatus model, to track the status of any file uploads. With RailsAdmin, there's an automagic CRUD interface connected to this model. Here's what the migration looked like:

```ruby
class CreateUploadStatuses < ActiveRecord::Migration
  def change
    create_table :upload_statuses do |t|
      t.string :filename, :nil => false
      t.boolean :success, :nil => false, :default => false
      t.string :message

      t.timestamps
    end
  end
end
```

RailsAdmin also leverages [CanCan](https://github.com/ryanb/cancan/), so I updated my ability class to allow list, reads, and delete on the UploadStatus table only, since there is no need to edit these records:

```ruby
      cannot [:create, :export, :edit], UploadStatus
      can [:delete, :read], UploadStatus
```

### KISS Script

Here's the simplified rake task that I used for the process:

```ruby
namespace :upload_files do
  task :run => :environment do
    files = Dir.glob("#{Rails.root}/to_upload/*.*")
    files.each do |full_filename|
      begin
        ext = File.extname(full_filename)
        name = File.basename(full_filename, ext)

        (klass_name, field, id) = name.split(':')
        klass = klass_name.classify.constantize
        item = klass.find(id)

        if item.nil?
          UploadStatus.create(:filename => "#{name}#{ext}", :message => "Could not find item from #{id}.")
          next
        end

        item.send("#{field}=", File.open(full_filename))

        if item.save
          FileUtils.rm(full_filename)
          UploadStatus.create(:filename => "#{name}#{ext}", :success => true)
        end
      rescue Exception => e
        UploadStatus.create(:filename => "#{name}#{ext}", :message => "#{e.inspect}")
      end
    end
  end
end
```

And here's how the process breaks down:

1. The script iterates through files in the #{Rails.root}/to_upload directory (lines 3-4).
1. Based on the filename, in the format "class_name:field:id.extension", the item to be updated is retrieved (line 11).
1. If the item does not exist, an upload_status record is created with a message that notes the item could not be found (lines 13-16).
1. If the file exists and the update occurs, the original file is deleted, and a successful upload status is recorded (lines 18-23).
1. If the process fails anywhere, the exception is logged in a new upload status record (lines 24-26).

This rake task is then called via a nightly cron job to slurp up the files. The simple script eliminates the requirement to upload large files via the admin interface, and decouples the upload from Paperclip/database management. It also has the added benefit of reporting the status to the administrators by leveraging RailsAdmin. Many features can be added to it, but it does the job that we need without much development overhead.
