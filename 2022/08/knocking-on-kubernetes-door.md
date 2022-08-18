---
author: "Jeffry Johar"
title: "Knocking on Kubernetes's Door (Ingress)"
date: 2022-08-18
tags:
- kubernetes
- ingress
- containers
---

![The door of Alhambra Palace, Spain](/blog/2022/08/knocking-on-kubernetes-door/blog06-alhambra.webp)<br>
Photo by Alberto Capparelli

According to the Merriam-Webster dictionary, the meaning of ingress is the act of entering or entrance. In the context of Kubernetes, Ingress is a resource that enables clients or users to access the services which reside in a Kubernetes cluster . Thus Ingress is the entrance or the door to a Kubernetes cluster!!! Let’s get to know more about it and test it out. 

### Prerequisites

We are going to deploy Nginx Ingress at Kubernetes on Docker Desktop. Thus the following are the requirements:

- Docker Desktop with Kubernetes enabled. If you are not sure how to do this, please [refer to my previous blog on Docker Desktop and Kubernetes.](https://www.endpointdev.com/blog/2022/06/getting-started-with-docker-and-kubernetes-on-macos/)
- Internet access to download the required YAML and Docker Images
- Git command to clone a git repository.
- A decent editor such as Vim or Notepad++ to view and edit the YAML

### Ingress and friends. 
To understand why we need Ingress, we need to know the other 2 other resources and their shortcomings in exposing Kubernetes services.The 2 resources are NodePort and LoadBalancer. Then we will go over the details of Ingress. 

1. NodePort<br>
NodePort is a type of Kubernetes Service which exposes the Kubernetes service at high numbered ports. By default the range is in between 30000-32767. Each of the worker nodes proxies the port. Thus, access to the service is by using the Kubernetes worker node IPs and the ports. In the following example the NodePort service is exposed at port 30000. 

![NodePort](/blog/2022/08/knocking-on-kubernetes-door/blog06-nodeport.webp)<br>

To have a single universal access and a secured SSL connection, we need some external load balancer in front of the Kubernetes cluster to do the SSL termination and to load balance the exposed IPs and ports from the worker nodes. This is illustrated in the following diagram: 

![NodePort with LB](/blog/2022/08/knocking-on-kubernetes-door/blog06-nodeport-lb.webp)<br>

2. LoadBalancer<br>
LoadBalancer is another type of Kubernetes Service which exposes Kubernetes services. Generally it is a OSI layer 4 load balancer which exposes static IP. The implementation of LoadBalancer depends on the Cloud or the Infrastructure provider. Thus the capability of LoadBalancer varies!.  In the following example LoadBalancer is exposed with the static public IP (13.215.159.65)  provided by a Cloud provider. The IP could also be registered to a DNS to be resolved to a domain name. 

![NodePort with LB](/blog/2022/08/knocking-on-kubernetes-door/blog06-loadbalancer.webp)<br>

3. Ingress<br>
Ingress is a Kubernetes resource that serves as OSI layer 7 load balancer. Unlike NodePort and LoadBalancer, Ingress is not a  Kubernetes service. It is another Kubernetes resource that sit in front of a Kubernetes service. It enables routing, SSL termination and virtual hosting. This is like a full fledged load balancer inside the Kubernetes cluster!! . The following diagram shows that ingress is able to route the someurl.com/web/ and someurl.com/app/ endpoints to the intended applications in the Kubernetes cluster, able to terminate SSL certificates and able to do virtual hosting and route the url to the intended destination. `Please take note that as of this writing, Ingress only support http and https protocol`. 

![Ingress](/blog/2022/08/knocking-on-kubernetes-door/blog06-ingress-controller.webp)<br>

In order to get Ingress in a Kubernetes cluster we need to deploy 2 main things

- `Ingress Controller` is the engine of the Ingress. It is responsible for providing the Ingress capability to Kubernetes. The Ingress Controller is a separate module from Kubernetes core components. There are multiple Ingress Controllers available to be use such as Nginx Ingress Controller, Istio Ingress Controller, NSX Ingress Controller and many more. The get a complete list of supported Ingress Controller go to this [kubernetes.io page on Ingress controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/).

- `Ingress Resource` is the configuration that manages the Ingress. It is made by applying the Ingress Resource YAML. This is a typical YAML file for Kubernetes resources which requires apiVersion, kind, metadata and spec. Go to [kubernetes.io documentation on Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) to know more of this YAML.

### How to deploy and use Ingress 

Now we are going to deploy the Nginx Ingress at Kubernetes in Docker Desktop . We will configure it to access a Nginx webserver,  a variant for Tomcat web application server and our old beloved Apache webserver. 


1. Start your Docker Desktop with Kubernetes Enable. Right click at the Docker Desktop icon at the top left area to see that both Docker and Kubernetes are running
 
![Docker Desktop](/blog/2022/08/knocking-on-kubernetes-door/blog06-docker-desktop.webp)<br>


2. Clone my repository to get the required deployments YAML
```plain
git clone https://github.com/aburayyanjeffry/nginx-ingress.git
```

3. Let’s go through the downloaded YAMLs . Go to the cloned directory and open the YAMLs with your favorite editor.

- `01-ingress-controller.yaml` : This is the main deployment YAML  for the ingress controller. It will create a new namespace named “ingress-nginx”. Then it will create the required service account, role, rolebinding, clusterrole, clusterolebinding, service, configmap and deployments in the “ingress-nginx” namespace. The origin of this YAML is from the nginx-ingress official documentation. To learn more about this deployment go here https://kubernetes.github.io/ingress-nginx/deploy/#quick-start

- `02-nginx-webserver.yaml, 03-tomcat-webappserver.yaml, 04-httpd-webserver.yaml` : These are the deployment YAMLs for the sample applications. They are the  typical Kubernetes deployments which contain the services and deployments.

- `05-ingress-resouce.yaml` : This is the configuration of the Ingress. It is using the test domain *.localdev.me. This is a domain that is available in most modern Operating systems. It can be used for testing without the need to edit the /etc/hosts. The Ingress is configured to route as the following diagram:


![Docker Desktop](/blog/2022/08/knocking-on-kubernetes-door/blog06-ingress.webp)<br>

4. Deploy the Ingress Controller
Execute the following to deploy the Ingress Controller
```plain
kubectl apply -f 01-ingress-controller.yaml
```

Execute the following to check on the deployment. The pod must be running and the Deployment must be ready
```plain
kubectl get all -n ingress-nginx
```
![ingress-nginx ns](/blog/2022/08/knocking-on-kubernetes-door/blog06-kubectl-ns-ing.webp)<br>

5. Deploy the sample applications

Execute the following to deploy the sample applications
```plain
kubectl apply -f 02-nginx-webserver.yaml
kubectl apply -f 03-tomcat-webappserver.yaml
kubectl apply -f 04-httpd-webserver.yaml
```

Execute the following to check on the deployments.All pods must be running and all deployments must be ready
```plain
kubectl get all 
```
![default ns](/blog/2022/08/knocking-on-kubernetes-door/blog06-kubectl-ns.webp)<br>

6. Deploy the Ingress resources

Execute the following to deploy the Ingress resouces
```plain
kubectl apply -f 05-ingress-resouce.yaml
```


Execute the following to check on the Ingress resources
```plain
kubectl get ing
```
![default ns ing](/blog/2022/08/knocking-on-kubernetes-door/blog06-kubectl-ing.webp)<br>

7. Access the following URL at your Web browser. All URL should bring to the intended services

http://demo.localdev.me 

http://demo.localdev.me/tomcat/ 

http://httpd.localdev.me

![apps](/blog/2022/08/knocking-on-kubernetes-door/blog06-apps.webp)<br>

### Conclusion

That's all folks . We have gone over the what, why and how about the Kubernetes Ingress. It is a powerful OSI layer 7 load balancer ready to be used with the Kubernetes cluster. There are free and open source solutions and there are also the paid ones. They are all listed here https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/.

