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

        print('Loading examples...')

        with open("data/jester_ratings.dat", "r") as file:
            for line in file:
                user_id, _, item_id, _, rating = line.strip().split("\t")

                user_ids.append(int(user_id))
                item_ids.append(int(item_id))
                ratings.append(float(rating) / 10.0)

        return np.asarray(list(zip(user_ids, item_ids, ratings)), dtype='float32')
    
    all_raw = get_all_raw_data()
    
    return DataIter(all_raw,  batch_size = batch_size)
```

Notice that I'm dividing each rating by `10` to scale the ratings from `<-10,10>` to `<-1,1>`. I did this because I found the process hitting overflows when using e. g. the `Adam` optimizer.

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
        user = self.user_embedding(x[0] - 1)
        item = self.item_embedding(x[1] - 1)
        
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
def fit(model, train, num_epoch):    
    trainer = Trainer(model.collect_params(), 'adam')

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
INFO:root:Epoch 1 / 10 | Batch 1000 | Mean Loss: 0.11189080774784088
INFO:root:Epoch 1 / 10 | Batch 2000 | Mean Loss: 0.12274568527936935
INFO:root:Epoch 1 / 10 | Batch 3000 | Mean Loss: 0.1204155907034874
INFO:root:Epoch 1 / 10 | Batch 4000 | Mean Loss: 0.12192331254482269

(...)

INFO:root:Epoch 10 / 10 | Batch 24000 | Mean Loss: 0.0003094784333370626
INFO:root:Epoch 10 / 10 | Batch 25000 | Mean Loss: 0.0006345464498735964
INFO:root:Epoch 10 / 10 | Batch 26000 | Mean Loss: 0.0007207655580714345
INFO:root:Epoch 10 / 10 | Batch 27000 | Mean Loss: 0.005522257648408413
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

[ 0.11911439 -0.01560098 -0.26248184  0.5341552   1.3078408  -0.82505447
  0.2181341   0.69577765 -0.22569533 -0.7669992   0.14042236  0.78608125
  0.07242275  0.49357334  0.7525147   0.37984315]
<NDArray 16 @cpu(0)>
```

And here is how the joke no 7 looks like:

```python
> joke_embed[7]

[ 0.11836094  0.14039275 -0.10859593 -0.13673168  0.14074579 -0.18800738
  0.0463879  -0.09659509  0.1629943   0.02109279 -0.0294639  -0.03487734
 -0.18192524 -0.13103536 -0.10280509  0.14753008]
<NDArray 16 @cpu(0)>
```

Let's first test to see if the known values got reconstructed:

```python
> F.dot(user_embed[0], joke_embed[7]) * 10

[-9.26895]
<NDArray 1 @cpu(0)>
```

Comparing it with the value from the file:

```bash
> cat data/jester_ratings.dat | rg "^1\t\t8\t"
1               8               -9.281
```

That's close enough. Let's now get the set of all joke ids that the first user ranked:

```python
test = get_data(1)
joke_ids = set()
for batch in test:
    user_id, joke_id = batch.data
    if user_id.asnumpy()[0] == 1:
        joke_ids.add(joke_id.asnumpy()[0])
joke_ids
```

Which outputs:

```python
{5.0, 7.0, 8.0, 13.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 29.0, 31.0, 32.0, 34.0, 35.0, 36.0, 42.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 61.0, 62.0, 65.0, 66.0, 68.0, 69.0, 72.0, 76.0, 80.0, 81.0, 83.0, 87.0, 89.0, 91.0, 92.0, 93.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0, 118.0, 119.0, 120.0, 121.0, 123.0, 127.0, 128.0, 134.0}
```

Because we're mostly interested in the items that have not been yet rated by the user, we'd like to see what the model gathered about them in this context:

```python
> sorted([ (i, F.dot(user_embed[0], joke_embed[i]).asnumpy()[0] * 10) for i in range(0, 150) if i + 1 not in joke_ids ], key=lambda x: x[1])

[(100, -25.34627914428711),
 (89, -23.647150993347168),
 (63, -23.543219566345215),
 (94, -23.415722846984863),
 (70, -22.017195224761963),
 (93, -21.375732421875),
 (140, -20.033082962036133),
 (81, -18.813319206237793),
 (40, -18.48101019859314),
 (135, -18.216774463653564),
 (39, -16.993610858917236),
 (123, -16.66216731071472),
 (45, -16.03758215904236),
 (59, -15.045435428619385),
 (43, -14.993469715118408),
 (74, -12.132725715637207),
 (72, -11.94629430770874),
 (76, -11.861177682876587),
 (29, -11.831218004226685),
 (114, -11.82992935180664),
 (38, -11.327273845672607),
 (98, -10.9122633934021),
 (62, -9.507511854171753),
 (32, -9.498740434646606),
 (83, -9.442780017852783),
 (56, -9.361632466316223),
 (78, -9.310351014137268),
 (109, -8.428668975830078),
 (77, -8.131155967712402),
 (47, -7.274705171585083),
 (99, -7.204542756080627),
 (42, -7.091279625892639),
 (69, -6.739482879638672),
 (57, -6.623743772506714),
 (96, -6.209834814071655),
 (134, -5.58724582195282),
 (73, -5.530622601509094),
 (110, -5.126549005508423),
 (131, -4.435622692108154),
 (9, -4.142558574676514),
 (46, -3.7173447012901306),
 (13, -3.1510373950004578),
 (44, -2.9845643043518066),
 (124, -2.7145612239837646),
 (137, -2.2213394939899445),
 (132, -2.2054636478424072),
 (116, -1.9229638576507568),
 (111, -1.9177806377410889),
 (121, -1.3515384495258331),
 (36, -1.119830161333084),
 (2, -1.0263845324516296),
 (136, -0.14549612998962402),
 (97, 0.02288222312927246),
 (138, 0.23310404270887375),
 (11, 0.34488800913095474),
 (1, 0.3801669552922249),
 (95, 0.42442888021469116),
 (5, 0.585017055273056),
 (0, 0.6578207015991211),
 (10, 1.0580871254205704),
 (148, 1.101222038269043),
 (85, 1.5351229906082153),
 (8, 1.8577364087104797),
 (129, 2.067573070526123),
 (84, 2.5856217741966248),
 (125, 2.927420735359192),
 (145, 3.010193407535553),
 (3, 3.240116238594055),
 (112, 3.8082027435302734),
 (115, 3.8878047466278076),
 (147, 4.29826945066452),
 (58, 5.724080801010132),
 (144, 6.969168186187744),
 (130, 7.328435778617859),
 (146, 8.421227931976318),
 (149, 8.71802568435669),
 (27, 10.014463663101196),
 (143, 10.086603164672852),
 (113, 11.049185991287231),
 (66, 11.210532188415527),
 (139, 11.213960647583008),
 (142, 11.479517221450806),
 (128, 11.862180233001709),
 (141, 12.742302417755127),
 (54, 13.011351823806763),
 (55, 16.884247064590454),
 (37, 18.53071689605713),
 (87, 23.8028883934021)]
```

The above output presents joke ids along with the predicted user #1 rating. We can see that some values fall outside of the `<-10, 10>` range which is fine. We can simply treat the smaller than `-10` ones as `-10` and greater than `10` as `10`.

Immediately we can see that with this recommender model we could recommend the jokes: `146, 149, 27, 143, 113, 66, 139, 142, 128, 141, 54, 55, 37, 87`.

To have a little bit more fun, let's create some code for reading the actual text of the jokes. The following class will handy when stripping HTML tags from the jokes file:

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

Let's now read the jokes from the disk and see one of the jokes our system would recommend to the first user:

```python
> jokes = get_jokes()
> jokes[87]

'A Czechoslovakian man felt his eyesight was growing steadily worse, and felt it was time to go see an optometrist.\n\nThe doctor started with some simple testing, and showed him a standard eye chart with letters of diminishing size: CRKBNWXSKZY...\n\n"Can you read this?" the doctor asked.\n\n"Read it?" the Czech answered. "Doc, I know him!"'
```

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

Let's see what jokes our system found to be cracking up the same kinds of people:

```python
> print_joke_stats(87)

Jokes making same people laugh compared to:

=== 
A Czechoslovakian man felt his eyesight was growing steadily worse, and felt it was time to go see an optometrist.

The doctor started with some simple testing, and showed him a standard eye chart with letters of diminishing size: CRKBNWXSKZY...

"Can you read this?" the doctor asked.

"Read it?" the Czech answered. "Doc, I know him!"
===:

---
A woman has twins, and gives them up for adoption. One of them goes to a family in Egypt and is named "Amal." The other goes to a family in Spain; they name him "Juan." Years later, Juan sends a picture of himself to his mom. Upon receiving the picture, she tells her husband that she wishes she also had a picture of Amal.

Her husband responds, "But they are twins--if you've seen Juan, you've seen Amal."
---

---
An explorer in the deepest Amazon suddenly finds himself surrounded by a bloodthirsty group of natives. Upon surveying the situation, he says quietly to himself, "Oh God, I'm screwed."

The sky darkens and a voice booms out, "No, you are NOT screwed. Pick up that stone at your feet and bash in the head of the chief standing in front of you."

So with the stone he bashes the life out of the chief. He stands above the lifeless body, breathing heavily and looking at 100 angry natives...

The voice booms out again, "Okay....NOW you're screwed."
---

---
A man is driving in the country one evening when his car stalls and won't start. He goes up to a nearby farm house for help, and because it is suppertime he is asked to stay for supper. When he sits down at the table he notices that a pig is sitting at the table with them for supper and that the pig has a wooden leg.

As they are eating and chatting, he eventually asks the farmer why the pig is there and why it has a wooden leg.
"Oh," says the farmer, "that is a very special pig. Last month my wife and daughter were in the barn when it caught fire. The pig saw this, ran to the barn, tipped over a pail of water, crawled over the wet floor to reach them and pulled them out of the barn safely. A special pig like that, you just don't eat it all at once!"
---
```

## Final words

The approach presented here is relatively simple. Provided that you have enough data for each item — it's surprisingly accurate.

In cases where you wouldn't have that much data though, the approach described in this article would inevitably degrade in its accuracy.

Accuracy isn't also the only goal. [Wikipedia page about the recommender systems](https://en.wikipedia.org/wiki/Recommender_system) lists e. g. "Serendipity" as an important factor in a successful system:

> Serendipity is a measure of "how surprising the recommendations are". For instance, a recommender system that recommends milk to a customer in a grocery store might be perfectly accurate, but it is not a good recommendation because it is an obvious item for the customer to buy. However, high scores of serendipity may have a negative impact on accuracy.

Researchers have been working on different approaches to tackling the above mentioned issues. E. g. Netflix is known to be using a so-called "Hybrid" approach — one that uses both content and collaborative based recommender. As per [Wikipedia](https://en.wikipedia.org/wiki/Recommender_system):

> Netflix is a good example of the use of hybrid recommender systems.[48] The website makes recommendations by comparing the watching and searching habits of similar users (i.e., collaborative filtering) as well as by offering movies that share characteristics with films that a user has rated highly (content-based filtering).

