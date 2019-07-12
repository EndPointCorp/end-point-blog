---
title: GraphQL Server Libraries
author: Zed Jensen
tags: graphql
gh_issue_number: 1536
---

<img src="/blog/2019/07/12/graphql-server-libraries/image-0.jpg" alt="Eroded Icelandic mountain" /><br>Photo by <a href="https://unsplash.com/photos/t07FAEn9wAA">Jon Flobrant</a> on Unsplash

This post is a followup to my previous post, [GraphQL — An Alternative to REST](/blog/2019/05/11/graphql-an-alternative-to-rest). Please check that out for an introduction to GraphQL and what makes it different from other API solutions. I’ve collected a list of some of the currently-maintained GraphQL libraries for a few different languages, along with some examples (most of which aren’t fully functional on their own, they’d need more configuration) so you can see what it might be like to use GraphQL in your project. I’ll be focusing on the ways each of these libraries implement GraphQL and what you’d need to do to start a project with each of them, so if you have questions about GraphQL itself, please check out my other blog post.

### Apollo Server (JavaScript/TypeScript)

[Apollo GraphQL](https://www.apollographql.com/) has libraries for both a GraphQL server and client (which I’ll discuss later). [Apollo Server](https://www.apollographql.com/docs/apollo-server/) can be used both as a standalone server as well as with libraries like [Express](https://expressjs.com/). Apollo Server is the server library I have the most experience with—I wrote a server last year using Express and Apollo Server, along with a client that used Apollo Client. I’m a fan of the flexibiliy of Apollo, but it takes more work to set up than some of the alternatives.

Setting up Apollo Server as a standalone can be done fairly simply following the directions on [their website](https://www.apollographql.com/docs/apollo-server/getting-started/). However, I’m going to go over the basics of integrating with Express. There are two main parts to writing a server with Apollo: your GraphQL schema and your resolvers. These stay more or less the same whether you’re using Apollo as a standalone server or combining it with Express. You do have to have a database set up separately; I’ll show examples with MongoDB, but you could easily swap it out with PostgreSQL or another database. I’ll show an example resolver along with its GraphQL schema for a blog post. The schema follows the GraphQL schema rules and might look like the following:

```js
const typeDefs = [gql`
  type Post {
    id: String!
    body: String!
  }

  query {
    post(id: String!): Post
  }
`];
```

Now for the resolver. Resolvers are functions that take information from the query (like arguments) and return the relevant data, usually from a database. For our blog post, a resolver might look like this:

```js
const resolvers = {
  post: (root, args, context, info) => {
    return Post.findById(args.id);
  }
};
```

Simple! We just get the data from the database and return it—as long as the property names match those of our schema, Apollo will automatically format it according to the frontend’s request and return it to them.

OK, next we create the server:

```js
import express from 'express';
import { ApolloServer } from 'apollo-server-express';

const PORT = 3000;

const app = express();
const server = ApolloServer({
  typeDefs,
  resolvers
});

server.applyMiddleware(app);

app.listen(PORT, () => {
  console.log(
    `Server running at http://localhost:${PORT}/graphql`
  );
});
```

And that’s it! Note that these examples are missing a few things like imports, and we didn’t add authentication of any kind, but this is the general format for creating a server with Apollo.

### Prisma

Prisma is a cool library developed by the same people as Graph.cool that does much of the work for you in enabling GraphQL access to your database.

Prisma offers configuration for existing databases, but unfortunately I had trouble getting it to work on my Ubuntu system—I ran into issues getting the Docker container to connect to my local Postgres and MongoDB databases. However, following the quick guide found [here](https://www.prisma.io/docs/get-started/01-setting-up-prisma-new-database-JAVASCRIPT-a002/) on the Prisma website, I was able to get a GraphQL server up and running inside a Docker container with a new database. The process was simple:

First, you have to install the Prisma command line utility:

```
npm install -g prisma
```

You also need to have Docker installed. Documentation for Docker can be found [here](https://docs.docker.com/get-started/).

Next, you need to configure Prisma. Create a directory for your Prisma server, and create a new file named `docker-compose.yml`:

```
mkdir hello-world
cd hello-world
touch docker-compose.yml
```

Then, paste the following into it:

```
version: '3'
services:
  prisma:
    image: prismagraphql/prisma:1.34
    restart: always
    ports:
      - '4466:4466'
    environment:
      PRISMA_CONFIG: |
        port: 4466
        databases:
          default:
            connector: mongo
            uri: mongodb://prisma:prisma@mongo
  mongo:
    image: mongo:3.6
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: prisma
      MONGO_INITDB_ROOT_PASSWORD: prisma
    ports:
      - '27017:27017'
    volumes:
      - mongo:/var/lib/mongo
volumes:
  mongo: ~
```

I used Mongo here, but Prisma’s site has guides for PostgreSQL and MySQL as well. It’s important to make sure now that you don’t have any conflicts with currently running databases—on my machine I had already had a MongoDB server running on port 27017. I fixed this by just stopping my local MongoDB server, but I’m sure you could configure the Docker containers to work with different ports as well. Running Ubuntu, I just ran `sudo service mongodb stop` and then the Prisma Docker containers worked just fine. When I was done, I ran `sudo service mongodb start` to start it up again.

Next, you’ll start the Prisma containers and initialize the Prisma server configuration:

```
docker-compose up -d
prisma init --endpoint http://localhost:4466
```

The final step is to deploy the service:

```
prisma deploy
```

If all goes well, you’ll see a message that includes a URL to the Prisma Admin, which is a browser tool to interact with your GraphQL endpoints. I used it for a little while when I was testing Prisma out, and it seems to work well and is easy to use.

All in all, Prisma seems like a great way to start if you don’t want to handle the messy details of setup. However, I did have issues getting it to play nice with my already-existing databases (including both PostgreSQL and MongoDB). However, it is still relatively new, so I would expect support to get better over time.

### Graphene (Python)

Graphene is a GraphQL framework for Python. It has integrations for a few different server frameworks (a list can be found [here](https://github.com/graphql-python/graphene)), but I’ll show examples from `graphene-django`, since Django is fairly common and something that we use fairly often at End Point.

Because you’re also setting up a Django project, the tutorial for graphene-django is a little more involved, so I’ll just share the relevant GraphQL sections so you can compare to the other libraries in this post. The most important part, the schema, is defined in Python with a similar format to Django models:

```
import graphene

from graphene_django.types import DjangoObjectType

from app.models import Category, Ingredient

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient

class Query(object):
    all_categories = graphene.List(CategoryType)
    all_ingredients = graphene.List(IngredientType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredients(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related('category').all()
```

As you can see, the format for defining your GraphQL schema is quite different from some other libraries, but you have the advantage of it looking similar to Django’s model definitions. You’ll also need a higher-level Query definition:

```
import graphene

import cookbook.ingredients.schema


class Query(cookbook.ingredients.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(query=Query)
```

Now that we have a schema defined, we need to add a few things to `settings.py`:

```
INSTALLED_APPS = [
    ...
    # This will also make the `graphql_schema` management command available
    'graphene_django',
]

GRAPHENE = {
    'SCHEMA': 'cookbook.schema.schema'
}
```

The last piece needed to use your GraphQL schema is in `urls.py`:

```
from graphene_django.views import GraphQLView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^graphql$', GraphQLView.as_view(graphiql=True)),
]
```

And finally we run the server:

```
$ python manage.py runserver
```

Now you should be able to use your GraphQL schema at http://localhost:8000/graphql just like with any other GraphQL server.

Graphene for Django seems like a good solution in that it uses a similar format to other aspects of Django, like the model definitions. However, its format (especially for schema definition) is rather different-looking from the GraphQL standard used by most other libraries, and it seems like it might make it more work to keep your frontend and backend in sync.

### Graph.cool

I won’t discuss Graph.cool in detail here, because I went over it in my previous blog post. However, it still merits mention here as an option for your GraphQL server. Essentially, Graph.cool lets you define a GraphQL schema and then handles the work of setting up a database and even hosting for you. If you just want to get a basic GraphQL server set up for testing, or if you don’t need too many features beyond data storage and retrieval, Graph.cool is a great choice.

### Additional links

For server libraries in other languages, these seem like good options:

- [GraphQL Ruby](https://graphql-ruby.org/)
- [GraphQL Java](https://www.graphql-java.com/)
- [graphql-go](https://github.com/graph-gophers/graphql-go)

Thanks for reading! Keep an eye out next week for a second post which will cover GraphQL client libraries.
