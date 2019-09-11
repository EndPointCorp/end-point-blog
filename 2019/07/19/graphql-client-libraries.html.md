---
title: GraphQL Client Libraries
author: Zed Jensen
tags: graphql
gh_issue_number: 1539
---

<img src="/blog/2019/07/19/graphql-client-libraries/image-0.jpg" alt="three brown wooden boat on blue lake water taken at daytime" /><br>Photo by <a href="https://unsplash.com/photos/T7K4aEPoGGk">Pietro De Grandi</a> on Unsplash

Last week I covered [some of the more popular GraphQL libraries for servers](/blog/2019/07/12/graphql-server-libraries). This post will cover some options for GraphQL clients. Similarly to last week, the examples in this post won’t necessarily be everything you’d need to get a server running; instead, they’re designed to give you an idea of what it might be like to use each library. If you’re unfamiliar with GraphQL, please check out my earlier post [GraphQL — An Alternative to REST](/blog/2019/05/11/graphql-an-alternative-to-rest) for more information.

### Apollo Client

This is the client with which I’m the most familiar—I’ve used its [React version](https://www.apollographql.com/docs/react/), so I’ll show an example of how you’d use it with a React component. However, there are also versions available for [Angular](https://www.apollographql.com/docs/angular/), [Vue.js](https://github.com/akryum/vue-apollo), [native iOS](https://www.apollographql.com/docs/ios/) and [Android](https://www.apollographql.com/docs/android/), and [Scala.js](https://www.apollographql.com/docs/scalajs).

First we need to set up our Apollo client so it knows where our server is:

```
import ApolloClient from "apollo-boost";

const client = new ApolloClient({
  uri: "https://your-server.com"
});
```

Next, you need to make sure the root component of your application is wrapped in an `ApolloProvider`:

```
class App extends Component {
  render() {
    return (
      <ApolloProvider client={client}>
        <RestOfYourApp />
      </ApolloProvider>
    );
  }
}
```

Everything within the `ApolloProvider` has access to your GraphQL API.

To give a component access to query results in a React component, you wrap it in a <Query> component like so:

```
class MyQueryComponent extends React.Component {
  render() {
    const QUERY = gql`
      query ($id: String!) {
        post(id: $id) {
          body
        }
      }
    `;

    return (
      <Query
        query={QUERY}
        variables={{ id: 'id here' }}
      >
        {({ data, error, loading }) => {
          if (loading) {
            return <p>Loading</p>;
          }

          if (error) {
            return <p>Error: {error}</p>;
          }

          return (
            <div>
              <h3>Here's the body of a blog post, fetched from the server:</h3>
              <p>{data.post.body}</p>
            </div>
          );
        }}
      </Query>
    );
  }
}
```

The Query component also lets you provide callback functions like `onComplete`, which runs on a successful response from the server.

Mutations work in much the same way. The main difference is that the child function of the Mutation component takes as its first argument a function that runs the mutation, which you can call whenever you like (in this example, when the user clicks a button).

```
class MyMutationComponent extends React.Component {
  render() {
    const MUTATION = gql`
      mutation ($id: String!, $body: String!) {
        updatePost(id: $id, body: $body)
      }
    `;

    return (
      <Mutation query={MUTATION}>
        {updatePost => (
          <Button
            onClick={() => {
              updatePost({
                variables: {
                  id: 'id here',
                  body: 'new body here'
                }
              });
            }}
          />
        )}
      </Mutation>
    );
  }
}
```

Apollo GraphQL works well with React, at the small cost of adding a couple levels of indentation.

### Relay

[Relay](https://relay.dev/) is another GraphQL library for JavaScript. It’s built specifically for React applications and has a similar format to Apollo. I’m not as familiar with it, but it has a similar setup process to that of react-apollo. Here are the same examples that I used for Apollo but with Relay instead:

```
import {
  Environment,
  Network,
  RecordSource,
  Store,
} from 'relay-runtime';

function fetchQuery(
  operation,
  variables,
) {
  return fetch('/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: operation.text,
      variables,
    }),
  }).then(response => {
    return response.json();
  });
}

const environment = new Environment({
  network: Network.create(fetchQuery),
  store: new Store(new RecordSource()),  
});
```

Here is one of the first differences from Apollo: Relay doesn’t have a `Provider` component that you put at the root of the app. Instead, you provide this `environment` variable to components that need access to your GraphQL API, as in the following example (corresponding to the earlier Apollo component with the same name) of a component displaying the result of a query:

```
import { graphql, QueryRenderer } from 'react-relay';

const environment = /* defined or imported above... */;

class MyQueryComponent extends React.Component {
  render() {
    return (
      <QueryRenderer
        environment={environment}
        query={graphql`
          query ($id: String!) {
            post(id: $id) {
              body
            }
          }
        `}
        variables={{ userID: 'id here' }}
        render={({error, props}) => {
          if (error) {
            return <div>Error!</div>;
          }
          if (!props) {
            return <div>Loading...</div>;
          }
          return (
            <div>
              <h3>Here's the body of a blog post, fetched from the server:</h3>
              <p>{data.post.body}</p>
            </div>
          );
        }}
      />
    );
  }
}
```

There’s one more step to do before you can use these queries, though—before you’re able to run the app, you have to compile your queries with `yarn relay`.

I haven’t used Relay much, but it seems like a similar option to Apollo, and is also developed and used by Facebook.

### GQL (Python)

[GQL](https://github.com/graphql-python/gql-next) is an alternative option for Python. However, it works pretty differently on the developer’s side. From their own README:

> `gql` works by parsing query files (`**/*.graphql` by default) into their own Python module where a class, named after the operation defined in the file, allows you to make that query and get a typed response.

Before doing anything else, you do have to initialize your project against your GraphQL server with `gql.init`. Setup after that is very simple; for our earlier query example, we’d have a file `getpost.graphql` with our query like this:

```
query GetPost($id: String!) {
  post(id: $id) {
    body
  }
}
```

Run `gql run` and the generated Python class would look something like this:

```
# AUTOGENERATED file. Do not Change!
from typing import Any, Callable, Mapping, List
from enum import Enum
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from gql.clients import Client, AsyncIOClient


@dataclass_json
@dataclass
class GetPost:
    @dataclass_json
    @dataclass
    class GetPostData:
        @dataclass_json
        @dataclass
        class Post:
            body: str
        post: Post = None

    data: GetPostData = None
    errors: Any = None

    @classmethod
    def execute(cls, id: str, on_before_callback: Callable[[Mapping[str, str], Mapping[str, str]], None] = None) -> GetPost:
        ...

    @classmethod
    async def execute_async(cls, id: str, on_before_callback: Callable[[Mapping[str, str], Mapping[str, str]], None] = None) -> GetPost:
        ...
```

So, to run a query, you just have to import the class and run execute:

```
from .get_post import GetPost

result = GetPost.execute('meaning_of_life')
post = result.data.post
```

GQL seems pretty straightforward, and is a little easier to set up and understand than some of the other examples we’ve seen. As you might have noticed from the Python class generated earlier, it also provides a way to execute queries asynchronously.

### Conclusion

That covers a few of the most popular libraries for GraphQL! Hopefully these posts have been helpful in bringing to light options for implementing GraphQL in your project. If there’s one you feel I should add, please leave a comment. Following are a few relevant links for languages I didn’t cover:

- End Pointer [Patrick Lewis](/team/patrick_lewis) documented some of his experiences using GraphQL with Ruby [here](/blog/2019/02/28/converting-graphql-ruby-resolvers-to-the-class-based-api) and [here](/blog/2019/03/29/eliminating-resolvers-in-graphql-ruby).
- [Apollo Android](https://github.com/apollographql/apollo-android)
- [graphql-php](https://github.com/webonyx/graphql-php)
