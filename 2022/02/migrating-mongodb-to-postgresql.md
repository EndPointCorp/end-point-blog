---
title: Migrating a Node.js app database from MongoDB to PostgreSQL
author: Phineas Jensen
date: 2022-02-25
github_issue_number: 1835
tags:
- postgres
- mongodb
- database
- nodejs
---

![Trees covered with a small amount of snow against a blue sky and some white puffy clouds](/blog/2022/02/migrating-mongodb-to-postgresql/20220101_214022-sm.webp)

<!-- Photo by Jon Jensen -->

Recently I worked on a web app designed for tracking, editing, and reporting on archaeological survey data. When I joined the project, it used React on the front-end, Node.js on the back-end, GraphQL as the API interface, and MongoDB as the database. For the most part, this architecture and choice of technology worked well, and I was quickly able to make meaningful contributions to the app both in the user interface and in the backend. However, after a while, things started to get difficult and we began to consider _why_ we were using MongoDB, and what might be better.

### MongoDB vs. PostgreSQL

First, why was MongoDB difficult to use in our case? The biggest difficulty was using their query language for certain aspects of our database. Part of the database involved representing artifacts found at a site using a specific type hierarchy defined by the state government. Representing that hierarchy within Mongo was difficult, and querying it even more so. It was hard to find _how_ to query a recursive structure using the MongoDB query language.

As I worked on this, scouring the documentation and Q&A websites to find ways to query this data efficiently, I began to realize that it was a problem that could be easily solved with PostgreSQL's [recursive queries](https://www.postgresql.org/docs/current/queries-with.html#QUERIES-WITH-RECURSIVE).

Now, a single recursive table isn't really a good reason to completely switch the database used by an application, but it got us thinking: Why _were_ we using MongoDB? What benefits was it offering?

I found a relevant article published on the official MongoDB website entitled [Comparing MongoDB vs PostgreSQL](https://www.mongodb.com/compare/mongodb-postgresql). That article is generally very positive in its portrayal of PostgreSQL, so I was interested to hear what they had to say for themselves. Here are some of the main points in favor of MongoDB that the article discusses:

- **MongoDB is horizontally scalable by default:** This seems cool, but we were working on a new app that was not expected to need to scale much, and a single PostgreSQL instance has been shown to scale more than enough for our anticipated needs.
- **MongoDB supports fancy new serverless and mobile paradigms:** Again, cool, but this was a fairly small-scale project using a pretty normal Linux/​Node.js stack. No need for serverless support.
- **MongoDB's document structure makes it easy for developers to change the structure of data on the fly:** While this can certainly be nice, it can also bring its own issues. If data is expected to fit a certain structure and one developer changes that structure, this will likely cause problems for other developers whether or not there is a schema. Additionally, our project had a small team of 1-3 developers working on it and changing the schema as needed just wasn't a problem.

The MongoDB vs. PostgreSQL article also mentions "resilience" as a strength of MongoDB, citing its ability to easily be replicated and broken into shards across datacenters and regions. However, research regarding the historical reliability of PostgreSQL and MongoDB showed that MongoDB's fairly short history is littered with data loss problems. Anecdotally, a Google search for "MongoDB data loss" returns 1.26 million results (an average of 0.14 million results per year since its initial release) while "PostgreSQL data loss" returns 1.57 million (0.06 million per year since release). More specifically, there are fascinating in-depth reviews of MongoDB's reliability, such as those conducted by Jepsen as recently as 2020 (see [#1](https://aphyr.com/posts/284-call-me-maybe-mongodb), [#2](https://aphyr.com/posts/322-jepsen-mongodb-stale-reads), [#3](https://jepsen.io/analyses/mongodb-3-4-0-rc3), [#4](https://jepsen.io/analyses/mongodb-3-6-4), [#5](https://jepsen.io/analyses/mongodb-4.2.6)).

PostgreSQL hasn't been perfect in the 25 years since its initial release, and MongoDB has improved a lot in recent years, but it's clear that Postgres is the winner when it comes to data reliability.

After reviewing all of these pros and cons of MongoDB, it became clear that it wasn't really offering anything that we needed, and our data, which was strictly organized and relational by nature, would fit much better in a relational database. We decided that it would be better to switch to PostgreSQL.

### Mongoose and Sequelize

Our database was only being used within the backend GraphQL server, using [Mongoose](https://mongoosejs.com/), an object modeling library for Node.js. Mongoose uses a schema/​model system, where every MongoDB collection contains documents fitting a schema defined within Mongoose model definitions, for example:

```javascript
import mongoose from "mongoose";
const { Schema } = mongoose;

const blogPostSchema = new Schema({
  title: String, // String is shorthand for {type: String}
  author: String,
  body: String,
  comments: [{ body: String, date: Date }],
  date: { type: Date, default: Date.now },
  hidden: Boolean,
  meta: {
    votes: Number,
    favs: Number,
  },
});

const BlogPost = mongoose.model("BlogPost", blogPostSchema);
```

Once a model is defined it can easily be used to query and create documents:

```javascript
const new_post = new BlogPost({
  title: "On the international epidemic of counterfeit at-home brogal treatments",
  author: "Ronald McClure",
  body: "...",
  // ...
});
await new_post.save();

const posts = await BlogPost.find({ author: "Ronald McClure" });
```

Mongoose provides [a lot of functions](https://mongoosejs.com/docs/api/model.html) for querying and editing documents in a collection on the `Model` class, as well as a rich [Query class](https://mongoosejs.com/docs/api/query.html) to make manual queries, among other things. Their [documentation](https://mongoosejs.com/docs/guide.html) provides helpful guides and a great API reference.

Because we generally liked the Mongoose interface and didn't want to have to change our existing code too drastically, we searched for a similar library that could work with PostgreSQL and settled upon [Sequelize](https://sequelize.org/).

Sequelize has a very similar interface to Mongoose, where you start by defining tables (instead of "collections") as models in JavaScript:

```javascript
const { Sequelize, DataTypes } = require('sequelize');
const sequelize = new Sequelize('postgres://user:pass@example.com:5432/dbname');

const BlogPost = sequelize.define('BlogPost', {
  // Model attributes are defined here
  title: DataTypes.STRING,
  author: DataTypes.STRING,
  body: DataTypes.STRING,
  // This will need to be modeled differently
  // comments: [{ body: DataTypes.STRING, date: Date }],
  date: {
    type: DataTypes.DATETIME,
    defaultValue: DataTypes.NOW
  },
  hidden: DataTypes.BOOLEAN,
  votes: DataTypes.INTEGER,
  favs: DataTypes.INTEGER
}, {
  // Other model options go here
});

// Object creation is similar
const new_post = BlogPost.build({
  title: "On the international epidemic of counterfeit at-home brogal treatments",
  author: "Ronald McClure",
  body: "...",
  // ...
});
await new_post.save();
```

Note that this model, while mimicking the Mongoose schema as much as possible, still requires some changes to fit the relational model. First, the `comments` field, which was an array of documents in the Mongoose object will need to be represented in another table, which can then be linked via foreign key.

While this seems annoying in some ways — creating a new table will require creating another Sequelize model, setting up the relations correctly, etc. — it makes a lot of sense for this example (a blog) and most other situations. We don't just want blog posts to have associated comments, but we likely also want those comments to be tied to an author and to have their own IDs, which would allow lookup by author (for example so that on a user's page they can see all comments they've made on all posts) and by individual comment (so it's easier to make links directly to a single comment).

So, rather than having comments be a subfield of a blog post, we want them to be defined by some kind of relation. In MongoDB this can be done in a few ways, most obviously by creating a `comments` collection making the comments list contain [`ObjectIDs`](https://mongoosejs.com/docs/schematypes.html#objectids):

```javascript
const mongoose = require("mongoose");
const { Schema } = mongoose;

const Comment = mongoos.model(
  "Comment",
  new Schema({
    body: String,
    date: Date,
  })
);

const blogPostSchema = new Schema({
  // ...
  comments: [{ type: Schema.Types.ObjectId, ref: "Comment" }],
  // ...
});

const BlogPost = mongoose.model("BlogPost", blogPostSchema);
```

Mongoose also has a way to automatically fill in those referenced objects with the real thing as needed, using their [populate](https://mongoosejs.com/docs/populate.html) functionality:

```javascript
BlogPost.findOne({ author: "Ronald McClure" })
  .populate("comments")
  .exec(function (err, post) {
    if (err) return handleError(err);
    post.comments.forEach((comment) => console.log(comment));
  });
```

With the call to `.populate('comments')`, the comments array is filled with objects instead of just the object IDs. Sequelize has similar functionality, but uses the concept of [associations](https://sequelize.org/v6/manual/assocs.html) which model the relational structure of SQL more closely:

```javascript
const { Sequelize, DataTypes } = require('sequelize');
const sequelize = new Sequelize('postgres://user:pass@example.com:5432/dbname');

const BlogPost = sequelize.define('BlogPost', {
  // ... fields here
}, {});

const Comment = sequelize.define('Comment', {
  body: DataTypes.TEXT,
  date: DataTypes.DATE,
}, {});

Comment.belongsTo(BlogPost;
BlogPost.hasMany(Comment);
```

These `belongsTo` and `hasMany` associations use foreign key/​primary key references on the models, and Sequelize also provides a similar interface for filling in the referenced data:

```javascript
const post = await BlogPost.findOne({
  where: {
    author: "Ronald McClure",
  },
  include: Comment,
});
```

Both libraries also have ways to lazy-load related objects, only fetching them as necessary. For MongoDB, this involves writing your own queries on referenced fields or using MongoDB's [`$lookup`](https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/) operator, while Sequelize allows custom queries using the foreign key fields, as well as a set of nice [methods to load associations](https://sequelize.org/v6/manual/assocs.html#special-methods-mixins-added-to-instances) on demand.

### Modeling and Migrating Data

Having weighed for this situation the pros and cons of PostgreSQL and MongoDB as well as Mongoose and Sequelize, the question then comes: How do we actually move the data from one system to another? Unfortunately, as far as I know there is no one tool that can be used to migrate data between MongoDB and PostgreSQL. However, using a combination of [`mongoexport`](https://docs.mongodb.com/database-tools/mongoexport/) and some basic SQL files, it was not too difficult to migrate data.

The first step and perhaps one of the more difficult ones is to create an SQL schema that works for your data. If your MongoDB data is already in a normalized and relational structure, it might not be too hard, but if you have a lot of subdocuments and arrays that need to be expanded into rows, things might be more difficult. My recommendation for how to approach this is:

1. Model your data in SQL. If you're doing a migration from MongoDB, you likely have an idea of what the application needs are and how data should be organized.
2. Test your model with some dummy data. This will probably be a bit of a back-and-forth iterative process as you iron out issues with relations, decide what kind of constraints will be necessary, etc.
3. Use `mongoexport` to export your data as appropriate. For many collections, it may be easy to simply export it as CSV and use Postgres's [`COPY`](https://www.postgresql.org/docs/current/sql-copy.html) command to import it into the appropriate table. However, many things won't be so simple and might require writing your own script that reads the exported CSV or JSON and writes it to the database, altering data as needed. This might be necessary for example to change MongoDB's object IDs to match a datatype in PostgreSQL, such as an identity column (defined in [`CREATE TABLE`](https://www.postgresql.org/docs/current/sql-createtable.html)), [`serial`](https://www.postgresql.org/docs/current/datatype-numeric.html#DATATYPE-SERIAL), or [`UUID`](https://www.postgresql.org/docs/current/datatype-uuid.html).
4. Use your set of import commands and scripts to import all of your data into a test database.
5. Modify your application to use Sequelize instead of Mongoose.
6. Find and update all cases in your code where a Mongoose model or instance was used and update it to use Sequelize instead.

### Caveats and Gotchas

One of the biggest problems we came across after our migration was the differences in query syntax between Mongoose and Sequelize. Compare the following queries:

```javascript
// Mongoose
post = await BlogPost.findOne({ author: 'Ronald McClure' });

// Sequelize
post = await BlogPost.findOne({ author: 'Ronald McClure' });
```

They look the same, they both run with no errors, and they both return the one post we created. But say we change which author we are querying for:

```javascript
// Mongoose
post = await BlogPost.findOne({ author: 'Darlene Roberts' });

// Sequelize
post = await BlogPost.findOne({ author: 'Darlene Roberts' });
```

Mongoose's query returns nothing, as we expect, but Sequelize... returns the same post as the "Ronald McClure" query returned? Astute readers might notice what the issue is from earlier examples: Sequelize's [find methods](https://sequelize.org/v6/class/src/model.js~Model.html#static-method-findAll) take an `options` object which doesn't use its fields as `WHERE` parameters by default. The correct way to write this query with Sequelize is:

```javascript
post = await BlogPost.findOne({ where: { author: "Darlene Roberts" } });
```

It's a bit of a silly mistake, but one that caused pain several times in the process of migration. Some queries seemed to work just fine, but just wouldn't return the right results!
