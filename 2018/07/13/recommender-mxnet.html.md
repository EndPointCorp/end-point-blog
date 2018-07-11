# Blog → Recommender Systems via simple Matrix Factorization


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
        
        self.provide_data = [('user', (batch_size, )), ('item', (batch_size, ))]
        self.provide_label = [('rating', (self.batch_size, ))]
        
    @property
    def count_all(self):
        return len(self.data)
        
    @property
    def user_count(self):
        return len(self.all_user_ids)
    
    @property
    def item_count(self):
        return len(self.all_item_ids)
        
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
            ratings = self.data[index:endindex, 2]

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

        print('Loading examples...')

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
    def __init__(self, hidden, k, dataiter, **kwargs):
        super(Model, self).__init__(**kwargs)

        with self.name_scope():
            self.user_embedding = nn.Embedding(input_dim = dataiter.user_count, output_dim=k)
            self.item_embedding = nn.Embedding(input_dim = 150, output_dim=k)
            
            self.user_embed_act = nn.Activation('tanh')
            self.item_embed_act = nn.Activation('tanh')
            
            self.user_fc = nn.Dense(hidden, activation = 'tanh')
            self.item_fc = nn.Dense(hidden, activation = 'tanh')
            
            self.flatten = nn.Flatten()

    def forward(self, x):
        user = self.user_embedding(x[0])
        user = self.user_embed_act(user)
        user = self.user_fc(user)
        
        item = self.item_embedding(x[1])
        item = self.item_embed_act(item)
        item = self.item_fc(item)
        
        pred = user * item
        pred = F.sum_axis(pred, axis = 1)
        
        return self.flatten(pred)
```



```python
context = mx.gpu() if mx.test_utils.list_gpus() else mx.cpu()
model = Model(8, 8, train)
model.collect_params().initialize(mx.init.Xavier(), ctx=context)
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
fit(model, train, num_epoch=2, learning_rate=.05)
```

```
INFO:root:Epoch 1 / 2 | Batch 1000 | Mean Loss: 0.15913794934749603
INFO:root:Epoch 1 / 2 | Batch 2000 | Mean Loss: 0.17600205540657043
INFO:root:Epoch 1 / 2 | Batch 3000 | Mean Loss: 0.16867533326148987
INFO:root:Epoch 1 / 2 | Batch 4000 | Mean Loss: 0.14042142033576965
INFO:root:Epoch 1 / 2 | Batch 5000 | Mean Loss: 0.14513427019119263

(....)

INFO:root:Epoch 2 / 2 | Batch 21000 | Mean Loss: 0.10960876941680908
INFO:root:Epoch 2 / 2 | Batch 22000 | Mean Loss: 0.08507367223501205
INFO:root:Epoch 2 / 2 | Batch 23000 | Mean Loss: 0.08566252887248993
INFO:root:Epoch 2 / 2 | Batch 24000 | Mean Loss: 0.0738331750035286
INFO:root:Epoch 2 / 2 | Batch 25000 | Mean Loss: 0.08409106731414795
INFO:root:Epoch 2 / 2 | Batch 26000 | Mean Loss: 0.07854850590229034
INFO:root:Epoch 2 / 2 | Batch 27000 | Mean Loss: 0.0929383859038353
INFO:root:Saving model parameters
```

```python
model.load_params("model.mxnet", ctx=context)
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

 [-0.1940057   0.03230569 -0.04879944  0.04697262  0.10779835 -0.15459293
  -0.01924264  0.18142588]
 <NDArray 8 @cpu(0)>
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
def print_joke_stats(ix):
    def sort_by_second(t):
      if t[1] is None:
          return -2
      else:
          return t[1]

    similar = get_scores(ix)
    similar.sort(key=sort_by_second)
    similar.reverse()
    
    print(f'Jokes making same people laugh compared to:\n=== \n{jokes[ix]}===:\n\n')

    for ix in range(1, 4):
        print(f'---\n{jokes[similar[ix][0]]}\n---\n\n')
```


```python
print_joke_stats(2)
```

```
    Jokes making same people laugh compared to:
    === 
    Q. What's 200 feet long and has 4 teeth?
    
    A. The front row at a Willie Nelson concert.===:
    
    
    ---
    What a woman says: 
    "This place is a mess! C'mon,
    you and I need to clean up,
    your stuff is lying on the floor and
    you'll have no clothes to wear
    if we don't do laundry right now!"
    
    What a man hears: 
    "blah, blah, blah, blah, C'mon
    blah, blah, blah, blah, you and I
    blah, blah, blah, blah, on the floor
    blah, blah, blah, blah, no clothes
    blah, blah, blah, blah, right now!"
    ---
    
    
    ---
    A lady bought a new Lexus. It cost a bundle. Two days later, she brought it back, complaining that the radio was not working.
    
    "Madam," said the sales manager, "the audio system in this car is completely automatic. All you need to do is tell it what you want to listen to, and you will hear exactly that!"
    
    She drove out, somewhat amazed and a little confused. She looked at the radio and said, "Nelson." The radio responded, "Ricky or Willie?" She was astounded. If she wanted Beethoven, that's what she got. If she wanted Nat King Cole, she got it.
    
    She was stopped at a traffic light enjoying "On the Road Again" when the light turned green and she pulled out. Suddenly an enormous sports utility vehicle coming from the street she was crossing sped toward her, obviously not paying attention to the light. She swerved and narrowly missed a collision.
    
    "Idiot!" she yelled and, from the radio, "Ladies and gentlemen, the President of the United States."
    ---
    
    
    ---
    What do you get when you run over a parakeet with a lawnmower?
    
    Shredded tweet.
    ---
```



```python
def predict_laughter(user_id, joke_id):
    user = mx.nd.array([user_id])
    joke = mx.nd.array([joke_id])
    return model([user, joke]).asnumpy()[0][0] * 10
```


```python
> predict_laughter(5, 77)

2.370649129152298

> jokes[77]

"Q: What's the difference between the government and the Mafia?\n\nA: One of them is organized."
```



