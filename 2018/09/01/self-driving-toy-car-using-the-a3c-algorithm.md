# Self driving toy car using the Asynchronous Advantage Actor-Critic algorithm

The field of [Reinforcement Learning](https://en.wikipedia.org/wiki/Reinforcement_learning) has seen a lot of great improvement in the past years. Researchers at Universities and companies like [Deep Mind](https://deepmind.com/) have been developing new and better ways to train intelligent, artificial agents to solve more and more difficult tasks. The algorithms being developed are requiring less and less time to train. They also are making the training more and more stable.

This article is about an algorithm that's one of the most cited lately: A3C - Asynchronous Advantage Actor Critic.

As the subject is both wide and deep, I'm assuming the reader has the relevant background mastered already. The following is a rough list of subjects that this article builds upon:

* [Neural Networks](https://en.wikipedia.org/wiki/Artificial_neural_network)
* [Basics of Reinforcement Learning](https://en.wikipedia.org/wiki/Reinforcement_learning)
* Experience Replay
* n-step
* OpenAI gym

## Theory

The A3C algorithm is part of the greater class of RL algorithms called [Policy Gradients](http://www.scholarpedia.org/article/Policy_gradient_methods).

In this approach, we're creating a model that **approximates the action-choosing policy itself**.

Let's contrast it with in e.g [Value Iteration](https://en.wikipedia.org/wiki/Markov_decision_process#Value_iteration). The goal of value iteration is to learn the [value function](https://en.wikipedia.org/wiki/Reinforcement_learning#Value_function) and have policy emerge as the function that chooses an action that transitions to the state of the greatest value.

In the policy gradient method, we're approximating the policy with a differentiable function. Such stated problem requires only a good approximation of the gradient that over time will maximize the rewards.

The unique approach of A3C adds a very clever twist: we're also learning an approximation of the value function at the same time. This helps us in getting the variance of the gradient down considerably, making the training much more stable.

These two aspects of the algorithm are being personified within its name: actor — critic. The policy function approximation is being called the actor, while the value function is being called the critic.

### The policy gradient

As we've noticed already, in order to improve our policy function approximation, we need a gradient that points at the direction that maximizes the rewards.

I'm not going to reinvent the wheel here. There are some great resources the reader can access to dig deep into the Mathematics of what's called the Policy Gradient Theorem:

* [Lilian Weng's excellent article](https://lilianweng.github.io/lil-log/2018/04/08/policy-gradient-algorithms.html)
* [Sutton & Barto - Reinforcement Learning: An Introduction](http://incompleteideas.net/book/bookdraft2017nov5.pdf)

The following equation presents the basic form of the gradient of the policy function:

$$\nabla_{\theta} J(\theta) = E_{\tau}[\,R_{\tau}\cdot\nabla_\theta\,\sum_{t=0}^{T-1}\,log\,\pi(a_t|s_t;\theta)\,]$$

This states that for each sampled trajectory $\tau$, the correct estimate of the gradient is the expected value of the rewards times the action probabilities moved into the log space. Ascending in this direction makes our rewards greater and greater over time.

You **can** derive all the needed intermediary gradients yourself by hand. In this article, I'm using [PyTorch](https://pytorch.org) though. With this approach, all I need to get the gradients for the sampled trajectory is the right loss function.

It's important to notice in the above equation that the **$R_\tau$ is being treated as a constant**. Let's figure out the right loss function formula that will produce the above stated gradient:

$$L_\theta=-J(\theta)$$

Also:

$$J(\theta)=E_\tau[R_\tau\cdot\sum_{t=0}^{T-1}\,log\,\pi(a_t|s_t;\theta)]$$

Hence:

$$L_\theta=-\frac{1}{n}\sum_{t=0}^{n-1}R_t\cdotlog\pi(a_t|s_t;\theta)$$

#### Formalizing the accumulation of rewards

For now we've been using the $R_\tau$ or $R_t$ terms in the equations. Let's make this part more intuitive and concrete now.

It's true meaning really is "the quality of the sampled trajectory". This should ring a bell and the following equation should immediately make sense:

$$R_t=\sum_{i=t}^{N+t}\gamma^{t-i}r_i\,+\,\gamma^{t+1-i}V(s_{N+1})$$

If it's still too cryptic let me explain. Each trajectory consists of multiple steps. Each time, we're sampling actions based on our policy function (which gives probabilities of a given action being best given the state).

What if we're taking 5 actions for which we're not being given any reward but overall it helped us get rewarded in the 6th step? This is exactly the case we'll be dealing with in this article later when training a toy car to drive based only on pixel values of the scene. In that environment, we'll be given $-0.1$ "negative" reward each step and something close to $7$ each new "tile" the car stays on the road.

We need a way to still reward the actions that after all make us earn rewards. We also need to be smart and **discount** future rewards somewhat so that the more immediate the reward is to our action — the more emphasis we put on it.

That's exactly what the above equation does. Notice that $\gamma$ becomes a hyper parameter now. It makes sense to give it value from $(0, 1)$.

We've said that in A3C we learning the value function at the same time. The $R_t$ as described above becomes the target value when training our $V(s)$. The value function becomes an approximation of the average of the rewards given the state (because $R_t$ depends on us sampling actions in this state).

### Making the gradients more stable

One of the greatest inhibitors of the policy gradient methods performance is what's broadly called: "high variance".

I have to admit, the first time I saw that term in this context, I was disoriented. I knew what "variance" was. It's the "variance of what" that was not clear to me.

Thankfully I found [a brilliant answer to this question](https://www.quora.com/Why-does-the-policy-gradient-method-have-a-high-variance?share=1). It explains the issue simply yet in detail.

Let me cite it here:

> When we talk about high variance in the policy gradient method, we’re specifically talking about the facts that the variance of the gradients are high - namely, that $Var(\nabla_{\theta} J(\theta))$ is big.

To put it in simple terms: because we're **sampling** trajectories from the space that is stochastic in nature, we're bound to have those samples give gradients that disagree a lot on the best direction to take our model's parameters into.

I encourage the reader to pause now and read the above mentioned answer as its very vital. The gist of the solution described in it, is that we can **subtract a baseline value from each $R_t$**. An example of a good baseline that was given was to make it into an **average of the sampled accumulated rewards**. The A3C algorithm uses this insight in a very, very clever way.

##### Value function as a baseline

We've said that in A3C we're also learning the approximation of the value function. We're typically using the MSE or Huber loss against the accumulated rewards for each step. This means that over time we're **averaging those rewards out based on the state we're finding ourselves in**.

Improving our gradient formula with those ideas we now get:

$$\nabla_{\theta} J(\theta) = E_{\tau}[\,\nabla_\theta\,\sum_{t=0}^{T-1}\,log\,\pi(a_t|s_t;\theta)\cdot(R_t-V(s_t))\,]$$

This is where we're getting the word "advantage" in the algorithm's name. The **advantage** is simply the difference between the accumulated rewards and what those rewards are **on average** for the given state:

$$A(a_{t,t+1,...},s_{t,t+1,...})=R_t(a_{t,t+1,...},s_{t,t+1,...})-V(s_t)$$

If we'll make $R_t$ into $Q(s,a)$ as it's commonly written in literature, we'll arrive at the formula often found over there as well:

$$A(s,a)=Q(s,a) - V(s)$$

What's the intuition here? Imagine that you're playing chess with a 5 year old. You win by a huge margin. Your friend that watches it though says that you still made lots of mistakes and that your 5 year old rival in 8 years has better chances to play better than you still. You've got your **critic** in this situation. Your score and what it looks like for the "observing critic" combined is what we call the advantage of the actions you took.

#### Guarding against the model's overconfidence

> Although he was warned, Icarus was too young and too enthusiastic about flying. He got excited by the thrill of flying and carried away by the amazing feeling of freedom and started flying high to salute the sun, diving low to the sea, and then up high again.
> His father Daedalus was trying in vain to make young Icarus to understand that his behavior was dangerous, and Icarus soon saw his wings melting.
> Icarus fell into the sea and drowned. The Icarian Sea, where he fell, was named after him and there is also a nearby small island called Icaria.

*[The Myth Of Daedalus And Icarus ( www.greekmyths-greekmythology.com )](https://www.greekmyths-greekmythology.com/myth-of-daedalus-and-icarus/)*

The job of an "actor" is to output probability values for each possible action the agent can take. The greater the probability, the greater model's confidence that this action will result in the highest reward.

What if at any point of the training process, the weights are being steered in a way that the model becomes *overconfident* of some particular action?

Let's look at the gradient formula again:

$$\nabla_{\theta} J(\theta) = E_{\tau}[\,\nabla_\theta\,\sum_{t=0}^{T-1}\,log\,\pi(a_t|s_t;\theta)\cdot(R_t-V(s_t))\,]$$

We can see that the term $\nabla_\thetalog\,\pi(a_t|s_t;\theta)$ scales the resulting overall gradient.

Let's look at the $log(x)$ and $\frac{d}{dx}log(x)$ functions graphs:

/log-deriv.png

The "overconfidence" case happens when our $\pi(a|s;\theta)$ approaches more and more $1$. Notice that the closer it is to this value, the **smaller the gradient**. With smaller gradient, the learning itself becomes slower.

Empirically, I have found myself seeing the process sometimes not even able to escape the "overconfidence" area at all.

Even in cases when the training **is** able to escape that area, it's still not desirable to be too confident of any action - at least early in the training. Why is that so? Because we're using the $\pi(a|s;\theta)$ distribution to sample trajectories with. We're not sampling totally at random. Instead we're using the probabilities to mark the more likely ones. In other words, for $\pi(a|s;\theta) = [0.1, 0.4, 0.2, 0.3]$ our sampling chooses the second option 40% of the time. With any action overwhelming the others, we're loosing the ability to **explore** different paths and thus learn valuable lessons.

#### Regularizing with entropy

Let's introduce the notion of an [entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory)).

In simple words in our case, it's the measure of how much "knowledge" does given probability posses. It's being maximized for the uniform distribution. Here's the formula:

$$H(X)=E[-log_b(P(X))]$$

This expands to the following:

$$H(X)=-\sum_{i=1}^{n}P(x_i)log_b(P(x_i))$$

Let's look closer at the values this functions produce using some simple [Calca](http://calca.io) code:

```calca
uniform = [0.25, 0.25, 0.25, 0.25]
more confident = [0.5, 0.25, 0.15, 0.10]
over confident = [0.95, 0.01, 0.01, 0.03]
super over confident = [0.99, 0.003, 0.004, 0.003]

y(x) = x*log(x, 10)

entropy(dist) = -sum(map(y, dist))

entropy (uniform) => 0.6021
entropy (more confident) => 0.5246
entropy (over confident) => 0.1068
entropy (super over confident) => 0.0291
```

We can use the above to "punish" the model whenever it's too confident of its choices. As we're going to use gradient descend, we'll be minimizing terms that appear in our loss function. Minimizing the entropy as shown above would encourage more confidence though. We'll need to make it into a negative in the loss to work the way we intend:

 $$L_\theta=-\frac{1}{n}\sum_{t=0}^{n-1}log\pi(a_t|s_t;\theta)\cdot(R_t-V(s_t))\,+\betaH(\pi(a_t|s_t;\theta))$$
 
 Where $\beta$ is a hyper parameter scaling the effects of the penalty that the entropy has on the gradients.

### The last A in A3C

So far we've went from the vanilla policy gradients to using the notion of an advantage. We've also improved it with the baseline that intuitively makes the model consist of two parts: the actor and the critic. At this point we have what's sometimes called the A2C - Advantage Actor - Critic.

Let us now focus on the last piece of the puzzle: the last A. This last A comes from the word "asynchronous". It's being explained very clearly in the [original paper on A3C](https://arxiv.org/pdf/1602.01783).

This idea, in my humble opinion is the least complex of all that have their place within the approach. I'll just comment on what was already written:

> These approaches share a common idea: the sequence of observed data en- countered by an online RL agent is non-stationary, and on-
> line RL updates are strongly correlated. By storing the agent’s data in an experience replay memory, the data can be batched (Riedmiller, 2005; Schulman et al., 2015a) or randomly sampled (Mnih et al., 2013; 2015; Van Hasselt et al., 2015) from different time-steps. Aggregating over memory in this way reduces non-stationarity and decorre- lates updates, but at the same time limits the methods to off-policy reinforcement learning algorithms.

The A3C unique approach is that it doesn't use experience replay for de-correlating the updates to the weights of the model. Instead, we're sampling many different trajectories **at the same time** in an **asynchronous** manner.

This means that we're creating many clones of the environment and we let our agents experience them at the same time. Separate agents share their weights in one way or another. There are implementations with agents sharing those weights very **literally** — and performing the updates to the weights on their own whenever they need to. There also are implementations with one main agent holding the main weights and doing the updates based on the gradients reported by the "worker" agents. The worker agents are then being updated with the evolved weights. The environments and agents are not being directly synchronized, working at their own speed. As soon as any of them collects the needed rewards to perform the n-step gradients calculations, the gradients are being applied in one way or another.

In this article I'm preferring the second approach - having one "main" agent that does the weights updates on its own thread.

## Practice

### The challenge

To present the above theory in practical terms, we're going to code the A3C to train a toy self driving game car. The algorithm will only have game's pixels as inputs. We're also going to collect rewards. 

Each step, the player will decide how to move the steering wheel, how much throttle to apply and how much brake.

Points are being assigned for each new “tile” that the car enters staying within the road. There’s a small penalty for each other case of $-0.1$ points.

We're going to use [OpenAI Gym](https://gym.openai.com) and the environment's called [CarRacing](https://gym.openai.com/envs/CarRacing-v0/).

You can read a bit more about the setup in the environment's source code on [GitHub](https://github.com/openai/gym/blob/master/gym/envs/box2d/car_racing.py).

### Coding the Agent

Our agent is going to output both $\pi(a|s;\theta)$ as well as $V(s)$. We're going to use the GRU unit to give the agent ability to remember it's previous actions and environments previous features.

I've also decided to use PRelu instead of Relu activations as it  **appeared** to me that this way the agent was  learning much quicker (although I don't have any numbers to back this impression up).

**Disclaimer**: the code presented below **has not been refactored** in any way. If this was going to be used in production I'd certainly hugely clean it up.

Here's the full listing of the agent's class:

```python
class Agent(nn.Module):
    def __init__(self, **kwargs):
        super(Agent, self).__init__(**kwargs)

        self.init_args = kwargs

        self.h = torch.zeros(1, 256)

        self.norm1 = nn.BatchNorm2d(4)
        self.norm2 = nn.BatchNorm2d(32)

        self.conv1 = nn.Conv2d(4, 32, 4, stride=2, padding=1)
        self.conv2 = nn.Conv2d(32, 32, 3, stride=2, padding=1)
        self.conv3 = nn.Conv2d(32, 32, 3, stride=2, padding=1)
        self.conv4 = nn.Conv2d(32, 32, 3, stride=2, padding=1)

        self.gru = nn.GRUCell(1152, 256)
        self.policy = nn.Linear(256, 4)
        self.value = nn.Linear(256, 1)

        self.prelu1 = nn.PReLU()
        self.prelu2 = nn.PReLU()
        self.prelu3 = nn.PReLU()
        self.prelu4 = nn.PReLU()

        nn.init.xavier_uniform_(self.conv1.weight, gain=nn.init.calculate_gain('leaky_relu'))
        nn.init.constant_(self.conv1.bias, 0.01)
        nn.init.xavier_uniform_(self.conv2.weight, gain=nn.init.calculate_gain('leaky_relu'))
        nn.init.constant_(self.conv2.bias, 0.01)
        nn.init.xavier_uniform_(self.conv3.weight, gain=nn.init.calculate_gain('leaky_relu'))
        nn.init.constant_(self.conv3.bias, 0.01)
        nn.init.xavier_uniform_(self.conv4.weight, gain=nn.init.calculate_gain('leaky_relu'))
        nn.init.constant_(self.conv4.bias, 0.01)
        nn.init.constant_(self.gru.bias_ih, 0)
        nn.init.constant_(self.gru.bias_hh, 0)
        nn.init.xavier_uniform_(self.policy.weight, gain=nn.init.calculate_gain('leaky_relu'))
        nn.init.constant_(self.policy.bias, 0.01)
        nn.init.xavier_uniform_(self.value.weight, gain=nn.init.calculate_gain('leaky_relu'))
        nn.init.constant_(self.value.bias, 0.01)

        self.train()

    def reset(self):
        self.h = torch.zeros(1, 256)

    def clone(self, num=1):
        return [ self.clone_one() for _ in range(num) ]

    def clone_one(self):
        return Agent(**self.init_args)

    def forward(self, state):
        state = state.view(1, 4, 96, 96)
        state = self.norm1(state)

        data = self.prelu1(self.conv1(state))
        data = self.prelu2(self.conv2(data))
        data = self.prelu3(self.conv3(data))
        data = self.prelu4(self.conv4(data))

        data = self.norm2(data)
        data = data.view(1, -1)

        h = self.gru(data, self.h)
        self.h = h.detach()

        pre_policy = h.view(-1)

        policy = F.softmax(self.policy(pre_policy))
        value = self.value(pre_policy)

        return policy, value
```

Next, I wanted to abstract out the notion of the "runner". It encapsulates the idea of a "running agent". Think of it as the game player — with the joystick and its brain to score game points:

```python
class Runner:
    def __init__(self, agent, ix, train = True, **kwargs):
        self.agent = agent
        self.train = train
        self.ix = ix
        self.reset = False
        self.states = []

        self.env = gym.make('CarRacing-v0')

    def get_value(self):
        _input = self.preprocess(self.states)
        _, _, _, value = self.decide(_input, 9999)
        return value

    def run_episode(self, yield_every = 10, do_render = False):
        self.reset = False
        step_ix = 0

        rewards, values, policies, actions = [[], [], [], []]

        self.env.reset()
        states = deque([ ])

        while len(states) < 4:
            _, r, _, _ = self.env.step([0.0, 0.0, 1.0])
            state = self.env.render(mode='rgb_array')
            states.append(state)
            logger.info('Init reward ' + str(r) )

        while True:
            _input = self.preprocess(states)
            action, action_ix, policy, value = self.decide(_input, step_ix)
            _, reward, terminal, _ = self.env.step(action)
            state = self.env.render(mode='rgb_array')

            states.append(state)
            while len(states) > 4:
                states.popleft()

            if do_render:
                self.env.render()

            self.states = states
            step_ix += 1

            rewards.append(reward)
            values.append(value)
            policies.append(policy)
            actions.append(action_ix)

            if self.ix == 2 and step_ix % 200 == 0:
                fname = './screens/car-racing/screen-' + str(step_ix) + '-' + str(int(time.time())) + '.jpg'
                im = Image.fromarray(state)
                im.save(fname)
                state.tofile(fname + '.txt', sep=" ")
                _input.numpy().tofile(fname + '.input.txt', sep=" ")

            if terminal or step_ix % yield_every == 0:
                yield step_ix, rewards, values, policies, actions, terminal
                rewards, values, policies, actions = [[], [], [], []]

            if self.reset:
                self.reset = False
                self.agent.reset()
                states = deque([ ])
                self.states = deque([ ])
                return

            if terminal:
                self.agent.reset()
                states = deque([ ])
                return

    def ask_reset(self):
        self.reset = True

    def preprocess(self, states):
        return torch.stack([ torch.tensor(self.preprocess_one(image_data), dtype=torch.float32) for image_data in states ])

    def preprocess_one(self, image):
        return rescale(rgb2gray(image), (0.24, 0.16), anti_aliasing=False, mode='edge', multichannel=False)

    def choose_action(self, policy, step_ix):
        policies = [[-0.8, 0.0, 0.0], [0.8, 0.0, 0], [0.0, 0.1, 0.0], [0.0, 0.0, 0.6]]

        if self.train:
            action_ix = np.random.choice(4, 1, p=torch.tensor(policy).detach().numpy())[0]
        else:
            action_ix = np.argmax(torch.tensor(policy).detach().numpy())

        logger.info('Step ' + str(step_ix) + ' Runner ' + str(self.ix) + ' Action ix: ' + str(action_ix) + ' From: ' + str(policy))

        return np.array(policies[action_ix], dtype=np.float32), action_ix

    def decide(self, state, step_ix):
        policy, value = self.agent(state)

        action, action_ix = self.choose_action(policy, step_ix)

        return action, action_ix, policy, value

    def load_state_dict(self, state):
        self.agent.load_state_dict(state)
```

(The importance of tuning of the n-step window size)

(Problems with the buggy gym state returning - overcoming with the explicit render)

(Tips for recognizing when the algorithm converges - rich logging)

(Coding the agent)

(The episode runner)

(The trainer)

(Results)

(Ending words - links to GitHub)