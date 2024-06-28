# Extracting and Manipulating Geospatial Data with OGR2OGR, KML and python GDAL
[pin_label_polygon.png]
  



## Introduction
One of our clients recently provided us with a dataset of properties that they manage, and asked us to generate content based off of these points.
 
We will walk through the process of extracting polygons, placemarks, and other info from a geodatabase file and converting them into separate KML files using the `ogr2ogr` terminal command, adding some logic to the data selection to limit the subset of features. As an alternative, we will explore the GDB file using the GDAL Python library to export the data as JSON for use in other scripts.


## Prerequisites
- Basic understanding of geospatial data.
- Installed versions of the `GDAL/OGR` library.
- A geodatabase file (`.gdb`, `.gdb.zip`, or `.shp`).


## A First Look into the Contents of the GDB File


```bash
ogrinfo example.gdb.zip
```


This will list all layers that are available in the dataset. Add one as a parameter to the same command, and it will output all the fields, their types, and values for every feature in the layer. (The parameter `-so` can be used to omit the values from the output and get only the layer field names and types):


```bash
ogrinfo example.gdb.zip a_layer_name
```
Example output using `-so` flag:
[layer_info.png]
  



This command shows you information for a single layer which can be helpful if you are only looking for some values, but the geographic data is not much to look at in the terminal. To see it, we can convert the data to KML, which applications like Google Earth or Cesium can render while keeping the information as text that can be read:


```bash
ogr2ogr -f "KML" example_output.kml example.gdb.zip layer_name
```


**Explanation:**
- `-f "KML"`: Specifies the output format.
- `example_output.kml`: Name of the output KML file.
- `example.gdb.zip`: Path to the geodatabase file.
- `layer_name`: The geodatabase layer to export.


This command will export into a KML file:
- All the geometries in the layer, be it placemarks or polygons in our case.
- All the other fields of information as extended data, which will show up for each feature as a balloon table when visualized in Google Earth.
[full_label.png]
  



The balloon popup was not the outcome we wanted for this KML file. The first solution was to use `sed` to remove all the extended data from the KML files. Looking into it a bit further, we found an `ogr2ogr` option that made the data filtering easier, `-sql`, which lets us add a query to the command just like getting the data from a SQL database:


### 1. Extract Property Names to KML


To create a KML with just the names of the properties, look up the layers and fields in them using `ogrinfo` and find the points layer that had the names. Then add the desired SQL query to the command:


```bash
ogr2ogr -f "KML" output_names.kml example.gdb.zip -sql "SELECT name FROM Layer_Points"
```


### 2. Extract Polygons Only to KML


The layers had either points or polygons for geometries, and the polygons were in the `Layer_Polygons`. They can be selected using the special OGR field name `OGR_GEOMETRY` that refers to the geometry of the selected layer:


```bash
ogr2ogr -f "KML" output_polygons.kml example.gdb.zip -sql "SELECT OGR_GEOMETRY FROM Layer_Polygons"
```
[polygons_only.png]
  



### 3. Create KML with Pins and Names


To create a KML with property names as placemarks with pins, we just select the name. The point placemark seems to be included with all data:


```bash
ogr2ogr -f "KML" output_pins.kml input.gdb layer_name -sql "SELECT name FROM layer_name"
```


### 4. Create KML with Pins Only, No Names


To get the points with nothing else, we used the following query. It uses the `MakePoint` function from SQLite so that is the only thing in the query, and the KML will only have a list of points:


```bash
ogr2ogr -f "KML" output_pins.kml input.gdb layer_name -dialect SQLite -sql "SELECT MakePoint(land_longitude, land_latitude) AS geom FROM Land_Points"
```


### 5. Extract Limited Properties


For extracting a limited number of properties, we can add the `WHERE` clause to the SQL command if using one, or use the `ogr2ogr` `-where` flag to use that part of the query only:


```bash
ogr2ogr -f "KML" limited_output_polygons.kml input.gdb layer_name -where "ID IN (1, 2, 3)"
```


### 6. Run It All in a Python Script to Redo with Different Data Requests


There is a Python GDAL library, and I will show the basics of it after, but first, here is a simplified example using Python `subprocess` to run the ogr2ogr commands we tested in the terminal:


```python
import subprocess 


gdb_file = "example.gdb.zip"
column_name = "p_code"
elem_str = "'a1', 'a2', 'b1', 'b3'"


sql_land_labels = f"SELECT land_name FROM Land_Points WHERE {column_name} IN ({elem_str})"
subprocess.run(['ogr2ogr', '-f', 'KML', 'land_labels.kml', gdb_file, '-sql', sql_land_labels])


sql_land_points = f"SELECT MakePoint(land_longitude, land_latitude) AS geom FROM Land_Points WHERE {column_name} IN ({elem_str})" 
subprocess.run(['ogr2ogr', '-f', 'KML', 'land_points.kml', gdb_file, '-dialect', 'SQLite', '-sql', sql_land_points])


sql_land_polygons = f"SELECT OGR_GEOMETRY FROM Land_Polygons WHERE {column_name} IN ({elem_str})" 
subprocess.run(['ogr2ogr', '-f', 'KML', 'land_pols.kml', gdb_file, '-sql', sql_land_polygons])
```


This script will create the three different KML files that we usually need for our presentations. We just built the `gdb_file`, `column_name`, and `elem_str` into command line parameters to reuse the script and some other scripts to join, apply custom styling, and add regions to the KMLs, which will be covered in another blog.


### 7. Extract All Data as JSON from One Layer Using Python GDAL


I should have probably started here, but I only used it later on in the process to join the gdp.zip file data with data from other sources (sheets, emails).


First, install GDAL:


```bash
pip install gdal
```


Then use the following Python script with any changes to the parameters gdb_file and layer_name to meet your data:


```python
#!/bin/python


import json
from osgeo import ogr


# Open the GeoDatabase file
driver = ogr.GetDriverByName('OpenFileGDB')
gdb_file = 'example.gdb.zip'
data_source = driver.Open(gdb_file, 0)


# Get the layer
layer_name = 'Building_Points'
layer = data_source.GetLayerByName(layer_name)
if layer:
    # Get the layer definition
    layer_defn = layer.GetLayerDefn()
    
    # Get the number of fields in the layer
    num_fields = layer_defn.GetFieldCount()
    
    # Initialize an empty list to store field names
    field_names = []
    
    # Iterate over each field and add its name to the list
    for i in range(num_fields):
        field_defn = layer_defn.GetFieldDefn(i)
        field_name = field_defn.GetName()
        field_names.append(field_name)
    
    print("Field names:", field_names)
else:
    print(f"Layer '{layer_name}' not found.")


all_info = {}

# iterate over all features and organize all field names under a unique one for the a dictionary structure
for feature in layer:
    if feature is not None:
        globalid = feature.GetField('globalid')
        all_info[globalid] = {}
        for fn in field_names:
            all_info[globalid][fn] = feature.GetField(fn)


# Close the data source
data_source = None


# Save information to a JSON file
output_file = 'info.json'
with open(output_file, 'w') as json_file:
    json.dump(all_info, json_file, indent=4)
print(f"Information saved to {output_file}")
```


The result will be a JSON file with all the information on the layer.


## Conclusion


Following these steps, we can efficiently manage and visualize geospatial data using `ogr2ogr`, SQL, and KML, and in some cases, JSON. These methods allow for a high degree of customization and can be tailored to specific project requirements.


## Additional Resources
- [GDAL/OGR Documentation](https://gdal.org)
- [GDAL Python Bindings](https://gdal.org/python/)
- [KML Documentation](https://developers.google.com/kml/documentation)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
