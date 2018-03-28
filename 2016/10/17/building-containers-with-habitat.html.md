---
author: Kirk Harr
gh_issue_number: 1262
tags: chef, containers, devops
title: 'Building Containers with Habitat'
---

### Many Containers, Many Build Systems

When working with modern container systems like Docker, Kubernetes, and Mesosphere, each provide methods for building your applications into their containers. However each build process is specific to that container system, and using similar applications across tiers of container environments would require maintaining each container’s build environment. When approaching this problem for multiple container environments, Chef Software created a tool to unify these build systems and create container-agnostic builds which could be exported into any of the containers. This tool is called [Habitat](https://www.habitat.sh/) which also provide some pre-built images to get applications started quickly.

I recently attended a Habitat Hack event locally in Portland (Oregon) which helped me get more familiar with the system and its capabilities. We worked together in teams to take a deeper dive into various aspects of how Habitat works, you can read about our adventures over on the [Chef blog](https://blog.chef.io/2016/09/09/habitat-hack-pdx-wrap/).

To examine how the various parts of the build environment work, I picked an example Node.js application from the Habitat Documentation to build and customize.

### Node.js Application into a Docker Container

For the most basic Habitat build, you must define a plan.sh file which will contain all the build process logic as well as all configuration values to define the application. Within my Node.js example, this file contains this content:

```nohighlight
pkg_origin=daehlie
pkg_name=mytutorialapp
pkg_version=0.3.0
pkg_maintainer="Kirk Harr <kharr@endpoint.com>"
pkg_license=()
pkg_source=https://s3-us-west-2.amazonaws.com/${pkg_name}/${pkg_name}-${pkg_version}.tar.gz
pkg_shasum=e4e988d9216775a4efa4f4304595d7ff31bdc0276d5b7198ad6166e13630aaa9
pkg_filename=${pkg_name}-${pkg_version}.tar.gz
pkg_deps=(core/node)
pkg_expose=(8080)

do_build() {
  npm install
}

do_install() {
  cp package.json ${pkg_prefix}
  cp server.js ${pkg_prefix}

  mkdir -p ${pkg_prefix}/node_modules/
  cp -vr node_modules/* ${pkg_prefix}/node_modules/
}
```

Within this is defined all the application details like the name of the author, the version of the application being packaged, as well as the package name. Each package can be defined with a license for the code in use as well as any code dependencies, like the Node.js application server (core/node), as well as the repository URL for locating these files. There are also two executable statements which build the package dependencies, and perform final installation setup during the eventual package installation.

Additionally to define this application we must provide the logic for how to start the Node application server, and provide configuration on what ports to listen on as well as the message to be displayed once it has started. To do so we must create a stub Node.js config.json which provides the port and message values:

```nohighlight
{
    "message": "Hello, World",
    "port": "8080"
}
```

We also need two hooks which will be executed at package install time and at runtime for the application respectively. These are named, init and run in our case, with init setting up the symbolic links to the various Node.js components from the core/node package which will be included in the build, and run provides the entry point for the applications flow effectively starting the npm application server. Just like with a Dockerfile, any additional logic needed during the process would be included in these two hooks, depending on if the logic was specific to install time or run time.

### Injected Configuration Values

 In this example, both the message to be displayed to the user, as well as the port that the Node.js application server will listen on are hard-coded into our build, and all the images that resulted from it would be identical. In order to allow for some customizing of the resulting image, you can replace the hard-coded values in the Node.js config.json into variables which can be replaced during the build process:

```nohighlight
{
    "message": "{{cfg.message}}",
    "port": "{{cfg.port}}"
}
```

To complete the replacement, we would provide a “Tom’s Obvious, Minimal Language” (.toml) file with has a key-value pair for each of these configuration variables we want to set. This .toml file will be interpreted during each build to populate these values, creating an opportunity to customize our builds by injecting specific values into the variables defined in the application configuration. Here is an example of the syntax from this example:

```nohighlight
# Message of the Day
message = "Hello, World of Habitat"

# The port number that is listening for requests.
port = 8080
```

### Conclusions

Habitat seeks to fill in the gaps between the various container formats for Docker, Kubernetes and others, by allowing common build infrastructure and dependency libraries to be unified in distribution. By utilizing the same build infrastructure, it becomes more feasible to have a hybrid environment with various container formats in use, without creating duplicate build infrastructure which basically performs the same task slightly differently right at the end to package the application into the proper container format. Habitat helps to decouple the actual build process and all that plumbing, from the process of exporting the build image into the proper format for whatever container is in use. In that way as new container formats are developed, all that is required to accommodate them is expanding the export function for that new format, without any changes to the overall build process or customization of your code.
