---
author: Richard Templet
gh_issue_number: 750
tags: css, performance, tools
title: 'CSS sprites: The easy way?'
---



I've always been interested in the use of CSS sprites to speed up page load times. I haven't had a real chance to use them yet but my initial reaction was that sprites would be quite painful to maintain. In my mind, you would have to load up the sprite into Gimp or Photoshop, add the new image and then create the css with the right coordinates to display the image. Being a guy with very little image editing skills, I felt that managing multiple images frequently would be quite time consuming. Recently, I was dealing with some page load times for a client and the use of sprites for the product listing pages came up as an option to speed them up. I knew the client wouldn't have time to create sprites for this so I went searching for a command line tool that would allow me to create sprites. I was quite happy when I stumbled upon [Glue](http://glue.readthedocs.org/en/latest/index.html).

[Glue](http://glue.readthedocs.org/en/latest/index.html) is free program that will take a directory of images and create a png sprite and a css file with the associated CSS classes. It has a ton of useful options. A few of the ones I thought were handy was being able to prefix the path to the image with a url instead of a relative path, being able to downgrade the png format to png8 to make the file sizes much smaller and being able to specify the start of the name of the class with something to help with being able to use them on a dynamic page.

The most basic use of the command is as follows:

```
glue blog output
```

In this example, blog is the directory where the images live that you want [Glue](http://glue.readthedocs.org/en/latest/index.html) to create a sprite of and output is the directory where it will generate the blog.png and blog.css file.

The output css file looks like this:

```css
/* glue: 0.2.9.1 hash: f9c9d6aa5b */
.sprite-blog-product2,
.sprite-blog-product1{background-image:url('blog.png');background-repeat:no-repeat}
.sprite-blog-product2{background-position:0px 0px;width:159px;height:200px;}
.sprite-blog-product1{background-position:-159px 0px;width:200px;height:168px;}
```

The naming convention by default is sprite-$input_directory-$filename.  You can override this with a few options. The version number and hash are used by [Glue](http://glue.readthedocs.org/en/latest/index.html) to ensure it doesn't rebuild the sprite if none of the source images have changed.  With these settings, I believe this could be a great program to run as a nightly routine to rebuild the sprites.  This is the explanation from the documentation:

```
By default glue store some metadata inside the generated sprites in order to not
rebuild it again if the source images and settings are the same. Glue set two different
keys, glue with the version number the sprite was build and hash, generated using the 
source images data, name and all the relevant sprite settings like padding, margin 
etc...
```

I'm still tinkering with all the different options and thinking about how to include the use of this program in our work flow for this client.  I'll make sure to write a follow up with more information as I learn more.

If you have a different command line tool which helps manage sprites, don't hesitate to leave a comment and let me know!


