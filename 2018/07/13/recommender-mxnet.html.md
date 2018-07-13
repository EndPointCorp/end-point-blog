# Recommender System via a simple Matrix Factorization

Recommender systems have a broad range of applications. We all like how Spotify or Last.fm can recommend a song. Discovering new libraries on GitHub through recommendations is also quite pleasing. In this article, we're going to get an overview of what it takes to build a system like that. We'll then move onto the practical side of things and will build our of recommender in `Python` and `MXNet`.

## Kinds of recommenders

The general setup of the content recommendation is that we have **users** and **items**. The task is to recommend items to a particular user.

There are two approaches to recommending content:

1. Content based filtering
2. Collaborative filtering

The first one bases its outputs on the the intricate features of the item and how they relate to the user itself. The latter one uses the information about the way other, similar users rank the items.

This article is going to focus on **collaborative filtering** only.

## A bit of theory: matrix factorization

In the simplest terms, we can represent interactions between users and items with a matrix:

|  | item1 | item2 | item3 |
|:--|:--|:--|:--|
| user1 | -1 | - | 0.6 |
| user2 | - | 0.95 | -0.1 |
| user3 | 0.5 | - | 0.8 |

In the above case users can rate items on the scale of `<-1, 1>`. Notice that in reality it's close to impossible to have them rate everything. The missing ratings are represented with the dash: `-`.

Just by looking at the matrix above, we know that no amount of math is going to change the fact that user1 completely dislikes item1. The same goes for the fact that user2 likes item2 a lot. The ratings we already have make up for an fairly easy set of items to propose. That's not the goal of a recommender though — we'd like to predict which of the "dashes" in the table would in reality have high enough values. It'd also be great to know which ones are most likely to have very low ones. In essence: we want to predict the full representation of the above matrix, basing only on its "sparse" representation as shown above.

To solve the above dilemma, we'll need to use just a little bit of linear algebra. Let's recall when can we multiply two matrices:

Given matrix `A: m × k` and `B: k × n`, their product is another matrix `C: m × n`.

```latex
C = AB
```

Imagine now that the "sparse" (not having all the values for all the row-column pairs) matrix represented by the table above is our `C`. This means that there exist matrices `A` and `B` that *factorize* `C`.

Notice also how this factorization can be helping in saving the space / memory for storing the full info about the matrix `C`.

Let's say that:

```
m = 1000000
n = 10000
```

Then the full representation takes:

```
m * n => 10,000,000,000
```

Now let's image that:

```
k = 16
```

Then to store both matrices: `A` and `B` we only need:

```
m * k + n * k => 16,160,000
```

Making it into a fraction of the original required space:

```
(m * k + n * k) / (m * n) => 0.001616
```

That's a **huge** saving. It goes with the small increase in the cost of the information retrieval. Inference of the rating from `C` based on `A` and `B` requires a **dot product** of the corresponding row and column of those matrices.

## Reasoning about the matrix factors

What intuition can we build for the above mentioned matrices `A` and `B`? Looking at their dimensions, we can see that each row of `A` is a `k`-sized vector that represents a user. Conversely, each column of `B` is a `k`-sized vector that represents an item. They are being called "latent features" or "latent representations" of users and items.

What could be the intuition? The factorizing algorithm takes all interactions with other users for any given item into account. The result is the latent feature vector of k elements. You can imagine the algorithm finding patterns in the ratings that later on match certain characteristics of the item. If this was about movies, the features could be that it's a comedy or sci-fi, that it's futuristic or embedded deeply in some ancient times etc. We're essentially taking the original vector of a movie, that contains ratings or empty value for each user — and based on that we're distilling features of the movie that describe it best.
 
## Factorizing the user / item matrix in practice

An extremely simple approach I'd like to show here, is to use a neural net. It's going to have matrices `A` and `B` as learnable parameters. The output for each row ow `A` and column of `B` is going to be a simple dot product. We're going to use a L2 loss which in essence sum of the squared differences between the output and the known rating.

The goal is to learn the values of `A` and `B` so that their product `AB` is very close to `C`.

## Getting the dataset

In this article, I'm going to use a freely available database of joke ratings, called "Jester". It contains data about ratings from 59132 users and 150 jokes.

It's available to download from [Berkeley](http://eigentaste.berkeley.edu/dataset/)

## Coding the model with MXNet

Let's first import some of the classes and functions we'll use later. 

```python
from mxnet.gluon import Block, nn, Trainer
from mxnet.gluon.loss import L2Loss
from mxnet import autograd, ndarray as F
import mxnet as mx

from sklearn.preprocessing import minmax_scale
import numpy as np
import random
import logging
import sys
import re
```

We'll need an iterator over the training batches read from the data files. In this simple scenario, it'll be just fine to read the whole data into memory and yield the batches from there.

It wouldn't be much more complicated to read the data on the fly from disk. This would be required in case e. g. the data not fitting into the memory.

Recent developments of `MXNet` bring a lot of the architectural goodness we've observed and loved in `PyTorch`. The `DataIter` class comes in the similar spirit. To create a custom data iterator, you'll need to inherit from `mxnet.io.DataIter` and implement two methods at least: `next` and `reset`. Here's our simple in-memory implementation:

```python
class DataIter(mx.io.DataIter):
    def __init__(self, data, batch_size = 16):
        super(DataIter, self).__init__()
        self.batch_size = batch_size
        self.all_user_ids = set()
        self.all_item_ids = set()
        self.data = data
        self.index = 0
        
        for user_id, item_id, _ in data:
            self.all_user_ids.add(user_id)
            self.all_item_ids.add(item_id)
        
    @property
    def user_count(self):
        return len(self.all_user_ids)
    
    @property
    def item_count(self):
        # we just know the value even though 10 of them were
        # not voted
        return 150
        
    def next(self):
        index = self.index * self.batch_size
        endindex = index + self.batch_size
        
        if len(self.data) <= index:
            raise StopIteration
        else:
            user_ids = []
            item_ids = []
            ratings = []

            user_ids = self.data[index:endindex, 0]
            item_ids = self.data[index:endindex, 1]
            ratings   = self.data[index:endindex, 2]

            data_all = [mx.nd.array(user_ids), mx.nd.array(item_ids)]
            label_all = [mx.nd.array([r]) for r in ratings]
            
            self.index += 1

            return mx.io.DataBatch(data_all, label_all)

    def reset(self):
        self.index = 0
        random.shuffle(self.data)
```

The above `DataIter` class expects to be given a `numpy` array with all the training examples. The first column represents a user, second an item and third the rating.

We'll need to write some code that will read data from disk and feed it into the `DataIter`'s constructor:

```python
def get_data(batch_size):
    def get_all_raw_data():
        user_ids = []
        item_ids = []
        ratings = []

        with open("data/jester_ratings.dat", "r") as file:
            for line in file:
                user_id, _, item_id, _, rating = line.strip().split("\t")

                user_ids.append(user_id)
                item_ids.append(item_id)
                ratings.append(rating)

        ratings = minmax_scale(np.asarray(ratings, dtype='float32').reshape(-1, 1), feature_range=(-1, 1))
        return np.asarray(list(zip(user_ids, item_ids, np.hstack(ratings).tolist())), dtype='float32')
    
    all_raw = get_all_raw_data()
    
    return DataIter(all_raw,  batch_size = batch_size)
```

Notice that I used the `minmax_scale` from `sklearn` to scale the ratings from `<-10,10>` to `<-1,1>`. This isn't mandatory but could help if you'd like to make the network architecture more complex and might run into overflow issues.

Here's how we can use the function to obtain the training data iterator:

```python
train = get_data(64)
```

To continue with the `PyTorch` style of coding, we're going to use the `mxnet.gluon` module with its classes to define the neural network.

The approach is very clean. You first inherit from the `mxnet.gluon.Block` and then you define the `forward` method that is going to be used during the forward network pass.

MXNet has its own implementation of automatic gradient calculations. You only need to care about the forward pass — the gradients will be computed automatically.

In our case, the `A` and `B` will be encoded within the `gluon` layers of type `Embedding`. It let's you specify the number of all the users and items as well as the dimension into which we're "squashing" them. It's also extremely handy as we won't need to "one hot encode" our user and item ids as the `Embedding` layer will do that for us.

Here's the implementation of our very simple network. Notice that all it really is, is a regression. The model also is linear so we're not going to use any activation functions:

```python
class Model(Block):
    def __init__(self, k, dataiter, **kwargs):
        super(Model, self).__init__(**kwargs)

        with self.name_scope():
            self.user_embedding = nn.Embedding(input_dim = dataiter.user_count, output_dim=k)
            self.item_embedding = nn.Embedding(input_dim = dataiter.item_count, output_dim=k)

    def forward(self, x):
        user = self.user_embedding(x[0])   
        item = self.item_embedding(x[1])
        
        pred = user * item
        
        return F.sum_axis(pred, axis = 1)
```

Next, we'll need to create the `MXNet` computation context as well as an instance of the model itself. Before doing any kind of learning, the parameters of the model will need to be initialized:

```python
context = mx.gpu() if mx.test_utils.list_gpus() else mx.cpu()
model = Model(16, train)
model.collect_params().initialize(mx.init.Xavier(), ctx=context)
```

We are going to save the state of the model periodically to a file. You'd then be able to load them with:

```python
model.load_params("model.mxnet", ctx=context)
```

The last bit of code that we need is the train ing procedure itself. We're going to code it as a function that take the model, the data iterator and the number of epochs and the learning rate:

```python
def fit(model, train, num_epoch, learning_rate):    
    trainer = Trainer(model.collect_params(), 'sgd', {'learning_rate': learning_rate})

    for epoch_id in range(num_epoch):
        batch_id = 0
        train.reset()
        
        for batch in train:
            with autograd.record():
                targets = F.concat(*batch.label, dim=0)
                predictions = model(batch.data)
                L = L2Loss()
                loss = L(predictions, targets)
                loss.backward()

            trainer.step(batch.data[0].shape[0])

            if (batch_id + 1) % 1000 == 0:                
                mean_loss = F.mean(loss).asnumpy()[0]

                logger.info(f'Epoch {epoch_id + 1} / {num_epoch} | Batch {batch_id + 1} | Mean Loss: {mean_loss}')

            batch_id += 1

        logger.info('Saving model parameters')
        model.save_params("model.mxnet")
```

Let's run the trainer for 10 epochs:

```python
fit(model, train, num_epoch=10, learning_rate=.05)
```

You should see the output similar to the one below:

```
INFO:root:Epoch 1 / 10 | Batch 1000 | Mean Loss: 1.8353286577621475e-05
INFO:root:Epoch 1 / 10 | Batch 2000 | Mean Loss: 0.00026763149071484804
INFO:root:Epoch 1 / 10 | Batch 3000 | Mean Loss: 0.00011451070167822763
INFO:root:Epoch 1 / 10 | Batch 4000 | Mean Loss: 0.006481964141130447
INFO:root:Epoch 1 / 10 | Batch 5000 | Mean Loss: 0.0004052179865539074

(...)

INFO:root:Epoch 10 / 10 | Batch 22000 | Mean Loss: 3.0491356661777047e-10
INFO:root:Epoch 10 / 10 | Batch 23000 | Mean Loss: 2.106314254957109e-12
INFO:root:Epoch 10 / 10 | Batch 24000 | Mean Loss: 1.0526101474825356e-12
INFO:root:Epoch 10 / 10 | Batch 25000 | Mean Loss: 8.65350542958443e-15
INFO:root:Epoch 10 / 10 | Batch 26000 | Mean Loss: 3.3907354701767645e-09
INFO:root:Epoch 10 / 10 | Batch 27000 | Mean Loss: 6.161449388891738e-12
INFO:root:Saving model parameters
```

## Using the trained latent feature matrices

To extract he latent matrices from the trained model we need to use the `collect_params` as shown below:

```python
user_embed = model.collect_params().get('embedding0_weight').data()
joke_embed = model.collect_params().get('embedding1_weight').data()
```

Let's see how the first user is represented in this latent matrix:

```python
> user_embed[0]

[ 0.00940212  0.00129892 -0.00468777  0.00196937 -0.00946468  0.0079565
 -0.00801473 -0.0075023  -0.00699834  0.00467664  0.00391158 -0.00587119
  0.00200101  0.00810665 -0.00443415 -0.00124632]
<NDArray 16 @cpu(0)>
```

And here is how the joke no 7 looks like:

```python
> joke_embed[7]

[-1.5784888   1.1132994  -0.02100371  0.47041285 -0.48450768  0.636578
 -0.65463674  0.8930625  -1.4069169   0.0397853  -1.556196   -0.92035794
  0.09348439  1.3967487   1.0877392   0.56826454]
<NDArray 16 @cpu(0)>
```

How would the user #0 score a joke #7?:

```python
> F.dot(user_embed[0], joke_embed[7]) * 10

[0.11154313]
<NDArray 1 @cpu(0)>
```

That's pretty neutral. To have a little bit more fun, let's create some code for reading the actual text of the jokes. The following class will handy when stripping HTML tags from the jokes file:

```python
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
```

Here's the function that reads the file and uses the HTML tags stripping class:

```python
def get_jokes():
    jokes = []
    joke = ''
    pattern = re.compile('^\\d+:$')
    with open("data/jester_items.dat", "r") as file:
        for line in file:
            if pattern.match(line):
                joke = ''
            else:
                if line.strip() == '':
                    jokes.append(strip_tags(joke).strip())
                else:
                    joke += line
    return jokes
```

Let's now read the jokes from the disk and what they look like:

```python
> jokes = get_jokes()
> jokes[7]

'Q. Did you hear about the dyslexic devil worshiper?\n\nA. He sold his soul to Santa.'
```

Okay, now I can see user #0's point here.

## Using the item feature vectors to find similar ones

One cool thing we can do with the latent representation of jokes, is that we can now measure how similar they are in terms of appealing to certain users.

To do that we can use a so-called **cosine similarity**. The subject is very clearly described by Christian S. Perone [in his blog post](http://blog.christianperone.com/2013/09/machine-learning-cosine-similarity-for-vector-space-models-part-iii/).

If you don't feel like reading it, let me just state that a cosine similarity makes use of the angle between the two vectors and returns its cosine. Notice that it only cares about the angle between the vectors, and **not** their magnitudes. The domain of the cosine function is `<-1, 1>` and so is for the *cosine similarity* as well.

We can trivially implement the function as a product of the dot products of the vectors normalized to units: 

```python
def cos_similarity(vec1, vec2):
    return mx.nd.dot(vec1, vec2) / (F.norm(vec1) * F.norm(vec2))
```

We can use the new measurement to rank the jokes in terms of it. Here's a function that takes a joke_id and returns list of ids along with the similarity ranks:

```python
def get_scores(joke_id):
    scores = []
    joke = joke_embed[joke_id]
    for ix in range(0, 150):
        scores.append((ix, cos_similarity(joke, joke_embed[ix]).asnumpy()[0]))
    return scores
```

The following function takes a joke_id and takes 4, most similar jokes. It then prints then one by one in a little summary:

```python
def print_joke_stats(ix):
		def sort_by_second(t):
		    if t[1] is None:
		        return -2
		    else:
		        return t[1]
    similar = get_scores(ix)
    similar.sort(key=sort_by_second)
    similar.reverse()
    
    print(f'Jokes making same people laugh compared to:\n\n=== \n{jokes[ix]}\n===:\n\n')

    for ix in range(1, 4):
        print(f'---\n{jokes[similar[ix][0]]}\n---\n')
```

Let's take some random joke as an example:

```python
> print_joke_stats(9)

Jokes making same people laugh compared to:

=== 
Two cannibals are eating a clown. One turns to the other and says:

"Does this taste funny to you?"
===:


---
Q. What's the difference between a man and a toilet?

A. A toilet doesn't follow you around after you use it.
---

---
What do you get when you run over a parakeet with a lawnmower?

Shredded tweet.
---

---
An explorer in the deepest Amazon suddenly finds himself surrounded by a bloodthirsty group of natives. Upon surveying the situation, he says quietly to himself, "Oh God, I'm screwed."

The sky darkens and a voice booms out, "No, you are NOT screwed. Pick up that stone at your feet and bash in the head of the chief standing in front of you."

So with the stone he bashes the life out of the chief. He stands above the lifeless body, breathing heavily and looking at 100 angry natives...

The voice booms out again, "Okay....NOW you're screwed."
---
```

Clearly we got a list of edgy jokes — similar in their "edginess" to the one given as an argument.

## Final words

The approach presented here is relatively simple. Provided that you have enough data for each item — it's surprisingly accurate.

In cases where you wouldn't have that much data though, the approach described in this article would inevitably degrade in its accuracy.

Accuracy isn't also the only goal. [Wikipedia page about the recommender systems](https://en.wikipedia.org/wiki/Recommender_system) lists e. g. "Serendipity" as an important factor in a successful system:

> Serendipity is a measure of "how surprising the recommendations are". For instance, a recommender system that recommends milk to a customer in a grocery store might be perfectly accurate, but it is not a good recommendation because it is an obvious item for the customer to buy. However, high scores of serendipity may have a negative impact on accuracy.

Researchers have been working on different approaches to tackling the above mentioned issues. E. g. Netflix is known to be using a so-called "Hybrid" approach — one that uses both content and collaborative based recommender. As per [Wikipedia](https://en.wikipedia.org/wiki/Recommender_system):

> Netflix is a good example of the use of hybrid recommender systems.[48] The website makes recommendations by comparing the watching and searching habits of similar users (i.e., collaborative filtering) as well as by offering movies that share characteristics with films that a user has rated highly (content-based filtering).

