---
author: "Matt Vollrath"
title: "Python concurrency: asyncio for threading users"
tags: python, performance
gh_issue_number: 1670
---

![Freeway lanes](/blog/2020/10/05/python-concurrency-asyncio-threading-users/freeway-lanes.jpg)

[Photo](https://unsplash.com/photos/XS7q-baZrmE) by [Adrian Schwarz](https://unsplash.com/@aeschwarz)

You’ve probably heard this classic software engineering mantra:

> Concurrency is hard.

The undeniable fact is that an entire category of software bugs, known for being elusive and frustrating to reproduce, is gated behind the introduction of concurrency to a project. Race conditions, mutual exclusion, deadlock, and starvation, to name a few.

Most programming languages with concurrency features ship with some or all of the classical concurrency primitives: threads, locks, events, semaphores, mutexes, thread-safe queues, and so on. While practically any concurrency problem can be solved with this toolkit, let me share a relevant life mantra:

> Just because you can doesn’t mean you should.

In the case of Python, you have access to a standard library alternative to threading, which factors out many of the trickier parts of concurrent programming: asyncio. Many existing applications of Python threads can be replaced by asyncio coroutines, potentially eliminating many of the difficulties of concurrency.

Understanding the differences between asyncio and threading can help you make informed choices about which to apply and when, so let’s take a closer look.

### The Python GIL

Any discussion of Python concurrency should mention Python’s GIL, or Global Interpreter Lock. The GIL ensures that only one thread may be executing Python code at a time. [A. Jesse Jiryu Davis](https://twitter.com/jessejiryudavis) writes [a succinct description of how the GIL affects Python threads](https://opensource.com/article/17/4/grok-gil):

> One thread runs Python, while N others sleep or await I/O.

Once a thread has acquired the GIL, there are two ways it can release the GIL for another thread to acquire:

1. Reaching a point in the script where it is sleeping, ending, waiting for I/O, or executing native code which explicitly releases the GIL. For example, calling `time.sleep(0)` forces a thread to release the GIL without ending the thread.
1. After executing for some amount of time and/or instructions, a thread may be forced to release the GIL for another thread to have a turn. Interrupting a thread in this way is preemption.

### A Contrived Example of Thread Preemption

Here I will set up a concurrency toy to demonstrate some characteristics of Python threading. One thread will increment a list of numbers in a for loop. The other thread will, roughly once per second, check the consistency of the list (all numbers are equal) and print a message. Observant readers can probably imagine a better non-threading solution to this problem, but allow me to entertain you.

All posted results are from running the examples in Python 3.8.6 in a Docker container on a laptop. Your results may vary.

Here is the naive approach, without any attempt at synchronization:

```python
import threading
import time

SIZE = 100000


class Counter():
  def __init__(self):
    self.values = [0] * SIZE

  def count(self):
    while True:
      for i in range(SIZE):
        self.values[i] += 1

  def heartbeat(self):
    t0 = time.monotonic()

    while True:
      time.sleep(1.0)

      # Check for consistency.
      for i in range(SIZE):
        assert self.values[i] == self.values[0], f'Value at index {i} is inconsistent'

      now = time.monotonic()
      print(f'All values are {self.values[0]} at +{now - t0:.5f}s')


if __name__ == '__main__':
  counter = Counter()

  t_count = threading.Thread(target=counter.count, daemon=True)
  t_count.start()

  t_heartbeat = threading.Thread(target=counter.heartbeat, daemon=True)
  t_heartbeat.start()

  print('Press Ctrl+C to end')

  # Wait for Ctrl+C or heartbeat crash.
  t_heartbeat.join()
```

If you run this code a few times, you’ll notice that you might get a few heartbeat messages (if you’re lucky), then the script crashes because the consistency check failed. Because the counter thread can be preempted at any time, this can include between value increments in the for loop. Similarly, the heartbeat thread can be preempted in the middle of its consistency check.

Threads can be very rude when left alone. We can prevent threads racing for access to shared state by using a `Lock`, which can only be held by one thread at a time:

```python
class Counter():
  def __init__(self):
    self.values_lock = threading.Lock()
    self.values = [0] * SIZE

  def count(self):
    while True:
      with self.values_lock:
        for i in range(SIZE):
          self.values[i] += 1

  def heartbeat(self):
    t0 = time.monotonic()

    while True:
      time.sleep(1.0)

      # Check for consistency.
      with self.values_lock:
        for i in range(SIZE):
          assert self.values[i] == self.values[0], f'Value at index {i} is inconsistent'

      now = time.monotonic()
      print(f'All values are {self.values[0]} at +{now - t0:.5f}s')
```

```nohighlight
All values are 693 at +9.12154s
All values are 797 at +10.60691s
All values are 877 at +11.83219s
All values are 957 at +13.04729s
All values are 1036 at +14.27122s
All values are 1157 at +16.15205s
```

When you run this code you may notice that the consistency check never fails, but the timing of the heartbeat message is not as consistent as we would like. In fact, it may be several seconds before you see a heartbeat message. There is a lot of timing jitter, which is deviation from the expected time interval. There is also a lot of drift, which is accumulated jitter.

This is happening because there is no guarantee that the counter thread will release the GIL while `values_lock` is available, or that `values_lock` won’t be acquired again by the counter thread immediately after releasing it.

When multiple threads are waiting to acquire a `Lock`, the order in which they are woken up is not defined. We might expect or sometimes observe that the `Lock` will be acquired first come, first served, or first in, first out, but Python makes no guarantees.

Remembering that we can explicitly release the GIL, we cleverly try doing so immediately before the counter thread acquires `values_lock` to give the heartbeat thread a chance to win the race:

```python
def count(self):
  while True:
    time.sleep(0)  # Explicitly yield the GIL.
    with self.values_lock:
      for i in range(SIZE):
        self.values[i] += 1
```

```nohighlight
All values are 114 at +1.41245s
All values are 206 at +2.57230s
All values are 315 at +4.05285s
All values are 432 at +5.75999s
All values are 514 at +6.94572s
All values are 662 at +9.05388s
```

This is much better, but there is still enough jitter and drift that we might not even be able to adequately compensate for the drift by reducing the sleep interval automatically. We’ve applied all of our knowledge of threading and this is the best we can do, within the constraints of the example.

All of this may seem like a lot to keep up with, and it is. Even if you are a threading master and craft perfectly safe and reasonably performant Python threading code, it is likely to be relatively difficult and expensive to maintain. There’s got to be a better way.

### Concurrency with asyncio

The [asyncio](https://docs.python.org/3/library/asyncio.html) approach to Python concurrency is relatively new. Its integration with the language has changed over the course of Python development, but it appears to be largely stable and useful as of Python 3.8. Instead of using Python threads to run instructions concurrently, asyncio uses an event loop to schedule instructions on the main thread.

Contrasted with threads, asyncio coroutines may never be interrupted unless they explicitly yield the thread with `async` or `await` keywords. However, there is no guarantee that saying `async` or `await` will yield the thread to another task.

The asyncio library is intended to be used for I/O-bound applications such as high performance network servers, which spend much of their time waiting for the OS to send or receive data on a file descriptor or socket. However, as we will see when applying asyncio to our toy concurrency example, it can be applied to otherwise pure and isolated Python code too.

This example requires Python 3.7 for the `asyncio.run()` method.

```python
import asyncio

SIZE = 100000


class Counter():
  def __init__(self):
    self.values = [0] * SIZE

  async def count(self):
    while True:
      await asyncio.sleep(0)  # Explicitly yield to other coroutines.
      for i in range(SIZE):
        self.values[i] += 1

  async def heartbeat(self):
    loop = asyncio.get_event_loop()
    t0 = loop.time()

    while True:
      await asyncio.sleep(1.0)

      # Check for consistency.
      for i in range(SIZE):
        assert self.values[i] == self.values[0]

      now = loop.time()
      print(f'All values are {self.values[0]} at +{now - t0:.5f}s')


async def main():
    counter = Counter()

    tasks = map(asyncio.create_task, [counter.count(), counter.heartbeat()])
    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == '__main__':
    asyncio.run(main())
```

```nohighlight
All values are 84 at +1.04261s
All values are 169 at +2.08948s
All values are 254 at +3.13599s
All values are 326 at +4.18760s
All values are 400 at +5.24720s
All values are 473 at +6.30465s
```

This timing is now in the ballpark where we can compensate for drift by automatically adjusting the heartbeat sleep interval. There is no more racing for the GIL. Instead the counter coroutine explicitly awaits whenever the state is consistent. It may not be interrupted by another coroutine at any other time, but it can still be interrupted by another thread or a signal.

If we imagine that the `asyncio.sleep(0)` incantation is actually awaiting data on a file descriptor or network socket saturated with data, this example is immediately relevant to the intended use of asyncio. The pattern of running top-level coroutines with `asyncio.wait()`, among other asyncio task scheduling tools, can potentially replace many existing uses of daemon threads for background tasks.

A caveat of asyncio is the consequence of one of its advantages: While a coroutine is running, it may never be interrupted by another coroutine unless it explicitly gives up control. One slow or malformed coroutine can freeze your entire application, where daemon threads would keep preempting and bypassing the blockage (at cost of some context-​switching overhead and developer sanity). If you must run blocking code concurrently you can [run it in an executor](https://docs.python.org/3.4/library/asyncio-eventloop.html#executor) to decouple it from the asyncio event loop, but understand that the usual thread synchronization problems may apply.

Just because asyncio never preempts doesn’t mean you will never need to synchronize access to shared state. The library does include threading-like synchronization primitives (which are not thread-safe), but the need for them should be the exception, not the norm.

### Conclusion

If you’re interested in using asyncio, I urge you to [explore its interfaces further](https://docs.python.org/3/library/asyncio.html). We’ve only scratched the surface in these examples. If you are shoehorning asyncio into an existing application or want to use it with a library or framework that relies on threads, know there are asyncio interfaces for safely adding coroutines from a thread.

Happy hacking!
