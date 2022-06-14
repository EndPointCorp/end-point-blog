---
author: "Jeffry Johar"
title: "Getting started with Docker and Kubernetes on MacOS"
date: 2022-06-13
tags:
- docker
- kubernetes
---

![Shipping infrastructure at a dock](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/shipping.webp)

Photo from [PxHere](https://pxhere.com/en/photo/1222170)


What is the best way to master American English? One school of thought says that the best way to learn a language is to live in the country of the origin. Thus, for American English that would be the USA. Why is that so? This is because we as the learners get to talk to the native speakers daily. By doing this, we get to know how the natives utilize the language and its grammar in the real world. 

The same goes for learning Docker and Kubernetes. The best way to learn Docker and Kubernetes is to get them in our Macbooks, laptops or PCs. By this way we can learn and try locally what works and what doesn’t work in our local host at any time, any day.

Lucky for us the earthlings Docker came out with Docker Desktop. As its name suggests, it is nicely built for the desktop. It came with GUI and CLI to manage our Docker and Kubernetes needs. Please take note of the Docker Desktop license. It is free for personal use, education, open source projects and has a fee for enterprise usage. You can check it out at https://www.docker.com/pricing/. Thus said, let's get things started.

### Docker Desktop Installation

The official Docker Desktop for can be found here https://docs.docker.com/desktop/ . It covers installation for macOS, Linux and Windows. For this blog we are going to install Docker Desktop for macOS by using Brew. Execute the following command to proceed with the Docker Desktop installation. 

```sh
brew install --cask docker
```

![](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-01.webp)

Then go to Finder->Application->Docker

![](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-02.webp)

Upon a successful installation, the Docker Desktop will appear as the following:

![](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-03.webp)

Click the Docker icon at the top menu bar to ensure the Docker Desktop is running:

![](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-04.webp)

### Run the first containerized application 

For the first application we are going to run the latest version of nginx official image from hub.docker.com. Open the terminal and execute the following to run the nginx image as a background service at port 80:

```sh
docker run -d -p 80:80 nginx:latest
```

Run the following command to check on the application. This is the equivalent to “ps -ef” on Linux OS.

```sh
docker ps
```

curl the application at localhost port 80:

```sh
curl http://localhost
```

Sample output:

![](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-05.webp)

### Stop the application

Execute the following command to get the application information and take note of the CONTAINER ID

```sh
docker ps
```

Execute the following to stop the application by its CONTAINER ID. In the following example the CONTAINER ID = f7c19b95fcc2

```sh
docker stop {container ID}
```

Run `docker ps` again to ensure that the stopped application is not being display as a running application.

Sample Output:

![](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-06.webp)

### Enable Kubernetes

Click the Docker icon at the top menu bar and click Preferences

![](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-07.webp)

Enable Kubernetes and Apply and Restart

![](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-08.webp)

Click the Docker icon at the top menu bar and ensure the Kubernetes is running

![](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-09.webp)

Open the terminal and check on the Kubernetes nodes. The status should be `Ready`:

```sh
kubectl get nodes
```

![](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-10.webp)

### Deploy the first application on Kubernetes

We are going to deploy the same official latest nginx images at Kubernetes. Execute the following commands:

```sh
kubectl run mynginx --image=nginx:latest
```

Execute the following commands to check on the application. Its status should be running. On a slow machine this will take some time and we might need to do this multiple times. 

```sh
kubectl get pod
```

Execute the following command to create the Kubernetes service resource for the application. A service in Kubernetes servers as an internal named load balancer. 

```sh
kubectl expose pod mynginx --port 80
```

Execute the following command to redirect the local host network to the Kubernetes network. By doing this we can curl or access the application form the localhost:port . This is a foreground process thus needing to be left open.

```sh
kubectl port-forward service/mynginx 8080:80
```

Open another terminal to curl localhost:8080 or open the address in a web browser

```sh
curl http://localhost:8080
```

![](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-11.webp)

In a browser:

![](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-12.webp)

### Clean up the Kubernetes resources

Ctrl-C at the port-forwarding terminal and list all the running Kubernetes resources. We should see our application in a pod and its services:

```
kubectl get all
```

![](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-13.webp)

Now we need to delete these resources

To delete the service

```sh
kubectl delete service/mynginx
```

To delete the application 

```sh
kubectl delete pod/mynginx
```

Now list back all resources. The mynginx related resources should not be displayed. 

```sh
kubectl get all
```

![](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-14.webp)

### To stop Docker Desktop

If we are done with Docker Desktop we can stop its services by going to the top menu bar and selecting the Quit Docker Desktop option. This will stop Docker and Kubernetes services

![](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-15.webp)

That’s all, folks. We now have the tools to learn and explore Docker and Kubernetes in our own local host. Now we may proceed with the official documentations and other tutorials to continue our journey in the path to learn Docker and Kubernetes.
