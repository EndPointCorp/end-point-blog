---
author: Josh Tolley
title: New Kamelopard version
github_issue_number: 898
tags:
- kamelopard
- liquid-galaxy
- ruby
- open-source
date: 2013-12-16
---

I recently pushed new [Kamelopard](https://github.com/LiquidGalaxy/kamelopard) version (v0.0.14), and thought I should briefly mention it here. This release includes a few bug fixes, including one that fatally affected several v0.0.13 installations, but its major improvement is a greatly expanded test suite. For quite some time many Kamelopard functions have had only placeholder tests, marked as “pending" in the code, or no test at all. In particular, this includes many of the more complex (or in other words, difficult to test) functions. Version 0.0.14 added 35 new tests, including for the frequently used orbit() function as well as for the relatively new multidimensional function logic.

The typical Kamelopard test creates a Kamelopard object, test that it responds to the right set of methods, renders it to KML, and finally inspects the result for correctness. This can quickly become complicated, as some KML objects can take many different forms. Here are a few selections from one of the new tests, as an example. This is for the ColorStyle object, which is an abstract class handling part of the options in other style objects.

This first section indicates that this test includes several other tests, defined elsewhere. Many objects in Kamelopard descend from Kamelopard::Object, for instance, this is far from the only test that refers to its behaviors.

```ruby
shared_examples_for 'Kamelopard::ColorStyle' do
    it_should_behave_like 'Kamelopard::Object'
    it_should_behave_like 'KML_includes_id'
    it_should_behave_like 'KML_producer'
```

The KML spec defines a limited set of “color modes” allowed in a valid ColorStyle object, so we’ll test the code that validates these modes, here.

```ruby
it 'should accept only valid color modes' do
        @o.colorMode = :normal
        @o.colorMode = :random
        begin
            @o.colorMode = :something_wrong
        rescue RuntimeError => f
            q = f.to_s
        end
        q.should =~ /colorMode must be either/
    end
```

KML asks for its color constants in a different order than I’m used to. HTML asks for three byte color constants, with one byte each for red, green, and blue values, in that order. OpenGL’s glColor function variants expect their arguments red first, then green, and then blue, with an optional alpha value at the end. So I sometimes get confused when KML wants alpha values first, then blue, then green, and finally red. Fortunately Kamelopard’s ColorStyle object lets you set color and alpha values independently, and can sort out the proper order for you. This test verifies that behavior.

```ruby
it 'should get settings in the right order' do
        @o.alpha = 'de'
        @o.blue = 'ad'
        @o.green = 'be'
        @o.red = 'ef'
        @o.color.should == 'deadbeef'
    end
```

Finally, this last segment renders the ColorStyle to KML and tests its validity. This particular test uses a helper function called get_obj_child_content(), defined elsewhere, because its particular XML parsing requirements are very common, but many of these tests which require more complex parsing make heavy use of XPath expressions to test the XML documents Kamelopard produces.

```ruby
it 'should do its KML right' do
        color = 'abcdefab'
        colorMode = :random
        @o.color = color
        @o.colorMode = colorMode
        get_obj_child_content(@o, 'color').should == color
        get_obj_child_content(@o, 'colorMode').should == colorMode.to_s
    end
```

This new Kamelopard version also includes the beginnings of what could be a very useful feature. The idea is that Kamelopard objects should be able to create themselves from their KML representation. So, for instance, you could provide some Kamelopard function with a KML file, and it could create a Kamelopard representation which you can then process further. We already support each_placemark(), which iterates through each placemark in a KML document and returns the data therein, but this would expand that ability. Right now we're far from having all Kamelopard objects support parsing themselves from KML, but when it's completed it will open up interesting possibilities. For instance, it was originally conceived as a way to take a pre-existing tour and make a [multicam](/blog/2013/07/kamelopard-update-panoramic-camera) version automatically. This, too, is still some way off.
