---
title: Docker and containers boot camp
author: Phineas Jensen
date: 2022-05-16
tags:
  - docker
  - containers
---

![Shipping containers stacked at a port](/blog/2022/05/container-boot-camp/pexels-samuel-wölfl-1427541.webp)
[Photo by Samuel Wölfl](https://www.pexels.com/photo/intermodal-container-stacked-on-port-1427541/)

In the modern landscape of web development, it’s almost impossible to avoid seeing or using _containers_: programs that are run in isolated, virtualized, user space, making it easy to develop and deploy various components of applications without respect to the specific system and dependencies. If that’s confusing, worry not; this post and the tutorials in this boot camp aim to clarify things for new developers and experienced developers who haven’t gotten around to using containers yet.

> Linux containers are all based on the virtualization, isolation, and resource management mechanisms provided by the Linux kernel, notably Linux namespaces and cgroups.
>
> —Wikipedia, [OS-level virtualization](https://en.wikipedia.org/wiki/OS-level_virtualization)

## Introduction

The terminology surrounding containers can get pretty confusing, but the basic idea is this: a _container_ is just a sandboxed process which is limited by the operating system in its ability to see and interact with other processes and parts of the system. This can provide security benefits (e.g. a container may only be given access to certain parts of the filesystem), help with performance (e.g. by limiting the amount of RAM or CPU given to a container), and help solve version and dependency problems (e.g. containers can be used to run multiple incompatible versions of one program on the same system). Unlike virtual machines, containers are isolated processes on an operating system, while virtual machines virtualize hardware to run an entire operating system including its kernel. Because of this, containers are lighter weight and faster than VMs.

From a developer’s perspective, containers are usually run from _images_, which are special packages of files needed to run a program. For example, a container image might contain the libraries, binaries, and source necessary to run a Node.js app server, while another image might contain everything needed to run PostgreSQL 14.

## Docker

Docker is the most popular container management suite, and you’ll most likely end up using it at some point in your career if you haven’t already. As such, it’s the best place to start learning about containers. Start with the official [getting started](https://docs.docker.com/get-started/) guide published by Docker Inc. which gives a great overview of containers, images, and container composition (i.e. using multiple containers together).

For our own employees, we point out a few things about this tutorial:

- It makes repeated reference to the non-free Docker Desktop tool, which can be useful but shouldn’t take priority in learning. For everything done in Docker Desktop, there are equivalent instructions for the CLI. Make sure to learn those!
- It tells you to create a Docker Hub user for one part where you publish a “getting started” image that you create as part of the tutorial. Everything else is possible without creating an account or publishing an image, so feel free to just read this section without creating an account.

After completing the tutorial, you should be familiar with the basics of creating and orchestrating Docker containers. Of course, there is a lot more to learn and other projects may require much more complicated setup. As you continue to use Docker, keep these reference pages handy:

- [Docker CLI](https://docs.docker.com/engine/reference/commandline/cli/)
- [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
- [compose file specification](https://docs.docker.com/compose/compose-file/)
- [docker-compose CLI](https://docs.docker.com/compose/reference/)

## Container standards and tools

While Docker popularized containers, a number of other tools have since been created for building, managing, and deploying containers, such as:

- [Kubernetes](https://kubernetes.io/) (also called K8s), a system for managing large-scale deployments of containers
- [containerd](https://containerd.io/), a container runtime (but _not_ an image-building tool) which was created for Docker
- [Podman](https://podman.io/), a “daemonless container engine” which provides Docker compatibility as well as support for other systems

These systems are based on open standards such as the [Open Container Initiative](https://github.com/opencontainers)’s image and runtime specifications and the Container Runtime Interface (an API standard for working with containers designed for Kubernetes). If you’re interested in understanding more, see this post on the [differences between these tools and systems](https://www.tutorialworks.com/difference-docker-containerd-runc-crio-oci/).

## End Point’s container expertise

Containers are one of our [areas of expertise](https://www.endpointdev.com/expertise/containers-virtualization/), and we’ve written [a number of blog posts](https://www.endpointdev.com/blog/tags/docker/) about containers. Here are a few highlights:

- [Kubernetes 101: Deploying a web application and database](https://www.endpointdev.com/blog/2022/01/kubernetes-101/) — an excellent, hands-on introduction to Kubernetes which clearly explains core concepts
- [Containerizing Magento with Docker Compose: Elasticsearch, MySQL and Magento](https://www.endpointdev.com/blog/2020/08/containerizing-magento-with-docker-compose-elasticsearch-mysql-and-magento/) - a hands-on guide to using multiple containers to run Magento, a complex full-stack application
- [Linux Development in Windows 10 with Docker and WSL 2](https://www.endpointdev.com/blog/2020/06/linux-development-in-windows-10-docker-wsl-2/) - an intro for Windows developers
- [Creating Composite Docker Containers with Docker Compose](https://www.endpointdev.com/blog/2016/02/creating-composite-docker-containers/) - a more complex, real-world example of docker-compose setup
