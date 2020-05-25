---
author: "Kamil Ciemniewski"
title: "Deploying production Machine Learning pipelines to Kubernetes with Argo"
tags: machine-learning, kubernetes, natural-language-processing, python
gh_issue_number: 1534
---

<img src="/blog/2019/06/28/deploying-production-pipelines-to-kubernetes/image-0.jpg" alt="Rube Goldberg machine" /><br><a href="https://commons.wikimedia.org/wiki/File:Rube_Goldberg_Machine_(278696130).jpg">Image by Wikimedia Commons</a>

In some sense, most machine learning projects look exactly the same. There are 4 stages to be concerned with no matter what the project is:

1. Sourcing the data
2. Transforming it
3. Building the model
4. Deploying it

It’s been said that #1 and #2 take most of ML engineers’ time. This is to emphasize how little time it sometimes feels the most fun part—#3—gets.

In the real world, though, #4 over time can take almost as much as the previous three. 

Deployed models sometimes need to be rebuilt. They consume data that need to constantly go through points #1 and #2. It certainly isn’t always what’s shown in the classroom, where datasets perfectly fit in the memory and model training takes at most a couple hours on an old laptop.

Working with gigantic datasets isn’t the only problem. Data pipelines can take long hours to complete. What if some part of your infrastructure has an unexpected downtime? Do you just start it all over again from the very beginning? 

Many solutions of course exist. With this article, I’d like to go over this problem space and present an approach that feels really nice and clean.

### Project description

End Point Corporation was founded in 1995. That’s 24 years! About 9 years later, [the oldest article](/blog/2004/10/04/red-hat-enterprise-linux-3-update-3) on the company’s blog was published. Since that time, a staggering number of 1435 unique articles have been published. That’s a lot of words! This is something we can definitely use in a smart way.

For the purpose of having fun with building a production-grade data pipeline, let’s imagine the following project:

- A [doc2vec](https://cs.stanford.edu/~quocle/paragraph_vector.pdf) model trained on the corpus of End Point’s blog articles
- Use of the paragraph vectors for each article to find the 10 other, most similar articles

I blogged about using the [matrix factorization](/blog/2018/07/17/recommender-mxnet) as a simple [collaborative filtering](https://en.wikipedia.org/wiki/Recommender_system#Collaborative_filtering) style of the recommender system. We can think about today’s doc2vec-based model as an example of the [content based filtering](https://en.wikipedia.org/wiki/Recommender_system#Content-based_filtering). The business value would be the potentially increased blog traffic from users staying longer on the website.

### Scalable pipelines

The data pipelines problem certainly found some really great solutions. The [Hadoop](http://hadoop.apache.org) project brought in the HDFS—a distributed file system for huge data artifacts. Its MapReduce component plays a vital role in distributed data processing.

Then, the fantastic [Spark](https://spark.apache.org) project came in. Its architecture makes data reside in memory by default—with explicit caching of the data on disks. The project claims to be running workloads 100 times faster than Hadoop.

Both projects though require the developer to use a very specific set of libraries. It’s not easy, for example, to distribute [spaCy](https://spacy.io) training and inference on Spark.

### Containers

On the other side of the spectrum, there’s [Dask](https://dask.org). It’s a Python package that wraps [Numpy](https://www.numpy.org), [Pandas](https://pandas.pydata.org) and [Scikit-Learn](https://scikit-learn.org/stable/). It enables developers to load huge piles of data, just as they would with the smaller datasets. The data is partitioned and distributed among the cluster nodes. It can work with groups of processes as well as clusters of containers. The APIs of the above-mentioned projects are (mostly) preserved while all the processing is suddenly distributed.

Some teams like to use Dask along with [Luigi](https://luigi.readthedocs.io/en/stable/) and build production pipelines around [Docker](https://www.docker.com) or [Kubernetes](https://kubernetes.io).

In this article, I’d like to present another Dask-friendly solution: Kubernetes-native workflows using [Argo](https://argoproj.github.io). What’s great about it compared to Luigi, is that you don’t even need to care about having a certain version of Python and Luigi installed to orchestrate the pipeline. All you need is the Kubernetes cluster and Argo installed on it.

### Hands down work on the project

The first thing to do when developing this project is to get access to the Kubernetes cluster. For the development, you can set up a one-node cluster using either one of:

- [Microk8s](https://microk8s.io)
- [Minikube](https://github.com/kubernetes/minikube)

I love them both. The first is developed by Canonical while the second by the Kubernetes team itself.

This isn’t going to be a step-by-step tutorial on using Kubernetes. I encourage you to read the documentation or possibly seek out a good online course if you don’t know anything yet. Read on even in this case though—it’s nothing that would be overly complex.

Next, you’ll need the Argo Workflows. The installation is really easy. The full yet simple documentation can be found [here](https://argoproj.github.io/docs/argo/demo.html).

#### The project structure

Here’s what the project looks like in the end:

```bash
.
├── Makefile
├── notebooks
│  └── scratch.ipynb
├── notebooks.yml
├── pipeline.yaml
├── tasks
   ├── base
   │  ├── Dockerfile
   │  └── requirements.txt
   ├── build_model
   │  ├── Dockerfile
   │  └── run.py
   ├── clone_repo
   │  ├── Dockerfile
   │  └── run.sh
   ├── infer
   │  ├── Dockerfile
   │  └── run.py
   ├── notebooks
   │  └── Dockerfile
   └── preprocess
      ├── Dockerfile
      └── run.py
```

The main parts are as follows:

- `Makefile` provides easy to use helpers for building images, sending them into the Docker repository and running the Argo workflow
- `notebooks.yml` defines a Kubernetes service and deployment for exploratory [Jupyter Lab](https://github.com/jupyterlab/jupyterlab) instance
- `notebooks` contains individual Jupyter notebooks
- `pipeline.yaml` defines our Machine Learning pipeline in the form of the Argo workflow
- `tasks` contains workflow steps as containers along with their Dockerfiles
- `tasks/base` defines the base Docker image for other tasks
- `tasks/**/run.(py|sh)` is a single entry point for a given pipeline step

The idea is to minimize the boilerplate while retaining the features offered e.g. by Luigi.

#### Makefile

```Makefile
SHELL := /bin/bash
VERSION?=latest
TASK_IMAGES:=$(shell find tasks -name Dockerfile -printf '%h ')
REGISTRY=base:5000

tasks/%: FORCE
        set -e ;\
        docker build -t blog_pipeline_$(@F):$(VERSION) $@ ;\
        docker tag blog_pipeline_$(@F):$(VERSION) $(REGISTRY)/blog_pipeline_$(@F):$(VERSION) ;\
        docker push $(REGISTRY)/blog_pipeline_$(@F):$(VERSION)

images: $(TASK_IMAGES)

run: images
        argo submit pipeline.yaml --watch

start_notebooks:
        kubectl apply -f notebooks.yml

stop_notebooks:
        kubectl delete deployment jupyter-notebook

FORCE: ;
```

When using this Makefile with `make run`, it will need to resolve the `images` dependency. This, in turn, will ask to resolve all of the `task/**/Dockerfile` dependencies too. Notice how the `TASK_IMAGES` variable is constructed: it uses the make’s `shell` command to use the Unix’s `find` to find the subdirectories of `tasks` that contain the Dockerfile. Here’s what the output would be if you were to use it directly:

```bash
$ find tasks -name Dockerfile -printf '%h '
tasks/notebooks tasks/base tasks/preprocess tasks/infer tasks/build_model tasks/clone_repo
```

#### Setting up Jupyter Notebooks as a scratch pad and for EDA

Let’s start off by defining our base Docker image:

```Dockerfile
FROM python:3.7

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
```

Following is the Dockerfile that extends it and adds the Jupyter Lab:

```Dockerfile
FROM endpoint-blog-pipeline/base:latest

RUN pip install jupyterlab

RUN mkdir ~/.jupyter
RUN echo "c.NotebookApp.token = ''" >> ~/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.password = ''" >> ~/.jupyter/jupyter_notebook_config.py

RUN mkdir /notebooks
WORKDIR /notebooks
```

The last step is to add the Kubernetes service and deployment definition in `notebooks.yml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jupyter-notebook
  labels:
    app: jupyter-notebook
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jupyter-notebook
  template:
    metadata:
      labels:
        app: jupyter-notebook
    spec:
      containers:
      - name: minimal-notebook
        image: base:5000/blog_pipeline_notebooks
        ports:
        - containerPort: 8888
        command: ["/usr/local/bin/jupyter"]
        args: ["lab", "--allow-root", "--port", "8888", "--ip", "0.0.0.0"]
---
kind: Service
apiVersion: v1
metadata:
  name: jupyter-notebook
spec:
  type: NodePort
  selector:
    app: jupyter-notebook
  ports:
  - protocol: TCP
    nodePort: 30040
    port: 8888
    targetPort: 8888
```

This can be run using our Makefile with `make start_notebooks` or directly with:

```bash
$ kubectl apply -f notebooks.yml
```

#### Exploration

The [notebook itself](https://github.com/kamilc/endpoint-blog-nlp/blob/master/notebooks/scratch.ipynb) feels more like a scratch pad than an exploratory data analysis. You can see that it’s very informal and doesn’t include much of the exploration or visualization. You’re likely not to omit those in more real-world code.

I used it to ensure the model would work at all. I then was able to grab portions of the code and paste it directly into step definitions.

#### Implementation

##### Step 1: Source blog articles

The blog’s articles are stored on [GitHub](https://github.com/EndPointCorp/end-point-blog) in Markdown files.

Our first pipeline task will need to either clone the repo or pull from it if it’s present in the pipeline’s shared volume.

We’ll use the Kubernetes [hostPath](https://kubernetes.io/docs/concepts/storage/volumes/#hostpath) as the cross-step volume. What’s nice about it is that it’s easy to peek into the volume during development to see if the data artifacts are being generated correctly.

In our example here, I’m hardcoding the path on my local system:

```yaml
# ...
volumes:
  - name: endpoint-blog-src
    hostPath:
      path: /home/kamil/data/endpoint-blog-src
      type: Directory
# ...
```

This is one of the downsides of the `hostPath`—it only accepts absolute paths. This will do just fine for now though.

In the `pipeline.yml` we define the task container with:

```yaml
# ...
templates:
  - name: clone-repo
    container:
      image: base:5000/blog_pipeline_clone_repo
      command: [bash]
      args: ["/run.sh"]
      volumeMounts:
      - mountPath: /data
        name: endpoint-blog-src
# ...
```

The full pipeline forms a tree which is expressed conveniently as a directed acyclic graph within the Argo. Here’s the definition of the whole pipeline (some steps were not shown yet):

```yaml
# ...
- name: article-vectors
    dag:
      tasks:
      - name: src
        template: clone-repo
      - name: dataframe
        template: preprocess
        dependencies: [src]
      - name: model
        template: build-model
        dependencies: [dataframe]
      - name: infer
        template: infer
        dependencies: [model]
# ...
```

Notice how the `dependencies` field makes it easy to tell Argo what order to take when executing the tasks. The Argo steps can also define inputs and outputs—just like Luigi. For this simple example, I decided to omit them and enforce the convention for the steps to expect data artifacts in a certain location in the mounted volume. If you’re curious about other Argo features though, [here](https://argoproj.github.io/docs/argo/examples/readme.html#parameters) is its documentation.

The entry point script for the task is pretty simple:

```bash
#!/bin/bash

cd /data

if [ -d ./blog ]
then
  cd blog
  git pull origin master
else
  git clone https://github.com/EndPointCorp/end-point-blog.git blog
fi
```

##### Step 2: Data wrangling

At this point, we’d have the source files for the blog articles in Markdown files. To be able to run them through any kind of machine learning modeling, we need to source it into the data frame. We’ll also need to clean the text a bit. Here is the reasoning behind the cleanup routine:

- I want the relations between the articles to omit the code snippets: **not** to group them by the used programming language or a library just by the keywords they contain
- I also want the metadata about the tags and authors to be omitted too as I don’t want to see only e.g. my articles listed as similar to my other ones

The full source for the `run.py` of the “preprocess” task can be viewed [here](https://github.com/kamilc/endpoint-blog-nlp/blob/master/tasks/preprocess/run.py).

Notice that unlike make or Luigi, the Argo workflows would run the same task fully again even with the step artifact already being created. I **like** this flexibility—it’s extremely easy after all to just skip the processing in Python or shell script if it already exists.

At the end of this step, the data frame is written as the [Apache Parquet](https://parquet.apache.org) file.

##### Step 3: Building the model

The model from the paper mentioned earlier has already been implemented in a variety of other projects. There are implementations for each major deep learning framework on GitHub. There’s also a pretty good one included in [Gensim](https://radimrehurek.com/gensim/index.html). Its documentation can be found [here](https://radimrehurek.com/gensim/models/doc2vec.html).

The [run.py](https://github.com/kamilc/endpoint-blog-nlp/blob/master/tasks/build_model/run.py) is pretty short and straight forward as well. This is one of the goals for the pipeline. In the end, it’s writing the trained model into the shared volume as well.

Notice that re-running the pipeline with the model already stored will not trigger the training again. This is what we want. Imagine a new article being pushed into the repository. It’s very unlikely that retraining with it would affect the model’s performance in any significant way. We’ll still need to predict the similar other documents for it. The model building step would short-circuit though with:

```python
if __name__ == '__main__':
    if os.path.isfile('/data/articles.model'):
        print("Skipping as the model file already exists")
    else:
        build_model()
```

##### Step 4: Predict similar articles

The listing of the [run.py](https://github.com/kamilc/endpoint-blog-nlp/blob/master/tasks/infer/run.py) isn’t overly long:

```python
import pandas as pd
from gensim.models.doc2vec import Doc2Vec
import yaml
from pathlib import Path
import os


def write_similar_for(path, model):
    similar_paths = model.docvecs.most_similar(path)
    yaml_path = (Path('/data/blog/') / path).parent / 'similar.yaml'

    with open(yaml_path, "w") as file:
        file.write(yaml.dump([p for p, _ in similar_paths]))
        print(f"Wrote similar paths to {yaml_path}")


def infer_similar():
    articles = pd.read_parquet('/data/articles.parquet')
    model = Doc2Vec.load('/data/articles.model')

    for tag in articles['file'].tolist():
        write_similar_for(tag, model)

if __name__ == '__main__':
    infer_similar()
```

The idea is to load up the saved Gensim model and the data frame with articles first. Then for each article use the model to get the 10 most similar other articles.

As the step’s output, the listing of similar articles is placed in the `similar.yml` file for each article’s subdirectory.

The blog’s Markdown → HTML compiler could then use this file and e.g. inject the “You might find those articles interesting too” section.

#### Results

The scratch notebook already includes the example results of running this doc2vec model. Examples:

```python
model.docvecs.most_similar('2019/01/09/liquid-galaxy-at-instituto-moreira-salles.html.md')
```

Giving the output of:

```python
[('2016/04/22/liquid-galaxy-for-real-estate.html.md', 0.8872901201248169),
 ('2017/07/03/liquid-galaxy-at-2017-boma.html.md', 0.8766101598739624),
 ('2017/01/25/smartracs-liquid-galaxy-at-national.html.md',
  0.8722846508026123),
 ('2016/01/04/liquid-galaxy-at-new-york-tech-meetup_4.html.md',
  0.8693454265594482),
 ('2017/06/16/successful-first-geoint-symposium-for.html.md',
  0.8679709434509277),
 ('2014/08/22/liquid-galaxy-for-daniel-island-school.html.md',
  0.8659971356391907),
 ('2016/07/21/liquid-galaxy-featured-on-reef-builders.html.md',
  0.8644022941589355),
 ('2017/11/17/president-of-the-un-general-assembly.html.md',
  0.8620222806930542),
 ('2016/04/27/we-are-bigger-than-vr-gear-liquid-galaxy.html.md',
  0.8613147139549255),
 ('2015/11/04/end-pointers-favorite-liquid-galaxy.html.md',
  0.8601428270339966)]
```

Or the following:

```python
model.docvecs.most_similar('2019/01/08/speech-recognition-with-tensorflow.html.md')
```

Giving:

```python
[('2019/05/01/facial-recognition-amazon-deeplens.html.md', 0.8850516080856323),
 ('2017/05/30/recognizing-handwritten-digits-quick.html.md',
  0.8535605072975159),
 ('2018/10/10/image-recognition-tools.html.md', 0.8495659232139587),
 ('2018/07/09/training-tesseract-models-from-scratch.html.md',
  0.8377258777618408),
 ('2015/12/18/ros-has-become-pivotal-piece-of.html.md', 0.8344655632972717),
 ('2013/03/07/streaming-live-with-red5-media.html.md', 0.8181146383285522),
 ('2012/04/27/streaming-live-with-red5-media-server.html.md',
  0.8142604827880859),
 ('2013/03/15/generating-pdf-documents-in-browser.html.md',
  0.7829260230064392),
 ('2016/05/12/sketchfab-on-liquid-galaxy.html.md', 0.7779937386512756),
 ('2018/08/29/self-driving-toy-car-using-the-a3c-algorithm.html.md',
  0.7659779787063599)]
```

Or

```python
model.docvecs.most_similar('2016/06/03/adding-bash-completion-to-python-script.html.md')
```

With:

```python
[('2014/03/12/provisioning-development-environment.html.md',
  0.8298013806343079),
 ('2015/04/03/manage-python-script-options.html.md', 0.7975824475288391),
 ('2012/01/03/automating-removal-of-ssh-key-patterns.html.md',
  0.7794561386108398),
 ('2014/03/14/provisioning-development-environment_14.html.md',
  0.7763932943344116),
 ('2012/04/16/easy-creating-ramdisk-on-ubuntu.html.md', 0.7579266428947449),
 ('2016/03/03/loading-json-files-into-postgresql-95.html.md',
  0.7410352230072021),
 ('2015/02/06/vim-plugin-spotlight-ctrlp.html.md', 0.7385793924331665),
 ('2017/10/27/hot-deploy-java-classes-and-assets-in.html.md',
  0.7358890771865845),
 ('2012/03/21/puppet-custom-fact-ruby-plugin.html.md', 0.718029260635376),
 ('2012/01/14/using-disqus-and-rails.html.md', 0.716759443283081)]
```
To run the pipeline all you need is to:

```bash
$ make run
```

Or directly with:

```bash
$ argo submit pipeline.yml --watch
```

Argo gives a nice looking output of all the steps:

```
Name:                endpoint-blog-pipeline-49ls5
Namespace:           default
ServiceAccount:      default
Status:              Succeeded
Created:             Wed Jun 26 13:27:51 +0200 (17 seconds ago)
Started:             Wed Jun 26 13:27:51 +0200 (17 seconds ago)
Finished:            Wed Jun 26 13:28:08 +0200 (now)
Duration:            17 seconds

STEP                             PODNAME                                  DURATION  MESSAGE
 ✔ endpoint-blog-pipeline-49ls5
 ├-✔ src                         endpoint-blog-pipeline-49ls5-3331170004  3s
 ├-✔ dataframe                   endpoint-blog-pipeline-49ls5-2286787535  3s
 ├-✔ model                       endpoint-blog-pipeline-49ls5-529475051   3s
 └-✔ infer                       endpoint-blog-pipeline-49ls5-1778224726  6s
```

The resulting `similar.yml` files look as follows:

```bash
$ ls ~/data/endpoint-blog-src/blog/2013/03/15/
generating-pdf-documents-in-browser.html.md  similar.yaml

$ cat ~/data/endpoint-blog-src/blog/2013/03/15/similar.yaml
- 2016/03/17/creating-video-player-with-time-markers.html.md
- 2014/07/17/creating-symbol-web-font.html.md
- 2018/10/10/image-recognition-tools.html.md
- 2015/08/04/how-to-big-beautiful-background-video.html.md
- 2014/11/06/simplifying-mobile-development-with.html.md
- 2016/03/23/learning-from-data-basics-naive-bayes.html.md
- 2019/01/08/speech-recognition-with-tensorflow.html.md
- 2013/11/19/asynchronous-page-switches-with-django.html.md
- 2016/03/11/strict-typing-fun-example-free-monads.html.md
- 2018/07/09/training-tesseract-models-from-scratch.html.md
```

Although it’s difficult to quantify, those sets of “similar” documents do seem to be linked in many ways to their “anchor” articles. You’re invited to read them and see for yourself!

### Closing words

The code presented here is hosted [on GitHub](https://github.com/kamilc/endpoint-blog-nlp). There’s lots of room for improvement of course. It shows a nice approach that could be used for both small model deployments (like the one above) but also very big ones too.

The Argo workflows could be used in tandem with Kubernetes deployments. You could e.g. run a distributed [TensorFlow](https://www.tensorflow.org) model training and then deploy it on Kubernetes via [TensorFlow Serving](https://www.tensorflow.org/tfx/guide/serving). If you’re more into [PyTorch](https://pytorch.org), then distributing the training would be possible via [Horovod](https://eng.uber.com/horovod/). Have data scientists that use R? Deploy [RStudio Server](https://www.rstudio.com) instead of the JupyterLab with [the image from DockerHub](https://hub.docker.com/r/rocker/rstudio) and run some or all tasks with the [simpler one](https://hub.docker.com/r/rocker/r-ver) with R-base only.

If you have any questions or projects you’d like us to help you with, contact us right away through the [contact form](/contact) or email [ask@endpoint.com](mailto:ask@endpoint.com).
