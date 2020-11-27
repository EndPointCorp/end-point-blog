---
author: "Matt Vollrath"
title: "ROS 2 Migration"
tags: ros
gh_issue_number: 1675
---

![Photo of wilderness waterfall (Iris Falls in Yellowstone)](/blog/2020/10/23/ros2-migration/20200821-144901-crop.jpg)

<!-- Photo by Jon Jensen -->

Migrating from ROS 1 to ROS 2 is much more than a “flip of a switch”. The internals of ROS are fundamentally changed, client libraries and their interfaces have been rewritten. The benefits of these changes are significant for users embedding ROS in a product.

Some of these benefits include:

* First-class support for real-time and embedded platforms such as microcontrollers
* Higher reliability under less-than-ideal network conditions
* Distributed, cooperative robotics systems without a single “master”
* More prescribed patterns for building systems with ROS

Because official ROS 1 support ends in 2025, the clock is ticking for all ROS 1 users to migrate their projects to ROS 2. While the amount of work required to port a project scales with its size, codebases of all sizes should have a migration plan.

By carefully approaching your ROS 2 migration, disruption to ongoing development and maintenance of the project can be minimized while maintaining the mission critical reliability required in the robotics domain.

### Dependencies

If your project depends on any of the numerous free open source ROS packages, they will need to be ported to ROS 2. Much progress has been made here, but it is not complete. Converging compatibility of all dependencies can be done in parallel with ongoing development, before making any changes to your own codebase.

### Forward Compatibility

Some ROS interfaces are compatible with both ROS 1 and ROS 2. These are a great place to start, because changes can be tested in your familiar ROS 1 environment with minimal disruption.

ROS 1 packages using older distributions should begin by upgrading to the “noetic” distribution, the final ROS 1 release. This release can be expected to have the most cross-compatibility with ROS 2, including Python 3 and newer package metadata formats.

### Porting the Code

Having done as much as possible in the ROS 1 environment, it’s time to start porting packages to ROS 2. If your project is split into multiple packages or entrypoints, you can leverage a ROS 1/2 compatibility tool to make these changes incrementally and test integration as you go.

Speaking of testing, porting automated tests should happen first. This is a great time to expand test coverage if it is not complete enough to give you confidence in the transition.

### Integration

Having finished all of the porting tasks, you can deploy your complete ROS 2 project to hardware and test it rigorously. When all of the smoke has been released and the bugs shaken off the tree, it’s time to continue building your product. Bring the turtles to the people!

### Further Reading

* The reasons for breaking changes are laid out in [Why ROS 2?](https://design.ros2.org/articles/why_ros2.html)
* The [official ROS 2 migration guide](https://index.ros.org/doc/ros2/Contributing/Migration-Guide/) has many more details about the changes I have outlined.
