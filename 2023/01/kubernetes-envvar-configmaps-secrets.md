---
author: "Jeffry Johar"
title: "Kubernetes environment variables, ConfigMaps and Secrets"
github_issue_number: 1930
featured:
  image_url: /blog/2023/01/kubernetes-envvar-configmaps-secrets/restaurant.webp
description: "This tutorial shows 3 ways to set environment variables for the container in the Kubernetes Pod: hard-coding, ConfigMaps, and Secrets."
tags:
- kubernetes
- containers
date: 2023-01-10
---

![A street style Thai restaurant](/blog/2023/01/kubernetes-envvar-configmaps-secrets/restaurant.webp)<br>
Photo by Jeffry Johar

<!-- https://www.pexels.com/photo/thai-restaurant-14026238/ -->

There are 3 ways to set environment variables for the container in the Kubernetes Pod: hard-coding, ConfigMaps, and Secrets, each with its own use case.

For those who are taking the Certified Kubernetes Administrator exam, you need to know all of these by heart. These skills fall under the domain of workloads and scheduling, which is 15% of the exam. Let's go over how to create the environment variables based on these methods.

### Hard-coding

This is the method that enables us to define the environment variables in the `containers` section of the Pod manifest. When using this method the environment variables will be visible when we describe the Pod. The following is an example of defining the environment variables `PET01=cat` and `PET02=dog` in an nginx container.

As with most Kubernetes resources, there are 2 ways of creating Pods. You can use either one of them. The first way is the imperative way, using the kubectl CLI. This is the preferred method for the CKA exam because it is convenient, fast, and saves time. The second way is the declarative way. Which requires you to build the YAML file and apply it.

#### The imperative

```plain
kubectl run mynginx --image=nginx --env=PET01=cat --env=PET02=dog
```

#### The declarative

This method requires the creation of the YAML and then applying it. Create a 'mynginx.yaml' file in your favorite text editor:

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: mynginx
  name: mynginx
spec:
  containers:
  - env:
    - name: PET01
      value: cat
    - name: PET02
      value: dog
    image: nginx
    name: mynginx
```

Then run:

```plain
kubectl apply -f mynginx.yaml
```

#### The description of the mynginx Pod

Once the Pod is running, we can see the environment variables and their values.

```plain
❯ kubectl describe pod mynginx
Name:             mynginx
Namespace:        default
.
.
.
    Environment:
      PET01:  cat
      PET02:  dog
.
.
.
```

### ConfigMaps

ConfigMaps is a Kubernetes resource used to move away the configuration portions of an application for its main container. Thus it can be used to define environment variables and use them in a Pod's YAML. ConfigMaps can be created either the imperative way or the declarative way. Following are the 2 different ways of creating a ConfigMaps for holding the `PET01=cat` and `PET02=dog` variables.

#### The imperative

```plain
kubectl create configmap myconfigmap --from-literal=PET01=cat --from-literal=PET02=dog
```

#### The declarative

Create the YAML in "myconfigmap.yaml" and apply it:

```yaml
apiVersion: v1
data:
  PET01: cat
  PET02: dog
kind: ConfigMap
metadata:
  name: myconfigmap
```

Then run:

```plain
kubectl apply -f myconfigmap.yaml
```

#### The description of myconfigmap

Take note that the environment variables and their values are visible.

```plain
❯ kubectl describe configmaps myconfigmap
Name:         myconfigmap
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
PET02:
----
dog
PET01:
----
cat

BinaryData
====

Events:  <none>
```

---

After the creation of ConfigMaps, we need to create the Pod’s YAML using the ConfigMaps. There are two ways to use the environment variables from the ConfigMaps: use all of the variables in the ConfigMaps, or selectively choose which which environment variable to use.

#### Using all of the environment variables from ConfigMaps in a Pod

Create "nginx-cm01.yaml":

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-cm01
spec:
  containers:
    - name: nginx-cm01
      image: nginx
      envFrom:
      - configMapRef:
          name: myconfigmap
```

Then run:

```plain
kubectl apply -f nginx-cm01.yaml
```

Here's the description of the `nginx-cm01` Pod:

```plain
❯ kubectl describe pod nginx-cm01
Name:             nginx-cm01
.
.
.    Environment Variables from:
      myconfigmap  ConfigMap  Optional: false
    Environment:   <none>
.
.
.
```

#### Selectively using the environment variables from the ConfigMaps in a Pod

In this example we are selecting both `PET01` and `PET02`.

Create "nginx-cm02.yaml":

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-cm02
spec:
  containers:
    - name: nginx-cm02
      image: nginx
      env:
        - name: PET01
          valueFrom:
            configMapKeyRef:
              name: myconfigmap
              key: PET01
        - name: PET02
          valueFrom:
            configMapKeyRef:
              name: myconfigmap
              key: PET02

```

Then run:

```plain
kubectl apply -f nginx-cm02.yaml
```

Here's the description of the `nginx-cm02` Pod:

```plain
❯ kubectl describe pod nginx-cm02
Name:             nginx-cm02
.
.
.
    Environment:
      PET01:  <set to the key 'PET01' of config map 'myconfigmap'>  Optional: false
      PET02:  <set to the key 'PET02' of config map 'myconfigmap'>  Optional: false
.
.
```

### Secrets

Secrets are just like ConfigMaps except their values are hidden when you describe them. Please note that the values in Secrets are not encrypted, just encoded with base64. Anybody with cluster admin privileges can get the values and decode them. Following are the imperative and declarative ways of creating Secrets for holding the `PET01=cat` and `PET02=dog` variables.

#### The imperative

```plain
kubectl create secret generic mysecret --from-literal=PET01=cat --from-literal=PET02=dog
```

#### The declarative

For the declarative Secrets YAML we need to encode the values to base64.

```plain
❯ echo -n "cat" | base64
Y2F0
❯ echo -n "dog" | base64
ZG9n
```

Then put the encoded values in the YAML file "mysecret.yaml".

```yaml
apiVersion: v1
data:
  PET01: Y2F0
  PET02: ZG9n
kind: Secret
metadata:
    name: mysecret

```

Then run:

```plain
kubectl apply -f mysecret.yaml
```

#### The description of mysecret

Note that the environment variable values are hidden.

```
❯ kubectl describe secrets mysecret
Name:         mysecret
Namespace:    default
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
PET02:  3 bytes
PET01:  3 bytes
```

---

Just like ConfigMaps, we can use all of the environment variables or selectively choose the desired variables.

#### Using all of the environment variables from the Secrets

Create "nginx-s01.yaml":

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-s01
spec:
  containers:
    - name: nginx-s01
      image: nginx
      envFrom:
      - secretRef:
          name: mysecret
```

And run:

```plain
kubectl apply -f nginx-s01.yaml
```

The description of `nginx-s01`:

```plain
❯ kubectl  describe pod nginx-s01
Name:             nginx-s01
.
.
.
    Environment Variables from:
      mysecret    Secret  Optional: false
    Environment:  <none>
.
.
```

#### Selectively using the environment variables from the Secrets

Create "nginx-s02.yaml":

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-s02
spec:
  containers:
    - name: nginx-s02
      image: nginx
      env:
        - name: PET01
          valueFrom:
            secretKeyRef:
              name: mysecret
              key: PET01
        - name: PET02
          valueFrom:
            secretKeyRef:
              name: mysecret
              key: PET02
```

Then run:

```plain
kubectl apply -f nginx-s02.yaml
```

The description of "nginx-s02.yaml":

```plain
❯ k describe pod nginx-s02
.
.
.
    Environment:
      PET01:  <set to the key 'PET01' in secret 'mysecret'>  Optional: false
      PET02:  <set to the key 'PET02' in secret 'mysecret'>  Optional: false
    Mounts:
.
.

```

### Conclusion

That's all, folks. I hope you understand how to get the environment variables in Kubernetes Pods. Good luck for those who are taking the CKA exam. Have a nice day!
