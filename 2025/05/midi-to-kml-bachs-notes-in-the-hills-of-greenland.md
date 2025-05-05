---
title: "Converting MIDI to KML using AI: Bach’s Notes in the Hills of Greenland"
date: 2025-05-02
author: Darius Clynes
github_issue_number: 2110
featured:
  image_url: /blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/bach-in-kml.webp
  visionport: true
description: The features and issues in an AI-written JavaScript program to visualize MIDI files using KML.
tags:
- kml
- gis
- artificial-intelligence
- visionport
---

![A 3D globe visualization at an oblique angle, with hills, lakes, and mountains, with several pins in the foreground reading "acoustic grand piano". There are extruded triangles which are green and red extending away from the viewpoint, regularly spaced in multiple straight lines, and varying in size.](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/bach-in-kml.webp)

I have always been interested in ways of representing music visually. Aside from conventional music notation, I imagined other cross-modal generation methods that could take a sound and generate an image. In the same vein, I have frequently envisioned a 3D landscape in which you could discover musical “objects”.

Well, now I've realized a version of this dream — with caveats which will be mentioned later. In this blog I would like to demonstrate how I used AI (in my case ChatGPT using GPT-4 Turbo) to create an interesting JavaScript application from just a few phrases. In this case, we will be making an application that can take as input an existing piece of music represented by a MIDI file and as output, create a KML file that you can view as 3D objects somewhere on the globe.

Here is how I enlisted ChatGPT to help me:

```plain
please make a javascript application that can take a MIDI file and covert it to extruded polygons in a kml file
```

Here is a part of its response:

![The response to the above ChatGPT query. Chat breaks the process down into 3 steps, "Parse the MIDI File", "Generate Data for Polygons", and "Create a KML File".](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/make-a-javascript-application.webp)

I was amazed. It included code to select the MIDI file, convert it to KML, and generate an output file. Plus, ChatGPT correctly interpreted my request despite my “covert” typo. :-)

Before testing it I was interested in having the color of the extruded polygon be dependent on the pitch of the note. So next I entered:

```plain
please change the color of the extruded polygon dependent on the pitch
```

Here is what it said:

![Chat's response to the above query: "To change the color of the extruded polygons based on the pitch, we can modify the KML content to include a `Style` element for each `Placemark`. We'll map MIDI note pitches to different colors.](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/change-the-color.webp)

It was implemented using npm and Node.js, which seemed excessive for this small application. To make an easier-to-run version in a single html file, I entered:

```plain
please rewrite it so it is in an html page without node.js
```

![Chat's response to the above query: "To create a web-based application that converts a MIDI file to extruded polygons in a KML file, we can use JavaScript and the Web MIDI API along with a client-side library for parsing MIDI files, such as `@tonejs/midi`.](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/rewrite-it.webp)

![An unstyled HTML app reading "MIDI to KML Converter". There is a "choose file" button, with adjacent text reading "bach_846.mid". To the right is a "Convert to KML" button. Below is a "Download KML" link. Below that, a "play" button, then three text inputs reading "Longitude", "Latitude", and "Direction", respectively.](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/plain-html-app.webp)

I thought it would be nice to be able to place the polygons, easily, wherever you wanted to, in the world.

I asked it to take a Google Street View position from Google Maps and decode the latitude, longitude, and heading.

Next, I asked it to make a nicer user interface. It “understood” the purpose of the application very well and came up with a very nice interface explaining what it does.

![The same app as above, but now styled using simple web design, including making the "Convert to KML" button Green, and including an explanation paragraph: "Upload your MIDI file below, and the application will convert it into a KML file with 3D polygons. Each note in the MIDI file will be represented by an extruded polygon, and different musical instruments will be visually distinct with images on each polygon. Download the KML file and view it in Google Earth.](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/styled-app.webp)

### How to try out the application

You can try out a version of the application at https://darius.endpointdev.com/midi2kml/midi2kml_improved.html.

![The same app as above, now with a "Play MIDI" button visible, the "choose file" box filled, and values entered for coordinates.](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/test-coordinates.webp)

1. Find a nice place to have the MIDI data displayed. Copy the URL and paste it into the Street View URL field.

  For example, here is [a place](https://www.google.com/maps/@60.8287681,-45.7810281,2a,66.4y,280.22h,98.22t/data=!3m7!1e1!3m5!1sPgzLk0iAbXx_eGh1Z7pS0g!2e0!6shttps:%2F%2Fstreetviewpixels-pa.googleapis.com%2Fv1%2Fthumbnail%3Fcb_client%3Dmaps_sv.tactile%26w%3D900%26h%3D600%26pitch%3D-8.219999999999999%26panoid%3DPgzLk0iAbXx_eGh1Z7pS0g%26yaw%3D280.22!7i13312!8i6656?entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D) in Greenland:

  ![A Google Street View spherical image of hills in Greenland, with a Google Maps label reading "Hvalsey Church", with a brick building and the ocean visible](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/greenland-sphere.webp)

  And here's one [on the beach](https://www.google.com/maps/@53.1000141,4.7522293,3a,75y,270.07h,90t/data=!3m8!1e1!3m6!1sAF1QipO8lOwNwAosMdcm3YTQT2CQleKuRXNRc59MsmA-!2e10!3e11!6shttps:%2F%2Flh3.googleusercontent.com%2Fp%2FAF1QipO8lOwNwAosMdcm3YTQT2CQleKuRXNRc59MsmA-%3Dw900-h600-k-no-pi0-ya271.06580195437505-ro0-fo100!7i8704!8i4352?entry=ttu&g_ep=EgoyMDI1MDMxMi4wIKXMDSoASAFQAw%3D%3D) in Texel in the Netherlands:

  ![A Google Street View spherical image of a beach, with a sunset, with a Google Maps label reading "Beachclub Texel"](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/beach-netherlands.webp)

2. Find a nice MIDI file like [Bach’s prelude and fugue in C major](https://darius.endpointdev.com/midi2kml/bach_846.mid). Download it and put it in the "choose MIDI file" field

3. Press "Convert to KML"

4. Click on the "download KML" link

4. Open the KML file in a KML viewer or by manually by loading it into a program like Google Earth or Cesium.

![A closer view of the triangles extruded from Google Earth imagery, both labeled "acoustic grand piano", and with some triangles smaller on the right, while the ones on the left have some duplicate triangles superimposed on others.](/blog/2025/05/midi-to-kml-bachs-notes-in-the-hills-of-greenland/midi-visualization-triangles.webp)

### Issues

This application works at least partially — it puts triangular prisms for each MIDI track, over time, and shows different colors for different notes (though the color–note correlation is not clear). There are plenty of issues and questions, however:

* There are lots of overlapping polygons. It's unclear whether these are just errors, or represent different dynamics or articulations
* The "Play MIDI" button doesn't work — it plays tones of some kind, but in my testing it was either a single bell sound, or computer noise reminiscent of an AOL dial-up modem.
* When I tested it on an orchestral score (Mozart's Requiem, Kyrie), the instrument label pins were off to the side, not indicating which line of notes they corresponded to, and were mostly labeled "acoustic grand piano," which is not an instrument included in the MIDI file.

### Using AI for blog post image processing

As an aside, I created this blog using Google Docs with PNG pictures embedded in it. Our blog structure requires a Markdown document with separate WebP images. Google Docs has a nice Markdown export function, but it converts the PNG images into embedded Base64-encoded PNG. So I asked ChatGPT to extract the Base64-encoded PNG and create WebP files. It created a Python script that did this perfectly:

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

Unfortunately, when Google Docs embeds the images, it seems to downsize the resolution, so for this post, old-school image processing it is!
