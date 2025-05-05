---
title: "Converting MIDI to KML using AI: Bach’s Notes in the Hills of Greenland"
date: 2025-05-02
author: Darius Clynes
github_issue_number: x
featured:
  image_url:
description:
tags:
- kml
- gis
---

### Using AI to create a Javascript program for data conversion

![](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/bach-in-kml.webp)

I have always been interested in various ways to represent music visually. Aside from traditional and conventional music notation, I imagined other cross modal generation methods that could take a sound and generate an image. In a similar vein I have frequently envisioned a 3D landscape in which you could discover musical “objects”.

Well, well, now I can realize a version of this dream, and in this blog I would like to demonstrate how you too can use AI, in my case ChatGPT GPT-4-turbo, to help you create an interesting Javascript application from just a few phrases. In this case, we will be making an application that can take an existing musical score as represented by a MIDI file, as input  and as output, create a KML file that you can view as 3D objects somewhere on the earth globe (see footnote for more about MIDI and KML files)

Here is how I enlisted ChatGPT to help me.

1) I typed the following at the ChatGPT prompt:

```plain
please make a javascript application that can take a midi file and covert it to extruded polygons in a kml file
```

Here is a part of its response:

![](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/make-a-javascript-application.webp)

I was truly amazed. It included code necessary to select the midi file, convert it to KML and generate an output file.  (And, yes, of course ChatGPT correctly interpreted my request despite my “covert” typo. :-))

It was implemented using npm and node.js and I was going to try it out later, but first I was interested in having the color of the extruded polygon be dependent on the pitch of the note. So, next I entered:

```plain
please change the color of the extruded polygon dependent on the pitch
```

Here is what it said:

![](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/change-the-color.webp)

Still not having tried or tested the application I wanted an easier-to-run version in a single html file, so I entered:

```plain
please rewrite it so it is in an html page without node.js
```

![](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/rewrite-it.webp)

![](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/plain-html-app.webp)

I thought it would be nice to be able to place the polygons, easily, wherever you wanted to,  in the world.

I asked it to take a Google Street View position from Google Maps and decode the latitude, longitude and heading.

Next, I asked it to make a nicer User interface. It “understood” the purpose of the application very well and came up with a very nice interface explaining what it does.

![](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/styled-app.webp)

You can try out a version of the application here:

[Here](https://darius.endpointdev.com/midi2kml/midi2kml_improved.html)

![](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/test-coordinates.webp)


Steps to try out the application:

1. Find a nice place to have the midi data displayed
   Copy the url and paste it into the StreetView URL field

  For example, here below is a place in Greenland: [Here](https://www.google.com/maps/@60.8287681,-45.7810281,2a,66.4y,280.22h,98.22t/data=!3m7!1e1!3m5!1sPgzLk0iAbXx_eGh1Z7pS0g!2e0!6shttps:%2F%2Fstreetviewpixels-pa.googleapis.com%2Fv1%2Fthumbnail%3Fcb_client%3Dmaps_sv.tactile%26w%3D900%26h%3D600%26pitch%3D-8.219999999999999%26panoid%3DPgzLk0iAbXx_eGh1Z7pS0g%26yaw%3D280.22!7i13312!8i6656?entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D)

  ![](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/greenland-sphere.webp)

  Or on the beach in Texel in the Netherlands : [Here](https://www.google.com/maps/@53.1000141,4.7522293,3a,75y,270.07h,90t/data=!3m8!1e1!3m6!1sAF1QipO8lOwNwAosMdcm3YTQT2CQleKuRXNRc59MsmA-!2e10!3e11!6shttps:%2F%2Flh3.googleusercontent.com%2Fp%2FAF1QipO8lOwNwAosMdcm3YTQT2CQleKuRXNRc59MsmA-%3Dw900-h600-k-no-pi0-ya271.06580195437505-ro0-fo100!7i8704!8i4352?entry=ttu&g_ep=EgoyMDI1MDMxMi4wIKXMDSoASAFQAw%3D%3D)

  ![](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/beach-netherlands.webp)

2. Find a nice midi file like this one:
   Bach’s prelude and fugue in C major: [Here](https://darius.endpointdev.com/midi2kml/bach_846.mid)
   Download it and put it in the choose midi file field

3. Press Convert Midi to KML
   Click on the link download KML

4. Open by clicking the downloaded KML file if you already have a KML viewer
    or manually by loading it into a program like Google Earth or Cesium.

![](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/midi-visualization-triangles.webp)

As an aside , I created this blog using Google Docs with png pictures pasted in. Our blog structure requires an md (Markdown) format with webp images. Google docs has a nice md export function but converts the png images into embedded base64 encoded png. So I asked chatGPT to extract the base64 encoded png and create webp files. It created a python script that did this perfectly:

```python
import os
import base64
import re
from PIL import Image
from io import BytesIO

# Path to your Markdown file
md_file_path = "example.md"

# Directory to store extracted and converted WEBP images
output_dir = "converted_images"
os.makedirs(output_dir, exist_ok=True)

# Load the Markdown content
with open(md_file_path, "r") as md_file:
    content = md_file.read()

# Regex to find base64-encoded PNGs in the Markdown

base64_pattern = re.compile(
    r"\[.*?\]:\s*<data:image/png;base64,([A-Za-z0-9+/=]+)>"
)

# Initialize a counter for naming the files
counter = 1

for match in base64_pattern.finditer(content):

    print(f"Match found: ")
    base64_data = match.group(1)
    print(base64_data)

    # Decode the base64 string to a PNG image
    png_data = base64.b64decode(base64_data)
    png_image = Image.open(BytesIO(png_data))

    # Save the PNG as a WEBP file
    webp_name = f"image_{counter}.webp"
    webp_path = os.path.join(output_dir, webp_name)
    png_image.save(webp_path, "WEBP")

    # Replace the base64 PNG in the Markdown with a reference to the WEBP file
    content = content.replace(match.group(0), f"![Image {counter}]({webp_path})")
    counter += 1

# Save the updated Markdown file
updated_md_path = os.path.splitext(md_file_path)[0] + "_updated.md"
with open(updated_md_path, "w") as updated_md_file:
    updated_md_file.write(content)

print(f"Updated Markdown file saved: {updated_md_path}")
print(f"WEBP images saved in: {output_dir}")
```

Midi and Kml files:

Input:
 	a MIDI file:

- a standard music file format for storing and playing musical note information using compatible software.

  Example: ( track1 instrument piano:  Ab7, 1 sec, velocity 32\)

generating

Output:
 	a KML file:

- a standard geospatial file format containing positional information and geodata (often “pins” and “polygon” data to highlight points of interest) to be used by map software such as google earth to display paths and information on a 3D globe
  (extruded polygon latitude and longitude and altitude)

What is a Midi File:

A **MIDI file** (Musical Instrument Digital Interface file) is a type of digital file that stores **musical performance data** rather than actual sound recordings. It contains instructions that tell electronic instruments, synthesizers, or software how to play a piece of music.

### **Key Features of MIDI Files:**

1. **No Actual Audio** – MIDI files do not contain recorded sound; they store **note data** like pitch, duration, velocity (intensity), and instrument type.
2. **Compact Size** – Since they only store instructions, MIDI files are much smaller compared to audio files like MP3 or WAV.
3. **Multi-Track Capabilities** – They can include multiple instrument tracks (e.g., drums, piano, strings) in a single file.
4. **Editable & Flexible** – You can modify the tempo, change instruments, adjust notes, and rearrange compositions easily.
5. **Standardized Format** – Most MIDI files follow the **Standard MIDI File (SMF) format**, which comes in:
  * **Type 0** (Single Track) – All musical data is merged into one track.
  * **Type 1** (Multi-Track) – Each instrument has its own separate track.

### **Common Uses of MIDI Files:**

* **Music Composition & Production** – Used in DAWs (Digital Audio Workstations) like Ableton, FL Studio, and Logic Pro.
* **Karaoke Systems** – Many karaoke machines use MIDI files to generate instrumental backing tracks.
* **Video Game Music** – Older video games used MIDI to produce music with limited hardware resources.
* **Educational Tools** – Music learning apps use MIDI to help students practice.

What is a KML File:

A **KML file** (Keyhole Markup Language file) is a **geospatial file format** used to store and share map locations, annotations, and imagery overlays. It is based on **XML** and is primarily used with mapping applications like **Google Earth, Google Maps, and GIS software**.

### **Key Features of KML Files:**

1. **Geographical Data Storage** – Stores locations using latitude and longitude coordinates.
2. **Supports Various Data Types** – Includes points, lines, polygons, images, 3D models, and descriptive text.
3. **Uses XML Structure** – The format is human-readable and machine-processable.
4. **Compatible with Mapping Software** – Works with applications like Google Earth, ArcGIS, and NASA World Wind.
5. **Custom Styling & Overlays** – Allows users to customize map elements with colors, icons, and labels.

### **Common Uses of KML Files:**

* **Mapping & Navigation** – Used for creating custom maps, marking routes, and sharing geographic data.
* **Urban Planning & GIS Analysis** – Helps city planners and researchers visualize land use and geographic trends.
* **Tourism & Travel Guides** – Provides interactive maps with locations of interest.
* **Disaster Management** – Used to plot evacuation routes, hazard zones, and emergency response plans.

KML files often come in a **compressed format (.KMZ)**, which includes additional resources like images and models.

[Iceberg in Qaqortoq Greenland](https://www.google.com/maps/@60.7622253,-45.9058007,2a,75y,230.61h,90.52t/data=!3m7!1e1!3m5!1sKpifq42NQgbjTAqrnQLQ3A!2e0!6shttps:%2F%2Fstreetviewpixels-pa.googleapis.com%2Fv1%2Fthumbnail%3Fcb_client%3Dmaps_sv.tactile%26w%3D900%26h%3D600%26pitch%3D-0.5223091546728966%26panoid%3DKpifq42NQgbjTAqrnQLQ3A%26yaw%3D230.61325990633804!7i13312!8i6656?entry=ttu&g_ep=EgoyMDI1MDMxMi4wIKXMDSoASAFQAw%3D%3D)

