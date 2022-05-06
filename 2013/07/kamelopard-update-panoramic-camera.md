---
author: Josh Tolley
title: Kamelopard update—​Panoramic camera simulation, and splines have returned
github_issue_number: 834
tags:
- google-earth
- graphics
- kamelopard
- visionport
- open-source
- ruby
date: 2013-07-16
---

A few days ago I pushed Kamelopard version 0.0.12 to [RubyGems](https://rubygems.org/gems/kamelopard). This version includes a couple big items. The first of these is a new implementation of the spline code that was removed a while ago. As I mentioned in [a previous blog post](/blog/2013/04/creating-smooth-flight-paths-in-google/), this original implementation was built in anticipation of an API that never materialized. The new version is built on the same API discussed in the previous post I mentioned, modified to support multidimensional functions. More information about these splines is available on the [wiki for Liquid Galaxy](https://github.com/liquidgalaxy/liquid-galaxy/wiki).

The other big new feature is the ability to simulate multiple-camera panoramic images, which we’re calling “multicam”. It has [its own wiki page](https://github.com/LiquidGalaxy/liquid-galaxy/wiki/KamelopardMulticam) as well, but I wanted to describe it in greater detail, because there’s a fair bit of 3D geometry involved that seemed blog-worthy. First, though, it’s important to understand the goal. In a Liquid Galaxy, each instance of Google Earth displays the view from one virtual “camera”. One display’s camera points exactly where you tell it to point; the others point to one side or the other, based on [a few settings](https://github.com/LiquidGalaxy/liquid-galaxy/wiki/QuickStart) in a Google Earth configuration file. When placed side-by-side in the right order, these displays form a single panoramic image. Google Earth itself figures out where these displays’ cameras should point, but for some applications, we wanted to be able to calculate those display angles and position the cameras on our own. For instance, it would sometimes be nice to pre-record a particular tour and play it back on a Liquid Galaxy as a simple video. For a seven-screen galaxy, we’ll need seven different video files, each with the same movements to and from the same geographic locations, but each with a slightly different camera orientation.

Camera orientation is controlled by [KML AbstractView elements](https://developers.google.com/kml/documentation/kmlreference#abstractview), of which there are two varieties: [Camera](https://developers.google.com/kml/documentation/kmlreference#camera), and [LookAt](https://developers.google.com/kml/documentation/kmlreference#lookat). The former tells the camera its position and orientation exactly; the latter describes it in terms of another point. For now, multicam only supports Camera objects, because LookAt is somewhat more complicated.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/07/kamelopard-update-panoramic-camera/image-0-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/07/kamelopard-update-panoramic-camera/image-0.png"/></a></div>

A Camera object gives the camera’s latitude, longitude, and altitude, and three angles called heading, tilt, and roll. The camera initially points straight down, positioned so that north is up. When orienting the camera, Google Earth first rotates around the Z axis, which extends through the lens of the camera, by the heading amount. Then it rotates around the X axis, which extends through the sides of the camera, by the amount given by the tilt angle. Finally, it rotates around the Z axis again, by the roll amount. The Y axis always points in whatever direction the camera thinks is “up”.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/07/kamelopard-update-panoramic-camera/image-1-big.png" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2013/07/kamelopard-update-panoramic-camera/image-1.png"/></a></div>

With that background, we’re ready to tackle the problem at hand. We’ll consider our cameras as shown in the drawing. Camera 0 is the master view, positively numbered cameras go off to the master camera’s right, and negatively numbered cameras to the left. Each camera has the same view angle. We want an API that will accept the master camera’s orientation, the number of the camera we’re interested in, and the view angle of each camera, and return the orientation for the camera number we gave. We’ll consider each camera’s orientation in terms of two vectors; the first will tell us what direction the camera is pointing, and the second, the up direction. I’ll call these the “camera” vector and the “up” vector. The first step will be to find these two vectors for the camera we want, and the second will be to translate that back into a Camera object.

Getting the position of these vectors for any given camera is a simple application of [rotation matrices](https://en.wikipedia.org/wiki/Rotation_matrix). In the Kamelopard code, there’s a function defined for rotating around each of the three axes. Here’s the example for the X axis; the others are all similar:

```ruby
def self.rot_x(a)
   # Convert the angle to radians
   a = a * Math::PI / 180.0
   return Matrix[[1, 0, 0], [0, Math.cos(a), -1 * Math.sin(a)], [0, Math.sin(a), Math.cos(a)]]
end
```

So we start with a camera pointed at the ground, and we multiply it by a rotation matrix, so that it points in the direction our camera would, before the heading, tilt, and roll rotations are applied. When we perform those rotations, we’ll end up with a vector pointed in the right direction for our camera. This code does just that.

```ruby
# The camera vector is [0,0,1] rotated around the Y axis the amount
# of the camera angle
camera = rot_y(cam_angle) * Vector[0,0,1]

# The up vector is the same for all cameras
up = Vector[0,1,0]
matrix = rot_z(heading) * rot_x(tilt) * rot_z(roll)
(h, t, r) = vector_to_camera(matrix * camera, matrix * up)
```

The last line of this snippet calculates the camera and up vectors, and passes them to the vector_to_camera() function, which takes care of the second step in the process: converting these vectors back into a usable heading, tilt, and roll. Two operations fundamental to linear algebra will become important here. Both take two vectors as input. The [dot product](https://en.wikipedia.org/wiki/Dot_product) returns product of the two vectors’ magnitudes and the cosine of the angle between them. We’ll use it here to find the angle between two vectors. The [cross product](https://en.wikipedia.org/wiki/Cross_product) returns a [normal](https://en.wikipedia.org/wiki/Surface_normal) vector, or a vector which is perpendicular to the two input vectors.

First we want to calculate the heading, which we can find by calculating the angle between two planes. The first plane is defined by the camera vector and the Z axis, and the second is the plane of the Y and Z axes. To find the angle between two planes, we find the angle between their normal vectors. The normal vector of the YZ plane is simply the X axis; the normal vector for hte first plane is the cross product of the camera vector and the Z axis. The dot product lets us find the angle between these two vectors, which is our heading.

Tilt is simply the angle between the camera vector and the original Z axis, but roll is a bit harder. To find it, we transform the original Y axis—​the original “up” vector—​using the heading and tilt calculated previously. We then find the angle between it and the current “up” vector, again using the dot product.

These calculations underlie a simple API, which simply takes a view, for the original camera, the number of the camera we’re interested in getting, and the camera angle or total number of cameras. Like this, for instance:

```ruby
view_hash = {:latitude => otp[:latitude], :longitude => lo,
    :altitudeMode => otp[:altitudeMode], :altitude => otp[:altitude],
    :roll => otp[:roll], :timestamp => Kamelopard::TimeStamp.new('1921-07-29'),
    :heading => otp[:heading], :tilt => otp[:tilt]}
v = Kamelopard::Multicam.get_camera_view(make_view_from(view_hash), camera, nil, CamCount)
```
