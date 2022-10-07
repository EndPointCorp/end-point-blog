---
author: "Jeffry Johar"
title: "Kubernetes From The Ground Up With AWS EC2"
date: 2022-10-06
github_issue_number: 1898
tags:
- kubernetes
- docker
- containers
- aws
- devops
---

![A docked fishing ship faces the camera. A man stands on a dinghy next to it.](/blog/2022/10/kubernetes-from-the-ground-up-with-aws-ec2/ship.webp)<br>
Photo by Darry Lin <!-- https://www.pexels.com/@darrylin/ -->

One way to learn Kubernetes infrastructure is to build it from scratch. This way of learning was introduced by the founding father of Kubernetes himself: [Mr. Kelsey Hightower](https://twitter.com/kelseyhightower). The lesson is known as [“Kubernetes The Hard Way”](https://github.com/kelseyhightower/kubernetes-the-hard-way).

For this blog entry I would like to take a less demanding approach than Kubernetes The Hard Way, while still being educational. I would like to highlight only the major steps in creating a Kubernetes cluster and what is covered in [CKA (Certified Kubernetes Administrator) exams](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/). Thus we are going to use the `kubeadm` tools to build the Kubernetes cluster.

The steps of creating a Kubernetes cluster are hidden to you if you are using a Kubernetes as a service such as AWS EKS, GCP GKE or the enterprise suites of Kubernetes such as Red Hat Openshift or VMware Tanzu. All of these products let you use Kubernetes without the need to worry about creating it.

### Prerequisites

For this tutorial we will need the following from AWS:

- An active AWS account
- EC2 instances with Amazon Linux 2 as the OS
- AWS Keys for SSH to access control node and managed nodes
- Security group which allows SSH and HTTP
- A decent editor such as Vim or Notepad++ to create the inventory and the playbook

### EC2 Instances provisioning

Provisioning of the the control plane, a.k.a. the master node:

1. Go to AWS Console → EC2 → Launch Instances.
2. Set the Name tag to `Master`.
3. Select the Amazon Linux 2 AMI.
4. Select a key pair. If there are no available key pairs, please create one according to Amazon’s instructions.
5. Allow SSH and 6443 TCP ports.
6. Set Number of Instances to 1.
7. Click Launch Instance.

Provisioning of the worker nodes, a.k.a. the minions:

1. Go to AWS Console → EC2 → Launch Instances.
2. Set the Name tag to `Node`.
3. Select the Amazon Linux 2 AMI.
4. Select a key pair. If there are no available key pairs, please create one according to Amazon’s instructions.
5. Allow SSH TCP port.
6. Set Number of Instances to 2.
7. Click Launch Instance.

### Installing the container runtime

All Kubernetes nodes require some sort of container runtime engine. For these nodes we are going to use Docker. Log in to all EC2 instances and execute the following:

1. Install Docker.

    ```plain
    sudo yum update -y
    sudo amazon-linux-extras install docker -y
    sudo usermod -a -G docker ec2-user
    sudo service docker start
    sudo systemctl enable docker.service
    sudo su - ec2-user
    ```

2. Verify the Docker installation.

    ```plain
    docker ps
    ```

    We should get an empty Docker status:

    ```plain
    CONTAINER ID   IMAGE          COMMAND                  CREATED       STATUS      PORTS                    NAMES
    ```

3. Install TC (Traffic Controller). This is required by the kubeadm tool.

    ```plain
    sudo yum install tc -y
    ```

### Kubernetes control plane setup

1. Add the Kubernetes repository. Log in to the node and paste the following:

    ```plain
    cat <<'EOF' | sudo tee /etc/yum.repos.d/kubernetes.repo
    [kubernetes]
    name=Kubernetes
    baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-$basearch
    enabled=1
    gpgcheck=1
    gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
    exclude=kubelet kubeadm kubectl
    EOF
    ```

2. Install the Kubernetes binaries for Control Plane (`kubelet`, `kubeadm`, `kubectl`) and enable it.

    ```plain
    sudo yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
    sudo systemctl enable --now kubelet
    ```

3. Initiate the Control Plane. The `--ignore-preflight-errors` switch is required because we are using a system which has fewer than 2 CPUs and less than 2 GB of RAM. The `--pod-network-cidr` value is the default value for flannel (a networking add-on).

    ```plain
    sudo kubeadm init --ignore-preflight-errors=NumCPU,Mem --pod-network-cidr=10.244.0.0/16
    ```

    There are 3 important points from the output of this command. They are the successful note on the cluster initalization, the kubeconfig setup and the worker node joining string. The following is a sample output:

    ![The output of kubeadm, with the three important points highlighted. They read: 1: "Your Kubernetes control-lane as been initialized successfully!", 2: "mkdir -p $HOME/.kube;
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config;
sudo chown $(id -u):$(id -g) $HOME/.kube/config", 3: "kubeadm join 172.XX.XX.XX:6643 --token XXXX --discover-token-ca-cert-hash XX"](/blog/2022/10/kubernetes-from-the-ground-up-with-aws-ec2/kubeadm01.webp)

4. Create the configuration file for kubectl a.k.a. kubeconfig to connect to the Kubernetes cluster. The scripts are from previous output:

    ```plain
    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config
    ```

5. Install the pod network add-on. We are going to use [flannel](https://github.com/flannel-io/flannel).

    ```plain
    kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
    ```

### Kubernetes worker nodes setup

Execute the following in all worker nodes:

1. Add the Kubernetes repository. Log in to the node and paste the following

    ```plain
    cat <<'EOF' | sudo tee /etc/yum.repos.d/kubernetes.repo
    [kubernetes]
    name=Kubernetes
    baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-$basearch
    enabled=1
    gpgcheck=1
    gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
    exclude=kubelet kubeadm
    EOF
    ```

2. Install the Kubernetes binaries for worker nodes (kubelet, kubeadm) and enable kubelet.

    ```plain
    sudo yum install -y kubelet kubeadm --disableexcludes=kubernetes
    sudo systemctl enable --now kubelet
    ```

2. Execute the join command with `sudo`. This command is from step #3 in the Kubernetes Control Plane Setup section.

    ![A command and its results: sudo kubeadm join 172.XX.XX.XX:6443 --token XXXX --discovery-token-ca-cert-hash sha256:4XXX](/blog/2022/10/kubernetes-from-the-ground-up-with-aws-ec2/kubeadm-join.webp)

### Hello, Kubernetes :)

We have successfully created a Kubernetes cluster. Let’s check on the cluster and try to deploy some sample applications.

1. Get the latest status of the nodes. You might need to wait a minute or more for all nodes to become `Ready`.

```plain
kubectl get nodes
```

Sample output:

![Results of the kubectl get nodes. 3 nodes appear, each with the Ready status.](/blog/2022/10/kubernetes-from-the-ground-up-with-aws-ec2/kubeadm02.webp)

2. Deploy a sample Nginx web server

```plain
kubectl create deployment mynginx --image=nginx
```

3. Scale the Deployment to have 6 replicas and check on where the pods run. The pods should be assigned randomly to the available worker nodes.

```plain
kubectl scale --replicas=6 deployment/mynginx
kubectl get pods -o wide
```

Sample output:

![Results of the kubectl get nodes and kubectl get pods. The two worker nodes are highlighted, pointing to their coinciding output from the command "kubectl get pods -o wide".](/blog/2022/10/kubernetes-from-the-ground-up-with-aws-ec2/kubeadm03.webp)

### Conclusion

That's all, folks. I hope this blog entry has shed some insights on what it takes to create a Kubernetes cluster. Have a nice day :)
