---
author: Marina Lohova
gh_issue_number: 884
tags: javascript, jquery, user-interface
title: Pagination days are over? Infinite scrolling technique
---



Love it or hate it, but the infinite scrolling technique became a big part of UX. Google Images use it, Flickr uses it, Beyonce's official website uses it. Twitter, Tumblr and the Facebook feed have it as well. The technique allows users to seamlessly scroll through content. When the user reaches the end of the page new content will automatically load at the bottom.

In my opinion, it allows for a much more natural and immersive experience while viewing images or articles, much better than pagination or once popular image slideshow galleries. In the real life you don't click on pagination links to get through your day, right?

To create the infinite scrolling page with images we will use the [jQuery Infinite Scroll](https://github.com/paulirish/infinite-scroll) plugin and [Masonry](http://masonry.desandro.com/) to lay out the images. Here is the [demo](http://desandro.github.io/masonry/demos/infinite-scroll.html) of what we are going to accomplish. The code is below.

First step is to include the necessary scripts:

```ruby
<script src="/javascripts/jquery.min.js" type="text/javascript"></script>
<script src="/javascripts/jquery.masonry.min.js" type="text/javascript"></script>
<script src="/javascripts/jquery.infinitescroll.min.js" type="text/javascript"></script>
```

Add the container element. The navigation element is a very important part that triggers the loading of the subsequent page. After the second page the page number will automatically increment to fetch the subsequent pages:

```html
<div id="container"><% @images.each do |i| %>
    <div class="item"><img src="..."/></div><% end %>
</div><nav id="page-nav" style="display: none;">
  <a href="/?p=2"></a>
</nav>
```

Ready to init the infinite scrolling script:

```javascript
$(function(){
    var container = $('#container');
    container.masonry({
       itemSelector: '.item'
     });

    container.infinitescroll({
      navSelector  : '#page-nav', 
      nextSelector : '#page-nav a',
      itemSelector : '.item',
      loading: {
          finishedMsg: 'No more pages to load.',
          img: 'http://i.imgur.com/6RMhx.gif'
        }
      },

      function( newElements ) {
        var newElems = $( newElements ).css({ opacity: 0 });
          newElems.animate({ opacity: 1 });
          container.masonry( 'appended', $newElems, true );
      }
    );
  });
```

Once the user scrolls down to the bottom of the first page, the script will fetch the second page and filter out the new elements by the item selector. The controller action will look like this:

```ruby
def list
  @images = Image.paginate(:page => params[:p] || 1, :per_page => 25)
end
```

Finally, we will add the styles to create a three-column layout and some nice animations to render the newly loaded items:

```css
#container .item {
  width: 33%;
}
.transitions-enabled.masonry .masonry-brick {
  transition-property: left, right, top;
}
.transitions-enabled.masonry, .transitions-enabled.masonry .masonry-brick {
  transition-duration: 0.7s;
}
```

