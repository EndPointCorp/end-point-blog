---
author: Mike Farmer
gh_issue_number: 599
tags: ruby, rails
title: Using CarrierWave without an ORM in Spree
---

I was recently adding some settings to Spree (an open source Ruby on Rails ecommerce framework) using Spree's built-in preferences system and found myself needing to upload an image as part of the settings. Our application was already using [CarrierWave](https://github.com/jnicklas/carrierwave) to handle some other uploads and wanted to use it to handle the uploading for my current image as well. Since the only setting I was setting was the image and there would only ever be one image, I didn't want to tie the setting to ActiveRecord. So I did some reading and found that you can tie a CarrierWave to a class without an ORM. The documentation on this is very sparse so I resorted to reading through the code to figure out how to get it working. After hours of playing with it I finally got it working. With the [current movement in the Rails community](http://blog.endpoint.com/2012/04/deconstructing-oo-blog-designs-in-ruby.html) to move more toward an Object Oriented approach to building applications, I've decided to document this here so that others will be able to quickly tie CarrierWave uploaders to their non-persisted classes.

The uploader I'll be working on is to add a banner to the checkout process in Spree (0.60.x). The idea is to store the image url in Spree::Config (the general preferences mechanism within Spree). For those who unfamiliar, Spree::Config acts very similar to a Hash object that is persisted to the preferences table in the database.

## The RSpec

Here are the tests that I will be using for the class. Hopefully these are fairly self explanatory.

```ruby
# spec/checkout_view_setting_spec.rb
require 'spec_helper'
require File.join(Rails.root, 'lib', 'checkout_view_setting.rb')

describe CheckoutViewSetting do
  include ActionDispatch::TestProcess
  before do
    @config = mock("Config")
    @cv = CheckoutViewSetting.new(@config)
    @uploaded_file = Rack::Test::UploadedFile.new(Rails.root.join('spec/support/test_image.png'), 'image/png')
  end

  it "should store the image in the config" do
    @config.should_receive(:[])
      .with(CheckoutViewSetting::IMAGE_ID_CONFIG_KEY)
      .and_return nil
    @config.should_receive(:set)
      .with({CheckoutViewSetting::IMAGE_ID_CONFIG_KEY => @uploaded_file.original_filename})

    @cv.image = @uploaded_file
    @cv.image_cache.include?(@uploaded_file.original_filename).should be_true
    @cv.write_image_identifier
    @cv.store_image!
  end

  it "should be able to set the image as form params" do
    @config.should_receive(:[])
      .with(CheckoutViewSetting::IMAGE_ID_CONFIG_KEY)
      .and_return nil

    @config.should_receive(:set)
      .with({CheckoutViewSetting::IMAGE_ID_CONFIG_KEY => @uploaded_file.original_filename})
      .and_return(@uploaded_file.original_filename)

    @cv.update_config(:image => @uploaded_file)
  end

  it "should be able to remove the image as form params" do
    @config.should_receive(:[])
      .with(CheckoutViewSetting::IMAGE_ID_CONFIG_KEY)
      .and_return nil
    @config.should_receive(:set)
      .with({CheckoutViewSetting::IMAGE_ID_CONFIG_KEY => nil})
      .and_return(nil)

    @cv.update_config(:remove_image => "1")
  end
end
```

The first thing I do here is mock the Spree config so that I can watch when the configuration gets written to make sure that works ok. I'm going to trust CarrierWave to do its thing as far as storing and removing the image. But what I'm really interested in for my tests is that the correct identifiers get read and set in the Spree::Config object. I'm also using the exact uploaded file object that will be passed to a Rails controller during the form submission so I don't have to worry about whether the image is the proper format.

In the next test, I want to make sure that I can use the standard conventions for setting the image straight from the class. The next two test cases I want to test the ability to pass a set of params as they would come from a form submission to save and remove an image. This matches the behavior you get when attaching CarrierWave to an ActiveRecord object.

## Building the Class

One of the really nice things about CarrierWave is the design of the library. The record that is going to hold the information about the uploaded file can be any class so long as it implements a few methods for handling the reading and the writing of a serialized identifier. In ActiveRecord, this is a string field. For our example here, we are going to use the Spree::Config object. But it could be any method you choose to implement.

In its simplest form, our class is going to look like this:

```ruby
# lib/checkout_view_setting.rb
require 'carrierwave/mount'

class CheckoutViewSetting
  extend CarrierWave::Mount
  mount_uploader :image do
    def default_url
      ""
    end
  end

  IMAGE_ID_CONFIG_KEY = :checkout_view_setting_image_id

  attr_reader :config

  def initialize(config)
    @config = config
  end

  def configured?
    ! @config[IMAGE_ID_CONFIG_KEY].nil?
  end

  # called to read the serialized identifier
  def read_uploader(column)
    @config[IMAGE_ID_CONFIG_KEY]
  end

  # called to write the serialized uploader
  # In Spree 0.60.x you cannot set attributes directly through []= like you can in the newer versions.
  # So I use the set method to assign the value
  def write_uploader(column, identifier)
    @config.set IMAGE_ID_CONFIG_KEY => identifier
  end

  def write_remove_image_identifier
    write_uploader(:image, nil)
  end

  def store_remove_image!
    remove_image!
  end
end
```

The code above will allow our first test to pass. There's a bunch of stuff going on here, so I'll walk through the important parts:

- require 'carrierwave/mount' just loads the CarrierWave mount library.
- extend CarrierWave::Mount will add the mount_uploader method to our class so that we can designate which uploader we are going to use. Each file that is uploaded requires an uploader, so if our class were going to upload a banner and footer image, we would need an uploader for both of those.
- IMAGE_ID_CONFIG_KEY = :checkout_view_setting_image_id is a unique key in the Spree::Config preferences system that is going to contain the image identifier.

The two most important methods here are the write_uploader and read_uploader. These methods will be called by CarrierWave to get and set your identifier. Here, I'm just setting those in the config. The configured? method is just for convenience to see if the value is set. The other two methods are used when removing the image.

When mount_uploader is called, a bunch of methods are automatically defined in your class and they will all have the name of your uploader in the method name. It also takes a configuration block where you can configure your uploader. Another option is to create your uploader class like you would in a typical CarrierWave setup, but I chose to use an anonymous uploader here for brevity. Oh, and all those methods that were defined? Here's a list of methods that were defined in my class:

- image
- image=
- image?
- image_url
- image_cache
- image_cache=
- remote_image_url
- remote_image_url=
- remove_image
- remove_image!
- remove_image=
- remove_image?
- store_image!
- image_integrity_error
- image_processing_error
- write_image_identifier
- image_identifier
- store_previous_model_for_image
- find_previous_model_for_image
- remove_previously_stored_image

Pretty nice! You can see how this is done by [checking out the source code on GitHub](https://github.com/jnicklas/carrierwave/blob/master/lib/carrierwave/mount.rb). Now that these methods are in place, my class will act just like an ActiveRecord object with CarrierWave!

Well, almost. CarrierWave lets you do some pretty cool stuff with ActiveRecord's update_attributes method. For example, setting a value of :remove_image => 1 in the params with a checkbox will call the remove_image= method on your class. Since my class doesn't have an update_attributes method, I'm going to implement something similar with a method called update_config that will accept params from a form and act in a similar fashion to ActiveRecord. Here's the code I came up with (borrowed heavily from ActiveRecord).

```ruby
# stores the setting similar update_attributes in ActiveRecord
# if a remove_image param is present, the image is removed instead of added.
def update_config(params)
  return @config if params.empty?
  begin
    safe_params = params.reject {|k,v| ! %w(image remove_image).include?(k.to_s) }
    safe_params.each do |k,v|
      send("#{k}=", v)
      send("write_#{k}_identifier")
      send("store_#{k}!")
    end
  rescue => e
    Rails.logger.error "Error uploading Checkout View Setting: #{e.message}"
    return false
  end
  return @config
end
```

First, I do some parameter checking so that only params that I want to processed are actually sent. Since I'm using metaprogramming here, I don't want to introduce a case where someone could run various methods by passing bad params (much like mass-assignment vulnerabilities). Then I loop through the params and run the commands needed to save the image.

## The Implementation

To use my class in my controller I just setup the following update method:

```ruby
class Admin::CheckoutViewSettingsController < Admin::BaseController
  before_filter :get_checkout_view_settings
  def update
    config = @cv.update_config(params[:checkout_view_settings])
    if config
      flash[:notice] = t("admin.success")
    else
      flash[:error] = t("admin.fail")
    end
    redirect_to admin_checkout_view_settings_path
  end

  private
  def get_checkout_view_settings
    @cv = CheckoutViewSetting.new(Spree::Config)
  end

end
```

And then in my form I have the following (haml):

```nohighlight
= form_tag admin_checkout_view_settings_path, :method => :put, :multipart => true do
  #formTop
    %fieldset
      .field
        = label_tag :image, t(".image.label")
        %br/
        = file_field_tag 'checkout_view_settings[image]', :accept => 'image/png,image/gif,image/jpeg'
    %fieldset
      .field
        = check_box_tag "checkout_view_settings[remove_image]"
        = label_tag "checkout_view_settings[remove_image]", t(".remove_image.label"), :style => "display: inline"
  #formBottom
    = image_tag(@cv.image.url) if @cv.configured?
    %br/
    = submit_tag
```

CarrierWave is an awesome library and a very suitable replacement for the more popular [Paperclip](https://github.com/thoughtbot/paperclip) library. I couldn't find anywhere online for showing a complete solution for implementing CarrierWave in an non-ActiveRecord class so I hope this helps anyone else that wants to go this route.
