---
author: "Jeffry Johar"
title: "Kubernetes Form The Ground Up With AWS EC2"
date: 2022-08-30
tags:
- kubernetes
- docker
- containers
- kubeadm
- aws
---

![The ship](/blog/2022/08/kubernetes-form-the-ground-up-with-aws-ec2/ship.webp)<br>
Photo by Darry Lin

One way to learn Kubernetes infrastructure is to build it from scratch. This  way of learning was introduced by the founding father of Kubernetes itself; Mr. [Kelsey Hightower](https://twitter.com/kelseyhightower?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor). The lesson  is known as “Kubernetes The Hard Way”. It is available [here](https://github.com/kelseyhightower/kubernetes-the-hard-way).
For this blog entry I would like to have a less demanding approach than Kubernetes The Hard Way but yet educational. I would like to highlight only the major steps in creating a Kubernetes cluster and what is covered in [CKA ( Certified Kubernetes Administrator)](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/) exams. Thus we are going to use the `kubeadm` tools to build the Kubernetes cluster. The steps of creating a Kubernetes cluster are hidden to you if you are using  a Kubernetes as a service such as  AWS EKS, GCP GKE or the enterprise suites of Kubernetes such as Red Hat Openshift or VMware Tanzu.  All of these products just let you use the Kubernetes without the need to worry about creating it. 

### Prerequisites

For this tutorial we will need the following from AWS:

- An active AWS account.
- EC2 instances with Amazon Linux 2 as the OS.
- AWS Keys for SSH to access control node and managed nodes.
- Security group which allows SSH and HTTP.
- A decent editor such as Vim or Notepad++ to create the inventory and the playbook.

### EC2 Instances provisioning

Provisioning of the The Control Plain a.k.a The Master Node 

1. Go to AWS Console → EC2 → Launch Instances.
2. Set the Name tag to `Master`
3. Select the Amazon Linux 2 AMI.
4. Select a key pair. If there are no available key pairs, please create one according to Amazon’s instructions.
5. Allow SSH and 6443
6. Set Number of Instances to 1
7. Click Launch Instance.

Provisioning of the Worker Nodes a.k.a The Minions

1. Go to AWS Console → EC2 → Launch Instances.
2. Set the Name tag to `Node`
3. Select the Amazon Linux 2 AMI.
4. Select a key pair. If there are no available key pairs, please create one according to Amazon’s instructions.
5. Allow SSH
6. Set Number of Instances to 2
7. Click Launch Instance.

### Installing the Container Runtime Engine
All Kubernetes nodes required some sort of container runtime engine. For these nodes we are going to use Docker as the container runtime engine. Login to all EC2 instances and execute the following: 

1. Docker installation
```plain
sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo usermod -a -G docker ec2-user
sudo service docker start
sudo systemctl enable docker.service
sudo su - ec2-user
```

2. Verify the Docker Installation
```plain
docker ps
```

We should get an empty Docker status as the following
```plain
docker ps
CONTAINER ID   IMAGE          COMMAND                  CREATED       STATUS      PORTS                    NAMES
```

3. Tc (Traffic Controller) installation . This is required by the kubeadm tool. 
```plain
sudo yum install tc -y 
```

### Kubernetes Control Plane Setup 

1. Add the Kubernetes repository.  Login to the node and paste the following

```plain
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
enabled=1
gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
EOF
```

2. Install the Kubernetes binaries for Control Plane ( kubelet,kubeadm,kubectl) and enable it. 
```plain
sudo yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
sudo systemctl enable --now kubelet
```

3. Initiate the Control Plane. The –ingore-preflight-errors switch is required because we are using a system which has less than 2 CPU and 2 GB. The –pod-network-cidr value is the default value for the Flannel ( Networking Addon) 
```plain
sudo kubeadm init --ignore-preflight-errors=NumCPU,Mem --pod-network-cidr=10.244.0.0/16
```

There are 3 important points from the above output. They are the successful note on the cluster initalization, the kubeconfig setup and the worker node joining string. The following is a sample output:
![kubeadm init](/blog/2022/08/kubernetes-form-the-ground-up-with-aws-ec2/kubeadm01.webp)<br>

4. Create the configuration file for kubectl a.k.a kubeconfig to connect to the Kubernetes cluster. The scripts are from previous output
```plain
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

5. Install the  pod network add-on. We are going to use Flannel
```plain
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
```


### Kubernetes Worker Nodes Setup 
Execute the following in all worker nodes :

1. Add the Kubernetes repository.  Login to the node and paste the following
```plain
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
enabled=1
gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm
EOF
```

2. Install the Kubernetes binaries for worker nodes ( kubelet,kubeadm) and enable it. 
```plain
sudo yum install -y kubelet kubeadm --disableexcludes=kubernetes
sudo systemctl enable --now kubelet
```

2. Execute the join command with `sudo`. This command is from step #3 in the Kubernetes Control Plane Setup section.
![kubectl get nodes](/blog/2022/08/kubernetes-form-the-ground-up-with-aws-ec2/kubeadm-join.webp)<br>
### Hello Kubernetes :) 
We have successfully created a Kubernetes cluster. Let’s check on the cluster and try to deploy some sample applications. 

1. Get the latest status of the nodes. You might need to wait for 1 minutes ++ to get all nodes to be `Ready`. 
```plain
kubectl get nodes
```

Sample output:
![kubectl get nodes](/blog/2022/08/kubernetes-form-the-ground-up-with-aws-ec2/kubeadm02.webp)<br>

2. Deploy a sample Nginx webserver
```plain
kubectl create deployment mynginx --image=nginx
```

3. Scale the Deployment to have 6 replicas and check on where the pods run. The pods should be assigned randomly to the available worker nodes. 
```plain
kubectl scale --replicas=6   deployment/mynginx
kubectl get pods -o wide 
```

Sample output:
![kubectl get pods](/blog/2022/08/kubernetes-form-the-ground-up-with-aws-ec2/kubeadm03.webp)<br>
### Conclusion
That's all folks . I hope this blog entry has shed some insights on what it takes to create a Kubernetes cluster. Have a nice day :) 


