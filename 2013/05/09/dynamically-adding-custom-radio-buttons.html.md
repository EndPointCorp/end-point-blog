---
author: Zed Jensen
gh_issue_number: 797
tags: android, mobile
title: Dynamically adding custom radio buttons in Android
---

I’ve been writing a timesheet tracking app for End Point. In working on various features of this app, I’ve had more than a few problems to work through, since this project is one of my first on Android and I’ve never used many of the Android features that I’m now using. One particularly fun bit was setting up a scrollable list of radio buttons with numbers from 0 – 23 (no, we don’t often have people working 23 hours on a project in a day, but just in case!) when the user is creating an entry, as a prettier and more backward-compatible alternative to using a number picker to indicate how many hours were spent on this particular job.

In Android, view layouts are usually defined in XML like this:

layout/activity_hour_picker.xml

```
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
  android:layout_width="match_parent"
  android:layout_height="match_parent" >
  <Button android:id="@+id/button"
    android:layout_height="wrap_content"
    android:layout_width="wrap_content"
    android:onClick="doStuff"
    android:text="Hello World!" />
</RelativeLayout>
```

Simple. But, as you can imagine, not so fun when you’re adding a list of 24 buttons—so, I decided to add them dynamically in the code. First, though, a ScrollView and RadioGroup (ScrollView only allows one child) need to be defined in the XML, no point in doing that programmatically. Let’s add those:

layout/activity_hour_picker.xml

```
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
   android:layout_width="match_parent"
   android:layout_height="match_parent" >
   <HorizontalScrollView
        android:id="@+id/hour_scroll_view"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:fillViewport="true"
        android:scrollbars="none" >
        <RadioGroup
            android:id="@+id/hour_radio_group"
            android:layout_width="wrap_content"
            android:layout_height="match_parent"
            android:orientation="horizontal">
            // This is where our buttons will be
        </RadioGroup>
    </HorizontalScrollView>
</RelativeLayout>
```

Okay. So, now, in our Activity, we need to override onCreate if we haven’t already and add the following code:

src/com/example/HourPickerActivity.java

```
@Override
public void onCreate(Bundle icicle) {
  super.onCreate(icicle);
  setContentView(R.layout.activity_hour_picker);  // This adds the views from the XML we wrote earlier
  ViewGroup hourButtonLayout = (ViewGroup) findViewById(R.id.hour_radio_group);  // This is the id of the RadioGroup we defined
  for (int i = 0; i < RANGE_HOURS; i++) {
    RadioButton button = new RadioButton(this);
    button.setId(i);
    button.setText(Integer.toString(i));
    button.setChecked(i == currentHours); // Only select button with same index as currently selected number of hours
    button.setBackgroundResource(R.drawable.item_selector); // This is a custom button drawable, defined in XML
    hourButtonLayout.addView(button);
  }
}
```

And this is what we get:

<a href="/blog/2013/05/09/dynamically-adding-custom-radio-buttons/image-0-big.png" imageanchor="1"><img border="0" src="/blog/2013/05/09/dynamically-adding-custom-radio-buttons/image-0.png"/></a>

It scrolls horizontally like we want, but there’s a problem—we don’t want the default radio button selector showing up, since we’ve already got custom button graphics showing. And we can’t forget that we’re still missing the code to make everything within the RadioGroup work properly—In other words, the buttons won’t do anything when a user clicks them. So, let’s add a listener to each button as it’s created:

src/com/example/HourPickerActivity.java

```
<font color="#969696">button.setId(i);</font>
button.setBackgroundResource(R.drawable.item_selector); // This is a custom button drawable, defined in XML
button.setOnClickListener(new OnClickListener() {
        @Override
        public void onClick(View view) {
            ((RadioGroup) view.getParent()).check(view.getId());
            currentHours = view.getId();
        }
    });
<font color="#969696">button.setText(Integer.toString(i));</font>
```

So now the currently selected value is ready in our static variable currentHours for whenever the user is finished. Now we need to get rid of the standard radio button graphics. The solution I found is to use selector XML, with just one item that points to a transparent drawable:

drawable/null_selector.xml

```
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android" >
  <item android:drawable="@android:color/transparent" />
</selector>
```

Set each button to use it (and to center the text) like this (R.drawable.null_selector is our selector XML):

src/com/example/HourPickerActivity.java

```
<font color="#969696">button.setText(Integer.toString(i));</font>
button.setGravity(Gravity.CENTER);
button.setButtonDrawable(R.drawable.null_selector);
<font color="#969696">button.setChecked(i == currentHours); // Only select button with same index as currently selected number of hours  </font>
```

Now, let’s see how this all has pulled together.

<a href="/blog/2013/05/09/dynamically-adding-custom-radio-buttons/image-1-big.png" imageanchor="1"><img border="0" src="/blog/2013/05/09/dynamically-adding-custom-radio-buttons/image-1.png"/></a>

There—that looks much better! And it works great.
