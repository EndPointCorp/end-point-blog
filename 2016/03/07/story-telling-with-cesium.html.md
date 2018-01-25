---
author: Dmitry Kiselev
gh_issue_number: 1209
tags: angular, cesium, javascript, kamelopard, maps
title: Story telling with Cesium
---

### Let me tell you about my own town

I was born in Yekaterinburg. It’s a middle-sized town in Russia.

Most likely you don’t know where it is. So let me show you:

```js
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Hello World!</title>
    <script src="/cesium/Build/Cesium/Cesium.js"></script>
    <link rel="stylesheet" href="layout.css"></link>
  </head>
<body>
  <div id="cesiumContainer"></div>
  <script>
    var viewer = new Cesium.Viewer('cesiumContainer');
    (function(){
        var ekb = viewer.entities.add({
          name : 'Yekaterinburg',
          // Lon, Lat coordinates
          position : Cesium.Cartesian3.fromDegrees(60.6054, 56.8389),
          // Styled geometry
          point : {
            pixelSize : 5,
          color : Cesium.Color.RED
          },
          // Labeling
          label : {
            text : 'Yekaterinburg',
            font : '16pt monospace',
            style: Cesium.LabelStyle.FILL_AND_OUTLINE,
            outlineWidth : 2,
            verticalOrigin : Cesium.VerticalOrigin.BOTTOM,
            pixelOffset : new Cesium.Cartesian2(0, -9)
          }
        });

        // How to place camera around point
        var heading = Cesium.Math.toRadians(0);
        var pitch = Cesium.Math.toRadians(-30);
        viewer.zoomTo(ekb, new Cesium.HeadingPitchRange(heading, pitch, 10000));
    })();
  </script>
</body>
</html>
```

<div class="separator" style="clear: both; text-align: left;"><a href="/blog/2016/03/07/story-telling-with-cesium/image-0-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2016/03/07/story-telling-with-cesium/image-0.png"/></a></div>

Now, I would like to tell you about the history of my town. In the beginning it was a fortified metallurgical plant with a few residential blocks and some public buildings. It was relatively small.

I could say that its size was about the size of a modern city-center, but that description is too vague.  I think the best way to tell you something about the city is with a map.

I’ll show you two maps.

1. A map from 1750, early in the town’s history when it was just a factory: [http://www.retromap.ru/m.php#r=1417506](http://www.retromap.ru/m.php#r=1417506)
1. A map from 1924 at about the start of Soviet industrialization, just before Yekaterinburg became the industrial center of the Urals: [http://www.retromap.ru/m.php#r=1419241](http://www.retromap.ru/m.php#r=1419241)

Thanks for these beautiful maps to [http://www.retromap.ru](http://www.retromap.ru/).

The map from 1750 is a small image, so I’ve added it via [SingleTileImageryProvider](http://cesiumjs.org/Cesium/Build/Documentation/SingleTileImageryProvider.html). Just specifying the src and coordinates:

```js
function setupImagery() {
    var layers = viewer.scene.imageryLayers;

    var s = 56.8321929;
    var n = 56.8442609;
    var w = 60.5878970;
    var e = 60.6187892;
    var l1750 = layers.addImageryProvider(new Cesium.SingleTileImageryProvider({
        url : 'assets/1750.png',
        rectangle : Cesium.Rectangle.fromDegrees(w,s,e,n)
    }));
    l1750.alpha = 0.75;
}
```

Now you can see how small my town was initially.

<div class="separator" style="clear: both; text-align: left;"><a href="/blog/2016/03/07/story-telling-with-cesium/image-1-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2016/03/07/story-telling-with-cesium/image-1.png"/></a></div>

The second image is larger, so I’ve split it up into tiles. If you use [gdal2tiles.py](http://www.gdal.org/gdal2tiles.html) for generating tiles, it creates all the metadata necessary for [TMS](http://wiki.osgeo.org/wiki/Tile_Map_Service_Specification) and you are able connect the imagery set via [TileMapServiceImageryProvider](https://cesiumjs.org/releases/1.17/Build/Documentation/TileMapServiceImageryProvider.html). Otherwise, you can use [UrlTemplateImageryProvider](http://cesiumjs.org/Cesium/Build/Documentation/UrlTemplateImageryProvider.html).

```js
var l1924 = layers.addImageryProvider(new Cesium.TileMapServiceImageryProvider({
    url: 'assets/1924t',
    minimumLevel: 8,
    maximumLevel: 16,
    credit: 'retromap.ru'
}));

l1924.alpha = 0.75;
```

I’ve used [QGIS](http://www.qgis.org/ru/site/) for geo referencing. Here is a good [tutorial](http://qgis.spatialthoughts.com/2012/02/tutorial-georeferencing-topo-sheets.html).

#### User interface and Angular.js

And below here you see how I’ve added some controls for visibility and opacity of the overlays. Later we will bind them with an Angular-driven GUI:

```js
// APP is global

var layersHash = {
    'l1750': l1750,
    'l1924': l1924
}

APP.setAlpha = function(layer, alpha) {
    if(layersHash[layer] && layersHash[layer].alpha !== undefined) {
        layersHash[layer].alpha = alpha;
    }
};

APP.show = function(layer) {
    if(layersHash[layer] && layers.indexOf(layersHash[layer]) < 0) {
        layers.add(layersHash[layer]);
    }
};
```

Why not keep our views in a namespace and access them directly from an Angular controller? Using this approach will give us a lot of flexibility:

- You can split up the GUI and Cesium modules and use something else instead of Cesium or Angular.
- You are able to make a proxy for `APP` and add business logic to the calls made to it.
- It just feels right not to meld all parts of the application into one unmanageble mish-mash of code.

For the GUI I’ve added a big slider for the timeline, small sliders for layer opacity, checkboxes for visibility, and call APP methods via Angular’s $watch.

<div class="separator" style="clear: both; text-align: left;"><a href="/blog/2016/03/07/story-telling-with-cesium/image-2-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2016/03/07/story-telling-with-cesium/image-2.png"/></a></div>

```js
$scope.$watch('slider.value', function() {
    var v = $scope.slider.options.stepsArray[$scope.slider.value];
    if (v >= 1723 && v <= 1830) {
        $scope.menu.layers[0].active = true;
        $scope.menu.layers[1].active = false;
    }
    if (v > 1830 && v < 1980) {
        $scope.menu.layers[0].active = false;
        $scope.menu.layers[1].active = true;
    }
    if(v >= 1980) {
        $scope.menu.layers[0].active = false;
        $scope.menu.layers[1].active = false;
    }

    $scope.updateLayers();
});

$scope.updateLayers = function() {
    for (var i = 0; i < $scope.menu.layers.length; i++) {
        if ($scope.menu.layers[i].active ) {
            APP.show && APP.show($scope.menu.layers[i].name);
        }
        else {
            APP.hide && APP.hide($scope.menu.layers[i].name);
        }
    }
};
```

#### Back to the history:

Yekaterinburg was founded on November 7, 1723. This is the date of the first test-run of the forging hammers in the new factory. The original factory design by Tatishew had 40 forging hammers and 4 blast furnaces. That may well have made it the best equipped and most productive factory of its time.

Now I want to add text to the application. Also, I have some cool pictures of the hammers and furnaces. Adding an overlay for text and binding its content is a matter of *CSS* and *ng-include/ng-bind* knowledge and it’s a bit out of scope for this post, but let’s push on and add some pictures and link them to the timeline. Cesium has [KmlDataSource](http://cesiumjs.org/Cesium/Build/Documentation/KmlDataSource.html) for KML loading and parsing. This is how my application loads and accesses these attributes:

```js
var entityByName = {};
var promise = Cesium.KmlDataSource.load('assets/foto.kml');
promise.then(function(dataSource) {
    viewer.dataSources.add(dataSource);

    //KML entities
    var entities = dataSource.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        // <Data> attributes, parsed into js object
        var ed = entity.kml.extendedData;

        entityByName[entity.id] = {
            'entity': entity,
            since: parseInt(ed.since.value),
            to: parseInt(ed.to.value)
        };
    }
});
```

Add bindings for Angular:

```js
APP.filterEtityByY = function(y) {
    for (var k in entityByName) {
        if(entityByName.hasOwnProperty(k)) {
            var s = entityByName[k].since;
            var t = entityByName[k].to;
            entityByName[k].entity.show = (y >= s && y <= t);
        }
    }
};

var heading = Cesium.Math.toRadians(0);
var pitch = Cesium.Math.toRadians(-30);
var distanceMeters = 500;
var enityHeading = new Cesium.HeadingPitchRange(heading, pitch, distanceMeters);

APP.zoomToEntity = function(name) {
    if(name && entityByName[name]) {
        viewer.zoomTo(entityByName[name].entity, enityHeading);
    }
};
```

I’ve added object timespans via extended data. If you want to use the Cesium/GE default timeline, you should do it via a *TimeSpan* section in the KML’s entries:

```html
<timespan>
  <begin>2000-01-00T00:00:00Z</begin>
    <end>2000-02-00T00:00:00Z</end>
 </timespan>
```

Another interesting fact about my town is that between 1924 and 1991 it had a different name: *Sverdlovsk (Свердловск)*. So I’ve added town name changing via APP and connected it to the timeline.

Using *APP.filterEtityByY* and *APP.zoomToEntity* it’s relatively easy to connect a page hash like *example.com/#!/feature/smth* with features from KML. One point to note is that I use my own hash’s path part parser instead of ngRoute’s approach.

<div class="separator" style="clear: both; text-align: left;"><a href="/blog/2016/03/07/story-telling-with-cesium/image-3-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2016/03/07/story-telling-with-cesium/image-3.png"/></a></div>

You can see how all these elements work together at [https://dmitry.endpoint.com/cesium/ekb](https://dmitry.endpoint.com/cesium/ekb),  the sources are on Github at [https://github.com/kiselev-dv/EkbHistory/tree/master](https://github.com/kiselev-dv/EkbHistory/tree/master).
