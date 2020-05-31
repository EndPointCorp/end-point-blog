---
author: "Will Plaut"
title: "Designing flexible CI pipelines with Jenkins and Docker"
tags: jenkins, docker, groovy
gh_issue_number: 1633
---

![Pipes](/blog/2020/05/25/flexible-ci-pipelines-jenkins-docker/pipes.jpg)

[Photo](https://unsplash.com/photos/9AxFJaNySB8) by [Tian Kuan](https://unsplash.com/@realaxer) on [Unsplash](https://unsplash.com/)

When deciding on how to implement continuous integration (CI) for a new project, you are presented with lots of choices. Whatever you end up choosing, your CI needs to work for you and your team. Keeping the CI process and its mechanisms clear and concise helps everyone working on the project. The setup we are currently employing, and what I am going to showcase here, has proven to be flexible and powerful. Specifically, I’m going to highlight some of the things Jenkins and Docker do that are really helpful.

### Jenkins

[Jenkins](https://www.jenkins.io/) provides us with all the CI functionality we need and it can be easily configured to connect to projects on GitHub and our internal GitLab. Jenkins has support for something it calls a multibranch pipeline. A Jenkins project follows a repo and builds any branch that has a `Jenkinsfile`. A `Jenkinsfile` configures an individual pipeline that Jenkins runs against a repo on a branch, tag or merge request (MR).

To keep it even simpler, we condense the steps that a `Jenkinsfile` runs into shell scripts that live in `/scripts/` at the root of the source repo to do things like test or build or deploy, such as `/scripts/test.sh`. If a team member wants to know how the tests are run, it is right in that file to reference.

The `Jenkinsfile` can be written in a declarative syntax or in plain Groovy. We have landed on the scripted Groovy syntax for its more fine-grained control of Docker containers. Jenkins also provides several ways to inspect and debug the pipelines with things like “Replay” in its GUI and using `input('wait here')` in a pipeline to debug a troublesome step. The `input()` function is especially useful when paired with Docker. The function allows us to pause the job and go to the Jenkins server where we use `docker ps` to find the running container’s name. Then we use `docker exec -it {container name} bash` to debug inside of the container with all of the Jenkins environment variables loaded. This has proven to be a great way to figure out why something isn’t working in our test stages.

### Docker

We love using [Docker](https://www.docker.com/) for our development and deployment for a variety of reasons. First, creating a Dockerfile for a project is essentially an exercise in figuring out how a project is built with a minimum of dependencies. Once a Docker container is built, the running container provides a great place to run tests as it is a clean checkout with little to no extra cruft.

Using our Jenkins pipeline, we can take builds triggered by tags and push an associated tagged Docker image up to our registry. With Docker’s layering, pushes are often the shortest stage of the Jenkins job. Deploying that tag is as simple as doing a `docker pull` on the target system. For the application deployment, we create a basic `docker-compose.yml` to start and serve the project from within the container, forwarding whatever ports we need on the local system.

### Example Jenkinsfile

Let’s take a look at a basic scripted `Jenkinsfile` (scripted in Groovy) that utilizes a `Dockerfile` in the source repo to build, test, and deploy a project:

```plain
node() {
  properties([gitLabConnection('gitlab-connect')])

  def vueImage
  def dockerTagName
 
  stage('Checkout') {
    checkout scm
  }

  stage('Build') {
    vueImage = docker.build("endpoint/vue-test")
  }
  vueImage.inside('-u 0') {
    stage('Test') {
      sh './scripts/test.sh'
    }
  }

  stage('Tag/Push') {
    docker.withRegistry('https://registry.hub.docker.com', 'ep_dockerhub_creds') {
      if (env.TAG_NAME != null) {
        vueImage.push("${env.TAG_NAME}")
      } else {
        vueImage.push("${env.BRANCH_NAME}")
      }
    }
  }
}
```

The script’s first stage, `Checkout`, checks out the repo using our `gitlab-connect` credentials that are stored on the Jenkins server. It then moves to the `Build` stage where it builds the image using the `Dockerfile` in our repo and names it after the org/repo it will use on DockerHub. Then, inside of the running container we enter the `Test` stage where we run the repo script `./scripts/test.sh`. After the `.inside` code block is closed the running container is stopped and removed. Finally, we get to the `Tag/Push` stage where we push our Docker image up to DockerHub using another set of stored credentials. We tag it with either the `TAG_NAME` or the `BRANCH_NAME`.

This `Jenkinsfile` provides us with a solid base to expand on. During development as requirements change, it’s easy to modify and update the `Jenkinsfile`. We have the ability to run steps inside and outside of the Docker. Combined with bash scripts that live in the repo, we can do almost anything. Most of the job mechanics can be tuned, down to the specific status updates GitLab receives during a run.

Say we want to handle a push a bit differently if the branch is named `Master` or we want to add another stage and break out the `Test` stage into `Unit Tests` and `E2E Tests`. These things are easily changed in the `Jenkinsfile` and then run on Jenkins when pushed. There’s no need to merge to see the pipeline change. Every branch/​tag/​MR has its own pipeline. Deploying the Docker you just built is easy; just use your `TAG_NAME` or `BRANCH_NAME` with `docker pull endpoint/vue-test:{}`.

### Conclusion

Although the above script is just an example script, the `Jenkinsfile`s we use in production are not far off from this in functionality and the ideas remain the same.

Jenkins is not the easiest to configure as some of the required functionality comes from plugins, and getting the correct combination of plugins can be a challenge. That being said, the functionality it provides paired with Docker is amazing and definitely worth considering when setting up CI for a new project.
