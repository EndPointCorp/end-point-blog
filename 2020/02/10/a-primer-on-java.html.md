---
author: "Árpád Lajos"
title: "A primer on Java"
tags: java, wildfly, language
gh_issue_number: 1590
---

###What is Java and why is it interesting?

Java is a descendant of C++ and it is a C-based language. C was therefore the original language and it is probably not an overstatement to say that C is the most popular programming language in history. Most programmers speak at least C or one of its descendants. Let’s take a quick look at the most popular on the [list of C-based languages](https://github.com/AnanthaRajuCprojects/List-of-programming-language-lists/blob/master/C-family%20programming%20languages.md):

- C
- C++
- C#
- Fantom
- Go
- Java
- JavaScript
- Objective C
- Perl
- PHP
- Swift
 
Java is a member of a large family of programming languages and as a result, if someone learns Java, then they will have an easier time learning one of its cousins. And at the same time, if someone already speaks a C-based language, then Java is not too difficult to learn. Also, if someone is already a programmer and does not speak a C-based language yet, then it is in his/​her interest in most cases to learn a C-based language and thus to have an understanding of the most popular language family.
 
Let’s see the list of popular languages according to [Stackify](https://stackify.com/popular-programming-languages-2018/8/):

<style>
#java-primer-table td {
  text-align: right;
}

#java-primer-table td:first-child {
  text-align: left;
}
</style>
<div class="table-scroll">
  <table style="margin: auto" id="java-primer-table">
    <tr>
      <th><p style="margin-right: 200px"><b>Programming Language</b></p></th>
      <th><p style="margin-left: 40px"><b>Ratings</b></p></th>
      <th><p><b>Change</b></p></th>
    </tr>
    <tr>
      <td><p>Java</p></td>
      <td><p>16.028%</p></td>
      <td><p>-0.85%</p></td>
    </tr>
    <tr>
      <td><p>C</p></td>
      <td><p>15.154%</p></td>
      <td><p>+0.19%</p></td>
    </tr>
    <tr>
      <td><p>Python</p></td>
      <td><p>10.020%</p></td>
      <td><p>+3.03%</p></td>
    </tr>
    <tr>
      <td><p>C++</p></td>
      <td><p>6.057%</p></td>
      <td><p>-1.41%</p></td>
    </tr>
    <tr>
      <td><p>C#</p></td>
      <td><p>3.842%</p></td>
      <td><p>+0.30%</p></td>
    </tr>
    <tr>
      <td><p>Visual Basic .NET</p></td>
      <td><p>3.695%</p></td>
      <td><p>-1.07%</p></td>
    </tr>
    <tr>
      <td><p>JavaScript</p></td>
      <td><p>2.258%</p></td>
      <td><p>-0.15%</p></td>
    </tr>
    <tr>
      <td><p>PHP</p></td>
      <td><p>2.075%</p></td>
      <td><p>-0.85%</p></td>
    </tr>
    <tr>
      <td><p>Objective-C</p></td>
      <td><p>1.690%</p></td>
      <td><p>+0.33%</p></td>
    </tr>
    <tr>
      <td><p>SQL</p></td>
      <td><p>1.625%</p></td>
      <td><p>-0.69%</p></td>
    </tr>
    <tr>
      <td><p>Ruby</p></td>
      <td><p>1.316%</p></td>
      <td><p>+0.13%</p></td>
    </tr>
    <tr>
      <td><p>MATLAB</p></td>
      <td><p>1.274%</p></td>
      <td><p>-0.09%</p></td>
    </tr>
    <tr>
      <td><p>Groovy</p></td>
      <td><p>1.225%</p></td>
      <td><p>+1.04%</p></td>
    </tr>
    <tr>
      <td><p>Delphi/​Object Pascal</p></td>
      <td><p>1.194%</p></td>
      <td><p>-0.18%</p></td>
    </tr>
    <tr>
      <td><p>Assembly language</p></td>
      <td><p>1.114%</p></td>
      <td><p>-0.30%</p></td>
    </tr>
    <tr>
      <td><p>Visual Basic</p></td>
      <td><p>1.025%</p></td>
      <td><p>+0.10%</p></td>
    </tr>
    <tr>
      <td><p>Go</p></td>
      <td><p>0.973%</p></td>
      <td><p>-0.02%</p></td>
    </tr>
    <tr>
      <td><p>Swift</p></td>
      <td><p>0.890%</p></td>
      <td><p>-0.49%</p></td>
    </tr>
    <tr>
      <td><p>Perl</p></td>
      <td><p>0.860%</p></td>
      <td><p>-0.31%</p></td>
    </tr>
    <tr>
      <td><p>R</p></td>
      <td><p>0.822%</p></td>
      <td><p>-0.14%</p></td>
    </tr>
  </table>
</div>

Yes, Java has lost almost a percent from its popularity according to the list above, but even though the trend is suboptimal for Java at the time of this writing, it’s still ahead of the second-placed C in a convincing manner, since between the two there is almost a whole percent and has an advantage of more than 6% over Python, which is not a C-based language, but nevertheless it’s popular and rapidly gaining popularity, but it’s still very far from Java. Any other language is way below the popularity of Java, not even close.
 
What this means:
 
- If you get a programming job and you are agnostic to languages, then Java is a language you may well work in.
- Due to the popularity of the language for most problems you will likely find a well written and well tested, reliable library.
- If you search for a programmer, he/​she will more likely speak Java than other languages.
 
According to [Towards Data Science](https://towardsdatascience.com/20-predictions-about-software-development-trends-in-2020-afb8b110d9a0), based on the data acquired from [TIOBE](https://www.tiobe.com/tiobe-index/), Java has been the most popular language since 2002 with two “pauses”, when C briefly took over, but even then, Java was the second:

<div style="width: 100%; text-align: center;"><img src="/blog/2020/02/10/a-primer-on-java/language-graph.png"></div>

As a result, taking into account the current situation, it is an imperative to speak a C-based language at least and due to Java’s popularity, it is advisable for programmers to be prepared to work in Java, by acquiring at least some practical knowledge about the language. Web programmers will naturally speak at least one C-based language if they work on the front-end, since in browsers JavaScript is standard.
 
Since there are many servers using Java and on smartphones Android is Java-based, Java’s future looks bright, so, if someone knows how to work with Java, then this knowledge will not lose its relevance in the foreseeable future.

###“A long time ago in a galaxy far, far away...”

(Or, in other words, when I was still a university student, when a deadline was closely linked to homework and exam sessions.)

If you ask me what my favorite language is, I will tell you that I’m agnostic, because programming languages are just means of transforming thoughts into software. The main feature of languages – even outside of the realm of programming – is their ability of transmitting thoughts between actors in a conversation. Yes, Java’s syntax is very neat and there are other languages having a neat syntax as well. So, at this point I have no favorite programming language, but back in the day, Java offered some mouth-watering novelties for me, that filled me with enthusiasm. In the first two hours of my encounter with Java I learned that there is:
 
- no need to worry about pointers
- or function pointers
- or allocating and freeing memory (due to the [Garbage Collector](https://www.guru99.com/java-garbage-collection.html))
- or different platforms (due to the [Java Virtual Machine](https://en.wikipedia.org/wiki/Java_virtual_machine))

Java enforces object-oriented coding, which helps us a lot, because that way, if we work in Java, then we do not need to worry about encountering procedural code written by others. Also, it forces us to think about the concepts we are about to use in our project. All these were great things to see.

If one just starts to code with Java, or has to work with classes or methods he/​she is not very experienced with, then the brilliantly written [documentation](https://docs.oracle.com/javase/9/docs/api/overview-summary.html) can help them. 

<div style="width: 100%; text-align: center;"><img src="/blog/2020/02/10/a-primer-on-java/doc-example.png"></div>

This method is the add method of ArrayList. We know that ArrayList is logically a collection (technically it’s inherited from AbstractList, which is inherited from AbstractCollection), so, adding an item to it is the capability of putting an item at the end of the set of items present in the collection. We can also see that it is public and it will return a boolean, which represents success (or lack of it). Some parameter of the type E is passed to it. Since the ArrayList is denoted as ArrayList&lt;E&gt; at the start of the [article](https://docs.oracle.com/javase/9/docs/api/java/util/ArrayList.html#add-E-), it’s clear that E is the type of the elements. So, taking a single glance on the first line inside the box one already understands the core information.

Of course, I had some prerequisite knowledge in C and C++ before sitting down for two hours to learn Java, but even then, being able to learn how to work with Java and being very comfortable with doing so in just two hours is a great achievement, but it’s not my achievement. It’s Java’s wonderful syntax, documentation and a great friend with the patience to teach, who achieved this for me. I only had to be curious.

###Java consulting

My first work was in C++, but after realizing that I do not intend to go to an office each morning in the long term, I had the bold idea of finding remote work. So I started to work as a freelancer, doing small and poorly paid work remotely, often investing more energy into winning projects via negotiation than actually doing the work, but I was confident that my efforts will pay off long term.

In this period I learned PHP, JavaScript, CSS, HTML, MySQL (this was easy, because I was comfortable with Oracle), and realized that Java is not an objective best, at least not for me. It is just a language that I subjectively like and have fond memories with, but objectively I can perform well in other technologies as well.
 
After a lot of struggle, doing a lot of negotiation and freelancing work for very different people, each having his/​her own preferences, cultural background, and temperament, I ended up working on .NET projects. Even though I enjoyed working with .NET as well, which was mostly in ASP.NET, I had difficulty working with Visual Basic, since my only coding with BASIC was some work I did with QBasic, when I was 11 years old. Even though I enjoyed working with QBasic as an early teen, writing code to display some graphic in motion, when I encountered Visual Basic with the purpose of developing the backend of ASP.NET projects, I had to relearn BASIC and having experience with C-based languages, I found it strange to see code like:

```plain
If foo IsNot Nothing AndAlso foo.IsValid Then
	'Some code
ElseIf foo IsNot Nothing Then
	'Some code
Else
	'Some code
End If
```

instead of

```java
if (foo != null && foo.isValid) {
 	//Some code
} else if (foo != null) {
	//Some code
} else {
	//Some code
}
```

I could work with either of the syntaxes, but the C-based syntax required much less characters to be typed on my part and the use of whitespace as operation separators is a source of worry for me (what happens if for any reason tabs are switched with spaces and vice-versa in Python, for example), which is a small problem for a small code but a bigger a problem if the code is bigger. But even though the situation was not very dramatic for me, I enjoyed [a parody about Java and .NET immensely](https://www.youtube.com/watch?v=RnqAXuLZlaE).

Over the years every now and then I received Java projects, mostly console or desktop applications, but occasionally I had some web work with Java as well. Since I began working with End Point I have been working on several Java projects running under [Wildfly](https://wildfly.org/), a very nice application server, developed by Red Hat.

In general, when some work is completed, I build it with an [ant](https://ant.apache.org/) command and deploy it using jboss.

In Linux I run `jboss-cli.sh`, for Windows there is a `jboss-cli.bat` alternative. After running it, we need to:

```plain
connect
```
 
and then deploy, like:
 
```plain
deploy <path to the ear file>
```

You can use the `--force` parameter to replace an older version of the deployment with the newer one.

Of course, this will only work if Wildfly is running. In order to make sure it is running, one needs to execute:

`
./standalone.sh -server-config=standalone-full.xml
`

Of course, one may use a different server config. It also has a Windows alternative, a file named `standalone.bat`, having the same purpose.

###Java ORM

I used several different database object-relational mappers (ORMs) in the past, like LINQ, Flourishlib, Doctrine, to name a few examples. In Java I have been using [Hibernate](https://hibernate.org/) in recent times and am very satisfied with it in general. I can nicely work with object entities to represent table rows using Hibernate.

The entities in Hibernate are defined as [POJO](https://en.wikipedia.org/wiki/Plain_old_Java_object) (plain old Java object) classes, where data members are private and they are accessible via public setters and getters. The classes and tables can be mapped via a mapping configuration XML. There are nice examples available online, for instance [this one](https://www.tutorialspoint.com/hibernate/hibernate_examples.htm). One has the option to use Hibernate annotations as well, like [here](https://www.tutorialspoint.com/hibernate/hibernate_annotations.htm).

Besides methods that can be used with the help of session objects, one can write custom Hibernate queries as well, like:

```java
String hql = "UPDATE Employee set salary = :salary "  +
             "WHERE id = :employee_id";
Query query = session.createQuery(hql);
query.setParameter("salary", 1000);
query.setParameter("employee_id", 10);
int result = query.executeUpdate();
System.out.println("Rows affected: " + result);
```

That example is from [Tutorials Point](https://www.tutorialspoint.com/hibernate/hibernate_query_language.htm).

###Is Java slow, or is that a myth?

Java is a language. It’s not slow or fast. Performance depends on what is running and how. Natively compiled languages like C or C++ are in general faster, but the difference is not in the language itself, but the way the code is executed. Java runs through the JVM (Java Virtual Machine).

<img src="/blog/2020/02/10/a-primer-on-java/jvm.svg" style="display: block; margin: auto"><br />
Taken from [net-informations.com](http://net-informations.com/java/intro/jvm.htm)

That’s slower than running the compiler separately for each target platform and avoiding the usage of a virtual machine at runtime. The JVM helps us to avoid worrying about different platforms, and performance issues due to the language itself are an unlikely cause of performance issues in general. However, if one has a Java project with performance problems and the culprit is JVM, then one can compile Java bytecode into machine code. Alternatively, Java code can be converted automatically into C or C++.
 
If one is worried about using Java which then might become C or C++ code, then it’s worth considering the fact that C or C++ code on their own are already abstractions in comparison to machine code. Python and Ruby environments are slower to run than Java these days in my experience, so Java’s slowness is a myth nowadays and the truth in it is rooted in the past, when JVM was slow to start. However, at that point it was not Java itself that was slow, but the virtual machine that was running it for the platform.

Naturally, if we do not convert our code into machine code, but we run it through a virtual machine, that, upon each run will have to detect what the platform is and to interpret the JAR file, that convenience at the time of development comes at a price at runtime. But this problem is only theoretically frustrating these days, since with the ever more performant computers, if we find our Java program to be slow, then we should review the actual code before blaming the JVM for our performance problems.

Consider the example when someone is speaking in English and a translator has to translate the speech into French in real-time. What would we say if the interpreter is arriving late by a minute? Would we consider English to be a slow language, because of our initial wait for the translator? Naturally not. The situation with JVM slowness is similar. If the project is very large, that is, there is a lot of work to do for the JVM, then we might still experience slowness these days as well at program start, but if that becomes a serious problem, then we of course can solve that. Note that slow, underperforming or buggy code can be written in any language.

In short, Java, as a language is not slow, especially if it was translated into machine code. If it’s running via the JVM, then there is a performance price we pay in order to have no worries about platforms, but that’s rarely felt nowadays because of today’s general computing power.

###Primitive and reference types

In Java there are primitive types and reference types. Reference types are Object and anything inherited from it. Primitive types, like float, int, or double are not objects and hence they cannot be used in a generic manner. To overcome this issue, Java offers wrapper classes for primitives, which are like Float, Integer or Double.

One cannot create a List of int, but a List of Integer can be created without problems. Integer is a reference type, hence we can use it as a specification for generics. I consider this to be a drawback of the language. I think that conceptually one might say that primitives and references are all types. So, if we could define some ultimately generic type as something special that represents the ultimate generic, even more abstract than Object, with the convention that any primitive or Object is of this generic type, then we should be able to create lists or collections of int or double.

I understand that this is not possible in the language, but I believe that this abstraction should be done under the hood. For example ArrayList&lt;int&gt; should be either inherently supported, or interpreted as ArrayList&lt;Integer&gt;. Of course, in order to establish this, some rules need to be implemented and tested thoroughly, but as a result we would be able to get rid of the unnecessary rule that primitive types cannot be referred to by generics.

###Summary

- Java is the most popular programming language and it is a C-based language.
- C-based languages are the most popular programming language family and it’s the interest of every programmer to have an understanding of C-like syntaxes.
- Due to its popularity it’s not difficult to find programmers who speak this language.
- The language enforces development to comply to object-orientation.
- Primitive types cannot be used as generic, one needs to use wrapper classes for this purpose.
- Java is a language and as such it cannot be fast or slow; its environment can be fast or slow though.
- JVM was slow to start in the past, but today this is less of a problem.
- Java has a bright future due to the many popular projects in Java and Android.
