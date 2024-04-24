---
title: "An OpenStreetMap Editor for Adding Public Transit Data Using GTFS"
author: Dmitry Kiselev
featured:
  visionport: true
  image_url: /blog/2024/04/an-openstreetmap-editor-for-incorporating-gtfs-data/app-overview.webp
date: 2024-04-24
github_issue_number: 2041
tags:
- gis
- visionport
- open-source
---

![The OpenStreetMap GTFS editor. The right side is a map with a darkened map, and blue, red, and black dots overlayed along the roads where public transit stops are. In the corner, the map reads "Leaflet | copyright OpenStreetMap". It has controls to zoom, change between satellite and OpenStreetMap, darken the map, and open in JOSM. The left side has navigation buttons reading "Import" (which is selected), "Stops", "Routes", "Trips", and "Changes". Below there is text on several lines: "gtfs.zip. Loaded 5246 stops" then a button reading "Query OSM data". Then, "OSM Tag with GTFS stop code: " and a text box with "gtfs:ref" typed inside. Next, bold text reading "Possible GTFS stop code tags", followed by a list of tags: "ref (6615 objects), route_ref (129 objects), local_ref (127 objects), ref:US-UT:uubus (24 objects), railway:ref (5 objects), loc_ref (7 objects), gtfs:stop_id (2 objects), ref:left (2 objects), ref:right (2 objects), noref (26 objects), crossing_ref (16 objects)". Next, "show help". "Match stops by name: " and an unchecked checkbox. Next, "Match stops by GTFS code in name: " and an unchecked checkbox. Next, bold text reading "Template tags for platform". Then, 3 rows in a table. The first two have minus sign buttons on the left, and two columns reading: "public_transport","platform" and "highway","bus_stop". The third row is just a plus sign button.](/blog/2024/04/an-openstreetmap-editor-for-incorporating-gtfs-data/app-overview.webp)

You can think of OpenStreetMap (OSM) as Wikipedia for maps. While it may not be as well known as Google Maps or Apple Maps, OSM becomes indispensable when you need data, rather than just a visual representation on your phone. Your options are rather limited: you can either consult a local agency or you can turn to OSM. If you're in search of a comprehensive and global cartographic dataset, OSM is the go-to choice.

OSM also excels in providing navigation for pedestrians and cyclists. For the past decade, I've navigated the US, Canada, and Europe using OSM through the OsmAnd app, a dedicated Android application for OpenStreetMap.

Overall, my experience has been quite positive, except for one significant weakness: public transportation. Specifically, I've been missing the convenient access to timetables for buses, trams, or any other form of public transit.

A significant part of the challenge in making public transportation data readily available on OSM and its associated applications is the fact that the OSM data model isn’t particularly well suited for this type of information. While OSM can store the location of bus and train stops, the actual timetables change so often that keeping them up to date in OSM is essentially impossible.

Enter the General Transit Feed Specification (GTFS), a widely adopted standard for managing public transportation data. I wanted to explore ways to integrate OSM with GTFS effectively.

### My OpenStreetMap editor for GTFS data

A simple approach for addressing this challenge would be to overlay an OSM map with stops from GTFS. While this would be relatively straightforward, it doesn't leverage OSM's biggest strength—its vibrant community. One of OSM's most significant advantages is that it dynamically incorporates user contributions: as soon as the community accesses useful data, members enhance the details and accuracy of its mapping data. Therefore, I’ve been working on truly integrating GTFS data with OSM, creating a cohesive mapping experience rather than settling for a disjointed overlay.

Although the implementation is a bit trickier, I believe the better approach for handling this challenge involves merging GTFS stops with those already present in OSM and incorporating GTFS stop codes into OSM data. Hence, I've developed a single-page online editor. This tool facilitates the creation, editing, and deletion of stops within OSM. It also highlights stops based on their alignment with stops specified in a given GTFS file.

Editing the routes wasn’t a priority, yet I found it necessary to match GTFS routes and trips with OSM routes and their variants. Displaying trips shows which part of a street a route uses and also which side of a street bus stops are located on.

I've deployed the app on my GitHub, where you can try it out: https://kiselev-dv.github.io/osm-gtfs/.

### How to use the app

To start, download a GTFS data dump. They are usually published by local transit companies. As an example, I'll use data from Halifax, Nova Scotia.

Open the GTFS ZIP file in the editor. The editor should parse stops from GTFS.

![The OSM editing app. The map is not darkened and does not have any blue, red, or black dots. The left bar does not have a list of tags anymore.](/blog/2024/04/an-openstreetmap-editor-for-incorporating-gtfs-data/gtfs-file.webp)

Next, query OSM data and select “OSM Tag with GTFS stop code.” After OSM data is loaded you will get OSM tags statistics which might help you to see if there are some popular tag combination for GTFS data in the area. OSM doesn’t have strict data model, but as a rule of thumb for that type of data `ref` or `gtfs:ref` should work. If there are multiple agencies sharing a stop and each of them publishes its own GTFS data, you can use something like `gtfs:<agency_name>:ref`. By default the editor will substitute the most popular tag containing `ref` or `gtfs`.

Now you can match stops from OSM with stops from GTFS. Matches are color coded:

* Blue: matching stops
* Red: stops which are present in GTFS but not mapped in OSM — stops to add
* Black: stops mapped in OSM but not matched with GTFS stop. Probably outdated stops which are no longer in use and may be deleted, or stops not used by the agency whose GTFS data you are using.

![The OSM editing app. The "Stops" navigation option is selected. On the map, there are black dots on top of bus stops visible in the actual map texture. Most of these black dots have nearby red circles. There are a couple of blue dots on top of bus stops. The text in the left app bar reads: "Filter matches by Route/Trip" then a dropdown select box reading "Select a route". Then, "Show matched: 4844" with a checked checkbox. Then, "Show unmatched GTFS: 402" with a checked checkbox. Then, "Show unmatched OSM: 1512" with a checked checkbox. Then a button, "Open listed stops in JOSM". Then, a list of bus stops: "Constitution Blvd @ 3700 S" with a blue circle, "Constitution Blvd @ 3601 S" with a blue circle, etc.](/blog/2024/04/an-openstreetmap-editor-for-incorporating-gtfs-data/stop-matching.webp)

### Adding stops to OSM

To add or match a stop there are two main cases:

* There is no stop in OSM at all and we want to create a new one.
* There is a stop in OSM and we want to edit it and add GTFS data.

Select one of the GTFS stops, on the left panel there are two buttons, “Create” and “Assign”. 

![The OSM editing app. The "Stops" tab is selected. In the map, there are red circles on either side of a road. One is larger than the other, indicating its selection. Text in the bar on the left reads: "900 E / 300 S (SB)", then "GTFS Stop code: 820054, GTFS Stop id: 21317". Then, "Routes on this stop: Provo Central Station (831 - PROVO GRANDVIEW)" with a filter icon and a rising arrow icon. There is another similar stop. Then "This GTFS stop has no matched OSM stop. Select one of the OSM stops nearby to set GTFS code in its tags". Then, "OSM Stop platform:" and two buttons reading "Create" and "Assign". These buttons are highlighted. Then there are stop filter options.](/blog/2024/04/an-openstreetmap-editor-for-incorporating-gtfs-data/create-assign-buttons.webp)

The “Create” button will switch the map into satellite mode, create a new OSM stop with GTFS code, and add a stop name at the point where you click. When creating a stop or editing its location, pay attention to which side of the road it should be on. To simplify that, you can highlight one of the routes in the “Routes on this stop” section.

![The OSM editing app. The map is showing satellite imagery. A blue stop is selected, with options on the left to move or reassign the stop, as well as OSM data: "name: 900 E / 300 S (SB), ref: 820054, public_transport: platform, highway: bus_stop". This data is in a two-column editable table.](/blog/2024/04/an-openstreetmap-editor-for-incorporating-gtfs-data/create-stop.webp)

The “Assign” button allows you to select one of the existing OSM stops, and set its GTFS code.

![The OSM editing app. One blue stop is highlighted. It has more OSM data filled out, including "network: UTA, network:wikidata: Q7902494", etc.](/blog/2024/04/an-openstreetmap-editor-for-incorporating-gtfs-data/assign-stop.webp)

### Demo videos

You can see a [video on my YouTube channel](https://www.youtube.com/watch?v=fG_RvC7AWfk) with the latest updates to the editor, along with a live editing session.

I have also created a [YouTube playlist](https://www.youtube.com/playlist?list=PL0eKSR1VCpIQiTntglaVhKXt4PKWTcEg6) with more demos.

### An important note

An important note is that I do not upload results directly into OSM. Instead, I generate an XML file for an OSM changeset which you can view and edit in JOSM or another editor. I do this partly so I do not have to deal with authentication, but more importantly, because I see editing public transport relations in OSM as an advanced topic and it makes sense for editors to demonstrate a higher level of sophistication than general users. But I might change my mind about this if I get feedback that it would be desirable.

My app is built using React and Leaflet. You can find the code on my GitHub: https://github.com/kiselev-dv/osm-gtfs

