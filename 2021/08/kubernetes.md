---
author: "Kevin Campusano"
title: "Kubernetes 101: Deploying a web application and database"
tags:
- kubernetes
- kustomize
- docker
- dotnet
- postgres
---

![A market at night](kubernetes/market-cropped.jpg)
[Photo](https://unsplash.com/photos/cpbWNtkKoiU) by [Sam Beasley](https://unsplash.com/@sam_beasley)

The devops world seems to have been taken over by [Kubernetes](https://kubernetes.io/) during the past few years. And rightfully so, I believe, as it is a great piece of software that promises and delivers when it comes to managing deployments of complex systems.

Kubernetes is hard though. But it's all good, I'm not a devops engineer. As a software developer, I shouldn't care about any of that. Or should I? Well... Yes. I know that very well after being thrown head first into a project that heavily involves Kubernetes, without knowing the first thing about it.

Even if I wasn't in the role of a devops engineer, as a software developer, I had to work with it in order to set up dev environments, troubleshoot system issues, and make sound design and architectural decisions.

So, after a healthy amount of struggle, I eventually gained some understanding on the subject. In this blog post I'll share those learnings. My hope is to put out there the things I wish I knew when I first encountered and had to work with k8s. So, I'm going to introduce the basic concepts and building blocks of Kubernetes. Then, I'm going to walk you through the process of containerizing a sample application, developing all the Kubernetes configuration files necesary for deploying it into a Kubernetes cluster, and actually deploying it into a local development cluster. We will end up with an application and its associated database running completely on and being managed by Kubernetes.

In short: if you know nothing about Kubernetes, and are interested in learning, read on. This post is for you.

# What is Kubernetes?

Simply put, Kubernetes is software for managing [computer clusters](https://en.wikipedia.org/wiki/Computer_cluster). That is, groups of computers that are working together in order to process some workload or offer a service. Kubernetes does this by leveraging [application containers](https://www.docker.com/resources/what-container). Kubernetes will help you out in [automating the deployment, scaling and management of containerized aplications](https://kubernetes.io/).

Once you've designed an application's complete execution environment and associated components, using Kubernetes you can specify all that declaratively via configuration files. Then, you'll be able to deploy that application with a single command. Once deployed, Kubernetes will give you tools to check on the health of your application, recover from issues, keep it running, scale it, etc.

There are a few basic concepts that we need to be familiar with in order to effectively work with Kubernetes. I think the [official documentation](https://kubernetes.io/docs/concepts/) does a great job in explaining this, but I'll try to summarize.

## Nodes, pods and containers

First up is "[containers](https://kubernetes.io/docs/concepts/containers/)". If you're interested in Kubernetes, chances are that you've already been exposed to some sort of container technology like [Docker](https://www.docker.com/). If not, no worries. For our purposes here, we can think of containers as an isolated process, with its own resources and file system, in which an application can run.

A container has all the software dependencies that an application needs to run, including the application itself. From the application's perspective, the container is its execution environment: the "machine" in which it's running. In more practical terms, a container is a form of packaging, delivering and executing an application. The advantage is that, instead of installing the application and its dependencies directly into the machine that's going to run it; having it containerized allows for a container runtime (like Docker) to just run it as a self-contained unit. This makes it possible for the application to be able to run anywhere that has the container runtime installed, with minimal configuration.

Something very related to containers is the concept of [images](https://kubernetes.io/docs/concepts/containers/images/). You can think of images as basically the blueprint for containers. An image is the spec, and the container is the instance that's actually running.

When deploying applications into Kubernetes, this is how it runs them: via containers. In other words, for Kubernetes to be able to run an application, it needs to be delivered to it within a container.

Next is the concept of a "[node](https://kubernetes.io/docs/concepts/architecture/)". This is very straightforward and not even specific to Kubernetes. A node is a computer within the cluster. That's it. Like I said before, Kubernetes is built to manage computer clusters. A "node" is just one computer, either virtual or physical, within that cluster.

Then there's "[pods](https://kubernetes.io/docs/concepts/workloads/pods/)". Pods are the main executable units in Kubernetes. When we deploy an application or service into a Kubernetes cluster, it runs within a pod. Kubernetes works with containerized applications though, so it is the pods that take care of running said containers within them.

These three work very closely together within Kubernetes. To sumarize: containers run within pods which in turn exist within nodes in the cluster.

There are other key components to talk about like [deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), [services](https://kubernetes.io/docs/concepts/services-networking/service/), [replica sets](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/) and [persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/). But I think that's enough theory for now. We'll learn more about all these as we get our hands dirty working though our example. So let's get started with our demo and we'll be discovering and discusing them organically as we go through it.

# Installing and setting up Kubernetes

The first thing we need is a Kubernetes environment. There are many Kubernetes implementations out there. [Google](https://cloud.google.com/kubernetes-engine), [Microsoft](https://azure.microsoft.com/en-us/services/kubernetes-service/) and [Amazon](https://aws.amazon.com/eks) offer so-called managed Kubernetes solutions on their respective cloud platforms, for example. There are also implementations that one can install and run on their own, like [kind](https://kind.sigs.k8s.io/docs/), [minikube](https://minikube.sigs.k8s.io/docs/) and [microk8s](https://microk8s.io/). We are going to use microk8s for our demo. For no particular reason other than "this is the one I know".

When done installing, microk8s will have set up a whole Kubernetes cluster, with your machine as its one and only node.

## Installing microk8s

So, if you're in Ubuntu and have [snapd](https://snapcraft.io/docs/installing-snapd), installing microk8s is easy. The [official documentation](https://microk8s.io/docs) explains it best. You install it with a command like this:

```
$ sudo snap install microk8s --classic --channel=1.21
```

microk8s will create a user group which is best to add your user account to in order to execute commands that would otherwise require admin priviledges. You can do so with:

```
$ sudo usermod -a -G microk8s $USER
$ sudo chown -f -R $USER ~/.kube
```

With that, our very own Kubernetes cluster, courtesy of microk8s, should be ready to go. Check its status with:

```
$ microk8s status --wait-ready
```

You can also shutdown your cluster anytime with `microk8s stop`. Use `microk8s start` to bring it back up.

## Introducing kubectl

microk8s also comes with [kubectl](https://kubectl.docs.kubernetes.io/guides/introduction/kubectl/). This is our gateway into Kubernetes, as this is the command line tool that we use to interact with it. By default, microk8s makes it so we can call it using `microk8s kubectl ...`. That is, namespaced. This is useful if you have multiple Kubernetes implementations running at the same time, or another, separate kubectl. I don't, so I like to create an alias for it, so that I can call it without having to use the `microk8s` prefix. You can do it like so:

```
sudo snap alias microk8s.kubectl kubectl
```

Now that all that's done, we can start talking to our Kubernetes cluster. We can ask it for example to tell us which are the nodes in the cluster with this command:

```
kubectl get nodes
```

That will result in:

<!-- PUT THE OUTPUT HERE -->

Notice how the only node in the cluster is your own machine.

## Installing add-ons

microk8s supports many add-ons that we can use to enhance our Kubernetes installation. We are going to need a few of them so let's install them now. We're going to need:

1. The [dashboard](https://microk8s.io/docs/addon-dashboard), which gives us a nice web GUI which serves as a window into our cluster. In there we can see all that's running, see logs, run commands, etc.
2. [dns](https://microk8s.io/docs/addon-dns), which sets up DNS for within the cluster. In general it's a good idea to enable this one because other add-ons use it.
3. storage, which allows the cluster to access the host machine's disk for storage. The application that we will deploy needs a persistent database so we need that plugin to make it happen.
4. registry, which sets up a [container image](https://kubernetes.io/docs/concepts/containers/images/) registry that Kubernetes can access. Like I said, Kubernetes runs containerized applications. Containers are based on images. So, having this add-on allows us to define an image for our application and make it available to Kubernetes.

To install these, just run the following commands:

```
$ microk8s enable dashboard
$ microk8s enable dns
$ microk8s enable storage
$ microk8s enable registry
```

That's all the add-ons that we're going to need.

The dashboard is one we can play with right now. You can start it up using:

```
$ microk8s dashboard-proxy
```

That will result in an output like this:

<!-- PUT OUTPUT HERE -->

With this information, you can go into your browser and see the app:

<!-- PUT DASHBOARD PICTURE HERE -->

As we work though our example, we'll see how the dashboard and the other add-ons come into play.

# Deployments and services

Pods are very much the stars of the show when it comes to Kubernetes. However, most of the time we don't create them directly. We usually do so through "[deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)". Deployments are a more abstract concept in Kubernetes. They basically control pods and make sure they behave as specified. You can think of them as wrappers for pods which make our lives easier than if we had to handle pods directly. Let's go ahead and create a deployment, that way things will be clearer.







# Persistent volumes and claims

# YAML configuration files and Kustomize

# Installing and setting up microk8s

# Enabling microk8s addons

# Exploring the dashboard

# What are we building

# Deploying the database

# Building the web application image

# Making the image accessible to the cluster

# Deploying the web application

# Exposing the components as services

# Putting it all together with Kustomize

Config maps and vars

# Bonus: Using the cluster as a development environment with Visual Studio Code

# Creating variants for a production and development environments

# Building the prod web application image

# Building a deployment for the web application for prod

patches
