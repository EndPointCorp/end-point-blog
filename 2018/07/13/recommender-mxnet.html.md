# Blog → Recommender Systems via simple Matrix Factorization

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

That's a **huge** saving. It goes with the small increase in the cost of there information retrieval. With matrices `A` and `B`, to infer the rating from `C` you need a **dot product** of the corresponding row and column of those matrices.

## Factorizing the user / item matrix in practice



```python
from mxnet.gluon import Block, nn, Trainer
from mxnet.gluon.loss import L2Loss, L1Loss
from mxnet import autograd, ndarray as F
import mxnet as mx

from sklearn.preprocessing import minmax_scale
import numpy as np
import random
import logging
import sys
import re
```


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

```python
train = get_data(64)
```

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


```python
context = mx.gpu() if mx.test_utils.list_gpus() else mx.cpu()
model = Model(16, train)
model.collect_params().initialize(mx.init.Xavier(), ctx=context)
```


```python
model.load_params("model.mxnet", ctx=context)
```


```python
def fit(model, train, num_epoch, learning_rate):    
    trainer = Trainer(model.collect_params(), 'sgd', {'learning_rate': learning_rate})
    rmse = mx.metric.RMSE()

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


```python
fit(model, train, num_epoch=10, learning_rate=.05)
```



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



```python
user_embed = model.collect_params().get('embedding0_weight').data()
joke_embed = model.collect_params().get('embedding1_weight').data()
```



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


```python
jokes = get_jokes()
```


```python
> jokes[0]

'A man visits the doctor. The doctor says, "I have bad news for you. You have cancer and Alzheimer\'s disease".\n\nThe man replies, "Well, thank God I don\'t have cancer!"'
```


```python
> joke_embed[0]

[-0.02011569 -0.1868052   0.16420332  0.06995389 -0.02797213  0.10479802
  0.07839763 -0.07516536 -0.05363695  0.03807874 -0.1073292  -0.13022287
  0.09191594  0.00539801 -0.07646554  0.09778512]
 <NDArray 16 @cpu(0)>
```


```python
def cos_similarity(vec1, vec2):
    return mx.nd.dot(vec1, vec2) / (F.norm(vec1) * F.norm(vec2))
```



```python
def abs_id_to_rel(abs_id):
    try:
        return list(train.all_item_ids).index(abs_id)
    except Exception as e:
        return None
```


```python
def get_scores(rel_id):
    scores = []
    joke = joke_embed[rel_id]
    for ix in range(0, 150):
        rel_id = abs_id_to_rel(ix)
        if rel_id is None:
            scores.append((ix, None))
        else:
            scores.append((ix, cos_similarity(joke, joke_embed[rel_id]).asnumpy()[0]))
    return scores
```


```python
def sort_by_second(t):
    if t[1] is None:
        return -2
    else:
        return t[1]
```


```python
def print_joke_stats(ix):
    similar = get_scores(ix)
    similar.sort(key=sort_by_second)
    similar.reverse()
    
    print(f'Jokes making same people laugh compared to:\n=== \n{jokes[ix]}\n===:\n\n')

    for ix in range(1, 4):
        print(f'---\n{jokes[similar[ix][0]]}\n---\n\n')
```


```python
print_joke_stats(9)
```

```
    Jokes making same people laugh compared to:
    === 
    Two cannibals are eating a clown. One turns to the other and says:
    
    "Does this taste funny to you?"
    ===:
    
    
    ---
    The father was very anxious to marry off his only daughter so he wanted to impress her date. "Do you like to screw?" he asks. "Huh?" replied the surprised first date. "My daughter, she loves to screw and she's good at it: you and her should go screw," the father carefully explained. Now very interested, the boy replied, "Yes, sir." Minutes later the girl came down the stairs, kissed her father goodbye and the couple left. After only a few minutes she reappeared, furious, dress torn, hair a mess and screamed, "Dammit, Daddy, it's the TWIST, get it straight!"
    ---
    
    
    ---
    A couple has been married for 75 years. For the husband's 95th birthday, his wife decides to surprise him by hiring a prostitute. That day, the doorbell rings. The husband uses his walker to get to the door and opens it.
    
    A 21-year-old in a latex outfit smiles and says, "Hi, I here to give you super sex!"
    
    The old man says, "I'll take the soup."
    ---
    
    
    ---
    A man piloting a hot air balloon discovers he has wandered off course and is hopelessly lost. He descends to a lower altitude and locates a man down on the ground. He lowers the balloon further and shouts, "Excuse me, can you tell me where I am?"
    
    The man below says, "Yes, you're in a hot air balloon, about 30 feet above this field."
    
    "You must work in Information Technology," says the balloonist.
    
    "Yes I do," replies the man. "And how did you know that?"
    
    "Well," says the balloonist, "what you told me is technically correct, but of no use to anyone."
    
    The man below says, "You must work in management."
    
    "I do," replies the balloonist, "how did you know?"
    
    "Well," says the man, "you don't know where you are, or where you're going, but you expect my immediate help. You're in the same position you were before we met, but now it's my fault!"
    ---
```
    


```python
def predict_rating(user_id, joke_id):
    user = mx.nd.array([user_id])
    joke = mx.nd.array([joke_id])
    return model([user, joke]).asnumpy()[0] * 10
```


```python
> jokes[77]

"Q: What's the difference between the government and the Mafia?\n\nA: One of them is organized."
```



```python
> predict_rating(5, 77)

0.9022721648216248
```



```python
> F.dot(user_embed, joke_embed.T)[5, 77]

[0.0902272]
<NDArray 1 @cpu(0)>
```


```python
> F.sum(user_embed[5] * joke_embed[77])

[0.09022722]
<NDArray 1 @cpu(0)>
```



```python
> F.dot(user_embed[5], joke_embed[77])

[0.09022722]
<NDArray 1 @cpu(0)>
```

