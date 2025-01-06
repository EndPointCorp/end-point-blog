---
author: "Bimal Gharti Magar"
title: "Learning Vue 3 composables by creating invoice generator"
featured:
  image_url:
description: 
date: 2025-01-06
tags:
- vue
---


### Introduction
 Vue 3, which is the latest major version of Vue, has new features that are not present in Vue 2, such as Teleport, Suspense and multiple root elements per template. Vue 3 provides smaller bundle sizes, better performance, better scalability and better TS/IDE support.


### What is Vue 3 composables?
Writing repetitive code can be a real pain in the frontend development realm. We can use Vue 3 [composables](https://vuejs.org/guide/reusability/composables) to encapsulate and reuse stateful logic in our components. In this post, we will look at how we can use composables to reuse business logic by building an invoice generator.

An invoice generator, simply said, is an application that creates and manages invoices. In this blog post, we will focus on creating Vue 3 composables to properly separte business logic while reusing it across different features.

### Core functionalites for Invoice Generator
- Adding, editing, and removing invoices and items
- Calculating totals with discounts, taxes, and shipping.
- Generating PDF invoices

We'll focus on:
- Creating composables to handle business logic.
- Reusing this logic across features and components.

### Prerequisites
- Basic understanding of:
    - Vue 3 and Composition API
    - JS/TS fundamentals

- Tools:
    - Node.js and npm installed
    - Vite
    - Optional: Tailwindcss

### Setting up the project
- Initialize Vue 3 project
```
$ npm create vite@latest ep-invoice-generator
Need to install the following packages:
create-vite@6.0.1
Ok to proceed? (y) y
√ Select a framework: » Vue
√ Select a variant: » TypeScript

Scaffolding project in G:\PersonalWork\blog\ep-invoice-generator...

Done. Now run:

  cd ep-invoice-generator
  npm install
  npm run dev
```

- Project Sturcture:
    
    - `src/components/` - For adding UI compnents

    - `src/composables/` - For adding composables

    - `src/router/` - For adding vue-router routes

    - `src/types/` - For adding type definitions
    
    - `src/views/` - For adding pages to render based on vue-router routes

### Create first composable for Invoice `useInvoice`
The composable is named `useInvoice.ts` and it will serve the following purposes:

- Handle invoice and invoice items data
- Add methods for adding, editing and removing invoice items
- Calculate totals automatically using item's rate and amount as well as discount, tax and shipping
- Reset invoice

#### Define interface for Invoice and Invoice Items
```typescript
export interface InvoiceItem {
    id: number,
    description: string,
    rate: number,
    quantity: number,
}

export interface Invoice {
    logo: string,
    name: string,
    number: number,
    ponumber: string,
    date: string,
    duedate: string,
    sender: string,
    buyer: string,
    items: InvoiceItem[];
    notes: string,
    terms: string,
    discount: {
        isUsed: boolean,
        isPercentage: boolean,
        value: number,
    },
    tax: {
        isUsed: boolean,
        isPercentage: boolean,
        value: number,
    },
    shipping: {
        isUsed: boolean,
        value: number,
    },
    total: number,
    paid: number,

    sentToContact: boolean,
    status: Status,
}
```


First we make an invoice object to create and edit an invoice. The code `state.storage.value.currentInvoiceNumber` gets the current invoice number to use for the new invoice, we will learn more about it later. 

We return the object containing the required data and methods that can be used by any SFC component. We will see the implementation of computed properties and methods in the next section.


```typescript
export function useInvoice(invoiceId?: number) {

    const invoice = reactive<Invoice>({
        logo: "",
        name: "",
        number: state.storage.value.currentInvoiceNumber,
        ponumber: "",
        date: format(date, "yyyy-MM-dd"),
        duedate: "",
        sender: "",
        buyer: "",
        items: [
            {
                id: 1,
                description: "",
                rate: 0,
                quantity: 0,
            },
        ],
        notes: "",
        terms: "",
        discount: {
            isUsed: false,
            isPercentage: false,
            value: 0,
        },
        tax: {
            isUsed: false,
            isPercentage: false,
            value: 0,
        },
        shipping: {
            isUsed: false,
            value: 0,
        },
        total: 0,
        paid: 0,
        sentToContact: false,
        status: Status.Draft,
    });

    const subtotal = computed(() => ...)
    const afterDiscount = computed(() => ...)
    const afterTax = computed(() => ...)
    const afterShipping = computed(() => ...)
    const total = computed(() => ...)
    const balance = computed(() => ...);
    
    const updateLineItem = (value: InvoiceItem, index: number) => ...);
    const addLineItem = () => ...)
    const removeLineItem = (index) => ...)

    return {
        // data helpers
        invoice,
        subtotal,
        afterDiscount,
        afterTax,
        afterShipping,
        total,
        balance,

        // Methods
        addLineItem,
        updateLineItem,
        removeLineItem,
    }
}

```

### Adding Business Logic
Now we implement the business logic for various methods, like adding an invoice item, updating an invoice item, etc. as well as calculating the various dynamic amounts.
The following methods add an invoice item as a line item to the invoice, which can be rendered on the UI as a line item. Then, the user can update the line item's rate and quantity, which calls `updateLinetItem` to update the invoice item data.
```typescript
    /**
     * Add a line item to the invoice line items array
     */
    const addLineItem = () => {
        invoice.items.push({
            id: invoice.items.length + 1,
            description: "",
            rate: 0,
            quantity: 0,
        });
    };

    /**
     * @param {invoice line item} value 
     * @param {index of invoice line item} index 
     * @returns 
     */
    const updateLineItem = (value: InvoiceItem, index: number) => (invoice.items[index] = { ...value });

    /**
     * Remove items from invoice items array
     * @param {*} index index of item to remove
     */
    const removeLineItem = (index) => {
        invoice.items.splice(index, 1);
    };

```

Based on the invoice item data, we then calculate
- subtotal
- subtotal after discount if available
- subtotal after tax if available
- subtotal after shipping if available

Moreover, discount and tax can be put as an amount or percentage value, so we update the logic to evaluate discount and tax based on the entered values and type; and calculate the subtotal. We can also include a previously overpaid amount and calculate the balance at the end of the calculations.

```typescript
// useInvoice.ts
    const subtotal = computed(() =>
        invoice.items.reduce((prev, acc) => prev + acc.rate * acc.quantity, 0)
    );

    /**
     * Compute total value after applying discount
     * based on `discount` percentage or value and `subtotal` value
     */
    const afterDiscount = computed(() => {
        if (invoice.discount.isUsed) {
            if (invoice.discount.isPercentage) {
                return subtotal.value - (subtotal.value * invoice.discount.value) / 100;
            } else {
                return subtotal.value - invoice.discount.value;
            }
        }
        return subtotal.value;
    });

    /**
     * Compute total value after applying tax
     * based on `tax` percentage or value and `afterDiscount` value
     */
    const afterTax = computed(() => {
        if (invoice.tax.isUsed) {
            if (invoice.tax.isPercentage) {
                return (
                    afterDiscount.value + (afterDiscount.value * invoice.tax.value) / 100
                );
            } else {
                return afterDiscount.value + invoice.tax.value;
            }
        }
        return afterDiscount.value;
    });

    /**
     * Compute total value after applying shipping
     * based on `shipping` value and `afterTax` value
     */
    const afterShipping = computed(() => {
        if (invoice.shipping.isUsed) {
            return afterTax.value + invoice.shipping.value;
        }
        return afterTax.value;
    });

    const total = computed(() => {
        return afterShipping.value;
    });

    // later if we track the payment done for the clients, we can easily
    // come up with the balance based on the payment and invoices
    const balance = computed(() => total.value - invoice.paid);
```

### Rendering the Invoice with Composable Functions

We create the `InvoiceGenerator.vue` SFC component to use the `useInvoice` composable we created. We use `<script setup>` for importing and using the composable.  `<script setup>` helps in using the [Composition API](https://vuejs.org/guide/extras/composition-api-faq.html) inside SFCs instead of the Options API. Using `<script setup>` syntax helps in removing boilerplate code while providing the ability to declare props, emitted events and [many more advantages](https://vuejs.org/api/sfc-script-setup#script-setup). 

```html
<!-- InvoiceGenerator.vue-->
<script setup>
import { useInvoice } from "../composables/useInvoice";

const {
  // data
  invoice,

  // computed / read only
  subtotal,
  total,
  balance,

  // methods
  addLineItem,
  updateLineItem,
  removeLineItem,
  resetInvoice
} = useInvoice(
</script>
```

I have already defined the `LineItems.vue` component where we render the line items which have textboxes to enter description, rate and amount. The totals for each item are calculated using the computed property. Let's see an example showing how we can use it with invoice items. 
- `LineItems` uses `items` props to render the invoice items.
- Emits `update-item` event when any value for an invoice line item changes.
- Emits `add-item` when user adds a new line item.
- Emits `close` when user removes a line item.

```html
<LineItems
    :items="invoice.items"
    @update-item="updateLineItem"
    @close="removeLineItem"
    @add-item="addLineItem"
    />
```

Similarly, we use `invoice.discount`, `invoice.tax` and `invoice.shipping` properties from composable in a textbox where the user can enter the value and type of the value. All of them have helper properties named `isUsed` and `isPercentage`, which we use to make the input box user-friendly. The `CustomInput`, `CustomToggleSwitch` and `WithLabel` are three custom components that are already created and they can be used as follows:

```html
<WithLabel label="Discount">
    <CustomInput
        v-model.number="invoice.discount.value"
        is-used
        label="Discount"
        toggle
        :currency="!invoice.discount.isPercentage"
        @close="invoice.discount.isUsed = false"
    >
        <CustomToggleSwitch
        v-model="invoice.discount.isPercentage"
        :for-value="'invoice-discount'"
        />
    </CustomInput>
</WithLabel>

<WithLabel label="Tax">
    <CustomInput
        v-model.number="invoice.tax.value"
        is-used
        label="Tax"
        toggle
        :currency="!invoice.tax.isPercentage"
        @close="invoice.tax.isUsed = false"
    >
        <CustomToggleSwitch
        v-model="invoice.tax.isPercentage"
        :for-value="'invoice-tax'"
        />
    </CustomInput>
</WithLabel>

<WithLabel label="Shipping">
    <CustomInput
        v-model.number="invoice.shipping.value"
        label="Shipping"
        is-used
        currency
        @close="invoice.shipping.isUsed = false"
    >
    </CustomInput>
</WithLabel>
```

All other properties can also be rendered however, we would like some input fields, like PO Number, Invoice Date and Amount Paid to be rendered differently, as you can see below. Using custom components like `CustomInput` and `CustomToggleSwitch` can help us get more control on the visual and functional aspects of the UI component.
```html
<WithLabel label="PO Number">
    <CustomInput
    v-model="invoice.ponumber"
    label="PO Number"
    type="text"
    />
</WithLabel>

<WithLabel label="Date">
    <CustomInput
    v-model="invoice.date"
    label="Date"
    type="date"
    />
</WithLabel>

<WithLabel label="Amount Paid">
    <CustomInput
    v-model.number="invoice.paid"
    label="Amount Paid"
    currency
    />
</WithLabel>
```

### Create a second composable for using localstorage to save and retrieve invoice data

`useInvoice` composable only gives us the invoice data along with computed properties, but now we have to save it somewhere so we can use it later. We can use `localStorage` to save the invoices. [VueUse](https://vueuse.org/) is a very good library that has a [collection](https://vueuse.org/functions.html) of vue composition utilities that can be used with Vue2 as well as Vue3. 

For accessing localStorage reactively, we will use a composable called `useStorage` from [VueUse](https://vueuse.org/). `useStorage` uses `localStorage` by default. We will define `saveInvoice`, `updateInvoice`, `deleteInvoice` and `findInvoices` methods that use the reactive variable from `useStorage` to perform the required operations.

We will create another composable called `useInvoiceStorage.ts`, where we initialize our storage using `useStorage`, which also stores the current invoice number.

```typescript
// useInvoiceStorage.ts

const storage = useStorage<InvoiceStore>('invoice-store', {
    currentInvoiceNumber: 10000,
    invoices: {}
}, localStorage);

```

Then we define and implement the earlier discussed methods for saving, updating, deleting and finding invoices. The update of the current invoice number happens in the `saveInvoice` method.
```typescript
// useInvoiceStorage.ts

export default function useState() {
    const state = reactive(storage);

    function saveInvoice(invoice: Invoice) {
        state.value.invoices[invoice.number] = { ...invoice };
        state.value.currentInvoiceNumber = invoice.number + 1;
    }

    function updateInvoice(invoice: Invoice) {
        state.value.invoices[invoice.number] = { ...invoice };
    }

    function deleteInvoice(invoiceId: number) {
        state.value.invoices = Object.keys(state.value.invoices)
            .filter(x => x != invoiceId.toString())
            .reduce((acc, curr) => {
                return {
                    ...acc,
                    [curr]: state.value.invoices[curr]
                }
            }, {})
    }
    
    function findInvoices(searchText: string) {
        searchText = searchText.toLowerCase();
        return Object.keys(state.value.invoices).filter(x => {
            const invoice = state.value.invoices[x];
            return invoice.number.toString().indexOf(searchText) > -1
                || invoice.buyer.toString().toLowerCase().indexOf(searchText) > - 1
                || invoice.date.toString().toLowerCase().indexOf(searchText) > - 1
                || invoice.total.toString().indexOf(searchText) > - 1
        })
            .map(x => ({ ...state.value.invoices[x] }))

    }
    return {
        // variables
        storage: state,

        // methods
        saveInvoice,
        updateInvoice,
        deleteInvoice,
        findInvoices
    }
}

```

Now, we can use data and methods from the `useInvoiceStorage` composable to show the latest invoice number as well as save, update, delete and find invoices. The composable `useInvoice` also uses `useInvoiceStorage` to set the current invoice number for the new invoice. Whenever a user creates a new invoice, the current invoice number is automatically assigned to the invoice obtained from the  `useInvoiceStorage` composable. 

Moreover, the `useInvoice` composable is updated to support the new invoice as well as edit invoice feature. The support of editing an invoice is achieved by passing `invoiceId` to the `useInvoice` composable, the `invoiceId` is then checked in the storage returned by `useInvoiceStorage`, if the invoice exists, the `useInvoice` composable returns the correct invoice data from storage.

The following code checks for the invoice in the storage.
```typescript
// If the invoice is already in the storage, use it
if(invoiceId){
    const invoiceToUse = state.storage.value.invoices[invoiceId];
    if(invoiceToUse) Object.assign(invoice, invoiceToUse);
}
```


### Printing Invoice
For printing invoices, we can simply use [print styles](https://tailwindcss.com/docs/hover-focus-and-other-states#print-styles) from tailwindcss to style the elements that we want to print for the invoice. A simple example is the `CustomButton` component in the source code. We don't want to show any buttons on the PDF so, we use tailwindcss style `print:hidden` to hide the buttons on the print view. We then need to call the below method on the invoice page to print the current page.

```typescript
const print = () => window.print();
```

### Bonus: Create a third composable for showing dashboard data
The dashboard is important to look at the high-level data and is crucial to any application. So, we add a new composable called `useDashboardData.ts` that will give us the total invoice amount, total paid amount, total due amount and total drafted amount but it can be further expanded to include any other business logic as well. We will again use the `useInvoiceStorage` composable to get the list of invoices and 

```typescript
// useDashboardData.ts
import useState from "./useInvoiceStorage";
import { Status } from "../types/index.type";

export function useDashboardData() {
    const state = useState();

    const totalInvoiceAmount = computed(() => {
        const invoices = state.storage.value.invoices;
        const amount = Object.keys(invoices).reduce((acc, item) => acc + invoices[item].total, 0);
        return amount.toFixed(2)
    })

    const totalPaid = computed(() => {
        const invoices = state.storage.value.invoices;
        const amount = Object.keys(invoices).reduce((acc, item) => {
            if (invoices[item].status === Status.Paid) {
                return acc + invoices[item].total
            }
            return acc;
        }, 0);
        return amount.toFixed(2);
    })

    const totalDue = computed(() => {
        const invoices = state.storage.value.invoices;
        const amount = Object.keys(invoices).reduce((acc, item) => {
            if (invoices[item].status === Status.Overdue) {
                return acc + invoices[item].total
            }
            return acc;
        }, 0);
        return amount.toFixed(2);
    })

    const totalDrafted = computed(() => {
        const invoices = state.storage.value.invoices;
        const amount = Object.keys(invoices).reduce((acc, item) => {
            if (invoices[item].status === Status.Draft) {
                return acc + invoices[item].total
            }
            return acc;
        }, 0);
        return amount.toFixed(2);
    })

    return {
        // variables
        totalInvoiceAmount,
        totalPaid,
        totalDue,
        totalDrafted
    }
}
```

After that we create the `Dashboard.vue` component to use data from `useDashboardData.ts` and display the data on the dashboard. We can keep adding business logic on `useDashboardData.ts` to display it on the dashboard or use it somewhere else to support some other business logic.

```html
<!-- Dashboard.vue -->
<template>
    <section class="max-w-[1800px] mx-auto">
        <div class="grid grid-cols-4 gap-x-4 mt-4">
            <Card>
                <template #header>Total Amount</template>
                <span>${{ totalInvoiceAmount }}</span>
                <template #footer></template>
            </Card>
            <Card>
                <template #header>Paid Amount</template>
                <span>${{ totalPaid }}</span>
                <template #footer></template>
            </Card>
            <Card>
                <template #header>Due Amount</template>
                <span>${{ totalDue }}</span>
                <template #footer></template>
            </Card>
            <Card>
                <template #header>Drafted Amount</template>
                <span>${{ totalDrafted }}</span>
                <template #footer></template>
            </Card>
        </div>
        <Invoices />
    </section>
</template>

<script setup lang="ts">
import Card from '../components/shared/Card.vue';
import { useDashboardData } from '../composables/useDashboardData';
import Invoices from './Invoices.vue';

const { totalInvoiceAmount, totalPaid, totalDue, totalDrafted } = useDashboardData();
</script>
```

The source code is available at [Github](https://github.com/bimalghartimagar/invoice-generator)

Application [demo](https://invoice-generator-iota.vercel.app/) is also available.

### Next Steps
- Use a REST API for saving the invoices to the database.
- Use Pinia to store the retrieved invoices so we can easily use the invoices.
- Add a composable to switch between different types of templates for printing PDFs.

### Conclusion:
We learned about Vue 3 composables and how to use the composition API to create composables. We saw how composable functions are a game changer that helps in building the complex, maintainable and scalable application by encapsulating the business logic, organizing the code and making it reusable. It helps to simplify the process and boost productivity.
