---
author: Josh Ausborne
title: Non-English Google Earth Layers on the Liquid Galaxy
github_issue_number: 1126
tags:
- google-earth
- liquid-galaxy
date: 2015-05-12
---

The availability to activate layers within Google Earth is one of the things that makes Earth so powerful.  In fact, there are many standard layers that are built into Earth, including weather, roads, place names, etc.  There are also some additional layers that have some really interesting information, including one I noticed relatively recently called “Appalachian Mountaintop Removal” which is interesting to me now that I live in Tennessee.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/05/non-english-google-earth-layers-on/image-0-big.png" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2015/05/non-english-google-earth-layers-on/image-0.png"/></a></div>

As you can see, however, that while some of these available layers are interesting on a desktop, they’re not necessarily very visually appealing on a Liquid Galaxy.  We have identified a standard set of layers to enable and disable within Earth so that things don’t appear too cluttered while running.  Some things we’ve disabled by default are the weather and the roads, as well as many levels of place names and boundaries.  For example, we have boundaries of countries and water bodies enabled, but don’t want lines drawn for states, provinces, counties, or other areas such as those.

To disable these layers, we modify the GECommonSettings.conf file on the machines that running Earth.  This file has everything pretty well spelled out in a readable manner, and it’s fairly easy to determine what layers you’re enabling or disabling.

Here’s an example of some of the entries contained within the GECommonSettings.conf file:

```nohighlight
1st%20Level%20Admin%20Names%20%28States_Provinces%29=false
2nd%20Level%20Admin%20Regions%20%28Counties%29=false
Islands=false
http%3A__mw1.google.com_mw-earth-vectordb_geographic_features_en.kml\Geographic%20Features=false
Water%20Bodies=true
Places%20=false
Panoramio=false
360%20Cities=false
Photorealistic%20=true
Trees=true
Populated%20Places=true
Roads=false
Gray%20=false
http%3A__mw1.google.com_mw-weather_base_files_kml_weather_en.kmz\Clouds=true
http%3A__mw1.google.com_mw-weather_base_files_kml_weather_en.kmz\Radar=true
http%3A__mw1.google.com_mw-weather_base_files_kml_weather_en.kmz\Conditions%20and%20Forecasts=true
http%3A__mw1.google.com_mw-weather_base_files_kml_weather_en.kmz\Information=true
http%3A__mw1.google.com_mw-earth-vectordb_gallery_layers_gallery_root_en.kmz\360Cities=false
```

See, that’s pretty self-explanatory, isn’t it?

Well, it is until you start introducing other languages to the mix.  For example, we needed to run Earth in Korean language mode for one of our clients.  Once we fired up Earth and specified that the language would be Korean, Earth came up with all of the default layers turned on.  All of those layers that we’d disabled in English Earth stayed on and cluttered the displays with so many icons for each and every layer.

It took some trial and error, but I was eventually able to figure out what to do to resolve this.  I loaded Google Earth in Korean mode on my Ubuntu VM, made my changes to the selected layers via the Layers selection area within Earth, then quit.  When I looked at the GECommonSettings.conf file after quitting Earth, I found a bunch of new line items added to the file.  It seems that each of the options had new lines, though I couldn’t exactly decipher which lines controlled which options.

Here’s an example of some of the new entries that are now contained within my GECommonSettings.conf file:

```nohighlight
http%3A__kh.google.com%3A80_\%UAD6D%UACBD=false
http%3A__kh.google.com%3A80_\%UAD6D%UAC00%UBA85=false
http%3A__kh.google.com%3A80_\%UD574%UC548%UC120=false
http%3A__kh.google.com%3A80_\1%UCC28%20%UD589%UC815%20%UACBD%UACC4%UC120%28%UC8FC_%UB3C4%29=false
http%3A__kh.google.com%3A80_\2%UCC28%20%UD589%UC815%UB2E8%UC704%20%UC9C0%UC5ED%28%UAD70%29=false
http%3A__kh.google.com%3A80_\%UC778%UAD6C%UBC00%UC9D1%UC9C0%UC5ED=true
http%3A__kh.google.com%3A80_\%UC12C=false
```

Now, I’ll be honest and say that I don’t have clue exactly what %UAD6D%UACBD and 1%UCC28%20%UD589%UC815%20%UACBD%UACC4%UC120%28%UC8FC_%UB3C4%29 mean, but I really don’t have to know.  All I know is that they got disabled when I disabled the undesired layers within Earth.  I then copied these lines to the configuration on my Liquid Galaxy, and the next time I fired it up in Korean, the layers were no longer cluttering up the displays.

I was able to use this exact same method to determine which layers to enable or disable for one of our Spanish-language clients, as well.
