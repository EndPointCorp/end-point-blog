---
author: Marina Lohova
gh_issue_number: 1196
tags: imagemagick, php, user-interface, wordpress
title: Medium-inspired Parallax Blur Effect For WordPress
---



Are you are running a WordPress blog, but secretly dying to have that [](http://pencilscoop.com/2015/02/recreating-mediums-parallax-blur-effect)[Medium](https://medium.com/) parallax blur effect? I recently implemented this, and would like to share it with you. By the way, while I was working on the article, the effect was removed from Medium, which only makes having one on the website more precious.

Let's assume that we have our custom theme class MyTheme. In functions.php:

```php
class MyThemeBaseFunctions {
  public function __construct() {
    add_image_size('blurred', 1600, 1280, true);
    add_filter('wp_generate_attachment_metadata', array($this,'wp_blur_attachment_filter'));
  }
}
```

We added a custom image size blurred, and a callback wp_blur_attachment_filter to wp_generate_attachment_metadata. Here's where the magic happens.

Before that let's talk a little about ImageMagick, a powerful library for image processing that we will use to create the blurred effect. After some experimenting I figured that the image needed to be darkened, and then a regular blur should be applied with sigma=20. You can read more about these settings at [ImageMagick Blur Usage](http://www.imagemagick.org/Usage/blur/#blur). I used Gaussian Blur at first, but found the processing was extremely slow, and there wasn't much difference in the end result compared to other blur methods.

Now we are ready to write a blurring function:

```php
public function wp_blur_attachment_filter($image_data) {
    if ( !isset($image_data['sizes']['blurred']) )
       return $image_data;
       $upload_dir = wp_upload_dir();
       $src = $upload_dir['path'] . '/' . $image_data['sizes']['large']['file'];
       $destination = $upload_dir['path'] . '/' . $image_data['sizes']['blurred']['file'];
       $imagick = new \Imagick($src);
       $imagick->blurImage(0, 20, Imagick::CHANNEL_ALL);
       $imagick->modulateImage(75, 105, 100);
       $imagick->writeImage($destination);
       return $image_data;
 }
```

I darken the image:

```php
$imagick->modulateImage(75, 105, 100);
```

And I blur the image:

```php
$imagick->blurImage(0, 20, Imagick::CHANNEL_ALL);
```

Now we are able to use the custom image size in the template. Place the helper function in functions.php:

```php
public static function non_blurred($src) {
  $url = get_site_url() . substr($src, strrpos($src, '/wp-content'));
  $post_ID = attachment_url_to_postid($url);
  list($url, $width, $height) = wp_get_attachment_image_src($post_ID, 'large');
  return $url;
}

public static function blurred($src) {
  $url = get_site_url() . substr($src, strrpos($src, '/wp-content'));
  $post_ID = attachment_url_to_postid($src);
  list($url, $width, $height) = wp_get_attachment_image_src($post_ID, 'blurred');
  return $url;
}
```

And now use it in the template like this:

```html
<div class="blurImg">
  <div style="background-image: url('<?php echo MyTheme::non_blurred(get_theme_mod( 'header' )); ?>')"></div>
  <div style="background-image: url('<?php echo MyTheme::blurred(get_theme_mod('header')); ?>'); opacity: 0;" class="blur"></div>
</div>
<header></header>
```

Add CSS:

```css
.blurImg {
  height: 440px;
  left: 0;
  position: relative;
  top: 0;
  width: 100%;
  z-index: -1;
}

.blurImg > div {
  background-position: center center;
  background-repeat: no-repeat;
  background-size: cover;
  height: 440px;
  position: fixed;
  width: 100%;
}

header {
  padding: 0 20px;
  position: absolute;
  top: 0;
  width: 100%;
  z-index: 1;
}
```

Add JavaScript magic sauce to gradually replace the non-blurred image with the blurred version as the user scrolls:

```javascript
(function() {
    jQuery(window).scroll(function() {
      var H = 240;
      var oVal = jQuery(window).scrollTop() / H;
      jQuery(".blurImg .blur").css("opacity", oVal);
    });
  }).call(this);
```

Generating the blurred version can be very strenuous on the server. I would oftentimes receive the error PHP Fatal error:  Maximum execution time of 30 seconds exceeded. There are ways to work around that. One way is to use a quicker method of blurring the image by shrinking it, blurring, and resizing it back. Another way is to use a background job, something like this:

```php
add_action( 'add_attachment', array($this, 'wp_blur_attachment_filter') );
add_action( 'wp_blur_attachment_filter_hook', 'wp_blur_attachment_filter_callback');
function wp_blur_attachment_filter_callback($path) {
  $path_parts = pathinfo($path);
  $imagick = new \Imagick($path);
  $imagick->blurImage(0, 20, Imagick::CHANNEL_ALL);
  $imagick->modulateImage(75, 105, 100);
  $destination = dirname($path) . "/" . $path_parts['filename'] . "_darken_blur." . $path_parts['extension'];
  $imagick->writeImage($destination);
}

public function wp_blur_attachment_filter($post_ID) {
  $path = get_attached_file( $post_ID );
  wp_schedule_single_event(time(), 'wp_blur_attachment_filter_hook', array($path));
}
```

Or better yet, use cloud image processing — I wrote about that [here](http://blog.endpoint.com/2015/12/image-processing-in-cloud-with-blitline.html).

I hope you found this writeup useful!


