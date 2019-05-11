---
author: "Zed Jensen"
title: "GraphQL — An Alternative to REST"
tags: graphql, database
gh_issue_number: 1523
---

![Banner](/blog/2019/05/11/graphql-an-alternative-to-rest/banner.jpg)

[GraphQL](https://graphql.org/) has become more and more popular recently as an alternative to traditional RESTful APIs since it was released as open source by Facebook in 2015. According to the GraphQL website, it is “a query language for APIs and a runtime for fulfilling those queries with your existing data”. In this blog post, I’ll go over some of what makes GraphQL different from other API solutions, and then show how to get a GraphQL API up and running so you can try it out yourself!

GraphQL is designed to fit on top of your database layer. With the help of libraries like [Apollo GraphQL](https://www.apollographql.com/), it can be used with many different databases. Some of the main differences between GraphQL and more traditional RESTful APIs include:

- GraphQL uses one endpoint. Most traditional APIs use an endpoint for each type of data; in my example, you’d probably have one each for users (`/user`), posts (`/post`) and comments (`/comment`). Each of these would return some JSON with the data you want. GraphQL, on the other hand, lives at one endpoint (usually `/graphql`) and changes what it returns based on what you ask for, as detailed in the next point.

- You can get multiple types in one request. For instance, if you want to get information about an author plus all of their posts, instead of making a request for the author and a request for posts, you do just one request for the author and specify that you’d like their posts as well:

```
query {
  user(id: "12345") {
    name
    posts {
      title
      body
    }
  }
}
```

- You decide which parts of the data you want. Traditional REST APIs give you data based on which endpoint you’re querying (`/post/:id`, `/user/:id`, etc.), and the format of the data is generally the same. For instance, no matter which `id` you ask for at `/posts/:id`, you’ll always get something that looks like this back:

```json
{
  "id":"123",
  "name":"Smash Mouth",
  "joined":"1994"
}
```

But what if we don’t need to know when they joined right now? Another example that better illustrates this problem (and GraphQL’s solution) is getting a list of blog posts. The home page of a blog usually shows several of the most recent posts, but you can also view a list of just post names that will go farther back. With a traditional REST API, you would have to create separate endpoints for each of these scenarios, for example `/first_posts` and `/posts`, or add GET parameters or similar. With GraphQL, you can just specify exactly what you want. The query to replace `/first_posts` might look like this:

```text
query {
  posts {
    title
    body
    author {
      name
    }
  }
}
```

The data returned might look like:

```json
{
  "data": {
    "posts": [
      {
        "title": "All Star",
        "body": "Somebody once told me the world is gonna roll me\n I ain't the sharpest tool in the shed\n She was looking kind of dumb with her finger and her thumb\n In the shape of an \"L\" on her forehead\n Well the years start coming and they don't stop coming\n Fed to the rules and I hit the ground running\n Didn't make sense not to live for fun\n Your brain gets smart but your head gets dumb\n So much to do, so much to see\n So what's wrong with taking the back streets?\n You'll never know if you don't go\n You'll never shine if you don't glow\n Hey now, you're an all-star, get your game on, go play\n Hey now, you're a rock star, get the show on, get paid\n And all that glitters is gold\n Only shooting stars break the mold\n Only shooting stars break the mold",
        "author": {
          "name": "Smash Mouth"
        }
      },
      {
        "title": "Less-interesting Stuff",
        "body": "Sed ut perspiciatis, unde omnis iste natus error sit voluptatem\n accusantium doloremque laudantium, totam rem aperiam eaque ipsa, quae ab illo inventore\n veritatis et quasi architecto beatae vitae dicta sunt, explicabo. Nemo enim ipsam\n voluptatem, quia voluptas sit, aspernatur aut odit aut fugit, sed quia consequuntur\n magni dolores eos, qui ratione voluptatem sequi nesciunt, neque porro quisquam est, qui\n dolorem ipsum, quia dolor sit amet consectetur adipisci[ng] velit, sed quia non-numquam\n [do] eius modi tempora inci[di]dunt, ut labore et dolore magnam aliquam quaerat\n voluptatem. Ut enim ad minima veniam, quis nostrum[d] exercitationem ullam corporis\n suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure\n reprehenderit, qui in ea voluptate velit esse, quam nihil molestiae consequatur, vel\n illum, qui dolorem eum fugiat, quo voluptas nulla pariatur?",
        "author": {
          "name": "Some Latin-speaking Guy"
        }
      }
    ]
  }
}
```

That’s great for `/first_posts`, but we probably don’t need to bloat the response with the entire post body if we’re just using the names for a list, right? Let’s try again, but this time we’ll remove `body` from the request:

```text
query {
  posts {
    title
    author {
      name
    }
  }
}
```

Now we just get the title and author, exactly like we want. Notice also that these queries are pulling in data from a related model, the User model, via the `author` property.

```json
{
  "data": {
    "posts": [
      {
        "title": "All Star",
        "author": {
          "name": "Smash Mouth"
        }
      },
      {
        "title": "Less-interesting Stuff",
        "author": {
          "name": "Some Latin-speaking Guy"
        }
      }
    ]
  }
}
```

Although you can get similar functionality by using GET parameters or creating extra endpoints, with GraphQL, you can just make that one simple change without needing to write extra code.

### Try it!

OK, so there are some of the things that sets GraphQL apart. However, reading about it is only so helpful—now I’ll show how to get a GraphQL backend up and running quickly using [Graph.cool](https://www.graph.cool/), a Node.js backend service that does most of the work of setting up a server, including setting up a database based on your schema. (Graphcool also offers a more flexible server option called Prisma, but graphcool itself is more than enough for this example.)

First, you need to install graphcool by running:

`npm install -g graphcool`

You’ll also need to sign up for a (free) account, but you can do that later. Once graphcool is installed, create a directory to use for your code and initialize it.

```bash
$ mkdir gql-blog
$ cd gql-blog
$ graphcool init
```

Open the file `types.graphql` and uncomment the lines describing a model called Post, as well as the related line in User; aftewards, it should look something like this:

```text
type User @model {
  # id is of type ID, must be not null (!), and must be unique
  id: ID! @isUnique
  name: String
  dateOfBirth: DateTime

  # posts contains an array of Post objects
  posts: [Post!]! @relation(name: "UserPosts")
}


type Post @model {
  id: ID! @isUnique
  title: String!

  # Graphcool relations have to be defined both ways so the service knows
  # whether it's a one-to-many, many-to-many, or many-to-one relation
  author: User! @relation(name: "UserPosts")
}
```

Note that there are a few extra descriptors here that aren’t part of the core GraphQL schema; `@isUnique`, `@relation`, `@model`, and `ID` are all part of the Graphcool service’s additions. However, they are allowed within GraphQL’s spec and provide some extra functionality to the API. [GraphQL’s website](https://graphql.org/learn/schema/#type-system) has more information about the type system.

Now that you have a basic schema, it’s time to run your server. In the directory where you ran `graphcool init`, run `graphcool deploy`. First, it’ll open a browser window and ask you to log in or create an account. Once you do that, you should see a prompt asking you which server cluster you want to deploy to. Pick any of them (but note that `local` requires a bit more setup before working). Push enter on the next few prompts to use the default options and you’ll get a big wall of text telling you that your server is up and running! To try it out, find the line near the end that looks like this:

```text
Here are your GraphQL Endpoints:

  Simple API:        https://api.graph.cool/simple/v1/bbd987478jjhhds902k2l
```

Copy and paste that URL into a browser and you’ll have access to the GraphQL Playground, where you can run queries and mutations (like queries, but for creating/updating data). You need some data to play with, so copy the following into the Playground one at a time and run them to create a User and a Post. Note that you’ll need to look at the ID returned by the first mutation and paste it into the second mutation so that the two are linked.

```text
mutation {
  createUser(
    name: "SmashMouth"
  ) {
    id
    name
  }
}
```

```text
mutation {
  createPost(
    title: "All Star",
    authorId: "USER_ID_HERE"
  ) {
    id
    title
  }
}
```

Once those are finished, you can run queries to get the data you want. Here’s an example of a query to return the author you created earlier plus any posts associated with it:

```text
query {
  User(id: "USER_ID_HERE") {
    id
    posts {
      id
    }
  }
}
```

You’ll notice that this query only returns the ID of the user and their posts. That’s because we only asked for the ID—if you want to get the name of the user and the title of the post, you’ll have to add that to the query:

```text
query {
  User(id: "USER_ID_HERE") {
    id
    name
    posts {
      id
      title
    }
  }
}
```

Pretty cool, huh? You get exactly what you ask for. Next, try getting your post (you’ll need its ID) and asking for its author along with it..

On the far right of the GraphQL Playground, there’s a tab labeled Schema that shows the entire schema of your app. If you look in there, you’ll see that there are far more types defined than were in the `types.graphql` file we edited earlier—this is because graphcool automatically generates them for you. That’s the main reason why it’s easier to use than other GraphQL libraries. In particular, you might try getting all posts or all users.

If you want to keep messing around with GraphQL, I’d suggest trying to add your own new `Comment` type to types.graphql, emulating the way User and Post are related to each other. Keep in mind that you’ll have to run `graphcool deploy` and reload your browser to see your changes show up in the Playground.

For more information and thorough documentation, the following sites are your best bet:

- [GraphQL website](https://graphql.org/learn/)
- [Graphcool Docs](https://www.graph.cool/docs)

If you want to try GraphQL without installing anything, these sites let you try it on their own servers:

- [graphql.nodaljs.com](http://graphql.nodaljs.com/)
- [try.sangria-graphql.com](http://try.sangria-graphql.org)
- [trygql.com](https://trygql.com/)

