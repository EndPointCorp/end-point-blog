---
author: Kamil Ciemniewski
gh_issue_number: 1212
tags: functional-programming, haskell, javascript, testing
title: QuickCheck - property based testing in Haskell and JavaScript
---

In my [last article](/blog/2016/03/11/strict-typing-fun-example-free-monads), I presented a [functional programming](https://en.wikipedia.org/wiki/Functional_programming) pattern. The goal was to reach out to the developers who weren’t familiar with advanced type systems like the one found in Haskell and make them a bit curious. This time I’d like to take a step further and present a testing approach coming from the same world, that can be used with mainstream languages with a great success.

### Many ways to test the code

The importance of testing is almost a cliché nowadays. Out of this relevance, a large number of testing frameworks and paradigms have been created. On the paradigm level we have notions like TDD and BDD. On the level of implementations we have hundreds of projects for each language like RSpec in Ruby and Jasmine or Mocha in JavaScript.

The ideas behind the libraries don’t differ that much. All of them are based on the idea of providing code examples with assertions on how the code should behave in these particular cases.

A bit more revolutionary in its approach was the Cucumber project. In its essence, it allows business people to express the system logic by stating it in specially formed, plain English. An example taken from the Cucumber’s website reads:

```scss
Feature: Refund item

  Scenario: Jeff returns a faulty microwave
    Given Jeff has bought a microwave for $100
    And he has a receipt
    When he returns the microwave
    Then Jeff should be refunded $100
```

In this article, I’d like to present an approach that was conceived in the realm of Haskell — the purely functional, statically typed language. Though it started just as a Haskell library, today it could be broadly named an “approach”. We now have implementations for almost every major language. This approach is what is known as **QuickCheck**.

### Code testing limitations

Having a good test coverage is a sign of a potentially stable code. However, even well-tested software needs to be improved occasionally as new bugs are discovered. This happens even in the projects with the largest test suites. Moreover, the tests are code too — they also are prone to being invalid. But do we have a really valid solution when all our tests are valid and the code passes all assertions? Realistically, we can only provide a few examples per use case at most. The best we can do is to choose the most probable use cases and the ones we have a hunch that might go wrong.

This implies that for the tests suite to be guarding us against bugs, we need to have an insight as to where the potential bugs may be before even testing. Isn’t a definition of a bug telling the other story though? If we knew where to find them, we would fix them in the first place. In reality the systems grow so complex that we only can have *a feeling* of what might go wrong.

In 1969, Edsger W. Dijkstra said at the “[Nato Software Engineering Conference](http://homepages.cs.ncl.ac.uk/brian.randell/NATO/nato1969.PDF)”:

>
>
>
> Testing shows the presence, not the absence of bugs.
>
>
>

### I’ve got lots of ammo, give me a machine gun for killing bugs!

What if we could ask the computer to come up with many different use cases for us? Instead of having 2 or 3 cases per some code aspect, we’d have 100 of them including the ones we’d never consider ourselves. We could describe **properties** of the code we’d like to hold for all of the randomly chosen cases. That is exactly the idea behind the QuickCheck. In its functional - Haskell form, it takes advantage of the supreme type system and generates a random set of function parameters based on their types. It then runs the property check for all of them and stops if it’s able to find a counter example making the property falsifiable.

If we’d compare coming up with traditional test cases to shooting with a pistol, the **QuickCheck** approach had to be called firing with a machine gun. The reason is that we’re not focusing on a specific use case, but we’re focusing on certain properties of the code that have to hold for any argument from the accepted domain.

One of the most basic examples we could show, could be ensuring that the *reverse* function applied twice returns the original array (pseudo-code):

```haskell
arr1 == reverse(reverse(arr1))
```

The idea here is to make sure this property holds against a large number of randomly selected arguments from the domain. In this example the checker would randomly generate e. g 100 arrays and test if the assertion evaluates to true for every one of them.

### Working example — the Haskell way

Let’s take a look at how the approach is being used in its original environment. Later on we'll see how the pattern can be used when coding in JavaScript. For this, let’s imagine that we’re developing a graph data structure, to be used in some e-commerce project we’re working on. Here’s the basic very incomplete draft:

```haskell
module BlogGraph where

import Data.Map as Map
import Data.List as List

-- Graph as an adjacency list as described here:
-- https://en.wikipedia.org/wiki/Adjacency_list

data Graph a = Graph (Map a [a]) deriving (Show)

empty :: Graph a
empty = Graph Map.empty

insertNode :: (Ord a) => a -> Graph a -> Graph a
insertNode node (Graph m) = Graph $ Map.insert node [] m

removeNode :: (Ord a) => a -> Graph a -> Graph a
removeNode node (Graph m) = Graph $ Map.delete node m

insertEdge :: (Ord a) => a -> a -> Graph a -> Graph a
insertEdge parent child (Graph m) =
  Graph $ Map.insertWithKey update parent [child] m
  where
    update _ _ old = List.nub $ child:old

nodes :: Graph a -> [a]
nodes (Graph m) = Map.keys m
```

If you’re not proficient yet in reading Haskell code, we’re just using a Map where keys are integers and values are arrays of integers to implement the graph as an [Adjacency List](https://en.wikipedia.org/wiki/Adjacency_list). So each node has its representation in a map as one of its keys. Also, each edge has its representation as a child stored in the parent’s array in the map.

You might be able to find a silly bug in the **removeNode** function. It doesn’t remove the node from the edge definitions of other nodes. We’ll use **QuickCheck** to show how this could be found automatically.

Before doing that, let’s have a warm up, by adding two simple properties:

```haskell
prop_insert_empty :: Int -> Bool
prop_insert_empty i =
  nodes (insertNode i BlogGraph.empty) == [i]

prop_insert_existing :: Int -> Bool
prop_insert_existing i =
  nodes (insertNode i $ insertNode i BlogGraph.empty) == [i]
```

Properties are just simple functions returning true or false. They take arguments which are randomly provided later on by the QuickCheck library.

The first property says that adding a node to an empty graph will always produce a one-node graph. The second one, that adding a node to a graph that already has this node will always return the same unmodified graph.

We can successfully run these cases:

```haskell
quickCheck prop_insert_empty
quickCheck prop_insert_existing
```

Now we should add a property stating that for all removals of a node from the graph, all references of this node in edge definitions for other nodes are always also being removed:

```haskell
prop_remove_removes_edges :: Graph Int -> Bool
prop_remove_removes_edges (Graph m) =
  List.null (nodes graph) || List.notElem node elemsAfter
  where
    graph = Graph m
    node = List.head $ BlogGraph.nodes graph
    elemsAfter = List.concat $ Map.elems mapAfter
    mapAfter =
      case removeNode node graph of
        (Graph m) -> m
```

As I wrote before, these property testing functions are being run by the **QuickCheck** framework repeatedly with randomly generated values as arguments. Out of the box we’re able to generate random examples for many simple types — including e.g Int. That’s the reason we were able to just specify properties depending on random Int variables — without any additional code. But with the last example, we’re asking QuickCheck to generate a set of random **graphs**. We need to tell it how to construct a random graph first:

```haskell
arbitrarySizedIntGraph :: Int -> Gen (Graph Int)
arbitrarySizedIntGraph s = do
  nodes <- vectorOf s $ choose (0, 32000)
  edges <- edges nodes
  let withNodes = List.foldr insertNode BlogGraph.empty nodes
  return $ List.foldr addEdge withNodes edges
  where
    addEdge (parent, child) = insertEdge parent child
    edges nodes = do
      parents <- sublistOf nodes
      let children = nodes List.\\ parents
      return [ (parent, child) | parent <- parents, child <- children ]

instance Arbitrary (Graph Int) where
  arbitrary = sized arbitrarySizedIntGraph
```

The above generator will be good enough for our case. It generates variable length graphs. A sublist of all nodes are made parents in edges and all parents are connected to the rest of non-parental nodes.

When we try to run the test we get:

```haskell
Failed! Falsifiable (after 3 tests):
Graph (fromList [(10089,[]),(25695,[10089])])
```

QuickCheck shows that the property doesn’t hold for the whole domain — it failed after 3 examples. It also prints the example for which our property did not hold.

We can now reexamine the code for the removeNode function and fix it as per the property’s specification:

```haskell
removeNode :: (Ord a) => a -> Graph a -> Graph a
removeNode node (Graph m) =
  Graph $ Map.map remNode $ Map.delete node m
  where
    remNode = List.delete node
```

Now running the test again we can see that it works.

### Another working example — the JavaScript land

As I stated before, this pattern became implemented for many different mainstream languages — this includes JavaScript. I’d like to show you the version of the above process for this language now. This might end up being helpful if you’d like to use it in your project but don't know much Haskell yet.

As a start, let’s make sure we have the following packages:

```bash
npm install jsverify
npm install lodash
```

We can now create a JS file with what might resemble the Haskell draft implementation:

```javascript
var jsc = require("jsverify");
var _   = require("lodash");

var Graph = function() {
    var self = this;

    self._map = {};

    self.insertNode = function(node) {
      if(self._map[node] === undefined) {
        self._map[node] = [];
      }
      return self;
    };

    self.removeNode = function(node) {
      self._map.delete(node);
      return self;
    };

    self.insertEdge = function(a, b) {
      if(self._map[a] === undefined) {
        self.insertNode(a);
      }
      self._map[a].push(b);
      return self;
    };

    self.nodes = function() {
      return _.keys(self._map);
    };
}

Graph.empty = function() {
    return new Graph();
}
```

To reproduce the first property — for all integers, inserting one as a node to an empty graph results in a graph with one node:

```javascript
var propInsertEmpty =
  jsc.forall("nat", function(i) {
    return _.isEqual(Graph.empty().insertNode(i).nodes(), [i]);
  });

jsc.assert(propInsertEmpty);
```

The jsVerify DSL takes some time to get used to. It cannot take advantage of the type system as in the Haskell example so aspects like generation of random data based on types requires some documentation reading.

Running *jsc.assert* we might have expected to get a success, but this time we’re getting:

```nohighlight
Error: Failed after 1 tests and 5 shrinks. rngState: 001d40a68297fbce35; Counterexample: 0;
```

We can see that jsVerify has found 0 as a counterexample. Let’s see what’s happening by running the code by hand passing 0 as a parameter:

```javascript
console.log(Graph.empty().insertNode(0).nodes());
```

Result:

```javascript
[ '0' ]
```

Aha! It’s quite easy to shoot your own foot in JavaScript. We can fix it really fast with the following:

```javascript
self.nodes = function() {
   return _.map(_.keys(self._map), function(i){ return parseInt(i, 10); });
};
```

Running the code again doesn’t show any errors which means that all assertions were valid. What about the bug we saw in the Haskell version? Let’s provide a property for that too:

```javascript
var propRemoveRemovesEdges =
  jsc.forall(graphG, function(g) {
    if(g.nodes().length === 0){
      return true;
    }
    else {
      var numNodes = g.nodes().length;
      var index = _.random(0, numNodes - 1);
      var node = g.nodes()[index];
      return !_.includes(_.flattenDeep(_.values(g.removeNode(node)._map)), node);
    }
  });

jsc.assert(propRemoveRemovesEdges);
```

We will still need to specify how to generate a random graph. We can use the notion of a [Functor](https://en.wikipedia.org/wiki/Functor) that's coming from the functional programming world and turn a random array into a random graph:

```javascript
var graphG = jsc.array(jsc.nat).smap(
  function(arr) {
    var ins = function(g, i) {
      return g.insertNode(i);
    };
    var graph = _.reduce(arr, ins, Graph.empty());
    var numParents = Math.floor(arr.length / 2);
    var parents = _.take(arr, numParents);
    var children = _.difference(arr, parents);
    var insEd = function(g, parent) {
      var insF = function(r, c) {
        return r.insertEdge(parent, c);
      };
      return _.reduce(children, insF, g);
    };
    return _.reduce(parents, insEd, graph);
  },
  function(graph) {
    return graph.nodes();
  }
);
```

When running the assert for that property we’re getting an error:

```nohighlight
Error: Failed after 1 tests and 1 shrinks. rngState: 085f6c82ea10439d7b; Counterexample: {"_map":{"21":[44]}}; Exception: self._map.delete is not a function
```

This isn’t the issue we were expecting though. Still it’s great to find a problem before showing the code to the client. We can iron it out with:

```javascript
self.removeNode = function(node) {
  delete self._map[node];
  return self;
};
```

When running again, we’re getting an error we were expecting:

```nohighlight
Error: Failed after 8 tests and 2 shrinks. rngState: 8c97e25bc36f41da08; Counterexample: {"_map":{"2":[7]}};
```

The jsVerify has found a counterexample falsifying our property. It’s also worth noting that it took 8 tests to find this issue. We can notice that for the event of removing a node that is a child and doesn’t have any children itself the property isn’t true. Let’s reexamine our removeNode function:

```javascript
self.removeNode = function(node) {
  delete self._map[node];
  return _.mapValues(self._map, function(children) {
    return _.without(children, node);
  });
};
```

And now it works!

### Not only Haskell and JavaScript

The QuickCheck style testing is available for many different languages. The Wikipedia says:

>
>
>
> Re-implementations of QuickCheck exist for C, C++, Chicken Scheme, Clojure, Common Lisp, D, Elm, Erlang, F# (and C#, VB.NET), Factor, Io, Java, JavaScript, Node.js, Objective-C, OCaml, Perl, Prolog, PHP, Python, R, Ruby, Rust, Scala, Scheme, Smalltalk, Standard ML and Swift.
>
>
>

You can find many useful links about the approach on [Wikipedia](https://en.wikipedia.org/wiki/QuickCheck). If you’re into Haskell, a good place to start reading about the library is the [Haskell Wiki](https://wiki.haskell.org/Introduction_to_QuickCheck2) as well as the documentation found on the [Hackage](https://hackage.haskell.org/package/QuickCheck).

The JavaScript counterpart can be found on [GitHub](https://github.com/jsverify/jsverify). It’s important to note that jsVerify isn’t the only JavaScript library implementing the QuickCheck approach.
