---
author: "Kannan Ponnusamy"
date: 2025-02-25
title: "Testing Ansible Automation with Molecule"
github_issue_number: 2095
featured:
  image_url: /blog/2025/02/case-of-the-mistimed-script/clock-tower.webp
description: "How to - Ansible role testing with Molecule and Docker, including setup, scenario creation, and GitLab CI/CD integration for automated, reliable automation testing"
tags:
- sysadmin
- linux
- CI/CD
- cloud
- devops
---

![A low-angle view of an old European church clock tower. The square tower with rounded corners is ornamented with gothic styling, and topped with a golden eagle.](/blog/2025/02/case-of-the-mistimed-script/clock-tower.webp)

![photo of optical disc drive.](/blog/2025/02/testing-ansible-with-molecule/photo-of-optical-disc-drive.jpg)<br>
[Photo](https://unsplash.com/photos/photo-of-optical-disc-drive-1iVKwElWrPA) by [Patrick Lindenberg](https://unsplash.com/@heapdump)


# Testing Ansible Automation with Molecule

## 1. Introduction: Why Test with Molecule?
- **What is Molecule?**  
    - Molecule project is designed to aid in the development and testing of Ansible roles.
    - Molecule provides support for testing with multiple instances, operating systems and distributions, virtualization providers, test frameworks and testing scenarios.

- **Why It Matters**  
  - Increases confidence in your automation and ensures roles are reliable.
  - Catches issues early in the development cycle, reducing production problems.
  - Ensures consistency across different environments and platforms.

## 2. Install Prerequisites
  - Make sure you have Python >= 3.6 and pip installed.
  - Install Ansible and Molecule using pip:
  ```bash
    pip install ansible
    pip install molecule
  ```
  - Molecule uses the  `delegated` driver by default. Other drivers can be installed separately from PyPI, most of them being included in molecule-plugins package. We are going to use the docker driver, so let's install that via:
    ```bash
    pip install "molecule[docker]"
    ```

## 3. Ansible Monorepo Structure
  -  We use the Ansible Monorepo structure, this means our playbooks, variables, scripts, roles, plugins, inventory scripts and configuration all resides together and is version controlled in the same repository.
  - Here is the high level layout:

    ```
    ~/ansible-endpoint
    ├── ansible.cfg
    ├── ansible_hosts
    ├── molecule/
    ├── playbooks/
    └── roles/
        ├── apache_server/
        ├── ...
        ├── nginx_server/
        └── ...
    ```

We'll focus on `roles/nginx_server`, showing how to add and configure the molecule scenarios for testing it and also verify it. 

## 4. Creating Your First Molecule Scenario
- **Molecule Init**  
  - Inside the `roles/nginx_server` directory, let's initialize the molecule scenario:
  ```bash
    cd roles/nginx_server
    molecule init scenario --driver-name docker --scenario-name default
  ```
  - This command will create the following files:
    ```
    roles/
    └── nginx_server/
        ├── tasks/
        │   └── main.yml
        ├── molecule/
        │   └── default/
        │       ├── molecule.yml
        │       ├── converge.yml
        │       ├── verify.yml
        │       └── destroy.yml
        └── ...
    ```

Here are some details about the files created by molecule:

- `molecule.yml` - Molecule configuration file.

    ```yaml
    ---
    driver:
      name: docker
    platforms:
      - name: "molecule-rocky9-${CI_JOB_ID}"
        image: geerlingguy/docker-rockylinux9-ansible:latest
        privileged: true
        pre_build_image: true
        volumes:
          - /sys/fs/cgroup:/sys/fs/cgroup:rw
        cgroupns_mode: host
        command: /usr/sbin/init
    provisioner:
      name: ansible
    ```

Some details:
- Provisioner is the tool that will be used to provision the scenario and we are using ansible to run the scenario itself. 
- Docker - As we discussed before, we are using docker as the driver.
- Platforms - Here we define the target platform for the scenario. We are using Rocky 9 docker image as the target platform. Thanks to [Jeff Geerling](https://github.com/geerlingguy/docker-rockylinux9-ansible) who created the Rocky 9 docker image for Ansible testing with systemd in it. 


- `converge.yml` - Playbook to converge the scenario. This tells Molecule to apply the nginx_server role to our test container (the "instance" defined in molecule.yml).
    ```yaml
    ---
    - name: Converge
      hosts: all
      gather_facts: false
      tasks:
        - name: Run the nginx_server role
          hosts: all
          roles:
            - nginx_server
    ```
- `verify.yml` - Playbook to verify whether the converge was successful. This tells Molecule to verify that our role has been correctly installed stuff on the docker instance. Here we are going to check if nginx is installed, running and also responding to requests.
    ```yaml
    ---
    - name: Verify
      hosts: all
      tasks:
        - name: Check if NGINX is installed
          ansible.builtin.package:
            name: nginx
            state: present
          check_mode: true
          register: install
          failed_when: (install is changed) or (install is failed)

        - name: Check if NGINX service is running
          ansible.builtin.service:
            name: nginx
            state: started
            enabled: true
          check_mode: true
          register: service
          failed_when: (service is changed) or (service is failed)

        - name: Verify NGINX is up and running
          ansible.builtin.uri:
            url: http://localhost
            status_code: 200
    ```


- `destroy.yml` - Destroys the instance defined in the molecule.yml file. There won't be any file, but the default docker driver will automatically destroy the instance after the test is finished. If you wanna override this behavior, you can add a destroy.yml file to the scenario directory.


## 5. Running molecule tests

- Molecule run consists of the various lifecycle events:
  - `create`
  - ...
  - `converge`
  - ...
  - `verify`
  - ...
  - `destroy`

These are some of the important events in the molecule lifecycle run.
To run the full lifecycle molecule run, we can use the following command:
```bash
cd roles/nginx_server
molecule test
```
This command executes the following steps in sequence:
- Create: Spins up a test rocky 9 container as mentioned in the molecule.yml file.
- Converge: Applies the nginx_server role inside the container.
- Verify: Verifies whether the nginx server is installed, running and responding to requests.
- Destroy: Cleans up the container.


- We can also run each step individually:
  - `molecule create`
  - `molecule converge`
  - `molecule verify`
  - `molecule destroy`
- To avoid rebuilding the containers, we can run commands from converge step. 


## 6. Integrating Molecule with Gitlab CI/CD

We want to run the molecule tests whenever a MR is created which involves the changes with the particular role.
To automatically run the molecule tests, we can use the Gitlab CI/CD.

Here is an example of a `.gitlab-ci.yml` file that runs the molecule tests in the Docker based environment for our nginx_server role. 


```yaml
stages:
  - test

before_script:
  - pip install molecule ansible docker molecule-docker

molecule_test:
  stage: test
  variables:
    ROLE_PATH: "roles/nginx_server"
  script:
    - cd $ROLE_PATH
    - molecule test
  rules:
    - changes:
        - $ROLE_PATH/**
```


With this setup, we've setup Molecule scenario for a specific Ansible role and run tests both manually and automatically via GitLab CI. This allows tests to trigger whenever a merge request modifies that role, ensuring a quick feedback loop and a higher degree of reliability in the automation.


To learn more about molecule, here are some of the useful links:
- [Molecule Documentation](https://ansible.readthedocs.io/projects/molecule/)
- [Molecule GitHub Repository](https://github.com/ansible/molecule)
- [Molecule Driver Plugins](https://github.com/ansible-community/molecule-plugins)



