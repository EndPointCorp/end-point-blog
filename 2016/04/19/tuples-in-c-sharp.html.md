---
author: "Dylan Wooters"
title: "Tuples in C#"
tags:  development

---

<div class="separator" style="clear: both; text-align: center;"><a href="/end-point-blog-git/2016/04/19/tuples-in-c-sharp/TwinsTuples.jpg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/end-point-blog-git/2016/04/19/tuples-in-c-sharp/TwinsTuples.jpg"/></a></div>

Dynamic and functional languages have greatly influenced C# as the language has matured. The introduction of the 'var' and 'dynamic' keywords allowed C# developers to write code that resembled a dynamic language like Python, and the fluent method chaining of one of C# greatest features, LINQ, came from functional programming concepts.

The [tuple class](https://msdn.microsoft.com/en-us/library/system.tuple(v=vs.110).aspx) is a good example of a recent C# feature that combines aspects of dynamic and functional paradigms. The tuple is a [common built-in feature](https://docs.python.org/2/tutorial/datastructures.html#tuples-and-sequences) in Python, but most C# developers are probably unaware of its benefits and usage. Tuples aren't a huge deal, but they come in handy in several modern programming scenarios.


###Returning Multiple Values

Say we need to call two APIs to create a music playlist and publish it to a social media site. We also want to wrap this functionality in a single method and return a boolean for whether or not the call was successful, as well as a specific, user-friendly error message. A tuple is helpful in this scenario.

```public static Tuple<bool, string> PublishPlaylist(string[] songIds)  
{
    var musicService = new MusicService();
    var socialMediaService = new SocialMediaService();
    string playlistId;

    try
    {
        playlistId = musicService.Create(songIds);
    }
    catch (Exception ex)
    {
        return Tuple.Create(false, "There was a problem creating your playlist.");
    }

    try
    {
        socialMediaService.PostPlaylist(playlistId);
    }
    catch (Exception ex)
    {
        return Tuple.Create(false, "There was a problem publishing your playlist to your page.");
    }

    return Tuple.Create(true, "");
}
```

The code above enables us to return multiple results without creating a strongly typed class with which to wrap them. Though the tuple is still strongly typed with a boolean and a string, it is more in the spirit of dynamic languages, or to use another term, "pythonic." You don't need to waste time and lines of code creating a throwaway class to wrap your results.

At this point, you may be thinking that you could use the `out` parameter to return multiple values. That is correct, and your method would look something like this.

```public static void PublishPlaylist(string[] songIds, out bool success, out string errorMessage)  
{
    //Instantiate local variables
    try
    {
        playlistId = musicService.Create(songIds);
    }
    catch (Exception ex)
    {
        success = false;
        errorMessage = "There was a problem creating your playlist.";
    }
    //etc.
}
```

###Enter Async


The problem with the `out` keyword is that it doesn't support [asynchronous methods](https://msdn.microsoft.com/en-us/library/hh156513.aspx#Anchor_1). To continue with our example, you may want to make PublishPlaylist an 'async' method, so that it doesn't block the thread while you are waiting for API calls. This is another case where returning a tuple is useful.

```public static async Task<Tuple<bool, string>> PublishPlaylist(string[] songIds)  
{
    var musicService = new MusicService();
    var socialMediaService = new SocialMediaService();
    string playlistId;

    try
    {
        playlistId = await musicService.Create(songIds);
    }
    catch (Exception ex)
    {
        return Tuple.Create(false, "There was a problem creating your playlist.");
    }

    try
    {
        await socialMediaService.PostPlaylist(playlistId);
    }
    catch (Exception ex)
    {
        return Tuple.Create(false, "There was a problem publishing your playlist to your page.");
    }

    return Tuple.Create(true, "");
}
```

###More on threads

I recommended making PublishPlaylist an async method "so that it doesn't block the thread." It turns out the [relationship between async and threads](https://msdn.microsoft.com/en-us/library/hh191443.aspx#Anchor_4) is pretty complicated. However, if you actually need to do "real" multi-threading, using the `Thread` class or `BackgroundWorker`, tuples come in handy as well.

As a basic example, say you are writing a WinForms app that creates a large Excel spreadsheet. You don't want to lock up the UI while the spreadsheet gets created, so you use `BackgroundWorker`. You can only pass one object between your main thread and the background thread when you fire off the [BackgroundWorker RunAsync method](https://msdn.microsoft.com/en-us/library/f00zz5b2(v=vs.110).aspx), but you actually need to pass multiple objects: a string path to write the Excel file to, and an Excel export options class. You can use a tuple for this as well.

```var xlsxOptions = new XlsxExportOptions();  
xlsxOptions.ExportMode = XlsxExportMode.SingleFile;  
xlsxOptions.ShowGridLines = true;  
xlsxOptions.TextExportMode = TextExportMode.Value;

var reportPath = @"C:\Clients\SeriesDigital\spreadsheet.xlsx";

var paramTuple = Tuple.Create<string, XlsxExportOptions>(reportPath, xlsxOptions);  
backgroundWorker.RunWorkerAsync(paramTuple);  
</code></pre>

In the <code> DoWork </code> event that is fired by the <code>RunAsync</code> method, you can just cast your event arg object back to a tuple, like this.

<pre><code>var paramTuple = e.Argument as Tuple<string, XlsxExportOptions>;  
//Call the ExportLandscape method to render the Excel file
ExportLandscape(paramTuple.Item1, paramTuple.Item2);  
StartProcess(paramTuple.Item1);  
```

One of the benefits of using a tuples in a multi-threaded application is that tuples are immutable and deemed [thread-safe](https://msdn.microsoft.com/en-us/library/system.tuple(v=vs.110).aspx#Anchor_6) (with a small caveat). Our `BackgroundWorker` example is too simplistic to highlight this, though it becomes very apparent in larger, multi-threaded, distributed computing environments. If you have multiple threads changing the state of an object, you can get into race conditions, inconsistent output, and other debugging nightmares. This is one reason why functional languages like F#, which champion immutability, are favored in these types of environments. Tuples are common in F#, so they eventually migrated over to C#.

The purpose of this post was not necessarily to highlight the Tuple class, but to show how C# is evolving thanks to the influence of other languages. Using dynamic and functional approaches with C# can help developers write code more efficiently and also can help in the asynchronous and distributed environments that are common today.


