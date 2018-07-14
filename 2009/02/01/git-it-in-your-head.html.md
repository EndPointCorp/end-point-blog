---
author: Ethan Rowe
gh_issue_number: 94
tags: git
title: Git it in your head
---

Git is an interesting piece of software. For some, it comes pretty naturally. For others, it’s not so straightforward.

Comprehension and appreciation of Git are not functions of intellectual capacity. However, the lack of comprehension/appreciation may well indicate one of the following:

1. Mistakenly assuming that concepts/procedures from other VCSes (particularly non-distributed “traditional” ones like CVS or Subversion) are actually relevant when using Git

1. Not adequately appreciating the degree to which Git’s conception of content and history represent a logical layer, as opposed to implementation details


CVS and Subversion both invite the casual user to basically equate the version control repository and all operations around it to the file system itself. They ask you to understand how files and directories are treated and tracked within their respective models, but that model is basically oriented around files and directories, period. Yes, there are branches and tags. Branches in particular are entirely inadequate in both systems. They don’t really account for branching as a core possibility that should be structured into the logical model itself; consequently, both systems can keep things simple (the model basically amounts to files and directories), neither one challenges the user mentally, and neither one does much for you when you have real problems to solve that involve branching.

With such a low barrier to entry, where the logical model is barely distinguishable for day-to-day use from the file system, it’s easy for engineers to think of the VCS as a taken-for-granted utility, that should “Just Work” and be really easy and not challenge assumptions, etc. Then Git comes along and punishes anyone who takes that view; if you try to treat Git as a simple utility to drop in the place of CVS/SVN, you will eventually suffer. The engineer **must** grasp the logical layer in order to make effective use of the tool on anything beyond the shallowest of levels.

So, here’s the deal: when they say that Git tracks content, not files, they mean it. They’re telling you that Git isn’t just a nice versioned history of your file system. Rather, Git offers you a deal: you take an hour or two to learn its logical layer (its object model, in a sense), and in exchange Git will give you branching and distributed workflow as a basic way of life. It’s a good deal.

Consequently, those new to Git or those having trouble with Git may do well to throw out any assumptions. Instead, memorize this:

- **Objects** are just things stored in Git that have a type, some data, some Git-oriented headers, and a unique ID consisting of a SHA1 hash of the components of the object. There aren’t very many object types to learn
- **Blobs** are simple objects that just contain some data and could be thought of as “leaves” on a tree. They might represent text files, binary files, symlinks, etc. But they are “blobs”, **not files**, because the blob only represents the **data**, not any real-world identity of that data (“content, not files”)

- **Trees** are objects that contain a list of blob ids paired with some properties and a real-world identity (relative to the tree) for each blob. File system directories map to trees, but they aren’t the same thing.

- **Commits** are objects that reference a single tree object (the top level tree of the repository) and some arbitrary number of parent commits.

- **Refs** aren’t standard Git objects, in that they aren’t storing versioned data or anything like that; rather, they are simply named pointers, each of which references a particular commit object. Branches are refs. Magic things like HEAD are refs. Again, all the ref needs to do is specify a particular commit object.

That’s really not all that much stuff to remember. Then, before thinking about how it relates to files, think through the implications of the object model above. You’ll never get how it works with the file system if you don’t get it as a standalone model first:

- Blobs aren’t versioned. They are standalone pieces of content that are referenced by trees. They **represent** content state, period.
- A tree’s identity is determined by the content of its blobs and their identity relative to that tree
- Consequently, two trees may ultimately only have one different blob (tree A has blob X under branch Z while tree B instead has blob Y under branch Z), but they are two unique trees, that happen to reference some arbitrary number of common trees/blobs (the member trees/blobs that are the same between both will literally be “the same” between both, as they are identified by SHA1)
 - Since the state of the tree determines its identity, it’s easy for Git to determine where differences between two trees occur.
- Since the tree and the parent commits make up a commit object, it’s easy for Git to easily determine whether or not a specific state (combination of tree state and revision history) exists or not in a given history; this is what allows for flexible branching and distributed operations

Once you get all that in your head, then map it to the filesystem.

- Files map to blobs
- Directories map to trees
- Your “checkout” is the mapping of a particular commit’s tree to your file system. That’s where your working tree starts.
- Changing a file means introducing a new blob, which introduces a new tree, which cascades up to the top of your working tree. That’s how the magic happens.

Study the object model, the logical layer, whatever you want to call it. It’s not an implementation detail; it’s the model that makes everything possible. You have to understand Git’s concept of revision history and whatnot if you’re going to make it work for you. Just like you need to learn something new and idiomatic whenever you pick up a new piece of sophisticated software.
