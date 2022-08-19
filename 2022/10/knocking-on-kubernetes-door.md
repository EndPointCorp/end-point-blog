---
author: "Jeffry Johar"
title: "Knocking on Kubernetes's Door (Ingress)"
github_issue_number: 1910
date: 2022-10-20
tags:
- kubernetes
- docker
- containers
description: "An overview of Kubernetes Ingress: what it is, and how to set it up."
featured:
  image_url: /blog/2022/10/knocking-on-kubernetes-door/blog06-alhambra.webp
---

![The door of Alhambra Palace, Spain. A still pool reflects grand doors, flanked on each side by arches and hedges.](/blog/2022/10/knocking-on-kubernetes-door/blog06-alhambra.webp)<br>
Photo by Alberto Capparelli

According to the Merriam-Webster dictionary, the meaning of ingress is the act of entering or entrance. In the context of Kubernetes, Ingress is a resource that enables clients or users to access the services which reside in a Kubernetes cluster. Thus Ingress is the entrance to a Kubernetes cluster! Let’s get to know more about it and test it out.

### Prerequisites

We are going to deploy Nginx Ingress at Kubernetes on Docker Desktop. Thus the following are the requirements:

- Docker Desktop with Kubernetes enabled. If you are not sure how to do this, please [refer to my previous blog on Docker Desktop and Kubernetes](/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/).
- Internet access to download the required YAML and Docker Images.
- Git command to clone a git repository.
- A decent editor such as Vim or Notepad++ to view and edit the YAML.

### Ingress and friends

To understand why we need Ingress, we need to know 2 other resources and their shortcomings in exposing Kubernetes services. Those 2 resources are NodePort and LoadBalancer. Then we will go over the details of Ingress.

#### NodePort

NodePort is a type of Kubernetes service which exposes the Kubernetes application at high-numbered ports. By default the range is from 30000–32767. Each of the worker nodes proxies the port. Thus, access to the service is by using the Kubernetes worker node IPs and the ports. In the following example the NodePort service is exposed at port 30000.

![A diagram of a Kubernetes Cluster. Within are 3 boxes, labeled as worker nodes, with the IP addresses: 192.168.1.1, 192.168.1.2, and 192.168.1.3. Each box contains several purple boxes labeled "Service Type: NodePort at port 30001". They point to three blue boxes labeled "Pods". Each worker node box points to a URL corresponding to its IP address: "http://192.168.1.1:30000" and so forth, with port 30000 for each.](/blog/2022/10/knocking-on-kubernetes-door/blog06-nodeport.webp)

To have a single universal access and a secured SSL connection, we need some external load balancer in front of the Kubernetes cluster to do the SSL termination and to load balance the exposed IPs and ports from the worker nodes. This is illustrated in the following diagram:

![The same diagram as above, but this time all three IP address have arrows pointing bidirectionally to a single circle, labeled Load Balancer + SSL Termination. This circle points to a single URL, "https://someurl.com".](/blog/2022/10/knocking-on-kubernetes-door/blog06-nodeport-lb.webp)

#### LoadBalancer

LoadBalancer is another type of Kubernetes service which exposes Kubernetes services. Generally it is an OSI layer 4 load balancer which exposes static IP. The implementation of LoadBalancer depends on the Cloud or the Infrastructure provider. Thus the capability of LoadBalancer varies. In the following example LoadBalancer is exposed with the static public IP (13.215.159.65) provided by a Cloud provider. The IP could also be registered to a DNS to be resolved to a domain name.

![A similar Kubernetes Cluster box, again with three boxes containing three blue Pods each, but this time every pod points to the same single box, encompassed only by the outer Kubernetes Cluster box. It is labeled "Service Type: LoadBalancer; Static IP: 13.215.159.65". The outer box points to a URL: "http://13.215.159.65", which in turn points to "http://someurl.com".](/blog/2022/10/knocking-on-kubernetes-door/blog06-loadbalancer.webp)

#### Ingress

Ingress is a Kubernetes resource that serves as an OSI layer 7 load balancer. Unlike NodePort and LoadBalancer, Ingress is not a Kubernetes service. It is another Kubernetes resource that sits in front of a Kubernetes service. It enables routing, SSL termination and virtual hosting. This is like a full fledged load balancer inside the Kubernetes cluster! The following diagram shows that Ingress is able to route the `someurl.com/web/` and `someurl.com/app/` endpoints to the intended applications in the Kubernetes cluster, able to terminate SSL certificates, do virtual hosting and route the URL to the intended destination. Please take note that as of this writing, Ingress only supports http and https protocol.

![An outer Kubernetes Cluster box contains three boxes again. Each box again has three Pods, but they are split into three colors (green, yellow, and red), distributed randomly through the three boxes. The three Pods of each color point to a matching box, in the larger Kubernetes Cluster box, reading "Service Type: ClusterIP; Name: X", where X is Web, App, and Blog. These three boxes point to another box labeled "Ingress: SSL Termination; Routing; Virtual Hosting. This box points to a URL, "http://13.215.159.65", which in turn points to a cloud icon with three URLS: "https://someurl.com/web/", "https://someurl.com/app/", "https://someurl.com"](/blog/2022/10/knocking-on-kubernetes-door/blog06-ingress-controller.webp)

In order to get Ingress in a Kubernetes cluster we need to deploy 2 main things:

- **Ingress Controller** is the engine of the Ingress. It is responsible for providing the Ingress capability to Kubernetes. The Ingress Controller is a separate module from Kubernetes core components. There are multiple Ingress Controllers available to be use such as Nginx Ingress Controller, Istio Ingress Controller, NSX Ingress Controller and many more. The get a complete list of supported Ingress Controller go to this [kubernetes.io page on Ingress controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/).
- **Ingress Resource** is the configuration that manages the Ingress. It is made by applying the Ingress Resource YAML. This is a typical YAML file for Kubernetes resources which requires apiVersion, kind, metadata and spec. Go to [kubernetes.io documentation on Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) to know more of this YAML.

### How to deploy and use Ingress

Now we are going to deploy the Nginx Ingress at Kubernetes in Docker Desktop. We will configure it to access an Nginx web server, a variant for Tomcat web application server and our old beloved Apache web server.

Start your Docker Desktop with Kubernetes Enable. Right click at the Docker Desktop icon at the top left area to see that both Docker and Kubernetes are running:

![Docker Desktop running on MacOS, with macOS's top bar Docker menu open. There are two green dots next to lines saying "Docker Desktop is running" and "Kubernetes is running".](/blog/2022/10/knocking-on-kubernetes-door/blog06-docker-desktop.webp)

Clone my repository to get the required deployments YAML files:

```plain
git clone https://github.com/aburayyanjeffry/nginx-ingress.git
```

Let’s go through the downloaded files.

- `01-ingress-controller.yaml` : This is the main deployment YAML for the Ingress controller. It will create a new namespace named “ingress-nginx”. Then it will create the required service account, role, rolebinding, clusterrole, clusterolebinding, service, configmap and deployments in the “ingress-nginx” namespace. The origin of this YAML is from the official ingress-nginx documentation. To learn more about this deployment go to https://kubernetes.github.io/ingress-nginx/deploy/#quick-start
- `02-nginx-webserver.yaml`, `03-tomcat-webappserver.yaml`, `04-httpd-webserver.yaml`: These are the deployment YAML files for the sample applications. They are the typical Kubernetes deployments which contain the services and deployments.
- `05-ingress-resouce.yaml` : This is the configuration of the Ingress. It is using the test domain `*.localdev.me`. This is a domain that is available in most modern operating systems. It can be used for testing without the need to edit the `/etc/hosts` file. Ingress is configured to route as the following diagram:

![An icon of several people points to three URLS: "http://demo.localdev.me", "http://demo.localdev.me/tomcat/", and "http://httpd.localdev.me". These three point through an Nginx Ingress box to three logos: Nginx, Tomcat, and Apache, respectively. The Nginx Ingress box and the logos all lie within a larger Kubernetes Cluster box.](/blog/2022/10/knocking-on-kubernetes-door/blog06-ingress.webp)

Deploy the Ingress Controller. Execute the following to deploy the Ingress Controller:

```plain
kubectl apply -f 01-ingress-controller.yaml
```

Execute the following to check on the deployment. The pod must be running and the Deployment must be ready:

```plain
kubectl get all -n ingress-nginx
```

![The results of the above command. Highlighted is a line giving the following values: name: "pod/ingress-nginx-controller-6bf7bc7f94-gfgdw"; ready: "1/1"; status: "Running"; restarts: "0"; age: "21s". Two sections down, another line is highlighted, with the values: name: "deployment.apps/ingress-nginx-controller"; ready: "1/1"; up-to-date: "1"; available: "1"; age: "21s"](/blog/2022/10/knocking-on-kubernetes-door/blog06-kubectl-ns-ing.webp)

Deploy the sample applications. Execute the following to deploy the sample applications:

```plain
kubectl apply -f 02-nginx-webserver.yaml
kubectl apply -f 03-tomcat-webappserver.yaml
kubectl apply -f 04-httpd-webserver.yaml
```

Execute the following to check on the deployments. All pods must be running and all deployments must be ready:

```plain
kubectl get all
```

![The output of the above command. Highlighted are lines from a table with the following values for name: "pod/myhttpd-xxxxxx", "pod/mynginx-xxxxxx", and "pod/mytomcat-xxxxxx". They share values for ready, status, restarts, and age: "1/1", "Running", "0", and "13s", respectively. A later section is highlighted. The names are: "deployment.apps/myhttpd", "deployment.apps/mynginx", and "deployment.apps/mytomcat". They share values for ready, up-to-date, available, and age: "1/1", "1", "1", and "13s", respectively.](/blog/2022/10/knocking-on-kubernetes-door/blog06-kubectl-ns.webp)

Deploy the Ingress resources. Execute the following to deploy the Ingress resouces:

```plain
kubectl apply -f 05-ingress-resouce.yaml
```

Execute the following to check on the Ingress resources:

```plain
kubectl get ing
```

![The outpu of the above command. The table only includes one line, with the following values: name: "myingress"; class: "nginx"; hosts: "demo.localdev.me,httpd.localdev.me", address: blank; ports: "80"; age: "3s"](/blog/2022/10/knocking-on-kubernetes-door/blog06-kubectl-ing.webp)

Access the following URLs in your web browser. All URLs should bring you to the intended services:

```plain
http://demo.localdev.me
http://demo.localdev.me/tomcat/
http://httpd.localdev.me
```

![Three browser windows displaying the above URLs. They display welcome pages for Nginx, Tomcat, and Apache, respectively.](/blog/2022/10/knocking-on-kubernetes-door/blog06-apps.webp)

### Conclusion

That's all, folks. We have gone over the what, why, and how about the Kubernetes Ingress. It is a powerful OSI layer 7 load balancer ready to be used with the Kubernetes cluster. There are free and open source solutions and there are also the paid ones. They are all listed here: https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/.
