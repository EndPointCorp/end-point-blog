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

You should see a "microk8s is running" message along with some specifications on your cluster. Including the available add-ons, which ones are enabled and which ones are disabled. 

You can also shutdown your cluster anytime with `microk8s stop`. Use `microk8s start` to bring it back up.

## Introducing kubectl

microk8s also comes with [kubectl](https://kubectl.docs.kubernetes.io/guides/introduction/kubectl/). This is our gateway into Kubernetes, as this is the command line tool that we use to interact with it. By default, microk8s makes it so we can call it using `microk8s kubectl ...`. That is, namespaced. This is useful if you have multiple Kubernetes implementations running at the same time, or another, separate kubectl. I don't, so I like to create an alias for it, so that I can call it without having to use the `microk8s` prefix. You can do it like so:

```
$ sudo snap alias microk8s.kubectl kubectl
```

Now that all that's done, we can start talking to our Kubernetes cluster. We can ask it for example to tell us which are the nodes in the cluster with this command:

```
$ kubectl get nodes
```

That will result in something like:

```
NAME     STATUS   ROLES    AGE   VERSION
pop-os   Ready    <none>   67d   v1.21.4-3+e5758f73ed2a04
```

The only node in the cluster is your own machine. In my case, my machine is called "pop-os" so that's what shows up. Yout can get more information out of this commant by using `kubectl get nodes -o wide`.

## Installing add-ons

microk8s supports many add-ons that we can use to enhance our Kubernetes installation. We are going to need a few of them so let's install them now. They are:

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

Those are all the add-ons that we'll use.

## Introducing the Dashboard

The dashboard is one we can play with right now. In order to access it, first run this:

```
$ microk8s dashboard-proxy
```

That will start up a proxy that will allow is access into the dashboard. The command will give you an URL and login token that you can use to access the dashboard. It results in an output like this:

```
Checking if Dashboard is running.
Dashboard will be available at https://127.0.0.1:10443
Use the following token to login:
<YOUR LOGIN TOKEN>
```

Now you can navigate to that URL in your browser and you'll find a screen like this:

![Dashboard login](kubernetes/dashboard-login.png)

Make sure the "Token" option is selected, and take the login token generated by the `microk8s dashboard-proxy` command from before and paste it in the field in the page. Click the "Sign In" button and you'll be able to see the dashboard, allowing you access to many aspects of your cluster. It should look like this:

![Dashboard home](kubernetes/dashboard-home.png)

Feel free to play around with it a little bit. You don't have to understand everything yet though. As we work though our example, we'll see how the dashboard and the other add-ons come into play.

# Deploying applications into a Kubernetes cluster

With all that setup out of the way, we can start using our k8s cluster for what it was designed: running applications.

## Deployments

Pods are very much the stars of the show when it comes to Kubernetes. However, most of the time we don't create them directly. We usually do so through "[deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)". Deployments are a more abstract concept in Kubernetes. They basically control pods and make sure they behave as specified. You can think of them as wrappers for pods which make our lives easier than if we had to handle pods directly. Let's go ahead and create a deployment, that way things will be clearer.

In kubernetes, there are various ways of managing objects like deployments. For this post, I'm going to focus exclusively on the configuration-file-driven declarative approach as that's the one better suited for real world scenarios.

> You can learn more about the different ways of interacting with kubernetes objects in [the official documentation](https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/).

So, simply put, if we want to create a deployment then we need to author a file that defines it. A simple deployment specification looks like this:

```yml
# nginx-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

> This example is taken straight from [the official documentation](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).

Don't worry if most of that doesn't make sense at this point. I'll explain it into detail later. First, lets actually do something with it.

Save that in a new file. You can call it `nginx-deployment.yaml`. Once that's done, you can actually create the deployment (and its associated objects) in your k8s cluster with this command:

```
$ kubectl apply -f nginx-deployment.yaml
```

Which should result in the following message:

```
deployment.apps/nginx-deployment created
```

And that's it for creating deployments! (Or any other type of object in kubernetes for that matter). We define the object in a file and then invoke `kubectl`'s `apply` command. Pretty simple.

> If you want to delete the deployment, then this command will do it:
>
> ```
> $ kubectl delete -f nginx-deployment.yaml 
> deployment.apps "nginx-deployment" deleted
> ```

## Using kubectl to explore a deployment

Now, let's inspect our cluster to see what this command has done for us.

First, we can ask it directly for the deployment with:

```
$ kubectl get deployments
```

Which outputs:

```
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   3/3     3            3           2m54s
```

As you can see, the deployment that we just created is right there with the name that we gave it.

Like I said, deployments are used to manage pods, and that's just what the `READY`, `UP-TO-DATE` and `AVAILABLE` columns allude to with those values of `3`. This deployment has three pods because, in our yaml file, we specified we wanted three replicas with the `replicas: 3` line. Each "replica" is a pod. For our example, that means that we will have three instances of nginx running side by side.

We can see the pods that have been created for us with this command:

```
$ kubectl get pods
```

Which gives us something like this:

```
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-66b6c48dd5-fs5rq   1/1     Running   0          55m
nginx-deployment-66b6c48dd5-xmnl2   1/1     Running   0          55m
nginx-deployment-66b6c48dd5-sfzxm   1/1     Running   0          55m
```

The exact names will vary, as the ids are autogenerated. But as you can see, this command gives us some basic information about our pods. Remember that pods are the ones that actually run our workloads via containers. The `READY` field is particularly insteresting in this sense then because it tells us hoy many containers are running in the pods vs how many are supposed to run. So, `1/1` means that the pod has one container ready out of 1. In other words, the pod is fully ready.

## Using the dashboard to explore a deployment

Like I said before, the dashboard offers us a window into our cluster. Let's see how we can use it to see the information that we just saw via `kubectl`. Navigate into the dashboard via your browser and you should now see that some new things have appeared:

![Dashboard home with deployment](kubernetes/dahsboard-home-with-deployment.png)

We now have new "CPU Usage" and "Memory Usage" sections that give us insight into the utilization of our machine's resources.

There's also "Workload status" that has some nice graphs giving us a glance at the status of our deployments, pods and [replica sets](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/).

> Don't worry too much about replica sets right now, as we seldom interact with them directly. Suffice it to say, replica sets are objects that deployments rely on to make sure that the number of specified replica pods is maintained. As always, there's more info in [the official documentation](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/).

Scroll down a little bit more and you'll find the "Deployments" and "Pods" sections, which contain the inforamtion that we've already seen via `kubectl` before.

![Dashboard home: deployments and pods](kubernetes/dashboard-home-deployments-and-pods.png)

Feel free to click around and explore the capabilities of the dashboard.

## Dissecting the deployment configuration file

Now that we have a basic understanding of deployments and pods, and how to create them. Let's look more closely into the configuration file that defines it. This is what we had:

```yml
# nginx-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

This example is very simple, but it touches on the key aspects of deployment configuration. We will be building more complex deployments as we work through this article, but this is a great start. Let's start at the top:

- `apiVersion`: Under the hood, a kubernetes cluster exposes its functionality via a REST API. We seldom interact with this API directly because we have `kubectl` that takes care of it for us. `kubectl` takes our commands, translates them into HTTP requests that the k8s REST API can understand, sends them, and gives us back the results. So, this `apiVersion` field specifies which version of the k8s REST API are we expecting to talk to.
- `kind`: It represents the type of object that the configuration file defines. All objects in kubernetes can be managed via yml configuration files and `kubectl apply`. So, this field specifies which one we are managing at any given time.
- `metadata.name`: Quite simply, the name of the object. It's how we and kubernetes refers to it.
- `metadata.labels`: These help us further categorize cluster objects. These have no real effect in the system so they are useful for user help more than anything else.
- `spec`: This contains the actual functional specification for the behavior of the deployment. More details below.
- `spec.replicas`: The number of replica pods that the deployment should create. We already talked a bit about this before.
- `spec.selector.labels`: This is one case when labels are actually important. Remember that when we create deployments, replica sets and pods are created with it. Within the k8s cluster, they each are their own individual objects though. This field is the mechanism that k8s uses to associate a given deployment with its replica set and pods. In practice, that means that whatever labels are in this field need to match the labels in `spec.template.metadata.labels`. More on that one below.
- `spec.template`: Specifies the configuration of the pods that will be part of the deployment.
- `spec.template.metadata.labels`: Very similar to `metadata.labels`. The only difference is that those labels are added to the deployment; while these ones are added to the pods. The only notable thing is that these labels are key for the deplopyment to know which pods it should care about. As explained in above.
- `spec.template.spec`: This section specifies the actual functional configuration of the pods.
- `spec.template.spec.container`: This section specifies the configuration of the containers that will be running inside the pods. It's an array so there can be many. In our example we have only one.
- `spec.template.spec.container[0].name`: The name of the container.
- `spec.template.spec.container[0].image`: The image that will be used to build the container.
- `spec.template.spec.container[0].ports[0].containerPort`: A port through which the contianer will accept traffic from the outside. In this case, `80`.

> You can find a detailed description of all the fields supported by deployment configuration files [in the official API reference documentation](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.22/#deployment-v1-apps). And much more!

## Connecting to the containers in the pods

Kubernetes allows us to connect to the containers running inside pods. This is pretty easy to do with `kubectl`. All we need to know the name of the pod and the container that we want to connect to. If the pod is running only one container (like our nginx one does), then we don't need the container name. We can find out the names of our pods with:

```
$ kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-66b6c48dd5-85nwq   1/1     Running   0          25s
nginx-deployment-66b6c48dd5-x5b4x   1/1     Running   0          25s
nginx-deployment-66b6c48dd5-wvkhc   1/1     Running   0          25s
```

Pick one of those, and we can open a bash session in it with:

```
$ kubectl exec -it nginx-deployment-66b6c48dd5-85nwq -- bash
```

Which results in a prompt like this:

```
root@nginx-deployment-66b6c48dd5-85nwq:/# 
```

We're now connected to the continer in one of our nginx pods. There isn't a lot to do with this right now, but feel free to explore it. It's got its own processes and file system which are isolated from the other replica pods and your actual machine.

We can also connect to containers via the dashboard. Go back to the dashboard in your browser, log in again if the session expired, and scroll down to the "Pods" section. Each pod in the list has an action menu with an "Exec" command. See it here:

![Dashboard pod exec](kubernetes/dashboard-pod-exec.png)

Click it, and you'll be taken to a screen with a console just like the one we obtained via `kubectl exec`:

![Dashboard pod bash](kubernetes/dashboard-pod-bash.png)

The dashboard is quite useful, right?

## Services

So far, we've learned quite a bit about deployments. How to specify and create them, how to explore them via command line and the dashboard, how to interact with the pods, etc. We haven't seen a very important part yet though: Actually accessing the application that has been deployed. That's where [services](https://kubernetes.io/docs/concepts/services-networking/service/) come in. We use services to expose an application running in a set of pods to the world outside the cluster.

Here's what a configuration file for a service that exposes access to our nginx deployment could look like:

```yml
# nginx-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
    - name: "http"
      port: 80
      targetPort: 80
      nodePort: 30080
```

Same as with the deployment's configuration file, this one also has a `kind` field that specifies what it is; and a name given to it via the `metadata.name` field. The `spec` section is where things get interesting.

- `spec.type` specifies, well... The type of the service. Kubernetes supports many [types of services](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types). For now, we want a `NodePort`. This type of service makes sure to expose itself as a static port (given by `spec.ports[0].nodePort`) on every node in the cluster. In our set up, we only have one node, which is our own machine.
- `spec.ports` defines which ports of the pods' containers will the service expose.
- `spec.ports[0].name`: The name of the port. To be used elsewhere to reference the specific port.
- `spec.ports[0].port`: The port that will be exposed by the service.
- `spec.ports[0].targetPort`: The port that the service will target in the container.
- `spec.ports[0].nodePort`: The port that the service will expose in all the nodes of the cluster.

Same as with deployments, we can create such a service with the `kubectl apply` command. If you save the contents from the YAML above into a `nginx-service.yaml` file, you can run the following to create it:

```
$ kubectl apply -f nginx-service.yaml
```

And to inspect it and validate that it was in fact created:

```
$ kubectl get services
NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes      ClusterIP   10.152.183.1    <none>        443/TCP        68d
nginx-service   NodePort    10.152.183.22   <none>        80:30080/TCP   27s
```

The dashboard also has a section for services. It looks like this:

![Dashboard: services](kubernetes/dashboard-services.png)

## Accessing an application via a service

We can access our service in a few different ways. We can use its "cluster IP" which we obtain from the output of the `kubectl get services` command. As given by the example above, that would be `10.152.183.22` in my case. Browsing to that IP gives us the familiar nginx default welcome page:

![NGINX via Cluster IP](kubernetes/nginx-via-cluster-ip.png)

Another way is by using the "NodePort". Remember that the "NodePort" specifies the port in which the service will be available on every node of the cluster. With our current microk8s setup, our own machine is a node in the cluster. So, we can also access the nginx that's running in our kubernetes cluster using `localhost:30080`. `30080` is given by the `spec.ports[0].nodePort` field in the service configuration file from before. Try it out:

![NGINX via NdoePort](kubernetes/nginx-via-nodeport.png)

How cool is that? We have identical, replicated NGINX instances running in a kubernetes cluster that's installed locally in our machine.

# Building up our own custom application

Alright, by deploying NGINX, we've learned a lot about nodes, pods, deployments, services and how they all work together to run and serve an application from a kubernetes cluster. Now, let's take all that knowledge and try and do the same for a completely custom application of our own.

## Deploying a database

# Persistent volumes and claims




# What are we building


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
