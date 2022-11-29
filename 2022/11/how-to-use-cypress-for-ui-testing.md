---
author: Edgar Mlowe
title: 'How to write End to End and Component Tests with Cypress in Vue'
tags:
- Cypress
- Vue
- JavaScript
- Vue Test Utils
date: 2022-11-18
featured:
  endpoint: true
  image_url: /blog/2022/11/how-to-use-cypress-for-ui-testing/beach-zanzibar.webp
description: This article walks readers through how to setup Cypress and use it to write End to End and Component Tests in Vue.
---

![Beach in Zanzibar, Tanzania during a hot sunny day](/blog/2022/11/how-to-use-cypress-for-ui-testing/beach-zanzibar.webp)

<!-- Photo by Edgar Mlowe, 2018 -->


### How to write End to End and Component Tests with [Cypress](https://www.cypress.io) in Vue

#### Introduction
Is writing tests painful for you? In this tutorial, I am going to explain how to handle UI testing with [Cypress](https://www.cypress.io) and convince you that writing tests is not always so tedious and expensive but fun instead.

[Cypress](https://www.cypress.io) is a purely **JavaScript-based front-end testing tool built for the modern web**. it can test anything that runs in browser and has built in support for testing modern frameworks such as Vue, React and Angular. see a full-list of all supported front-end frameworks [here](https://docs.cypress.io/guides/component-testing/overview#Supported-Frameworks).

We are going to use a Todo app built using Vue as an example, through that we are going to learn;

* How to Install and Setup Cypress.
* Creating a simple Todo App with Vue 3
* How to write End to End tests.
* How to write component tests.



####  How to Install and Setup Cypress
1. First thing first lets create new Vue project using Vue CLI.
Install Vue CLI if you don't have it in your machine:

```bash

npm install -g @vue/cli

```

2. create a project(pick `Vue 3,babel,eslint` preset ):

```bash

vue create todo-app

```
3. `cd` into the **todo-app** project and Install cypress with only one command:
_No dependencies, extra downloads, or changes to your code required!_

```bash
 npm install cypress --save-dev

```

3. Edit package.json file in scripts section add a command `"cypress:open": "cypress open"`. see example below.

```json

"scripts": {
    "cypress:open": "cypress open"
  },

```
4. Launch cypress:

```bash

 npm run cypress:open

```
When Cypress opens up you should be able to view the cypress launch pad as shown in the image below.

![Screenshot of Cypress launcher window displaying testing options ](/blog/2022/11/how-to-use-cypress-for-ui-testing/cypress-launcher.png)


Use the Launch pad to configure both E2E Testing and Component Testing, note that cypress will automatically generate configuration files as you configure the tests in the Launch pad. if you get stuck please visit this [link here](https://docs.cypress.io/guides/getting-started/opening-the-app#The-Launchpad) to cypress official docs on how to configure cypress. 




#### Create a Todo App with Vue 3
Open **todo-app** project in your favourite Editor and add the following single file components:
1. Add BaseTextInput Component `src/components/BaseTextInput.vue` 

```javaScript

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
 BaseTextInput will contain a text input and a button for adding new todos.

2. Add TodoListItem Component `src/components/TodoListItem.vue`

```javaScript

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
TodoListItem displays a todo along with a button for removing that Todo


3. Add TodoList component `src/components/TodoList.vue`

```javaScript

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

TodoList component lists all todos.

4. Edit App component `src/App.vue` to include code that will render the Todo App.

```javaScript

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

Lastly run:
```bash

npm run serve

```
and visit [http://localhost:8080](http://localhost:8080) to view your todo App!

![Screenshot of the Todo App opened in browser](/blog/2022/11/how-to-use-cypress-for-ui-testing/todo-app.png)



#### End to End testing
End to end testing is used to test an application flow from start to finish. Tests are designed to use the application the same way that a user would.
In our example we are going to test the whole todo app with the following test cases:

1. User should see message when todo list is empty
2. User should be able to view list of todos
3. User should be able to add a new todo
4. User should be able to remove an existing todo


Cypress is built on top of [Mocha](https://docs.cypress.io/guides/references/bundled-libraries#Mocha) and [Chai](https://docs.cypress.io/guides/references/bundled-libraries#Chai). If you're familiar with writing tests in JavaScript, then writing tests in Cypress will be a breeze.
Visit official cypress docs [here](https://docs.cypress.io/guides/end-to-end-testing/writing-your-first-end-to-end-test#Write-your-first-test) to learn more about How to start testing a new project in Cypress.


Without futher ado lets start testing our todo app.
Inside cypress folder that was added during cypress installation create a file `cypress/e2e/todo.cy.js` add the following tests. _Please visit this [link here](https://docs.cypress.io/guides/core-concepts/writing-and-organizing-tests#Folder-structure) to learn more about how to organise tests in cypress and understand the generated cypress folder structure_ 


```javaScript

 /* eslint-disable no-undef */

// describe() function is used to group tests
describe('Todo tests', () => {
  it('should display empty state message', () => {
    // cy.visit() used to visit a remote url
    // learn more about it here: https://docs.cypress.io/api/commands/visit#Syntax
    cy.visit('http://localhost:8080');

    // cy.get() command Gets one or more DOM elements by selector or alias
    // learn more about cypress commands/api here: https://docs.cypress.io/api/table-of-contents
    cy.get('.empty-state-message')
    .contains('Nothing left in the list. Add a new todo in the input above.')
    .should('be.visible'); 
  });

  it('should add todo', () => {

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
    // delete the first todo
    cy.get(':nth-child(1) > button').click();

    // check if the todo is deleted
    // cy.should() command is used to assert that the todo list has only one todo
    // learn more about cypress assertions here: https://docs.cypress.io/guides/references/assertions
    cy.get('ul').find('li').should('have.length', 1);
  });
});

```

Now run:

```bash
# to make sure vue is available on http://localhost:8080
npm run serve

```

Then run:
```bash
# this will lounch cypress
npm run cypress:open

```
On the cypress launcher select "End2End Tests" click on `todo.cy.js` spec to run your tests.
![Screenshot displaying Todo App End2End that have run successfuly](/blog/2022/11/how-to-use-cypress-for-ui-testing/todo-app-end-to-end-tests.png)



#### Component Testing
Cypress Component Test Runner executes your component tests in the browser as a user would by simulating real interactions. Since it runs in the browser, you get to debug your components using your favourite developer tools.



To demonstrate how to write component tests using cypress we are going to write tests for the following components:

1. `BaseTextInput.vue`

2. `TodoListItem.vue`


 Component tests for `BaseTextInput.vue`:

Here we are going to assert the following;

1. Text input is rendered with `placeholder` text "Add a new todo"
2. When 'add' button is clicked 'newTodo' event is emitted with payload containing text that was typed in the text input

First create a spec `src/components/BaseTextInput.cy.js` and add the following code:

```javaScript

/* eslint-disable no-undef */
import BaseTextInput from './BaseTextInput.vue'

describe('<BaseTextInput />', () => {
  it('renders base text input component', () => {
    // renders the component in DOM
    // cy.mount() is a custom command learn more about 
    // cypress custom commands here https://docs.cypress.io/api/commands/mount#Creating-a-New-cy-mount-Command
    cy.mount(BaseTextInput);

    // asserts that the text input is rendered with the correct placeholder
    cy.get('input').should('have.attr', 'placeholder', 'Add a new todo');

    // asserts that when 'add' button is clicked, an event is emitted
    // with the  payload containing the value of the text input
    cy.get('input[type="text"]').type('new todo');
    cy.get('input[type=submit]').click().then(() => {
      // Cypress.vueWrapper provides access to the Vue Test Utils
      // with this wrapper you can access any Vue Test Utils API
      // learn more about Vue Test Utils here https://vue-test-utils.vuejs.org/
      // e.g cy.vueWrapper().emitted() returns all the events emitted by the BaseTextInput component
      cy.wrap(Cypress.vueWrapper.emitted()).should('have.property', 'newTodo');
      expect(Cypress.vueWrapper.emitted().newTodo[0]).to.deep.equal(['new todo']);
    });
  })
});

```

To run the test, launch cypress using `cypress:open`. this time select "component testing", then click on `BaseTextInput.cy.js`  to run tests.

![Screenshot displaying BaseTextInput component tests that have run successfuly](/blog/2022/11/how-to-use-cypress-for-ui-testing/base-text-input-tests.png)



Component tests for `TodoListItem.vue`:

Here we are going to assert the following

1. Todo list item is rendered with correct text
2. on-click button remove todo button, 'remove' event is emitted with payload containing the id of the todo to be removed

First create a spec `src/components/TodoListItem.cy.js` and add the following code:

```javaScript

/* eslint-disable no-undef */
import TodoListItem from './TodoListItem.vue'

describe('<TodoListItem />', () => {
  it('renders todo list item', () => {
    const text = 'new todo';
    const id = 1;
    // mount the component with props
    //see: https://test-utils.vuejs.org/guide/
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

To run the test, launch cypress using `cypress:open`. again select "component testing", then click on `TodoListItem.cy.js`  to run tests.
![Screenshot displaying TodoListItem component tests that have run successfuly](/blog/2022/11/how-to-use-cypress-for-ui-testing/todo-list-item-tests.png)



The final source code with all the tests can be found [here](https://github.com/Mloweedgar/todo-app).

#### Next Steps

This article is meant to provide you with knowledge on how to setup and run tests using cypress, however you may need to further learn cypress and its API to write better and efficient tests. below are links to resources further learning testing with cypress.

1. **Cypress core concepts:** https://docs.cypress.io/guides/core-concepts/introduction-to-cypress

2. **Network Requests:** https://docs.cypress.io/guides/guides/network-requests#What-you-ll-learn

3. **Cypress Best Practices:** https://docs.cypress.io/guides/references/best-practices
