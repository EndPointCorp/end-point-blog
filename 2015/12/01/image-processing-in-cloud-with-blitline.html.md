---
author: Marina Lohova
gh_issue_number: 1180
tags: cloud, imagemagick, php, wordpress
title: Image Processing In The Cloud With Blitline and Wordpress
---



Working with ImageMagick can be difficult. First, you have to get it installed on your OS (do you have Dev libs in place?), then you have to enable it in the language of your choice, then get it working in your application. After all that, do it all over again on the staging server where debugging may be complicated, and you may not have Admin rights. Meet Image Processing in the Cloud. Meet Blitline.

I'm doing a lot of things with Wordpress now, so we'll set it up with Wordpress and PHP.

## Step 1

Get a free developer account with [Blitline](https://blitline.com/signup), and note your application id.

## Step 2

Get the Blitline PHP wrapper library [Blitline_php](https://github.com/karikas/blitline_php). It's clean and awesome, but unfortunately at the time of writing it was missing a few things, like being able to run your own Image Magick script and set a postback URL for when the job is finished. Yes, those are all useful features of Blitline cloud image processing! I'm still waiting on my pull request to be incorporated into the official version, so you can use mine that has these two useful features for now [Ftert's Blitline_php](https://github.com/ftert/blitline_php)

## Step 3

Now it's time to integrate it in our application. Since it's Wordpress, I'm doing it in the 'wp_generate_attachment_metadata' callback in functions.php

```php
require_once dirname(__FILE__) . '/blitline_php/lib/blitline_php.php';
...
add_filter( 'wp_generate_attachment_metadata', array($this,'wp_blur_attachment_filter'), 10, 2 );
...
public function wp_blur_attachment_filter($image_data, $attachment_id) {

$url =  wp_get_attachment_url($attachment_id);

list($src, $width, $length) = wp_get_attachment_image_src($attachment_id);

$data = pathinfo($src);

$dest = $data['filename'] . '_darken_75_105_100_blur_0_20.' . $data['extension'];

$Blit = new Blitline_php();

$Blit->load($url, $dest);

$Blit->do_script("convert input.png -blur 0x20 -modulate 75,105,100 output.png");

$Blit->set_postback_url( get_site_url() . '/wp-json/myapp/v1/blitline_callback');

$results = $Blit->process();

if ($results->success()) {
foreach($results->get_images() as $name => $url) {
error_log("Processed: {$name} at {$url}\n");
}
} else {
error_log($results->get_errors());
}
}
```

We are sending a JSON POST request to Blitline to make the blurred and saturated version of the uploaded image. You can track the progress of your jobs [here](https://blitline.com/dashboard). The request will return a URL to the image on the Blitline server, but the image may not be there right away, because the processing is asynchronous. I tried to set up S3 bucket integration (yes, Blitline can upload to S3 for you!), but the setup procedure is quite tedious. You have to manually enter your AWS Canonical ID (and obtain it first from Amazon) on the Blitline page. Then you have to create a special [policy](https://www.blitline.com/docs/s3_permissions) in your bucket for Blitline. This is a lot of hassle, and giving permissions to someone else might not be the way to go for you. For me personally it didn't work, because my policy was being automatically overwritten all the time. I don't even know why. So here's where the [postback URL]( https://blitline.com/docs/postback#returnedData
) comes in play.

## Step 4

I'm using [this plugin WP-API V2](http://v2.wp-api.org) that soon will become part of Wordpress to make REST endpoints. In wp-content/mu-plugins/my-app-custom-endpoints/lib/endpoints.php

```php
add_action('rest_api_init', function () {

register_rest_route('portfolio/v1', '/blitline_callback', array(
'methods' => 'POST',
'callback' => 'process_blitline_callback',
));
});
```

In wp-content/mu-plugins/loader.php

```php
require_once dirname(__FILE__) . '/blitline_php/lib/blitline_php.php';

require_once dirname(__FILE__) . '/my-app-custom-endpoints/api.php';
```

In wp-content/mu-plugins/my-app-custom-endpoints/api.php

```php
if( ! defined( 'ABSPATH' ) ) exit;

require_once dirname(__FILE__) . '/lib/endpoints.php';
```

Here's the fun part. Add to wp-content/mu-plugins/my-app-custom-endpoints/lib/endpoints.php

```php
use Aws\S3\S3Client;

function process_blitline_callback($request) {

if( !class_exists( 'WP_Http' ) )
include_once( ABSPATH . WPINC. '/class-http.php' );

$s3Client = S3Client::factory(array(
'credentials' => array(
'key'    => 'YOUR S3 KEY',
'secret' => 'YOUR S3 SECRET'
)
));
$photo = new WP_Http();

$body = $request->get_body_params();

$var = (array) json_decode(stripslashes($body['results']), true);

if (isset($var['images'][0]['error'])) {
error_log('Error ' . $var['images'][0]['error']);
return;
}

$photo = $photo->request( $var['images'][0]['s3_url'] );

$photo_name = $var['images'][0]['image_identifier'];

$attachment = wp_upload_bits( $photo_name , null,
$photo['body'],
date("Y-m", strtotime( $photo['headers']['last-modified'] ) ) );

$upload_dir = wp_upload_dir();

$s3Client->putObject(array(
'Bucket' => "yourbucket",
'Key'    => 'wp-content/uploads' . $upload_dir['subdir'] . '/' . $photo_name,
'SourceFile'   => $attachment['file'],
'ACL'    => 'public-read'
));
}
```

In the callback we download the processed image from the temporary Blitline URL. One little bonus in here is the upload to Amazon S3 bucket. I use [Amazon PHP SDK](http://docs.aws.amazon.com/aws-sdk-php/v2/api/index.html) to achieve that. Note the permissions. This was one last thing when I actually almost gave up trying to make Blitline postback URL work. When the image finally appeared in my bucket, it wasn't accessible from the outside, because I didn't set permissions

## Step 5. If it doesn't work. Debugging.

I used [Firefox add-on HttpRequester](https://addons.mozilla.org/en-us/firefox/addon/httprequester/) to post the mock response from Blitline to my application.  If you don't want to deploy each time you change the code, here's another useful thing [LocalTunnel](https://localtunnel.me/), so you can expose your localhost to the internet and set the postback to your local app.

And that's how you do image processing in the cloud!


