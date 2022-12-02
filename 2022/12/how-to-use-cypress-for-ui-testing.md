---
author: Edgar Mlowe
title: "How to write End-to-End and Component Tests with Cypress in Vue"
date: 2022-12-10
featured:
  image_url: /blog/2022/12/how-to-use-cypress-for-ui-testing/beach-zanzibar.webp
description: In this tutorial, I am going to explain how to handle UI testing with Cypress and convince you that writing tests is not always so tedious and expensive, but can be fun instead.
github_issue_number: 1923
tags:
- cypress
- vue
- javaScript
---

![A white beach in Zanzibar, Tanzania during a hot sunny day. A few trees provide shade for the beach, looking out at a light blue ocean.](/blog/2022/12/how-to-use-cypress-for-ui-testing/beach-zanzibar.webp)

<!-- Photo by Edgar Mlowe, 2018 -->

Is writing tests painful for you? In this tutorial, I am going to explain how to handle UI testing with [Cypress](https://www.cypress.io) and convince you that writing tests is not always so tedious and expensive, but can be fun instead.

Cypress is a purely JavaScript-based front-end testing tool built for the modern web. it can test anything that runs in browser and has built-in support for testing modern frameworks such as Vue, React, and Angular. See the full list of supported front-end frameworks [here](https://docs.cypress.io/guides/component-testing/overview#Supported-Frameworks).

We are going to use a Todo app built using Vue as an example, through that we are going to learn:

* How to install and set up Cypress.
* How to create a simple Todo app with Vue 3.
* How to write end-to-end tests.
* How to write component tests.

### How to install and set up Cypress

1. First things first, let's create a new Vue project using Vue CLI.

    Install Vue CLI if you don't have it in your machine:

    ```plain
    npm install -g @vue/cli
    ```

2. create a project (pick the `Vue 3,babel,eslint` preset):

    ```plain
    vue create todo-app
    ```

3. `cd` into the `todo-app` project and install Cypress with only one command:

    ```plain
    npm install cypress --save-dev
    ```

    No dependencies, extra downloads, or changes to your code are required!

3. Edit `package.json`. In the `scripts` section, add a command, `"cypress:open": "cypress open"`. See the example below.

    ```json
    "scripts": {
        "cypress:open": "cypress open"
    }
    ```

4. Launch Cypress:

    ```plain
    npm run cypress:open
    ```

When Cypress opens up you should be able to view the Cypress launchpad as shown in the image below:

![Screenshot of Cypress launcher window displaying testing options. The header reads "todo-app (master)". The body reads "Welcome to Cypress!", and has a link reading "Review the differences between each testing type". Two boxes read "E2E Testing" and "Component Testing", both with buttons reading "Not Configured" next to an unfilled circle.](/blog/2022/12/how-to-use-cypress-for-ui-testing/cypress-launcher.webp)

We will use the Launchpad to configure both E2E Testing and Component Testing. Cypress will automatically generate configuration files as you configure the tests in the Launchpad. If you get stuck, please visit the [docs for Launchpad](https://docs.cypress.io/guides/getting-started/opening-the-app#The-Launchpad).

### How to create a simple Todo app with Vue 3

Open the `todo-app` project in your favourite editor and add the following single-file components:

1. `src/components/BaseTextInput.vue`

    BaseTextInput will contain a text input and a button for adding new Todo items.

    ```javascript
    <template>
        <form class="add-todo-form">
            <input type="text" class="input" placeholder="Add a new todo" v-model="todo">
            <input type="submit" value="Add" @click="emitNewTodoEvent">
        </form>
    </template>

    <script>
    export default {
        data() {
            return {
                todo: ''
            }
        },
        methods: {
            emitNewTodoEvent(e) {
                e.preventDefault();
                this.$emit('newTodo', this.todo);
                this.todo = '';
            }
        }
    }
    </script>

    <style scoped>
    .input {
        width: 100%;
        padding: 8px 10px;
        border: 1px solid #32485F;
    }

    .add-todo-form {
        width: 100%;
        display: flex;
        align-items: center;
    }

    input[type="submit"] {
        margin-left: 5px;
        padding: 8px 10px;
        border: 1px solid #32485F;
        background-color: #32485F;
        color: #fff;
        font-weight: bold;
        cursor: pointer;
    }

    input[type="submit"]:hover {
        background-color: #00C185;
    }
    </style>
    ```

2. `src/components/TodoListItem.vue`

    TodoListItem displays a Todo along with a button for removing that Todo.

    ```javascript
    <template>
        <li>
          {{ todo.text }}
          <button @click="$emit('remove', todo.id)">
            X
          </button>
        </li>
      </template>

      <script>
      export default {
        props: {
          todo: {
            type: Object,
            required: true
          }
        }
      }
      </script>
    ```

3. `src/components/TodoList.vue`

    TodoList component lists all todos.

    ```javascript
    <template>
      <div>
        <BaseTextInput
          @newTodo="addTodo"
        />
        <ul v-if="todos.length">
          <TodoListItem
            v-for="todo in todos"
            :key="todo.id"
            :todo="todo"
            @remove="removeTodo"
          />
        </ul>
        <p class="empty-state-message" v-else>
          Nothing left in the list. Add a new todo in the input above.
        </p>
      </div>
    </template>

    <script>
    import BaseTextInput from './BaseTextInput.vue'
    import TodoListItem from './TodoListItem.vue'

    let nextTodoId = 1

    export default {
      components: {
        BaseTextInput, TodoListItem
      },
      data () {
        return {
          todos: []
        }
      },
      methods: {
        addTodo (todo) {

          const trimmedText = todo.trim()
          if (trimmedText) {
            this.todos.unshift({
              id: nextTodoId++,
              text: trimmedText
            })

          }
        },
        removeTodo (idToRemove) {
          this.todos = this.todos.filter(todo => {
            return todo.id !== idToRemove
          })
        }
      }
    }
    </script>
    ```

4. Edit `src/App.vue` to include code that will render the Todo App.

    ```javascript
    <template>
      <div id="app">
        <h1>My Todo App!</h1>
        <TodoList/>
      </div>
    </template>

    <script>
    import TodoList from './components/TodoList.vue'

    export default {
      components: {
        TodoList
      }
    }
    </script>

    <style>

    *, *::before, *::after {
      box-sizing: border-box;
    }

    #app {
      max-width: 400px;
      margin: 0 auto;
      line-height: 1.4;
      font-family: 'Avenir', Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      color: #00C185;
    }

    h1 {
      text-align: center;
    }
    </style>
    ```

Then, run:

```plain
npm run serve
```

and visit [http://localhost:8080](http://localhost:8080) to view your Todo App!

![Screenshot of the Todo App opened in browser. The browser is viewing localhost:8080, and on the page, the header reads "My Todo App!" wth a box underneath labeled "Add a new todo", along with an "Add" button to the right. Below is green text reading "Nothing left in the list. Add a new todo in the input above".](/blog/2022/12/how-to-use-cypress-for-ui-testing/todo-app.webp)

### How to write end-to-end tests

End-to-end (E2E) testing is used to test an application flow from start to finish. Tests are designed to use the application the same way that a user would.

In our example we are going to test the whole Todo app with the following test cases:

* The user should see a message when Todo list is empty.
* The user should be able to view a list of Todos.
* The user should be able to add a new Todo.
* The user should be able to remove an existing Todo.

Cypress is built on top of [Mocha](https://docs.cypress.io/guides/references/bundled-libraries#Mocha) and [Chai](https://docs.cypress.io/guides/references/bundled-libraries#Chai). If you're familiar with writing tests in JavaScript, then writing tests in Cypress will be a breeze.

Visit the official [Cypress docs](https://docs.cypress.io/guides/end-to-end-testing/writing-your-first-end-to-end-test#Write-your-first-test) to learn more about how to start testing a new project in Cypress.

Without futher ado lets start testing our Todo app.

Inside the `cypress` folder that was added during installation create a file, `cypress/e2e/todo.cy.js`, and add the following tests.

> Please visit the [folder structure docs](https://docs.Cypress.io/guides/core-concepts/writing-and-organizing-tests#Folder-structure) to learn more about how to organise tests in Cypress and understand the generated Cypress folder structure.

```javascript
/* eslint-disable no-undef */

// describe() function is used to group tests
describe('Todo tests', () => {
  it('should display empty state message', () => {
    // cy.visit() used to visit a remote url
    // learn more about it here: https://docs.cypress.io/api/commands/visit#Syntax
    cy.visit('http://localhost:8080');

    // cy.get() command Gets one or more DOM elements by selector or alias
    // learn more about Cypress commands/api here: https://docs.cypress.io/api/table-of-contents
    cy.get('.empty-state-message')
    .contains('Nothing left in the list. Add a new todo in the input above.')
    .should('be.visible');
  });

  it('should add todo', () => {
    cy.visit('http://localhost:8080');

    // add todo by typing in the input and pressing enter
    cy.get('input[type="text"]').type('new todo{enter}');

    // check if the todo is added
    cy.get('ul').contains('new todo').should('be.visible');
    cy.get('ul').find('li').should('have.length', 1);


    // add another todo by typing in the input and pressing 'add' button
    cy.get('input[type="text"]').type('more todo');
    cy.get('input[type=submit]').click();

    // check if the todo is added
    cy.get('ul').contains('more todo').should('be.visible');
    cy.get('ul').find('li').should('have.length', 2);
  });

  it('should delete todo', () => {
    cy.visit('http://localhost:8080');

    // delete the first todo
    cy.get(':nth-child(1) > button').click();

    // check if the todo is deleted
    // cy.should() command is used to assert that the todo list has only one todo
    // learn more about Cypress assertions here: https://docs.cypress.io/guides/references/assertions
    cy.get('ul').find('li').should('have.length', 1);
  });
});
```

To make sure Vue is available at `http://localhost:8080`, run:

```plain
npm run serve
```

Then, to launch Cypress, run:

```plain
npm run cypress:open
```

On the Cypress launcher select "End2End Tests" and click on the `todo.cy.js` spec to run your tests.

![Screenshot displaying Todo App End2End tests that have run successfully. A test browser in the sidebar is open to todo.cy.js, with a successful test to the right. There are green check marks next to "should display empty state message", "should add todo", and "should delete todo". After the first is the test body in a code block reading "visit http://localhost:8080; get .empty-state-message; -contains Nothing left in the list. Add a new todo in the input above.; -assert expected <p.empty-state-message> to be visible".](/blog/2022/12/how-to-use-cypress-for-ui-testing/todo-app-end-to-end-tests.webp)

### How to write component tests

Cypress Component Test Runner executes your component tests in the browser as a user would by simulating real interactions. Since it runs in the browser, you get to debug your components using your favourite developer tools.

To demonstrate how to write component tests using Cypress we are going to write tests for the following components:

* `BaseTextInput.vue`
* `TodoListItem.vue`

#### Component tests for `BaseTextInput.vue`

Here we are going to assert the following;

1. Text input is rendered with `placeholder` text "Add a new todo".
2. When the "add" button is clicked a `newTodo` event is emitted with a payload containing text that was typed in the text input.

First create a spec, `src/components/BaseTextInput.cy.js`, then add the following code:

```javascript
/* eslint-disable no-undef */
import BaseTextInput from './BaseTextInput.vue'

describe('<BaseTextInput />', () => {
  it('renders base text input component', () => {
    // Renders the component in DOM.
    // cy.mount() is a custom command.
    // Learn more about cypress custom commands here:
    // https://docs.cypress.io/api/commands/mount#Creating-a-New-cy-mount-Command
    cy.mount(BaseTextInput);

    // Asserts that the text input is rendered with the correct placeholder
    cy.get('input').should('have.attr', 'placeholder', 'Add a new todo');

    // asserts that when the 'add' button is clicked, an event is emitted
    // with the payload containing the value of the text input
    cy.get('input[type="text"]').type('new todo');
    cy.get('input[type=submit]').click().then(() => {
      // Cypress.vueWrapper provides access to the Vue Test Utils.
      // With this wrapper you can access any Vue Test Utils API.
      // Learn more about Vue Test Utils here: https://vue-test-utils.vuejs.org/
      // e.g. cy.vueWrapper().emitted() returns all the events emitted by the BaseTextInput component
      cy.wrap(Cypress.vueWrapper.emitted()).should('have.property', 'newTodo');
      expect(Cypress.vueWrapper.emitted().newTodo[0]).to.deep.equal(['new todo']);
    });
  })
});
```

To run the test, launch Cypress using `cypress:open`. This time select "component testing", then click on `BaseTextInput.cy.js` to run tests.

![Screenshot displaying BaseTextInput component tests that have run successfully. Cypress is open to src/components/BaseTextInput.cy.js. In the test output sidebar, there is one green check mark, next to "renders base text input component". It is followed by the test body in a code block, which reads: "-mount <BaseTextInput ... />; get input; -assert expected \[ <input.input>, 1 more...\] to have attribute placeholder with the value Add a new todo; get input\[type="text"\]; -click; assert expected \[ new todo \] to deeply equal \[ new todo \]; wrap Object{25}; -assert expected { Object (DOMSubtreeModified, pointerover, ...) } to have property newTodo".](/blog/2022/12/how-to-use-cypress-for-ui-testing/base-text-input-tests.webp)

#### Component tests for `TodoListItem.vue`

Here we are going to assert the following:

1. A Todo list item is rendered with correct text.
2. When the "remove" button is clicked, a "remove" event is emitted with payload containing the ID of the Todo to be removed.

First create a spec, `src/components/TodoListItem.cy.js`, and add the following code:

```javascript
/* eslint-disable no-undef */
import TodoListItem from './TodoListItem.vue'

describe('<TodoListItem />', () => {
  it('renders todo list item', () => {
    const text = 'new todo';
    const id = 1;
    // mount the component with props
    // see: https://test-utils.vuejs.org/guide/
    cy.mount(TodoListItem, {props: {todo: { id, text }}});

    // asserts that the todo list item is rendered with the correct text
    cy.get('li').contains(text);

    // asserts that when 'x' button is clicked, 'remove' event is emitted with the correct payload
    cy.get('button').click().then(() => {
      cy.wrap(Cypress.vueWrapper.emitted()).should('have.property', 'remove');
      expect(Cypress.vueWrapper.emitted().remove[0]).to.deep.equal([id]);
    })
  })
});
```

To run the test, launch Cypress using `cypress:open`. Select "component testing" again, then click on `TodoListItem.cy.js` to run tests.

![Screenshot displaying TodoListItem component tests that have run successfully. The same cypress window is navigated to src/components/TodoListItem.cy.js. There is a green check mark next to "renders todo list item. The test body cody block reads "-mount <TodoListItem ... />; get li; -contains new todo; get button; -click; assert expected \[ 1 \] to deeply equal \[ 1 \]; wrap Object{16}; -assert expected { Object (DOMSubtreeModified, pointerover, ...) } to have property remove".](/blog/2022/12/how-to-use-cypress-for-ui-testing/todo-list-item-test.webp)

The final source code with all the tests can be found [here](https://github.com/Mloweedgar/todo-app).

### Next steps

This article is meant to provide you with knowledge on how to setup and run tests using Cypress. However, you may need to further learn Cypress and its API to write better and efficient tests. Below are links to resources for further learning about testing with Cypress.

* **Cypress core concepts:** https://docs.cypress.io/guides/core-concepts/introduction-to-cypress
* **Network Requests:** https://docs.cypress.io/guides/guides/network-requests
* **Cypress Best Practices:** https://docs.cypress.io/guides/references/best-practices
