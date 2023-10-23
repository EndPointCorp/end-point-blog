---
title: Upgrade Vue to TypeScript
author: Nicholas Piano
github_issue_number: 2006
featured:
  image_url: /blog/2023/08/upgrade-vue-to-typescript/sunset-field.webp
date: 2023-08-28
tags:
- vue
- typescript
---

![An expansive sky filled with faintly red clouds extends above a field turned red from the sunset. A layer of trees separates the field from the sky](/blog/2023/08/upgrade-vue-to-typescript/sunset-field.webp)

<!-- Photo by Seth Jensen, 2023. -->

It's important to keep your code up to date so that time can be dedicated to improving an application instead of version-related mishaps. This is especially true for web development as the landscape changes so quickly.

I recently upgraded a Vue project to exclusively use Vuex. This was a great opportunity to also upgrade the project from JavaScript to TypeScript. This article will cover the steps I took.

Some of the changes can be difficult to understand if you are not familiar with TypeScript. I recommend reading the [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) to become more familiar.

Several features of Vue, originally written in JavaScript without types, are hard to convert to TypeScript. These include `this.$parent`, `this.$refs`, and `this.$emit`. These allow you to access the parent component, child components, and emit events respectively. We will make changes to these features along with adding types to the global state handler provided by `Vuex.Store`.

### Installation

Before you begin, make sure the necessary dependencies are installed:

```plain
~$ vue add typescript
```

Also make sure that Vuex is installed:

```plain
~$ yarn add vuex@next
```

### Convert your component files

There are several changes that must be made to component files, such as `App.vue`.

1. Add `lang="ts"` to the `<script>` tag.
2. Replace the default export with a class that extends `Vue` and uses the `@Component` decorator.
3. Replace `props` with class properties marked with the `@Prop` decorator.
4. Replace `data` with individual class properties.
5. Add a typed `$refs` class property.
6. Replace `computed` with getter and setter class properties.
7. Lifecycle hooks simply become class methods, so they can be copied directly.
8. Replace `methods` with individual class methods.
9. Replace `this.$emit` with class methods using the `@Emit` decorator.

Let's look at each change separately.

#### Add `lang="ts"` to the `<script>` tag

This is the easiest change. Simply add `lang="ts"` to the `<script>` tag.

```diff
-<script>
+<script lang="ts">
```

#### Replace the default export with a class that extends `Vue` and uses the `Component` decorator

This change can be complicated to visualise, but the `@Component` decorator provided by `vue-class-component` makes it easy to convert a component incrementally by accepting existing properties of the default export as arguments to allow backwards compatibility.

First, replace the default export with a class component:

```diff
-export default {
-  name: 'App',
-  components: {
-    HelloWorld
-  },
-  props: ['msg'],
-}
+import Component from 'vue-class-component'
+import { Vue } from 'vue-property-decorator'
+
+@Component({
+  components: {
+    HelloWorld
+  },
+  props: ['msg'],
+})
+export default class App extends Vue {}
```

Note that the `name` property is no longer necessary. The name of the component is now the name of the class.

Also, to illustrate the capability of the `@Component` decorator, the `props` property is passed as an argument. This allows the component to be used as before with no other changes. Next, we will replace `props` with class properties marked by the `@Prop` decorator.

#### Replace `props` with class properties marked by the `@Prop` decorator

The `@Prop` decorator is used to mark class properties as props. It accepts an optional argument to specify the type of the prop. If no argument is provided, the type is inferred from the default value.

```typescript
import Component from 'vue-class-component'
import { Prop, Vue } from 'vue-property-decorator'

@Component
export default class App extends Vue {
  @Prop() msg!: string
  @Prop({ type: Number }) count!: number // type can also be specified explicitly
  @Prop(Boolean) disabled!: boolean // shorthand for { type: Boolean }
}
```

Now, when a prop is referenced in a function or the template, it will be typed correctly.

#### Replace `data` with individual class properties

The `data` property is replaced with individual class properties.

```javascript
export default {
  name: 'App',
  data() {
    return {
      count: 0,
      msg: 'Hello World',
      complex: { /* ... */ },
    },
  },
}
```

Becomes:

```typescript
@Component
export default class App extends Vue {
  count = 0
  msg: string = 'Hello World'
  complex: ComplexType = { /* ... */ }
}
```

As before, types can be specified explicitly or inferred from the default value.

#### Add a typed `$refs` class property

The `$refs` property is typed by adding a class property with the same name and type.

```typescript
@Component
export default class App extends Vue {
  $refs!: {
    input: HTMLInputElement
  }
}
```

Now, references to `$refs.input` will be typed correctly.

#### Replace `computed` with getter and setter class properties

The `computed` property is replaced with getter and setter class properties.

```javascript
export default {
  name: 'App',
  computed: {
    count() {
      return this.$store.state.count
    },
    msg() {
      return this.$store.state.msg
    },
  },
}
```

Becomes:

```typescript
@Component
export default class App extends Vue {
  get count() {
    return this.$store.state.count
  }
  set count(value: number) {
    this.$store.commit('setCount', value)
  }
  get msg() {
    return this.$store.state.msg
  }
  set msg(value: string) {
    this.$store.commit('setMsg', value)
  }
}
```

Now the getters and setters can accept and return the correct types.

#### Lifecycle hooks become class methods

Lifecycle hooks such as `created` and `mounted` are represented as class methods.

```javascript
export default {
  name: 'App',
  created() {
    this.$store.commit('setCount', 0)
    this.$store.commit('setMsg', 'Hello World')
  },
}
```

Becomes:

```typescript
@Component
export default class App extends Vue {
  created() {
    this.$store.commit('setCount', 0)
    this.$store.commit('setMsg', 'Hello World')
  }
}
```

#### Replace `methods` with individual class methods

The `methods` property is replaced with individual class methods. Not much about the methods needs to change.

```javascript
export default {
  name: 'App',
  methods: {
    increment() {
      this.$store.commit('increment')
    },
    decrement() {
      this.$store.commit('decrement')
    },
  },
}
```

Becomes:

```typescript
@Component
export default class App extends Vue {
  increment() {
    this.$store.commit('increment')
  }
  decrement() {
    this.$store.commit('decrement')
  }
}
```

#### Replace `this.$emit` with class methods using the `@Emit` decorator

The `@Emit` decorator is used to mark class methods as emitters. It accepts an optional argument to specify the event name. If no argument is provided, the event name is the name of the method.

```javascript
export default {
  name: 'App',
  methods: {
    setValue(value) {
      this.$emit('set-value', value)
    },
  },
}
```

Becomes:

```typescript
@Component
export default class App extends Vue {
  @Emit('set-value') setValue(value: string) {
    return value
  }
}
```

This would be called from the parent component in the same way:

```html
<template>
  <app @set-value="onSetValue" />
</template>
```

Now that your components have been converted, let's look at the store.

### Convert your store

State in Vuex is managed using the `Vuex.Store` object. Below is a basic example:

```typescript
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    count: 0,
    msg: 'Hello World',
  },
  mutations: {
    setCount(state, value) {
      state.count = value
    },
    setMsg(state, value) {
      state.msg = value
    },
    increment(state) {
      state.count++
    },
    decrement(state) {
      state.count--
    },
  },
  getters: {
    count: state => state.count,
    msg: state => state.msg,
  },
  actions: {
    increment(context) {
      context.commit('increment')
    },
    decrement(context) {
      context.commit('decrement')
    },
  },
})
```

Inside a component, access to the store can be typed using the `@State`, `@Mutation`, `@Getter`, and `@Action` decorators.

```typescript
import { Component } from 'vue-property-decorator';
import { Mutation, Getter, Action } from 'vuex-class';

@Component
export default class MyComponent extends Vue {
    @State count!: number
    @State msg!: string
    @Mutation setCount!: (value: number) => void
    @Mutation setMsg!: (value: string) => void
    @Mutation increment!: () => void
    @Mutation decrement!: () => void
    @Getter count!: number
    @Getter msg!: string
    @Action increment!: () => void
    @Action decrement!: () => void
}
```

Parts of the store can also be namespaced using the `modules` key in the store object:

```typescript
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: { ExampleModule },
});
```

Where a module is an object with the same structure as the store object. See the [Vuex module documentation](https://vuex.vuejs.org/guide/modules.html) for more information.

The namespaced state can then be typed and accessed from components:

```typescript
import { Component } from 'vue-property-decorator';
import { namespace } from 'vuex-class';

const Store = {
  ExampleModule: namespace('ExampleModule'),
};

@Component
export default class ImportExample extends Vue {
  @Store.ExampleModule.Action('import') import!: ({ file, config }: { file: File; config: ExampleConfig }) => Promise<boolean>;
}
```

Note that this adds types to the store access points within components, but does not fully statically type the store itself. For more information on how to do this, refer to this excellent article: [Vuex + TypeScript](https://dev.to/3vilarthas/vuex-typescript-m4j).

### Conclusion

In conclusion, despite the number of steps needed to convert your Vue components and store, the process is relatively simple. The result is a fully typed Vue application that is easier to maintain and refactor. You won't regret the ability to trace the flow of data through your application. Additionally, currently developed packages for Vue such as [Vuetify](https://vuetifyjs.com/en/) and [Vuelidate](https://vuelidate.js.org/) are fully typed and will work seamlessly with your new Vue application.
