---
author: "Kannan Ponnusamy"
date: 2025-03-28
title: "Testing Ansible Automation with Molecule"
github_issue_number: 2104
featured:
  image_url: /blog/2025/03/testing-ansible-with-molecule/optical-disc-drive.webp
description: "How to - Ansible role testing with Molecule and Docker, including setup, scenario creation, and GitLab CI/CD integration for automated, reliable automation testing"
tags:
- sysadmin
- linux
- integration
- cloud
- devops
---

![Photo of an open hard drive, with the data reading arm extended over the disc.](/blog/2025/03/testing-ansible-with-molecule/optical-disc-drive.webp)<br>
[Photo](https://unsplash.com/photos/photo-of-optical-disc-drive-1iVKwElWrPA) by [Patrick Lindenberg](https://unsplash.com/@heapdump)

### 1. Why Test with Molecule?

Molecule is a test framework for Ansible roles. It supports testing with multiple instances, operating systems and distributions, virtualization providers, test frameworks, and testing scenarios.

Molecule is useful because it increases confidence in your automation and ensures roles are reliable. It catches issues early in the development cycle, reducing production problems. It also ensures consistency across different environments and platforms.

### 2. Install Prerequisites

Make sure you have Python >= 3.6 and pip installed. Then install Ansible and Molecule using pip:

```plain
pip install ansible
pip install molecule
```

Molecule uses the `delegated` driver by default. Other drivers can be installed separately from PyPI, most of them being included in the molecule-plugins package. We are going to use the Docker driver, so let's install that by running:

```plain
pip install "molecule[docker]"
```

### 3. Ansible Monorepo Structure

We use the Ansible monorepo structure. This means our playbooks, variables, scripts, roles, plugins, inventory scripts, and configuration all reside and are version controlled together in the same repository.

Here is the high level layout:

```plain
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

We'll focus on `roles/nginx_server`, showing how to add and configure the Molecule scenarios for testing and also how to verify it.

### 4. Creating Your First Molecule Scenario

Inside the `roles/nginx_server` directory, let's initialize the Molecule scenario:

```plain
cd roles/nginx_server
molecule init scenario --driver-name docker --scenario-name default
```

This command will create the following files:

```plain
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

Here are some details about the files created by Molecule:

- `molecule.yml` - The Molecule configuration file.

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

  Key blocks from `molecule.yml`:

  - `provisioner` is the tool that will be used to provision the scenario. We are using Ansible to run the scenario itself.
  - `driver` — As mentioned above, we are using Docker as the driver.
  - `platforms` — Here we define the target platform for the scenario. We are using the Rocky 9 Docker image as the target platform. Thanks to [Jeff Geerling](https://github.com/geerlingguy/docker-rockylinux9-ansible) who created the Rocky 9 Docker image for Ansible testing with systemd in it.

- `converge.yml` — The playbook to converge the scenario. This tells Molecule to apply the `nginx_server` role to our test container (the "instance" defined in `molecule.yml`).

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

- `verify.yml` - The playbook to verify whether the converge was successful. This tells Molecule to verify that our role has been correctly installed on the Docker instance. Here we are going to check if NGINX is installed, running and also responding to requests.

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


- `destroy.yml` - Destroys the instance defined in the `molecule.yml` file. There won't be any file, but the default Docker driver will automatically destroy the instance after the test is finished. If you want to override this behavior, you can add a `destroy.yml` file to the scenario directory.


### 5. Running Molecule tests

- A Molecule run consists of the various lifecycle events:

  - `create`
  - ...
  - `converge`
  - ...
  - `verify`
  - ...
  - `destroy`

These are some of the important events in the Molecule lifecycle run. To run the full lifecycle Molecule run, we can use the following command:

```plain
cd roles/nginx_server
molecule test
```

This command executes the following steps in sequence:

- Create: Spins up a test Rocky 9 container as mentioned in the `molecule.yml` file.
- Converge: Applies the `nginx_server` role inside the container.
- Verify: Verifies whether the NGINX server is installed, running, and responding to requests.
- Destroy: Cleans up the container.

We can also run each step individually:

- `molecule create`
- `molecule converge`
- `molecule verify`
- `molecule destroy`

To avoid rebuilding the containers, we can run commands from converge step.

### 6. Integrating Molecule with GitLab CI/CD

We want to run the Molecule tests whenever a merge request which changes the particular role is created.

To automatically run the Molecule tests, we can use the GitLab CI/CD.

Here is an example of a `.gitlab-ci.yml` file that runs our Molecule tests in the Docker based environment for our `nginx_server` role.

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

With this setup, we've set up a Molecule scenario for a specific Ansible role, then run tests both manually and automatically via GitLab CI. This allows tests to trigger whenever a merge request modifies that role, ensuring a quick feedback loop and a higher degree of reliability in the automation.

To learn more about Molecule, here are some useful links:

- [Molecule documentation](https://ansible.readthedocs.io/projects/molecule/)
- [Molecule GitHub repository](https://github.com/ansible/molecule)
- [Molecule driver plugins](https://github.com/ansible-community/molecule-plugins)

