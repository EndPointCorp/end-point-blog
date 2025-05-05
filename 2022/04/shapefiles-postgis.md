---
author: Josh Tolley
title: "On Shapefiles and PostGIS"
date: 2022-04-02
tags:
- tips
- open-source
- tools
- gis
- maps
- postgres
- kml
github_issue_number: 1851
---

![Partial map of the voyage of the Endurance, from the book "South", Ernest H. Shackleton](/blog/2022/04/shapefiles-postgis/endurance-clip.webp)
Partial map of the voyage of the Endurance, from ["South", by Ernest Shackleton](https://www.gutenberg.org/ebooks/5199)

The shapefile format is commonly used in geospatial vector data interchange, but as it's managed by a commercial entity, Esri, and as GIS is a fairly specialized field, and perhaps because the format specification is only ["mostly open"](https://en.wikipedia.org/wiki/Shapefile), these files can sometimes be confusing to the newcomer. Perhaps these notes can help clarify things.

Though the name "shapefile" would suggest a single file in filesystem parlance, a shapefile requires at least three different files, including filename extensions `.shp`, `.shx`, and `.dbf`, stored in the same directory, and the term "shapefile" often refers to that directory, or to an archive such as a zipfile or tarball containing that directory.

### QGIS

[QGIS](https://qgis.org) is an open-source package to create, view, and process GIS data. One good first step with any shapefile, or indeed any GIS data, is often to take a look at it. Simply tell QGIS to open the shapefile directory. It may help to add other layers, such as one of the world map layers QGIS provides by default, to see the shapefile data in context.

### GDAL

Though QGIS can convert between GIS formats itself, I prefer working in a command-line environment. [The GDAL software suite](https://gdal.org/) aims to translate GIS data between many available formats, including shapefiles. I most commonly use its `ogr2ogr` command-line utility, along with the excellent accompanying manpage.

In short, a typical `ogr2ogr` command tells the utility where to find the input data and where to put the converted output, optionally with various reformatting and processing options. You'll find some examples below.

### PostGIS

Much of our (ok, my) GIS work has involved [PostGIS](https://postgis.net), an extension to the PostgreSQL database for handling GIS data. It's been convenient for me to process GIS data using the same language and tools I use to process other data. It uses GDAL's libraries internally.

### Examples

#### Import Shapefile data into PostGIS

The example below comes from a customer's project we recently worked on. They provided us a set of several shapefiles, which I first arranged in a directory structure. This code imports each of them into a PostGIS database, in the `shapefiles` schema.

The other arguments to `ogr2ogr` specify the output format ("PostgreSQL"), the destination database name, and the directory which stores the shapefile. `ogr2ogr` expects the destination and source arguments in that order, as two positional arguments, so here the destination is `PG:dbname=destdb`, and the source file name comes from the the `$i` script variable.

```bash
for i in `find . -name "*shp"`; do
    j=$(basename $i)
    k=${j/.shp/}
    ogr2ogr -f PostgreSQL -nln shapefiles.${k} PG:dbname=destdb $i
done
```

#### Export PostGIS data as KML

This example creates a KML file from PostGIS query results. The arguments provide the query to use to fetch the data, the output format ("KML"), the output file name, and the source database. This will create a KML file containing a set of unstyled placemarks, with names from the `property_code` column, and geometry data from the `outline_geom` column in the `properties` table of our database.

In this project, `outline_geom` contained GIS "linestrings", data types consisting of a series of lines, which `ogr2ogr` translated into KML polygons. Had `outline_geom` contained points, for instance, the KML result would also have been points. In other words, `ogr2ogr` automatically chooses the correct KML object type based on the GIS object type in the input data.

```bash
ogr2ogr -sql "select property_code, outline_geom from properties" -f KML outlines.kml PG:dbname=properties
```

Note that though the examples above use PostGIS, `ogr2ogr` can take shapefile input and produce KML output directly without the PostGIS intermediary. We used PostGIS in these cases for other purposes, such as to filter the output and limit the attributes stored in the KML result.

By default, `ogr2ogr` puts all the attributes from the shapefile into `ExtendedData` elements in the KML, but in our case we didn't want those. We also didn't want all the entries in the shapefile in our resulting KML. To skip the PostGIS step, we might do something like this:

```bash
ogr2ogr -f kml output.kml shapefile_directory/
```

What tools do you use for shapefile processing? Please let us know!
