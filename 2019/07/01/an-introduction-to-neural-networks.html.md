---
author: "Ben Ironside Goldstein"
title: "An Introduction to Neural Networks"
tags: machine-learning, artificial-intelligence
gh_issue_number: 1535
---

<img src="/blog/2019/07/01/an-introduction-to-neural-networks/image-0.jpg" alt="Weird Tree Art (Neural Network)" /> [Photo](https://flic.kr/p/5eL8Ag) by [Sudhamshu Hebbar](https://www.flickr.com/photos/sudhamshu/), used under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)

Earlier this year I wrote a [post](/blog/2019/05/01/facial-recognition-amazon-deeplens) about my work with a machine-learning camera, the [AWS DeepLens](https://aws.amazon.com/deeplens/), which has onboard processing power to enable AI capabilities without sending data to the cloud. Neural networks are a type of ML model which achieves very impressive results on certain problems (including computer vision), so in this post I give a more thorough introduction to neural networks, and share some useful resources for those who want to dig deeper.

### Neurons and Nodes

Neural networks are models inspired by the function of biological neural networks. They consist of nodes (arranged in layers), and the connections between those nodes. Each connection between two nodes enables one-way information transfer: a node either receives input from, or sends output to each node to which it is connected. Nodes typically have an “activation function”, parameterized by the node’s inputs, and its output is the result of this function.

As with the function of biological neural networks, the emergence of information processing from these mathematical operations is opaque. Nevertheless, complex artificial neural networks are capable of feats such as vision, language translation, and winning competitive games. As the technology improves, even more impressive tasks will become possible. As with organic brains, neural networks can achieve complex tasks only as a result of appropriate architecture, constraints, and training—for machine learning, humans must (for now) design it all.

### Neural Network Architecture

<img src="/blog/2019/07/01/an-introduction-to-neural-networks/image-1.png" style="float: right; max-width: 200px" /> 
<p>
Nodes are grouped in layers: the input layer, the output layer, and all the layers between them, known as hidden layers. Nodes can be networked in a variety of ways within and between layers, and sophisticated neural network models can include dozens of layers configured in various ways. These include layers which summarize, combine, eliminate, direct, or transform information. Each receives its input from the previous layer, and passes its output to the next layer. The last layer is designed such that its output answers the relevant question (for example, it would offer 9 options if the goal were to identify the hand-written numbers 1–9).
</p>

For all this information processing to achieve a given task, the parameters of each node need appropriate values. The process of choosing those values is called training. In order to train a neural network, one needs to provide examples of what the network should do. (For example, to train it to write requires examples of writing. To train it to identify objects in images requires images and their appropriately labeled counterparts.) The more data a model can learn from, the better it can work. Gathering enough data is typically a major undertaking.

### Training a Neural Network

Before training, models have random parameters for all nodes. Each time data is passed through the model, the effectiveness of the model is measured using a “loss function”. Loss functions measure how wrong a model’s output is. Different loss functions (also known as cost functions or error functions) measure this in different ways, but in general, the more wrong a model is, the higher its loss/error/cost. Loss functions thus summarize the quality of a model’s output with a single number. Models are optimized to minimize the loss. (For more on the role of loss functions in neural networks, I suggest [this excellent article](https://machinelearningmastery.com/loss-and-loss-functions-for-training-deep-learning-neural-networks/).)

One of the most interesting details of the entire process has to do with how the parameters are tuned. Model optimization relies on variations of a process called gradient descent, in which parameter values are adjusted by small intervals in an attempt to minimize the loss. Over many thousands of repetitions, the training program uses calculus to pick values that help to minimize the loss. As you can imagine, this process becomes extremely computationally intensive when the neural network is large and complex. However, in order to solve hard problems, networks must be large and complex. This is why training neural networks requires substantial computing power, and often takes place in the cloud. (For more on stochastic gradient descent, I suggest [this video](https://www.youtube.com/watch?v=vMh0zPT0tLI) as a great starting point, or [this review](http://ruder.io/optimizing-gradient-descent/) for a more advanced overview.)

### Further reading

- It turns out that a relatively simple neural network can approximate any function. This remarkable [demonstration](https://towardsdatascience.com/can-neural-networks-really-learn-any-function-65e106617fc6) is quite accessible.
- There are countless useful implementations of neural network models. End Pointer [Kamil Ciemniewski](/team/kamil_ciemniewski) wrote two in-depth and fascinating blogs about neural network projects which he completed in the past year: [Speech Recognition From Scratch](blog/2019/01/08/speech-recognition-with-tensorflow), and [Self-Driving Toy Car](blog/2018/08/29/self-driving-toy-car-using-the-a3c-algorithm).
- If you’re interested in getting a sense for the general state of the art, [here](https://www.topbots.com/most-important-ai-research-papers-2018/) are summaries of some of the most influential papers in machine learning since 2018.
- For those curious about the inner workings of the training process, here’s one about [back-propagation](http://neuralnetworksanddeeplearning.com/chap2.html).
- This blog post describes “densely connected” network layers; here’s an article about [convolutional layers](https://towardsdatascience.com/a-comprehensive-guide-to-convolutional-neural-networks-the-eli5-way-3bd2b1164a53).
- And finally, this article describes [recurrent neural networks](https://medium.com/explore-artificial-intelligence/an-introduction-to-recurrent-neural-networks-72c97bf0912).
