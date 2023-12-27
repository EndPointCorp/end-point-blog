---
title: "Compressed CZML"
author: Dmitry Kiselev
tags:
- visionport
- gis
- cesium
featured:
  visionport: true
  image_url: /blog/2023/06/compressed-czml/crowded-city.webp
github_issue_number: 1981
date: 2023-06-13
---

![A crowded city on an overcast day. Tall apartment buildings fill the foreground while skyscrapers form a skyline in the background.](/blog/2023/06/compressed-czml/crowded-city.webp)

<!-- Image by Zed Jensen, 2023. -->

Let’s talk about CZML, Cesium's main language for specifying 3D scenes, and how to incorporate external resources such as billboard graphics, material textures, and 3D models into CZML files.

For example, let’s look at how we can include glTF models.

glTF models are composed of multiple files: a single JSON index file along with a variable number of binary buffer files and textures. So, in order to package CZML assets that include glTF models for distribution, you have to read the CZML document itself, then read the referenced glTF files. If they are not binary GLB files, you must also read the glTF files and package all of the files referenced by the glTF models. And if you find this paragraph cumbersome, that's no accident. Indeed, the whole process is quite cumbersome!

So we are dealing with something like:

* CZML Document

    * glTF Model

        * buffer1.bin
        * buffer2.bin
        * texture1.png
        * texture2.png
        * …

If you want to keep the glTF model as a single asset, you can convert the glTF files into binary (GLB) files, and then embed them as base64 data links into CZML. 

Another example would be a set of points with billboards, let’s say a couple hundred points with plenty of different images. Keeping track of what images you have to ship along with a CZML document is very inconvenient, so you might want to embed the images. 

As with 3D models you could use base64 data links, but you will lose readability. You won’t be able to easily edit an image itself; you will have to decode it back into an image file, edit it, re-encode it, and write it back into the CZML file.

And furthermore, while many billboards can share the same image, if you are going to encode it to base64, you either have to repeat the same base64-encoded string over and over or use [CZML reference properties](https://cesium.com/learn/cesiumjs/ref-doc/ReferenceProperty.html). On the one hand, repeating the same base64 string makes a file terribly bloated, while on the other, with CZML reference properties you have to keep track of Entity IDs. Tracking Entity IDs means you need to be sure that you don’t accidentally delete the Entity which others refer to, and you’ll need to copy it if you want to split the dataset into different files.

What I really want is to use the same approach that Google Earth uses for KMZ files: KMZ is just a ZIP archive with a KML document and referenced assets packed together. Let’s do the same trick with CZML.

So the general approach would be:

1. Read CZMZ ZIP archive.
2. Index ZIP entries as blob objects.
3. Find the main CZML document.
4. Load it with Cesium CzmlDataSource and proxy all local URLs to blobs from step 2.
5. Add destructor to DataSource to revoke blob URLs.

To set a proxy we have two main options: read the whole CZML document as a JavaScript object and replace all of the URLs with [Cesium.Resource](https://cesium.com/learn/cesiumjs/ref-doc/Resource.html) objects using a proxy, or provide a Cesium.Resource to [CzmlDataSource.load](https://cesium.com/learn/cesiumjs/ref-doc/CzmlDataSource.html#load) instead of URLs. In most cases the second option is easier, unless you do some preprocessing on the CZML document before loading.

You can read zip archives with a library of your choice. I’m using zip.js because Cesium already uses some methods from it.

```js
const data = await (await fetch(assetPath)).blob();
const reader = new zip.ZipReader(new zip.BlobReader(data));

const entriesMap = new Map();

for (let entry of entries) {
   const blob = await entry.getData(new zip.BlobWriter());
   const blobURL = URL.createObjectURL(blob);

   entriesMap.set('/' + entry.filename, blobURL);
}
```

Now get the document:

```js
const documentEntry = entries.find(e => /\.czml$/i.test(e.filename));
const documentBlob = entriesMap.get('/' + documentEntry.filename);
```

And load the DataSource:

```js
DataSourceInstance.load(new Cesium.Resource({
   url: documentBlob,
   proxy: {
      getURL: URL => {
          if (/^blob:/.test(URL)) {
               const blobId = new URL(URL.replace(/^blob:/, '')).pathname;
               const blobURL = entriesMap.get(blobId);
               return blobURL ? blobURL : URL;
           }
           console.warn('URL not found inside czmz', URL);
           return URL;
       }
   }
}));
```

That’s mostly it. We just want to clean up after ourselves; we have to unregister blob URLs to free the resources.

It’s not documented, but if you remove a DataSource from DataSourceCollection with the `destroy` parameter set to true, and DataSource has a destroy method, it will be called.

```js
DataSourceInstance.destroy = function() {
   for (let blobUrl of entriesMap.values()) {
       URL.revokeObjectURL(blobUrl);
   }
};
```
