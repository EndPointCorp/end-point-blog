---
author: Jeff Boes
gh_issue_number: 372
tags: cloud, javascript
title: Simple audio playback with Yahoo Mediaplayer
---



Recently I had need to show a list of MP3 files with a click-to-play interface.

I came upon a very simple self-contained audio player:

```nohighlight
<script type="text/javascript" src="http://mediaplayer.yahoo.com/js"></script>
```

The code to set up my links for playing was dirt-simple:

```javascript
<script type="text/javascript">
var player = document.getElementById('player');
function add_to_player() {
    var link = this;
    player.src.replace(/audioUrl=.*/,'audioUrl=' + link.src);
    return false;
}
var links = document.getElementsByTagName('A');
for (var i = 0; i < links.length; i++) {
    if (links[i].src.match(/\.mp3$/)) {
        links.onclick = add_to_player;
    }
}
</script>
```

You could use various ways to identify the links to be player-ized, but I chose to just associate the links with a class, "mp3":

```nohighlight
<a class="mp3" href="/path/to/file.mp3">Audio File 1</a>
```

Obviously, if jQuery is in use for your page, you can reduce the code to an even smaller snippet.


