---
author: "Jeffry Johar"
title: "Getting started with Docker and Kubernetes on macOS"
github_issue_number: 1875
date: 2022-06-20
tags:
- docker
- kubernetes
- containers
---

<style>
img {
  max-height: 70vh;
}
</style>

![Shipping infrastructure at a dock](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/shipping.webp)

<!-- Photo licensed under CC0 (public domain) from https://pxhere.com/en/photo/1222170 -->

What is the best way to master American English? One school of thought says that the best way to learn a language is to live in the country of the origin. For American English that would be the USA. Why is that so? Because we as the learners get to talk to native speakers daily. By doing this, we get to know how the natives use the language and its grammar in the real world.

The same goes for learning Docker and Kubernetes. The best way to learn Docker and Kubernetes is to get them in our MacBooks, laptops, and PCs. This way we can learn and try locally what works and what doesn’t work in our local host at any time, any day.

Lucky for us earthlings who enjoy GUIs, Docker now has Docker Desktop. As its name suggests, it is nicely built for the desktop. It comes with GUI and CLI to manage our Docker and Kubernetes needs. Please take note of the Docker Desktop license. It is free for personal use, education, and open source projects, and has [a fee for enterprise usage](https://www.docker.com/pricing/). With that out of the way, let's get things started.

### Docker Desktop Installation

The official Docker Desktop for can be found [on Docker's website](https://docs.docker.com/desktop/). It covers installation for macOS, Linux, and Windows. For this post we are going to install Docker Desktop for macOS using Brew. Execute the following command to proceed with the Docker Desktop installation:

```sh
brew install --cask docker
```

![Installing Docker Desktop with Brew](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-01.webp)

Then run it at Finder ➝ Application ➝ Docker.

![Docker in the Finder list of Applications](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-02.webp)

Upon a successful installation, Docker Desktop will appear as the following:

![Screenshot of Docker Desktop](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-03.webp)

Click the Docker icon at the top menu bar to ensure the Docker Desktop is running.

![The Docker icon in the top menu bar of macOS](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-04.webp)

### Run the first containerized application

For the first application we are going to run the latest version of nginx official image from hub.docker.com. Open the terminal and execute the following to run the nginx image as a background service at port 80:

```sh
docker run -d -p 80:80 nginx:latest
```

Run the following command to check on the application. This is the Docker equivalent to the standard `ps` Unix command to list processes.

```sh
docker ps
```

curl the application at localhost port 80:

```sh
curl http://localhost
```

Sample output:

![curl outputting the default nginx HTML](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-05.webp)

### Stop the application

Execute the following command to get the application information and take note of the container ID.

```sh
docker ps
```

Execute the following to stop the application by its container ID. In the following example the container ID is `f7c19b95fcc2`.

```sh
docker stop {container ID}
```

Run `docker ps` again to ensure that the stopped application is not being display as a running application.

Sample Output:

![Docker ps output container list](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-06.webp)

### Enable Kubernetes

Click the Docker icon at the top menu bar and click Preferences:

![The preferences under Docker's menu icon](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-07.webp)

Enable Kubernetes and click Apply and Restart:

![Kubernetes enable button in Docker Desktop preferences](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-08.webp)

Click the Docker icon at the top menu bar and ensure the Kubernetes is running:

![Docker icon menu, now showing that Kubernetes is running](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-09.webp)

Open the terminal and check on the Kubernetes nodes. The status should be `Ready`:

```sh
kubectl get nodes
```

![Docker Desktop node running](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-10.webp)

### Deploy the first application on Kubernetes

We are going to deploy the same official latest nginx images at Kubernetes. Execute the following command:

```sh
kubectl run mynginx --image=nginx:latest
```

Execute the following command to check on the application. Its status should be `Running`. On a slow machine this will take some time and we might need to do this multiple times.

```sh
kubectl get pod
```

Execute the following command to create the Kubernetes service resource for the application. A service in Kubernetes serves as an internal named load balancer.

```sh
kubectl expose pod mynginx --port 80
```

Execute the following command to redirect the localhost network to the Kubernetes network. By doing this we can curl or access the application from `localhost:{port}`. This is a foreground process, so it needs to be left open.

```sh
kubectl port-forward service/mynginx 8080:80
```

Open another terminal to curl localhost:8080 or open the address in a web browser.

```sh
curl http://localhost:8080
```

![Curl showing nginx's default html output](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-11.webp)

In a browser:

![Nginx's default output in a browser](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-12.webp)

### Clean up the Kubernetes resources

Ctrl-C at the port-forwarding process in the terminal and list all the running Kubernetes resources. We should see our application in a pod and its services:

```sh
kubectl get all
```

![kubectl with mynginx pod's age and service highlighted as 21 minutes](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-13.webp)

Now we need to delete these resources.

To delete the service:

```sh
kubectl delete service/mynginx
```

To delete the application:

```sh
kubectl delete pod/mynginx
```

Now list back all resources. The mynginx-related resources should not be displayed.

```sh
kubectl get all
```

![kubectl listing the kubernetes service](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-14.webp)

### To stop Docker Desktop

If we are done with Docker Desktop we can stop its services by going to the top menu bar and selecting the Quit Docker Desktop option. This will stop Docker and Kubernetes services.

![A Quite Docker Desktop button under the Docker icon menu in the top menu bar](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/image-15.webp)

That’s all, folks. We now have the tools to learn and explore Docker and Kubernetes in our own local host.

Now we may proceed with the official documentation and other tutorials to continue on the path to learn Docker and Kubernetes.
