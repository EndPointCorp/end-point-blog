---
author: Ron Phipps
title: Kubernetes Volume definition defaults to EmptyDir type with wrong capitalization of hostPath
date: 2022-10-26
github_issue_number: 1913
featured:
  image_url: /blog/2022/10/kubernetes-volume-definition-defaults-emptydir-type-wrong-capitalization-hostpath/20220411_112819.webp
tags:
- kubernetes
- docker
description: Kubernetes gives no warning of an invalid volume type and quietly defaults to EmptyDir!
---

![Cow with light red-brown fur and an inventory ear tag standing in a dry field with scattered desert grass and brush, in front of a fench](/blog/2022/10/kubernetes-volume-definition-defaults-emptydir-type-wrong-capitalization-hostpath/20220411_112819.webp)
Photo by Garrett Skinner

Kubernetes Host Path volume mounts allow accessing a host system directory inside of a pod, which is helpful when doing development, for example to access the frequently-changing source code of an application being actively developed. This allows a developer to edit the code with their normal set of tools without having to jump through a bunch of hoops to get the code into a pod.

We use this setup at End Point in development where the host system is running MicroK8s and there is a single pod for an application on a single node. In most other cases, host path volume mounts are not recommended. But here it means the developer can edit code on the host machine and the changes are immediately reflected within the pod without having to deploy a new image. If the application server running within the pod is also running in development mode with dynamic reloading, the changes can be viewed with a refresh of the browser accessing the application.

While working on a test environment to run EpiTrax within Kubernetes, the need arose to set up a Host Path volume mount so that the source code on the host machine would be available within the pod. I used this simple Deployment definition:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: epitrax
  namespace: app
  labels:
    app: epitrax
spec:
  template:
    spec:
      securityContext:
        fsGroup: $USERID
      containers:
      - name: shell
        image: epitrax/epitrax
        command: ["sh", "-c", "tail -f /dev/null"]
        securityContext:
          runAsNonRoot: true
          runAsUser: $USERID
          runAsGroup: $USERID
        volumeMounts:
      - mountPath: /opt/jboss/epitrax
          name: epitrax-source-directory
      volumes:
      - name: epitrax-source-directory
        hostpath:
          type: Directory
          path: $PWD/projects/epitrax
```

After applying this deployment and shelling into the pod I found that `/opt/jboss/epitrax` was an empty directory and not a host path volume. Describing the pod showed the following:

```yaml
Volumes:
  epitrax-source-directory:
    Type:       EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:
    SizeLimit:  <unset>
```

I tried changing many different things, viewed the various logs, and searched the Internet for reports of the same problem, but could not figure out what was wrong.

Eventually I found [a single GitHub issue on the Kubernetes project](https://github.com/kubernetes/kubernetes/issues/46950), which did not explain the trouble but did explain that the volume type always defaults to EmptyDir to match Docker’s behavior.

That’s when I realized the problem: I had used `hostpath` (all lower case) instead of `hostPath`. Kubernetes could not find a valid volume type of `hostpath` so it defaulted to `EmptyDir`.

Updating the volumes section to the following resolved the issue:

```yaml
# snip
      volumes:
      - name: epitrax-source-directory
        hostPath:
          type: Directory
          path: $PWD/projects/epitrax
```

Be aware that Kubernetes will not warn or error out if there is an invalid volume type referenced in the volumes section—it will quietly default to EmptyDir!
