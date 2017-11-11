---
author: Steph Skardal
gh_issue_number: 462
tags: ecommerce, graphics, spree
title: 'Paperclip in Spree: Extending Product Image Sizes'
---



Spree uses the popular gem [Paperclip](https://github.com/thoughtbot/paperclip) for assigning images as attachments to products. The basic installation requires you to install the gem, create a migration to store the paperclip-specific fields in your model, add the **has_attached_file** information to the model with the attachment, add the ability to upload the file, and display the file in a view. In Spree, the Image model has an attached file with the following properties:

```ruby
class Image &lt; Asset
  ...
  has_attached_file :attachment,
                    :styles =&gt; { :mini =&gt; '48x48&gt;',
                      :small =&gt; '100x100&gt;',
                      :product =&gt; '240x240&gt;',
                      :large =&gt; '600x600&gt;'
                    },
                    :default_style =&gt; :product,
                    :url =&gt; "/assets/products/:id/:style/:basename.:extension",
                    :path =&gt; ":rails_root/public/assets/products/:id/:style/:basename.:extension"
  ...
end
```

As you can see, when an admin uploads an image, four image sizes are created: large, product, small, and mini.

<img alt="" border="0" id="BLOGGER_PHOTO_ID_5615185163090719650" src="/blog/2011/06/06/paperclip-spree-overriding-product/image-0.jpeg" style="width: 160px;"/>
<img alt="" border="0" id="BLOGGER_PHOTO_ID_5615185163090719650" src="/blog/2011/06/06/paperclip-spree-overriding-product/image-0.jpeg" style="width: 120px;"/>
<img alt="" border="0" id="BLOGGER_PHOTO_ID_5615185163090719650" src="/blog/2011/06/06/paperclip-spree-overriding-product/image-0.jpeg" style="width: 100px;"/>
<img alt="" border="0" id="BLOGGER_PHOTO_ID_5615185163090719650" src="/blog/2011/06/06/paperclip-spree-overriding-product/image-0.jpeg" style="width: 48px;"/>
Four images are created per product image uploaded in Spree (Note: not to scale).

Last week, I wanted to add several additional sizes to be created upon upload to improve performance. This involved several steps, described below.

### Step 1: Extend attachment_definitions

First, I had to override the image attachment styles, with the code shown below. My application is running on Spree 0.11.2 (Rails 2.3.*), so this was added inside the extension activate method, but in Rails 3.0 versions of Spree, this would be added inside the engine's activate method.

```ruby
Image.attachment_definitions[:attachment][:styles].merge!(
      :newsize1 =&gt; '200x200&gt;',
      :newsize2 =&gt; '284x284&gt;'
)
```

### Step 2: Add Image Helper Methods

Spree has the following bit of code in its base_helper.rb, which in theory should create methods for calling each image (mini_image, small_image, product_image, large_image, newsize1_image, newsize2_image):

```ruby
Image.attachment_definitions[:attachment][:styles].each do |style, v|
    define_method "#{style}_image" do |product, *options|
      options = options.first || {}
      if product.images.empty?
        image_tag "noimage/#{style}.jpg", options
      else
        image = product.images.first
        options.reverse_merge! :alt =&gt; image.alt.blank? ? product.name : image.alt
        image_tag image.attachment.url(style), options
      end
    end
  end
```

But for some reason in this application, perhaps based on order of extension evaluation, this was only applied to the original image sizes. I remedied this by adding the following code to my extension base helper:

```ruby
  [:newsize1, newsize2].each do |style|
    define_method "#{style}_image" do |product, *options|
      options = options.first || {}
      if product.images.empty?
        image_tag "noimage/#{style}.jpg", options
      else
        image = product.images.first
        options.reverse_merge! :alt =&gt; image.alt.blank? ? product.name : image.alt
        image_tag image.attachment.url(style), options
      end 
    end 
  end 
```

### Step 3: Create Cropped Images for Existing Images

Finally, instead of requiring all images to be re-uploaded to create the new cropped images, I wrote a quick bash script to generate images with the new sizes. This script was placed inside the RAILS_ROOT/public/assets/products/ directory, where product images are stored. The script iterates through each existing directory and creates cropped images based on the original uploaded image with the ImageMagick command-line tool, which is what Paperclip uses for resizing.

```bash
#!/bin/bash

for i in `ls */original/*`
do
    image_name=${i#*original\/}
    dir_name=${i/\/original\/$image_name/}
    mkdir $dir_name/newsize1/ $dir_name/newsize2/
    convert $i -resize '200x200' $dir_name/newsize1/$image_name
    convert $i -resize '284x284' $dir_name/newsize2/$image_name
    echo "created images for $i"
done
```

### Step 4: Update Views

Finally, I added newsize1_image and newsize2_image methods throughout the views, e.g.:

```nohighlight
&lt;%= link_to newsize1_image(product), product %&gt;
&lt;%= link_to newsize2_image(taxon.products.first), seo_url(taxon) %&gt;
```

### Conclusion

It would be ideal to remove Step 2 described here by investigating why the image methods are not defined by the Spree core BaseHelper module. It's possible that this is working as expected on more recent versions of Spree. Other than that violation of the DRY principle, it is a fairly simple process to extend the Paperclip image settings to include additional sizes.


