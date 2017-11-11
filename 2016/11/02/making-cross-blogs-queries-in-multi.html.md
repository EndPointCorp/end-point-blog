---
author: Kamil Ciemniewski
gh_issue_number: 1265
tags: database, mysql, php, extensions, wordpress
title: Making cross-blogs queries in multi-site WordPress performant
---

Some time ago I was working on customizing a WordPress system for a client. The system was running in a multi-site mode, being a host of a large number of blogs.

Because some blogs had not been updated in a long while, we wanted to pull information about recent posts from all of the blogs. This in turn was going to be used for pruning any blogs that weren't considered 'active'.

While the above description may sound simple, the scale of the system made the task a bit more involving that it would be usually.

### How WordPress handles the "multi-site" scenario

The goal of computing the summary of posts for many blogs residing in the hypotethical blogging platform, **in the same database** doesn't seem so complicated. Tasks like that are being performed all the time using relational databases.

The problem in WordPress arises though because of the very **unusual** way that it organises blogs data. Let's see how the database tables look like in the "normal" mode first:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2016/11/02/making-cross-blogs-queries-in-multi/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2016/11/02/making-cross-blogs-queries-in-multi/image-0.png"/></a></div>

It has a number of tables that start with user configurable prefix. In the case of the screenshot above, the prefix was wp_.

We can see there's a wp_posts table which contains rows related to blog posts. Thinking about the multi-blog setup, one would expect some kind of a blog_id column in the wp_posts column. Selecting data for the given blog would still be a cinch. It would also be very performant after adding an index on that column.

Instead, this is what we're getting when setting up WordPress in a multi-site mode:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2016/11/02/making-cross-blogs-queries-in-multi/image-1.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2016/11/02/making-cross-blogs-queries-in-multi/image-1.png"/></a></div>

WordPress just creates a new set of tables we seen before appending the index of the blog to the tables prefix! Instead of having a nice, clean and easy to use wp_posts with the blog_id column, we get a number of tables - one for each blog: wp_1_posts, wp_2_posts etc. Why does it matter that much? Just try to get the counts of posts in each blog in one query — it's impossible with such a tables setup. Getting such info involves querying **each table separately**. This means that with each new blog within the system, the cost of running such sequence of queries adds up dramatically. This is also known as a N+1 problem — bad WordPress! bad!

### The approach around it

The counts of posts for each blog was needed to be computed very quickly in my case. The system consisted of hundreds of different mini-blogs and the stats were to be shown in the admin dashboard. Obviously making admins wait for the page to load for a long time wasn't an option.

I went the route of creating an additional database table, holding the info about the number of posts for each blog. This table was then being updated upon each post creation, update and deletion. It was also updated upon the blog removal.

WordPress has a helper function for ensuring the table is created in the database. You feed it the DDL containing the definition of the table and it makes sure it is present in the database.

I created a function that was being fired on each plugin class instantiation, while making that class a singleton. Here's the code that makes the plugin class a singleton:

```php
class BlogsPruner
{
  private static $instance;

  private function __construct()
  {
    $this->ensureDatabaseSetup();
    $this->ensureBlogStatsGetUpdated();
    // ... other initialization here
  }

  public static function singleton()
  {
    if(!isset(self::$instance))
    {
      $_class = __CLASS__;
      self::$instance = new $_class;
    }
    return self::$instance;
  }

  public function __clone()
  {
    trigger_error('Cannot clone the pruner plugin', E_USER_ERROR);
  }

  // ... rest of the class
}

BlogsPruner::singleton();
```
The next step was to implement the function ensuring there's a stats table in the database:

```php
function ensureDatabaseSetup()
  {
    global $wpdb;
    $tableName = $this->blogStatsTableName();
    $charsetCollate = $wpdb->get_charset_collate();

    $sql = "CREATE TABLE $tableName (
            blog_id bigint(20),
            count_posts int(2),
            UNIQUE KEY blog_id (blog_id)
    ) $charsetCollate;";

    require_once( ABSPATH . 'wp-admin/includes/upgrade.php' );
    dbDelta( $sql );
    $this->ensureBlogStatsUpdated();
  }
```
This code uses a helper function to correctly construct the name for the table:

```php
function blogStatsTableName()
{
  global $wpdb;
  return $wpdb->base_prefix . 'blog_stats';
}
```
This made sure the table was using the correct prefix, just like all the other tables in the database.

Now, I needed to ensure the stats were updated upon each post change:

```php
function ensureBlogStatsGetUpdated()
{
  add_action('save_post', array($this, 'onPostUpdated'));
  add_action('delete_post', array($this, 'onPostDeleted'));
}

function onPostUpdated($postId)
{
  global $blog_id;
  $post = get_post($postId);
  if(wp_is_post_revision($postId) || $post->post_status == 'auto-draft')
  {
    return;
  }
  $this->updateBlogStats($blog_id);
}

function onPostDeleted()
{
  global $blog_id;
  $this->updateBlogStats($blog_id);
}

function updateBlogStats($blogId)
{
  $count = $this->getBlogUserCreatedPostsCount($blogId);
  $this->updateBlogPostsCount($blogId, $count);
}

// Here we're specifically not including the post that is auto-created
// upon the blog creation:
function getBlogUserCreatedPostsCount($blogId)
{
  global $wpdb;
  $sql = "SELECT
            COUNT(DISTINCT `wp_" . $blogId . "_posts`.`id`) AS count_user_posts
          FROM `wp_blogs`
          INNER JOIN `wp_" . $blogId . "_posts`
                  ON `wp_blogs`.`blog_id` = $blogId
          WHERE
            `wp_" . $blogId . "_posts`.`post_type` = 'post' AND
            `wp_" . $blogId . "_posts`.`post_status` = 'publish' AND
            TIMESTAMPDIFF(SECOND, `wp_" . $blogId . "_posts`.`post_date`, `wp_blogs`.`last_updated`) > 60";
  $row = $wpdb->get_row($sql);
  return intval($row->count_user_posts);
}

function updateBlogPostsCount($blogId, $count)
{
  global $wpdb;
  $data = array('count_posts' => $count);
  $where = array('blog_id' => $blogId);
  $wpdb->update($this->blogStatsTableName(), $data, $where);
}
```
The actual production plugin implemented many more features than this sample code demonstrates. It was listing the blogs that could be considered stale, automatically pruning them after specified in the admin screen time and allowing admins to configure it via the WordPress interface. The full set of features is beyond the scope of this post.

The overall result made getting the statistics about very large set of blogs very fast. The cost of querying for the number of posts of each blog was moved to incremental, small updates upon each post being created, modified or removed. For the end user, this cost was imperceptable.

### Final thoughts

WordPress is loved by many users. If you're not just a user but also working with the code, there's a number of traps you may fall into though. If I were to employ techniques that get advised as "WordPress usual/default/preferred" — I'd end up with a very unhappy client who's be owning a very broken WordPress system. Fortunately, the set of WordPress tables isn't casted in stone and you can freely extend it - as long as you're cautious and know what you're doing. Provided that these two prerequisites are met — WordPress is just a database backed platform - like any other.
