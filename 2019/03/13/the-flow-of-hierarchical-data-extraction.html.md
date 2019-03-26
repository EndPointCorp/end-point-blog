---
author: "Árpád Lajos"
title: "The flow of hierarchical data extraction"
tags: data-mining, machine-learning, data-processing
gh_issue_number: 1503
---

![forest view through glass ball on wood stump](/blog/2019/03/13/the-flow-of-hierarchical-data-extraction/art-ball-ball-shaped-235615-smaller.jpg)

[//]: # (CC0 image source: https://www.pexels.com/photo/ball-ball-shaped-blur-color-235615/)

### 1. Problem statement

There are many cases when people intend to collect data, for various purposes. One may want to compare prices or find out how musical fashion changes over time. There are a zillion potential uses of collected data.

The old-fashioned way to do this task is to hire a few dozen of people and explain them where should they go on the web, what should they collect, how they should write a report and how they should send it.

It is more effective to teach them this at the same time than to teach them separately, but even then, there will be misunderstandings, mistakes with high cost, not to mention the limit a human has when processing data in terms of the amount to process. As a result, the industry strives to make sure this is as automatic as possible.

This is why people write software to cope with this issue. The terms data-extractor, data-miner, data-crawler, data-spider mean software which extracts data from a source and stores it at the target. If data is mined from the web, then the more-specific web-extractor, web-miner, web-crawler, web-spider terms can be used.

![](/blog/2019/03/13/the-flow-of-hierarchical-data-extraction/SemanticDataExtractorFigure1.png "Extraction, to put it simply")

In this article I will use the term “data-miner”.

This article deals with the extraction of hierarchical data in semantic manner and the way we can parse the data we obtained this way.

#### 1.1. Hierarchical structure

A hierarchical structure involves a hierarchy, that is, we have a graph involved with nodes and vertices, but without a cycle. Specialists call this structure a **forest**. A forest consists of **trees**; in our case we have a forest of rooted trees. A rooted tree has a root node and every other node is its descendant (child of child of child …), or, if we put it inversely, the root is the ancestor of all other nodes in a rooted tree.

If we add a node to a forest and we make sure that all the trees’ roots in the forest are children of the new node, the new root, then we transformed our hierarchical structure, our forest into a tree.

Common hierarchical structures a data-miner might have to work with are:

- HTML
- XML
- Trees represented in JSON
- File structure

Other, non-hierarchical structures could be texts, pictures, audio files, video, etc. In this article we focus on hierarchical structures.

#### 1.2. Purpose of the data-miner

Of course the purpose of the data-miner is to mine data; however, more specifically, we can speak about general-purpose data-miners, thematic data-miners and narrow-spaced data-miners.

General-purpose data-miners are the data-miners which extract and prepare data for search engines. The technique one can imagine is to find the text in the source (for example a web-page) and map it to keywords, so that when people are searching for the keywords, the source is shown as the result. Of course, it is highly probable that these data-miners are much more smart and complex than described here, but that is out of scope from our perspective.

If we speak about general-purpose data-mining, then even if it is to mine from a hierarchical data-source, it is very difficult to define all the semantics involved by humans, so, if one wants to create a general-purposed data-miner, machine-learning will play a large part to define all the concepts. However, a general-purposed data-miner is a generalized version of thematic data-miner. If we add up a lot of thematic data-miners, we get a general-purpose data-miner and inversely, if we divide the different areas a general-purposed data-miner deals with, we get thematic data-miners. This is true if we look at what they accomplish, but the implementation will differ a lot when the developers implement a general-purposed data-miner from the case when developers implement a thematic data-miner. As a result, when we discuss the thematic data-miners, we can keep in mind that the general-purposed data-miners are a broader version of the same thing, at least if we look at what they achieve.

Thematic data-miners are dealing with a given cluster of concepts, that is, concepts which are logically related to each-other. For example, if we are to extract real-estate details, then we have concepts of “type”, “bedroom number”, “picture” and so on. All these concepts are interrelated; the cluster is defined by the real-estate entity we want to extract. If we speak of the “type”, we really mean “the type of the real estate” entity.

Narrow-spaced data-miners are data-miners which extract data from very specific data-sources, like a single website. These data-miners are always particular cases of thematic data-miners, however, in many cases narrow-spaced data-miners have a lot of hard-coded logic, so, when the space of a narrow-spaced thematic data-miner is broadened, there is usually a lot of code refactoring involved.

This article focuses on thematic data-miners, which could have thousands of different sources.

#### 1.3. The human element

We need to pay attention to legality and to the ethical aspect. If data mining from the source is illegal, then we must avoid doing it. If it is against the will of those who own it, then it is unethical and we should avoid it. Sources should be at least neutral to our extraction, but, preferably happy about us extracting their data.

Why would the owner of a data source be against extracting their data? There can be many possible causes. For example, the owner might want to attract many human visitors to a website, who would visit to see their data and would be unhappy if another website were created and people would visit the new website instead of theirs.

But why would the owner of a data source be happy about extracting their data? It depends on the purpose of their data. If the purpose is to spread the information as far as possible, then data extractors are considered to be “helping hands”.

For example, if an estate agent of a small village wants to target global audience, he/she might want to create a website and hope that people would see his/her data, but without advertisement and a lot of care to raise the popularity of the site, including design, SEO measures and so on, people searching for real estate might never see his/her site. A large website which is searchable by region and shows the results of extracted data could boost the business of the estate agent, especially if the data of the estate agent is publicized without him/her having to pay a penny. People will search for real estate in the region where the estate agent works and will find the big site showing the mined data, emphasizing the contact of the estate agent.

So, to cope with all possible needs of data-source owners, the planner of a data-miner project might want to support listing results with or without details page. Imagine the case when one wants visitors to his/her website and would not like another site to be visited instead. In this case, one can tell him/her that, if he/she allows the extraction of data from his/her site, then they will appear in the list of results, but will not have a details page, instead, when the user clicks on such a result, the website of the owner of the data-source would be opened in a new tab. In this case we are giving them an attractive offer, so that our site will essentially help getting visitors to his/her site. And of course, for those who just want to share the information with as many people as possible, one could show a details page for his/her data. This is a simplified strategy, but illustrates the idea of how people can be convinced to allow us to extract their data.

#### 1.4. The actual problem statement

In this article we intend to have solid ideas of how hierarchical data can be extracted by a thematic data-extractor from data-sources where the owner is content with their data being extracted.

### 2. The extraction

Now we have hierarchies to work with, possibly many. Nodes can have the parent-child relation, but they can have the ancestor-descendant relation as well. A is the ancestor and D is its descendant, if A is the parent of D, or we have a sequence of nodes S, where Si is the parent of Si+i for each neighboring pair of the sequence and A is the parent of S1, Sn is the parent of D. Consider this HTML code chunk:

```
<div class="dimensions">
    <div class="large-width">
        <div class="area">Area<span class="dimension-data">500</span> <span class="unit">sqm</span></div>
        <div class="height">Height<span class="dimension-data">60</span> <span class="unit">m</span></div>
    </div>
</div>
```

We see that the div having the class of dimensions is the parent of the div with the large-width class and the ancestor of the spans having the area and height classes, respectively. In the case of hierarchical data, a descendant is inside the ancestor; knowing this gives us a lot of context in many cases.

#### 2.1. Semantic concepts

In hierarchical structures we have some nodes, a (usually small) subset of which contains interesting data for us. For instance, in the example shown at point 2 we have a div which exists to style the shown data, which has some useful information in its descendants, which have the classes of area and height having the class of dimension-data.  However, the div having the class of large-width by itself does not have any useful information outside those descendant nodes, and frankly, it is just a styling node, which makes it irrelevant from our point of view. This means that the large-width div should not exist for us conceptually, we just need to know that we have a concept of dimensions, inside which we should be able to find the area and height. In terms of JavaScript selectors we know that we can find dimensions inside the document and area and height inside it, like this:

```
let dimensions = [];
let dimensionContainers = document.querySelectorAll(".dimensions");
for (let dimensionContainer of dimensionContainers) {
    const dimension = {};
    let areaContainer = dimensionContainer.querySelector(".area");
    if (areaContainer) {
        let value = areaContainer.querySelector(".dimension-data");
        let unit = areaContainer.querySelector(".unit");
        if (value && unit) {
            dimension.area = {value: value.innerText, unit: unit.innerText};
        }
    }
    let heightContainer = dimensionContainer.querySelector(".height");
    if (heightContainer) {
        let value = heightContainer.querySelector(".dimension-data");
        let unit = heightContainer.querySelector(".unit");
        if (value && unit) {
            dimension.unit = {value: value.innerText, unit: unit.innerText};
        }
    }
     dimensions.push(dimension);
}
```

We immediately notice some details in the code:

- It does not deal with large-width at all, because it’s irrelevant, instead, it just focuses on nodes, which are semantically relevant.
- When a concept is found, its direct sub-concept is searched inside its structural context instead of the whole context, so we are particularizing the search.
- Our code smartly searches for plural results in the case of dimensions and is aware that area and height is singular in its parent concept, the dimension.
- The code does not assume the existence of any data.

There are also problems to cope with:

- What happens if the structure changes over time? How can we maintain the code we have above?
- The code above is based on empiric evidence, on the findings of a developer, but this is only proving that the hierarchy the code above is dealing with exists, but it certainly does not prove this is the only structure to work with.
- How can we cope with composite data, like extracting something like “height: 60m”.
- How can we cope with the variance of data, such as synonyms?
- How can we cope with paging where applicable?

All these are serious questions, which show that such a concrete code will not solve the problems we face. We will need abstraction to progress further than the limits of particularity and achieve the level of a thematic data-miner. We have seen that in our examples we had a hierarchy of semantic concepts and also, we can observe the rule that an ancestor concept is an ancestor structurally as well. Also, the algorithm we had above has a pattern of searching for the child concept in the context of the parent concept.

In reality we also have the problem of conceptual inconsistency, that is, the structure of the same data-source can be varied and in some cases they are at a totally different location in the structure. To give you a practical example, let’s consider the example we had about real-estate properties and their dimensions particularly. It is possible that the height of the real estate makes it very attractive for buyers, so the developers of the data-source decided to show the height separately, in an emphasized manner, at the top of the page and not to show it at its usual place. In this case, if we would not cope with this important detail, we would miss the height for real-estate properties where the height is the most important detail; we would miss the stars of the show.

#### 2.2. Semantic rules

In 2.1 we have seen how we can have an understanding about the conceptual essence. Naturally, the concepts are useful by themselves, but we need to build up a powerful structure, a signature of the concepts, which, if shown on a diagram would describe the essence of the structure, the conceptual essence in such a powerful way that one could understand it at a glance (unless there are too many nodes for a human, of course).

In order to gain the ability to build up such a powerful structure we need to find patterns, but in a more systematic way than the one we have seen in the naive code used as an example. Concepts can be described by rules. I call these rules semantic rules. What attributes describe a concept:

- **parent concept(s):** Which concepts can be the parents of the current concepts? A special case is a root parent. Also, the possibility to define multiple parents is to avoid duplication when the very same concept in the very same substructure can be present at various places.
- **descendant(s):** Useful to make the rule more specific and possibly filter out unneeded cases and thus increase performance.
- **relative path:** How can the given concept be found starting from the parent concept as root?
- **plurality:** Should we stop at the first match, or continue searching?
- **excludes:** Which concepts are excluded if this concept is matched? (this is a symmetrical relation)
- **implies:** What concepts imply this concept? (consequently, if this concept is not matched, the concepts which imply it can be excluded as well)
- **value:** Where the actual value of the concept can be found.

If the structure of the data source changes over time, then occasionally the semantic rules will have to change as well. However, arguably in the majority of cases the relative path of the concepts will be the only thing to be changed in this case, which is much easier to maintain than to refactor code. If the relative path descriptor does not change and the virtual structure of our semantic rules remains similar, then our data-miner might just work well even if the data-source is changed.

For example, in the case of web-crawlers, writing the initial code-base is just a fraction of the long-term costs. The real financial burden is maintaining the crawlability of many thousands of different sites, all changing from time to time. With semantic rules, even if they are defined manually the maintainability is largely simplified. Yet, if we have a module which proposes the new semantic rules, it would not hurt if there are many data-sources.

Imagine the case when we already have a well-defined set of semantic rules and a cron job detects that some data from a data source was not found in the last few hours, so it would search for the missing data in the data-source and, once found, it would generate the semantic rules for it and propose a new semantic tree of rules, which would run in parallel with the main semantic tree and store data in some experimental place. When the human developers would arrive back and check the reports, they would see that the data-miner thinks that the semantic tree needs to be changed and even has a proposal, also, for the case when the data-miner is right with its proposal, nothing was missed, the extracted data is among the experimental data, but once the new semantic tree is accepted, the experimental data would override the actual data.

Of course, the engine will not be 100% accurate in such a case, its suggestion might be mistaken, or, even if accurate, slight adjustments might be helpful. A relative path might be less accurate than needed, or the concept in the changed structure might have a different plurality, but even if there is room for improvement, such an automatic feature, generating a new semantic tree would be extremely helpful and would make sure that data is accurately extracted even in the case of large changes.

If the owner of the data-source is cooperating, then he/she could provide the changed semantic tree.

The parser is the part of the project which should do the job of handling composite data, but at the level of semantic rules the parser could be helped with a strategy of defining rules. One could define a syntax for the parser, so it would know which concepts are not atomic and maybe even some clues about how should they be parsed.

Synonyms could be dealt with keyword clusters.

Navigation can be handled by a module created for this purpose, we can call it the navigation module. The algorithm below describes how data-mining should occur:

```
initialNavigation()
while (page ← page.next())
    for each element in elements
        for each node in semanticTree  // breadth-first or depth-first traversing
            if (applicable(node)) then extract(node)
        end for
    end for
end while
finalNavigation()
```

Before we move on to deal with semantic trees we need to solve the problem of conceptual inconsistencies. We have seen that concepts can have multiple conceptual parents, but this is not inconsistent, nor violating the criteria of a tree. In reality for each element a concept will have a single parent, but it is perfectly possible that a given concept will have a parent for an element and a different parent for another element. This is what we described with the possibility of a concept having one of many possible parents/​element. However, even though we have a very good explanation for a concept having more parents, we still have to deal with the possibility of a concept being present twice for the same element. How is this possible?

Let’s consider the example of books displayed on a website. A book may have main author(s) and secondary author(s). It would not be surprising at all if the main authors are displayed differently than secondary authors. Also, a main picture might be displayed of the book’s cover and maybe some smaller images elsewhere, shown in a gallery. This would be a nice feature on a site which shows children’s books. However, from our perspective this means that the same concept is placed at several places at the same time. One may think of quantum mechanics, where time-place discrepancies are also possible.

How can we solve this problem for ourselves? We need to have an understanding, otherwise the whole thought process will go astray. My solution is to differentiate the concepts in the different stages of extraction and parsing. This would mean that the concept of “author” or “picture” is conceptually unique when we store it, even though these might be plural. More elements do not necessarily mean more concepts. On the other hand, at the time of extraction, the main picture is a different concept than the other pictures, also, the main authors are a different concept from the secondary authors. The moment of merging happens at the point when we store these and therefore have to convert the extraction concepts into the concepts we store.

#### 2.3. Semantic tree

The semantic rules we define have a parent-child and ancestor-descendant relation. The semantic tree is the blueprint of the conceptual essence, a plan to extract data and also, its attributes instruct the extractor about what concept should be found where, how should the extractor operate to have good performance and so on.

However, the entities to extract can vary greatly and there might be cases when  seemingly the same concept is distributed among various places. The word “seemingly” here means that even though at the end these concepts will be merged, at the phase of the actual data-mining we view these to be similar, but different concepts. The fact that a conceptual node might have several parents in the semantic rules only means that one of the parents of the list is to be expected, which means that all of the listed parents are possible. Consider a semantic rule which says that the parent of currency can be the description or the price:

```parent: description,price```

This means that the parent can be any of the elements of the list, that is, in the case of some elements the parent will be description, but in the case of some other elements, the parent will be price, so we do not violate by design our aim to have a semantic tree.

We have to watch out for cycles though. Without additional tools there is no protection against cycles, that we might accidentally add while we define the semantic rules, or our semantic rule generator does its magic. However, it makes sense to check whether there is a cycle in the semantic tree. If this is done automatically, then all the better.

However, since the description of semantic trees can define multiple disjunct parents to cope with the possibility to cope with the actual tree of concepts for all elements, at least those whose pattern is known, the semantic tree in reality is a semantic tree pattern and when we use it or we search for the cycles, we will need to traverse the possible parents where more of them are listed.

![](/blog/2019/03/13/the-flow-of-hierarchical-data-extraction/SemanticDataExtractorFigure2.png "Semantic tree example")

Consider the example we have brought for a semantic tree. 

We can see that we have a single main concept, “REAL-ESTATE”. This is not a general pattern, there might be several main concepts to extract on the same data-source, but for the sake of simplicity we have a single one. Implicitly, the technical implementation involves a single, abstract root, which is the parent of all the main concepts. We see that “TYPE” is plural for “REAL-ESTATE”, but “BEDROOM #” is singular. The conceptual reason is that we technically defined type in such a way, that not all pairs of types are mutually exclusive so if a type is found, for example “Bungalow”, the engine should not stop searching for other types, but if the number of bedrooms is found, then there is no point to further search for numbers of bedroom, because it is safe to assume that even if there are several different occurrences of this concept, they will be equivalent.

Why is “CURRENCY” special? It has two potential parents: “DESCRIPTION” or “PRICE”. In some cases it can be found inside “DESCRIPTION”, in other cases it can be found inside price. For example, if there are several values for “PRICE”, then “CURRENCY” is inside “DESCRIPTION”, but otherwise “CURRENCY” is inside “PRICE”.

But why could a real-estate property have several different prices? Well, this is outside the scope of data-mining, but to have an understanding, it is good to consider a viable example. Let’s consider the example of an estate agent who has a 20% bonus if he/she successfully sells a given real-estate property within a month. In this case, the agent might want to draw buyers and put a 5% discount on the property for a month and if he/she is successful in selling it, then he/she will still have a nice bonus. Considering this economic mechanism the data-source might be showing the prices in a special way if there is such a discount, like:

```
<div class="description">
    <table class="prices">
        <tr>
            <td>
                <p class="price"><span>100000</span></p>
                <p class="price red"><span>90000</span> 10% discount!</p>
            </td>
            <td>
                <div class="currency">$</div>
            </td>
        </tr>
    </table>
    <!-- … -->
</div>
```

while, if there is a single price, a different structure is generated:

```
<div class="description">
    <p class="price">
        <span>100000</span>
        <div class="currency">$</div>
    </p>
</div>
```

We notice again that the possibility of multiple parents does not mean that there will be any extracted element with multiple parents, it just describes that among the many elements some of the items will have “PRICE” as parent, the others will have “DESCRIPTION” as parent.

If we take a look at “DIMENSIONS”, we will see several concepts with the same name (“VALUE” and “UNIT”), but they have a different meaning in their specific context (“AREA” and “HEIGHT”, respectively).

Another interesting region is “CONTACT”, which has “PERSON” and “COMPANY” elements as conceptual children and both “PERSON” and “CONTACT” is plural. The underlying logic is that several companies or persons can be contacted when one wants to buy/​view a real-estate. We have sub-concepts of “FACEBOOK”, “EMAIL”, “PHONE”, “NAME”, “OTHER” and “WEBSITE” for both “PERSON” and “COMPANY”, but similarly to the example we have seen with “CURRENCY”, here the concepts have different meanings. A corporate website is a different thing from a personal website.

However, if we draw/​generate such a semantic tree, then it is better than a long documentation. It actually describes for coders the exact way the engine will operate and in the case when the engine is suggesting a new semantic tree for a reason, then, provided that the engine generates the tree’s picture, one will immediately understand what the essence of the engine’s suggestion is. Also, with such a nice diagram managers will understand the mechanism of the system at a glance.

#### 2.4. Parallelization

It is feasible to send parallel requests at the same time, which could happen using promises and the event queue in the case of JavaScript, or multiple threads in a multi-threaded environment.

### 3. Symbiosis

If the owner of the data-source is happy and supportive for his/her data to be extracted, then they might notify the maintainers of the data-miner whenever structural changes occur, or he/she can provide an API from which data can be extracted, for example a large JSON. However, this JSON will be probably hierarchical as well.

In some extremely lucky cases the owner of the data-source will be happy to provide and maintain the semantic rules. This could happen in the case when “spreading the word” via a data-miner is deeply valued by the owner of the data-source. The key is to have an offer, which helps reaching the goals of the data-source, so the owner of the data-source will see the data-miner as his/her extended hand instead of seeing it as a barrier in reaching the goals of the data-source.

### 4. Parsing the data

At the point when the data was successfully extracted, the results can be parsed just before storing it. For example in some cases we might have textually composite data in the same node, which is impossible to separate via the semantic tree, which needs leaf nodes of the original structure as atoms. So, in many cases a separate layer is needed to decompose composite textual data which holds data applicable to different concepts.

Also, if, for some technical reasons the semantic tree split a concept into different concepts (for example main authors and secondary authors), then the data-parser can merge the concepts which belong to be together into a single concept. There are many possible jobs the data-parser might fulfill, depending on the actual needs.

### 5. Analyzing the data

Let’s assume that we have a very nice schema and we store the data we have efficiently. However, we might be interested to know what patterns can we find in our data. Let’s see what patterns we are interested to find. They include:

- <a href="http://www.vldb.org/conf/1994/P487.PDF">association rules</a>
- <a href="https://opentextbc.ca/dbdesign01/chapter/chapter-11-functional-dependencies/">functional dependencies</a>
- conditional functional dependencies (a functional dependency upon the table or cluster records provided a condition is met)

**AR (Association Rule):** ```c => {v1, …, vn}```

If a certain condition (c) is fulfilled, then we have a set of constant values for their respective (database table) columns.

For example, let’s consider the table:

```person(id, is_alive, has_right_to_vote, has_valid_passport)```

Now, we can observe that:

```(is_alive = 0) => ((has_right_to_vote = 0) ^ (has_valid_passport = 0))```

So, this is an association rule, which has the condition of is_alive = 0 (so the person is deceased) and we know for a fact that dead people will not vote and their passport is invalid.

When we extract data from a source, there might be some association rules (field values are associated to a condition) we do not know about yet. If we find those out, then it will help us a lot. For instance, imagine the case when for whatever reason an insert/​update is attempted with values:

```
is_alive = 0
has_right_to_vote = 1
```

In this case we can throw an exception, so, this way we can find bugs in the code or mistakes in the semantic tree. This kind of inconsistency prevention is useful even if we are not speaking of data-mining, but, in the context of this article it is extremely useful, as it might detect problems in the semantic tree automatically.

**FD (Functional Dependency):** ```S → D```

The column-set S (Source):

```S = {S1, …, Sm}```

determines the column-set D (Destination):

```D = {D1, …, Dn}```

The formula more explicitly looks like this:

```{S1, …, Sm} → (D1, …, Dn)```

This relation means that if we have two different records/​entities with the same source values:

```Source1 = Source2 = {s1, …, sm}```, then their destination will match as well:

```Destination1 = Destination2 = {d1, …, dn}```

Inversely this is not necessarily true. If two records/​entities have the same destination values, then the functional dependency does not require them to have the very same sources.

**CFD (Conditional Functional Dependency):** ```c => S → D```

A CFD is a more generalized term of FD. It adds a condition to the formula, so that the functional dependency’s applicability is only guaranteed if the condition is met. We can describe functional dependencies as particular conditional functional dependencies, where the condition is inherently true:

```(true => S → D) <=> S → D```

Also, an AR can be described as

```c => {} → D```

#### 5.1. The More Useful (MU) relation 

Let’s consider that we have two patterns, P1 and P2, which could be ARs, FDs or CFDs. Is there a way to determine which of them is more useful? Generally speaking:

P1 MU P2 if and only if P1 is more general than P2.

Since both ARs and FDs are particular cases of CFDs, we will work with the formula of CFDs:

```
P1 = (c1 => S1 → D1)

P2 = (c2 => S2 → D2)

P1 MU P2 <=> ((c2 => c1) ^ (S1 ⊆ S2) ^ (D1 ⊇ D2))
```

Note that MU is reflexive, transitive, antisymmetrical and has a neutral element.

Reflexive: ```(c1 => c1) ^ (S1 ⊆ S1) ^ (D1 ⊇ D1)``` is trivially true.

Transitive:

Let’s suppose that

```
((c2 => c1) ^ (S1 ⊆ S2) ^ (D1 ⊇ D2))

((c3 => c2) ^ (S2 ⊆ S3) ^ (D2 ⊇ D3))
```

is true. Is

```((c3 => c1) ^ (S1 ⊆ S3) ^ (D1 ⊇ D3))```

also true?

Since ```c3 => c2 => c1```, due to the transitivity of the implication relation we know that ```c3 => c1```.

Since ```S1 ⊆ S2 ⊆ S3```, due to the transitivity of the subset relation we know that ```S1 ⊆ S3```.

Since ```D1 ⊇ D2 ⊇ D3```, due to the transitivity of the superset relation we know that ```D1 ⊇ D3```.

The three transitivities together prove that MU is transitive.

Neutral element (the least useful):

```false => {} → All columns```

```false => c``` is always true, ```{}``` is the subset of everything else, including itself and all columns is the subset of all combinations of columns, or, in other words, it’s a superset of all its subsets.

Antisymmetrical:

```
If P1 MU P2 and P2 MU P1, then P1 <=> P2.

P1 MU P2:

((c2 => c1) ^ (S1 ⊆ S2) ^ (D1 ⊇ D2))

P2 MU P1

((c1 => c2) ^ (S2 ⊆ S1) ^ (D2 ⊇ D1))

P1 MU P2 ^ P2 MU P1 <=>

((c2 => c1) ^ (c1 => c2)) ^

((S1 ⊆ S2) ^ (S2 ⊆ S1)) ^

((D1 ⊇ D2) ^ (D2 ⊇ D1)) <=>

(c1 <=> c2) ^ (S1 = S2) ^ (D1 = D2) <=>

P1 <=> P2
```

so the relation is antisymmetrical:

```((P1 MU P2) ^ (P2 Mu P1)) <=> (P1 <=> P2)```

This means that MU is a poset (partially ordered set) and all the algebra applicable for partially ordered sets in general can be used to analyze MU as well.

The importance of the MU relation is that we can start searching for such patterns in an ordered manner, starting from the most useful we consider and eventually composing S and decomposing D into less useful relation candidates whenever a candidate for a pattern proved to be false, also, knowing that a pattern seems to be accurate we also know that all less useful patterns seem to be accurate as well. Also, if we know that a pattern is accurate, we know that all less useful patterns are accurate as well. We can start our search from a useful pattern candidate, but not necessarily from the most useful, as, intuitively, it is not very probable that all the columns will invariably have the same value of all records. It would defeat the purpose of storing so many values. This means that defining the most useful *possible* patterns would make sense.

#### 5.2. MU Lattice

Possible patterns can be represented using a <a href="http://mathworld.wolfram.com/LatticeTheory.html">Lattice</a>, where the root would be the most useful node and the leaf would be the least useful node. We have a join and a meet operation, which are closures.

```
P1 join P2 = (c1 v c2) => (S1 ⋂ S2) → (D1 ⋃ D2)

P1 meet P2 = (c1 ^ c2) => (S1 ⋃ S2) → (D1 ⋂ D2)
```

Of course

```(P1 join P2) MU (P1 meet P2)```

Proof

```
(c1 ^ c2) => (c1 v c2) is trivially true and

(S1 ⋂ S2) ⊆ (S1 ⋃ S2) is trivially true and

(D1 ⋃ D2) ⊇ (D1 ⋂ D2) is trivially true.
```

We can split the lattice into many different simple lattices, each having its own condition. Since an AR never has source columns, it cannot be less useful than a non AR CFD. Also, since an FD has a condition which is implied by any possible other condition, FDs are never less useful than CFDs with real conditions.

#### 5.3. Domain of search

The domain of search can vary. It can be limited to a single table. Or it can be limited to a cluster of tables, related to each other in one-to-one, one-to-many, many-to-one or many-to-many manner. The condition can be considered to be in a simplistic way, checking only the equals operator of some columns, or, it can be complex and considering several columns, even in a cross-table manner, using several possible operators. This depends on the kinds of patterns we intend to find, the cumulative power of resources, the ability of the development team to work out something serious, time, and, yes, money.

#### 5.4. Differentiation between patterns and reality

We can have a P pattern, which was automatically found. We only know that there is no counter-example of the pattern P, or, if we have a level of tolerance, we know that there were not as many counter-examples so we would discard the pattern. So, P appears to be true. But is appearance equivalent to the truth in this case? As a matter of fact nature produces infinitely many examples of seemingly impossible occurrences or highly improbable coincidences.

It is a common fallacy to concentrate on a pattern and due to the improbability of the result being a mere coincidence to exclude the possibility that it was just a coincidence. Indeed, it’s the so-called <a href="https://www.logicallyfallacious.com/tools/lp/Bo/LogicalFallacies/175/Texas-Sharpshooter-Fallacy">Texas sharpshooter</a> fallacy, even though it’s unconscious in our specific case.

If I have a cube which has 6 sides, each having a number from 1–6 and I toss it 1000 times and the result will always be six, then I will have the natural feeling that something must be not right, I might be divinely favored, or the stars are lining up in my favor, but in this case I'm ignoring the fact that there is no connection between the results of the tosses, or, in other words, my experiments are independent from each other. I could calculate that having a result of 6 for 1000 times has a probability of 1 / 6^1000, which is quasi-impossible. Yet, it is only quasi-impossible and not actually impossible.

If I toss the same cube 1000 times randomly and get a sequence of 1000 numbers, then I could calculate the probability of my random, not special sequence of 1000 elements occuring in the exact same way it occurred. And, surprise, surprise, the result will be exactly equal to 1 / 6^1000, but, if the results of the sequence are varied, I do not feel the results to be special. As a result, having a result of 6 for 1000 tosses is not special at all either.

There is no mathematical difference between the probability of tossing a cube 1000 times and getting only sixes and tossing a cube 1000 times and getting a specific sequence of 1000 elements you might choose. The probability of the exact same sequences will be exactly the same before I start tossing the cube. The difference between the two sequences is the meaning I, as a person attribute to one of them.

Also, if I win a lottery, I might think about the probability of my choice of numeric combination being correct and feel that I'm especially lucky, but if I calculate the probability of the actual result when I do not win, I will not find any difference in the probability itself. Yet, people tend to calculate the chances of the case when they get lucky, but not to calculate the chances when they are not. The low probability of a given event is only special because we are interested in it, but we can find infinitely many similarly low-​probability events happening all the time, but we are just not interested enough in the majority of such events to analyze it.

But let’s see this example further. Before I toss the cube 1000 times I do not know the exact sequence I will get in advance. In fact, it is almost impossible to guess it, but I know that whatever the sequence will be, its a priori probability is converging to zero.

This means that whenever we do not attribute a pattern a meaning, we are inclined to fallaciously not even consider it to be the nature of how things are. Yet, if we attribute a meaning to a pattern, then we might be inclined to fallaciously not understand that it was a mere coincidence if it happens not to be the natural rule of how things are according to our understanding.

If we find a pattern with a tool, we get enthusiastic and we almost want it to be the nature of things, but we need to be much more severe before we factually accept a pattern. Consider the example of primes. How many primes are there? The answer is simple: infinitely many.

Proof (reductio ad absurdum):

Let’s assume that there is a finite n number of primes and there is no other, except them:

```p1, …, pn```

Now, let’s consider the number:

```N = (p1 * … * pn) + 1```

We know that N is indivisible with any of p1, …, pn, so there are two cases: N is either a prime or a composite number. If N is a prime, then we found a new prime. Otherwise, if N is composite, then it is divisible by at least a prime which is not among p1, …, pn. So, in either case we find a new prime, therefore there are infinitely many prime numbers.

How many primes are pair? Exactly one. It is the number 2. Now, if we have a huge set of primes, among which we do not find 2, not knowing that 2 is a prime, we might be inclined to think that primes can only be odd numbers, which is of course wrong. If we pick a prime randomly from the infinitely many primes, the chance that it will be exactly two is extremely small, rather minuscule. However, if a human has to pick a prime number, a human will know only a few primes and 2 is the “first”, so, among the primes 2 is one that has a high chance of being chosen by a human.

The point of all this contemplation is that if something is very frequent or highly probable, then it is not necessarily true. When we take a look at a pattern, it is good to be very critical about it and think about how that pattern could fail and what the consequences would be if we assume the pattern to be accurate, yet it leaves us in trouble in the most inappropriate time.

#### 5.5. Usage of factually validated patterns

Now, if we accept a rule to be factually accurate, then we might want to make sure that it is respected. Assuming that

```c => S → D```

is accurate, we also assume that if the condition is met and there is already a record having the source values of s1, …, sm, then, inserting/​updating another record with the same source values, but with different destination values leads to an error. Let’s suppose that we throw an exception when an accepted pattern is to be violated. If many such exceptions are thrown, then we have a problem. What could the problem be:

- the semantic tree might have wrong/​deprecated rules
- the older records might be broken
- the pattern might be no longer valid, or, it might have been wrongly accepted in the first place

See? By analyzing the data we can add some features of machine-​learning, so our data-miner will really rule the problem space it is responsible for. Naturally, such patterns can also be used at insertion and update, when we do not get some of the destination values, but we have a pattern from which we can deduce it. Naturally, a tableau of at least the most frequent source values and conditions could come to our help.

Knowledge is power. Instead of failing gracefully, outside our limits of what we perceive could result in many months-​long gibberish data. But instead of that pain, we could instantly know when a problem appears and, if we have some helping robotic hands — even if they are only virtual — at the end of the day we will be rarely alerted with urgencies. And such patterns deepen our understanding of the data we work with, even if they cannot be accepted as a general rule. With better understanding we will have better ideas. With better ideas we will have better features and performance. With better features and performance we will have more patterns. And with more patterns: we deepen our understanding further.

### 6. The flow

![](/blog/2019/03/13/the-flow-of-hierarchical-data-extraction/SemanticDataExtractorFigure3.png "The flow")

This diagram is an idealized representation of the flow. In reality we might have several different cron jobs, we might be working with threads, in asynchronous manner and the parser is invoked much more frequently, not just at the end of the whole extraction, because we do not have infinite resources. All these nuances would complicate the diagram immensely.
