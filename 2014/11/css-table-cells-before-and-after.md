---
author: Kent Krenrich
title: CSS table-cells ::before and ::after
github_issue_number: 1049
tags:
- css
- html
date: 2014-11-05
---

When laying out HTML forms, instead of using a table (re: tables-are-only-for-tabular-data et al), I’ve had good results making use of the table family of values for the CSS display property. I find it a reliable way to ensure items line up in a wide range of situations, a change in the size of labels or a resize of the browser’s window for example.

Something simple like the following has worked well for me on several occasions:

```css
.table {
  display: table;
}
.table>* {
  display: table-row;
}
.table>*>* {
  display: table-cell;
}
```

Occasionally though, I’ve wanted to leave a column empty for one reason or another. To accomplish this I found myself including empty HTML tags like:

```html
<form class="table">
  <div>
    <div>A Cell</div>
    <div>A Cell</div>
  </div>
  <div>
    <div></div>
    <div>A Cell</div>
  </div>
</form>
```

The empty elements function well enough but they feel a little out of place. Recently I came up with a solution I like better. By using the CSS ::after and ::before selectors, you can insert an arbitrary element that can take the place of a missing cell. The following CSS rule can be used to replace the empty div above.

```css
.table>*:nth-child(2)::before {
  content: " ";
  display: table-cell;
}
```

The nth-child(2) selector can be tailored to your given situation. You could replace it with something like a specific CSS class that you assign to the rows that you want to include empty columns.

Making use of CSS selectors instead of extra HTML elements can help you respect the separation of your document content from your document presentation. If at a later date, you decide you want to switch to a layout that doesn’t resemble a table, you can simply update the CSS rules to achieve a different look.
