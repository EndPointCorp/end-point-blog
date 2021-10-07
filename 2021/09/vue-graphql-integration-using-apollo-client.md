---
author: Daniel Gomm
title: Vue GraphQL Integration Using Apollo Client
date: 2021-09-22
---

### Introduction
In this post I’ll go over everything you need to know to get your Vue app using GraphQL to send and receive data. This post only covers the frontend -- stay tuned for my next post on making a graphql server using django and graphene-python! 

For the uninitiated, [GraphQL](https://graphql.org/) is a query language that aims to replace the traditional REST API. The idea is that, instead of having separate endpoints for each resource in your API, you could have one endpoint that accepts GraphQL queries and mutations for all your resources. Overall, this makes data access on the frontend more like querying a database. Not only does it give you more control over your data, but it also can be much faster than using a REST API, providing a better user experience. 

### Getting Started

To get your Vue app set up using GraphQL we'll need to do two things. First, we'll install [vue-apollo](https://www.npmjs.com/package/vue-apollo), a Vue plugin for the [Apollo](https://www.apollographql.com/) GraphQL client and [apollo-boost](https://www.npmjs.com/package/apollo-boost), which bootstraps configuration of Apollo. With these you'll be able to:

* Manually run GraphQL queries and mutations from any Vue component via the `this.$apollo` helper
* Automatically map GraphQL queries to a component’s data fields by adding the `apollo` property to your component
   * These queries will lazy load data from Apollo's cache to minimize requests across multiple components

Second, we'll add webpack configuration so that you can store your graphql queries and mutations in separate files (`.gql` or `.graphql`), and import them directly into your component files.

Let's begin by installing the required npm packages:

```bash
npm install graphql vue-apollo apollo-boost graphql-tag
```

#### Setting up VueApollo

To set up the `VueApollo` plugin, we'll use the `ApolloClient` helper from `apollo-boost`, and pass it the URL to your GraphQL api endpoint:

**main.js**
```js
import Vue from 'vue';
import App from './App.vue';
import ApolloClient from 'apollo-boost';
import VueApollo from 'vue-apollo';

// Create the apolloProvider using the ApolloClient helper
// class from apollo-boost
const apolloProvider = new VueApollo({
  defaultClient: new ApolloClient({
    uri: '<YOUR_GRAPHQL_ENDPOINT_HERE>'
  })
});

// Add VueApollo plugin
Vue.use(VueApollo);

// Instantiate your Vue instance with apolloProvider
new Vue({
  apolloProvider,
  render: h => h(App),
}).$mount('#app')
```

With this configuration in place, you now have access to `this.$apollo` in all your components, and you can add smart queries to them using the `apollo` property. 

####  GraphQL File Imports

To enable file GraphQL file imports, update **vue.config.js** to use the included graphql loader from `graphql-tag` to parse all files with a `.graphql` or .`gql` extension:

**vue.config.js**
```js
module.exports = {
    chainWebpack: (config) => {
        // GraphQL Loader
        config.module
          .rule('graphql')
          .test(/\.(graphql|gql)$/)
          .use('graphql-tag/loader')
          .loader('graphql-tag/loader')
          .end();
      },
};
```

Once this configuration is in place, you can create a `.gql` or `.graphql` file, and import it directly into your javascript files:

```js
import MY_QUERY from "./my-query.gql";
```

This imported query (named `MY_QUERY` in the example) is a `DocumentNode` object, and can be passed directly to Apollo.

As a side note: If you have an existing GraphQL server, it’s usually possible to export your schema into a `.gql` file that contains the queries and mutations your server uses. Not only does this save a lot of time, but it helps minimize inconsistencies between the queries on the frontend and what the backend actually does.

### Loading Data With Apollo Queries
With Apollo, you can configure any Vue component to map graphql queries to fields in its data. You can do this by adding an `apollo` object to your component. Each field on this object is an [Apollo Smart Query](https://apollo.vuejs.org/api/smart-query.html), which will automatically run the query (lazily loading from the cache) and then map the query results to a field in the component’s data. The name of the mapped data field will be the same as the field name within the `apollo` object.

For example, let’s say we needed to make a component load a list of blog posts, given a user ID, and display the total number of posts for that user. To do this using Apollo, you’ll need to define a GraphQL query that accepts a userId as a variable, and queries for a user’s posts. Here’s how that query would look:

**posts.gql**
```graphql
query ($userId: String!) {
    posts(userId: $userId) {
        id 
        content
    }
}
```

We can then define an apollo object on the component that loads the data from the query into our component’s data:

**posts.vue**
```vue
<template>
    <p>
        Total number of posts: {{posts.length}}
    </p>
</template>
<script>
import POSTS_BY_USER from "./posts.gql";

export default {
    name: 'NumPosts',
    props: ['userId'],
    data() {
        return {
            // This value is updated by apollo when the query
            // is run and receives data
            posts: [],
        }
    },
    // This smart query will automatically run the POSTS_BY_USER
    // query when the component is mounted. It also responds to 
    // changes in any of its variables, and will automatically 
    // rerun the query if the userId changes.
    apollo: {
        posts: {
            query: POSTS_BY_USER,
            variables() {
                return { userId: this.userId };
            },
        },
    },
}
</script>
```

The smart query accepts a graphql query, and a variables object where the keys are the variable names, and the values are the variable values. What this will do is run the `POSTS_BY_USER` query when the component mounts, and store the results of that query in the `posts` data field. Then, any time one of the variables changes (in this case, it would happen if the `userId` prop receives a new value), the query will be rerun and `posts` will again be updated. Additionally, the results of the query are stored in Apollo’s cache. So, if another component has the same smart query in it, only one actual request will be made. 

### Updating Data With Apollo Mutations
To update existing objects using GraphQL, we use mutations. GraphQL mutations look similar to queries, except that on the server, they will update or create new resources. For example, a mutation to update an existing user’s post would look like this: 

```graphql
mutation ($id: Int!, $content: String!) {
    updatePost(id: $id, content: $content) {
        id
        content
    }
}
```

Running this mutation will cause the server to update the post with the specified `$id`. To run GraphQL mutations from your component, you can use the apollo mutate method:

```javascript
this.$apollo.mutate({
    mutation: UPDATE_POST,
    variables: { id: this.post?.id, content: this.newContent }
});
```

This function sends the `UPDATE_POST` mutation to the server to be run, and then updates the cache for all occurrences of the post with the given `id` when it receives the response.

For updating existing objects, Apollo is able to automatically handle updating the cache. However, when creating a new object, the cache needs to be updated manually. I’ll demonstrate this in the next section.

### Creating Data And Handling Cache Updates

Apollo has a global cache of query results, which prevents duplicate requests from being made when the same query is run again in the future. In the cache, each query is indexed using the query itself, and the variables it was run with. 

When you run a mutation that updates an existing object, Apollo is smart enough to update the cache because it can use the ID of that object (from the mutation's variables) to find all cached queries that include it. However, when creating new objects, Apollo won’t update the cache because there’s no object in any cached queries with the ID of the new object. This is why you’ll have to either update the cache yourself, or specify which queries need to be re-fetched after running the mutation. 

While specifying the queries to re-fetch makes the code much simpler, it might make more sense to do a manual update if the query to be re-fetched is costly. 

Continuing with our blog posts example, let’s assume we have a query `POSTS_BY_USER`, which returns a list of all posts for a given user ID. If we wanted to create a new post, we’d need to update the cached results for `POSTS_BY_USER` with the given user ID to include the new post. 

To create a new post, and then re-fetch the `POSTS_BY_USER` query, it would look like this:

```javascript
this.$apollo.mutate({
    mutation: ADD_POST,
    variables: { content: this.newPostContent },
    refetchQueries: [
        {
            query: POSTS_BY_USER, 
            variables: { userId: this.currentUser.id }
        }
    ]
});
```

To do the same exact thing with a manual cache update, it would look like this:

```javascript
this.$apollo.mutate({
    mutation: ADD_POST,
    variables: { content: this.newPostContent },
    update: (cache, result) => {
        // the new post returned from the server. notice how 
        // the field on data matches the name of the mutation 
        // in the graphql code.
        let newPost = result.data.addPost;

        // Queries are cached using the query itself, and the
        // variables list used.
        let cacheId = {
            query: POSTS_BY_USER,
            variables: { userId: this.currentUser.id },
        };

        // Get the old list from the cache, and create a new array
        // containing the new item returned from the server along 
        // with the existing items
        const data = cache.readQuery(cacheId);
        const newData = [...data.postsByUser, newPost];

        // Write the new array of data for this query into 
        // the cache
        cache.writeQuery({
            ...cacheId,
            data: { postsByUser: newData },
        });
    },
    // By specifying optimistic response, we're instructing apollo 
    // to update the cache before receiving a response from the 
    // server. This means the UI will be updated much quicker.
    optimisticResponse: {
            __typename: "Mutation",
        addPost: {
            __typename: "Post",
            id: "xyz-?",
            content: this.newPostContent,
            userId: this.currentUser.id,
        },
    },
});
```

There’s a few things to note about the above code. First, it specifies an `optimisticResponse` field on the mutation. This field can be used to pass a response to Apollo before the server actually responds. If you know exactly what the response will look like, you can use it to enhance the user experience by making the UI respond instantaneously, rather than delay while the server processes the request. 

As you can see, manually updating the cache requires quite a bit of code to accomplish, and is a bit hard to read. In my own projects, I found it best to abstract the Apollo mutations into separate helper functions that just accept the variables object. This way, the cache updates stay separate from the business logic of the components, and aren’t scattered throughout the codebase.

### Conclusion
And that’s it! My experience converting an existing Vue codebase to use Apollo/GraphQL was a very positive one. The resulting code had much better performance than manually sending requests and updating a Vuex store, and was a lot easier to work on. 

Have any questions? Feel free to leave a comment!
