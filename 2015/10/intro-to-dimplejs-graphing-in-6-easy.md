---
author: Matt Galvin
title: Intro to DimpleJS, Graphing in 6 Easy Steps
github_issue_number: 1162
tags:
- visualization
- javascript
date: 2015-10-15
---

Data Visualization is a big topic these days given the giant amount of data being collected. So, graphing this data has been important in order to easily understand what has been collected. Of course there are many tools available for this purpose but one of the more popular choices is [D3](https://d3js.org/).

D3 is very versatile but can be a little more complicated than necessary for simple graphing. So, what if you just want to quickly spin up some graphs quickly? I was recently working on a project where we were trying to do just that. That is when I was introduced to [DimpleJS](http://dimplejs.org/).

The advantage of using DimpleJS rather than plain D3 is speed. It allows you to quickly create customizable graphs with your data, gives you easy access to D3 objects, is intuitive to code, and I’ve found the creator [John Kiernander](https://twitter.com/jkiernander) to be very responsive on [Stack Overflow](https://stackoverflow.com/) when I ran in to issues.

I was really impressed with how flexible DimpleJS is. You can make a very large variety of graphs quickly and easily. You can update the labels on the graph and on the axes, you can create your own tooltips, add colors and animations, etc..

I thought I’d make a quick example to show just how easy it is to start graphing.

### Step 1

After including Dimple in your project, you simply create a div and give it an id to be used in your JavaScript.

```html
<head>
  <script src="http://d3js.org/d3.v3.min.js"></script>
  <script src="http://dimplejs.org/dist/dimple.v2.0.0.min.js"></script>
</head>
<body>
  <div id="chart" style="background:grey"></div>
</body>
```

### Step 2

In your JavaScript you use Dimple to create an SVG, targeting the element with your id, in this case “chart” and I’ve given it some size options.

```javascript
var svg1 = dimple.newSvg("#chart", 600, 400);
```

### Step 3

Then, you get your data set through an API call, hardcoded, etc.. I’ve hardcoded some sample data of weeks and miles ran for two runners.

```javascript
var data1 = [
    [
      {week: 'week 1', miles: 1},
      {week: 'week 2', miles: 2},
      {week: 'week 3', miles: 3},
      {week: 'week 4', miles: 4}
    ],
    [
      {week: 'week 1', miles: 2},
      {week: 'week 2', miles: 4},
      {week: 'week 3', miles: 6},
      {week: 'week 4', miles: 8}
    ]
  ];
```

### Step 4

Next, you set up your axes. You can create multiple x and y axes with Dimple but for the sake of this example I will just create one x and one y. The two that I use most are category and measure. Category is used for string values, here the runners’ names. One word of caution form the [docs](https://github.com/PMSI-AlignAlytics/dimple/wiki/dimple.axis#measure) for the measure axes is that “If the field is numerical the values will be aggregated, otherwise a distinct count of values will be used.”. This means that if I had two runners who were both named Bill *in the same data set*, and say the first Bill ran 1 mile in week 1 and the second Bill ran 2 miles in week 1, Dimple would graph one x-value Bill and one y-value 3 rather than two Bills, one with 1 mile and one with 2.

```javascript
var xAxis = chart1.addCategoryAxis("x", "week");
var yAxis = chart1.addMeasureAxis("y", "miles");
```

### Step 5

Now we’ve set up the axes, so we want to actually plot the points. In Dimple we call this “adding a series”. We are telling it what kind of graph we want, and what to call the data (in this case, the runner’s name), and we assign it the data we’d like to use.

```javascript
s1 = chart1.addSeries("Bill", dimple.plot.line);
  s1.data = data1[0];
  s1.plot=dimple.plot.line;

  s2 = chart1.addSeries("Sarah", dimple.plot.line);
  s2.data = data1[1];
  s2.plot=dimple.plot.line;
```

### Step 6

Lastly, we simply tell Dimple to actually draw it.

```javascript
chart1.draw(1000);
```

The code in full as well as a working JSBin can be found [here](http://jsbin.com/wivoxuvipe/edit?js,output).

```javascript
var chart1 = new dimple.chart(svg1);
var xAxis = chart1.addCategoryAxis("x", "week");
var yAxis = chart1.addMeasureAxis("y", "miles");

var data1 = [
  [
    {week: 'week 1', miles: 1},
    {week: 'week 2', miles: 2},
    {week: 'week 3', miles: 3},
    {week: 'week 4', miles: 4}
  ],
  [
    {week: 'week 1', miles: 2},
    {week: 'week 2', miles: 4},
    {week: 'week 3', miles: 6},
    {week: 'week 4', miles: 8}
  ]
];

s1 = chart1.addSeries("Bill", dimple.plot.line);
s1.data = data1[0];
s1.plot=dimple.plot.line;
s2 = chart1.addSeries("Sarah", dimple.plot.line);
s2.data = data1[1];
s2.plot=dimple.plot.line;
chart1.draw(1000);
```
