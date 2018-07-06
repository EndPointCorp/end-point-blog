---
author: Ethan Rowe
gh_issue_number: 186
tags: community
title: lessons = colors.find_all {|c| c.kind_of? Blue}
---

As noted in this [nice article at Slate.com](https://www.slate.com/articles/arts/music_box/2009/08/kind_of_blue.html), the much-loved “Kind of Blue” celebrated its 50th anniversary recently. In the article, Fred Kaplan asks, and attempts to answer, “what makes this album so great?”

As somebody who has made a point of introducing his daughter (at infancy) to Miles Davis, who succumbed to the allure of jazz thanks in no small part to this very album, I would be remiss in my duties as a Caring Human not to blog about it. And yet this is a corporate blog for a consulting company that does lots of stuff with free software (as demonstrated so effectively [here](/blog/2008/08/18/alaska-basin)). What to do?

Fortunately, there’s something we in the software world can learn from this album and the lessons Mr. Kaplan derives from it. Let’s look at one key paragraph:

> So Kind of Blue sounded different from the jazz that came before it. But what made it so great? The answer here is simple: the musicians. Throughout his career, certainly through the 1950s and ’60s, Miles Davis was an instinctively brilliant recruiter; a large percentage of his sidemen went on to be great leaders, and these sidemen—especially Evans, Coltrane, and Adderley—were among his greatest. They came to the date, were handed music that allowed them unprecedented freedom (to sing their “own song,” as Russell put it), and they lived up to the challenge, usually on the first take; they had a lot of their own song to sing.

How does one write music that providers the players “unprecedented freedom”? In this case, it meant giving them musical forms with relatively few harmonic changes; instead of four, or two, or even one chord per measures, a given chord/scale would last for several measures at a time; the improviser could thus think horizontally (melodically) rather than vertically (harmonically) and be freer in the choice of notes employed.

So of course the quality of the musicians mattered; the musical material was fairly bare, by standards of the day, and the musicians really needed to have something interesting to offer to make something worthwhile of it. As noted, these musicians did.

Let’s derive two lessons from this:

1. Given fairly sparse requirements and room to interpret intelligently, great things can happen
1. Those great things will depend on the people you hire

Neither notion is particularly startling or insightful. But let’s combine it with the next observation from Mr. Kaplan:

> The album’s legacy is mixed, precisely for this [freedom]. It opened up a whole new path of freedom to jazz musicians: Those who had something to say thrived; those who didn’t, noodled. That’s the dark side of what Miles Davis and George Russell (and, a few months later, Ornette Coleman, in his own even-freer style of jazz) wrought: a lot of noodling—New Age noodling, jazz-rock-fusion noodling, blaring-and-squealing noodling—all of it baleful, boring, and deadly (literally deadly, given the rise of tight and riveting rock ‘n’ roll). Some of their successors confused freedom with just blowing whatever came into their heads, and it turned out there wasn’t much there.

Let’s now note that the musicians on “Kind of Blue” were not inexperienced, and in some cases not markedly young (though by no means “old” or even middle-aged). Davis and Coltrane both were around 32 or 33 (my age; remind me to denigrate myself when I’m done); Adderley, Evans, and Cobb were right around 30. The youngest, Paul Chambers, was around 24, but had played with Davis for four or five years by that time. All of them had been working musicians for years—​in some cases many years—​and had worked with a variety of illustrious colleagues. Given that such musicians typically start musical training and a young age, play their instrument all through their teen years, college years, etc., and often begin working professionally in college if not high school, it’s probably fair to say that their respective experience within their profession absolutely dwarfs that of the typical similarly-aged early-21st-century technology employee.

All the people on that recording spoke a common musical syntax. They didn’t invent a new syntax by simplifying the tunes; they applied their common knowledge and experience to a new situation and made something beautiful. A ten year-old pianist armed with fingering patterns for the minor keys of D and E-flat could have played in time with the band on “So What”. That pianist would not have known what to do with the fourths-laden voicings for the bass/piano call and response at the head of the tune. That pianist would not have known how to interact with Paul Chambers’ beautiful bass lines, because he/she would lack the melodic and formal grammar, and the harmonic vocabulary, to know what the bass was saying, let alone conceive of an intelligent response. It took Bill Evans to do these particular things in such a stirring, striking manner. (And Wynton Kelly on the blues; let’s not overlook that, because his solo on “Freddie” is burning.)

And yet, in addition to this common syntax, they each brought something different—​akin to an accent, or regional dialect. Evans’ Ravel/Debussy-tinged harmonic voicings are perhaps like a more expansive lexicon. The intersection of their respective approaches was most important, but the differences made for a more colorful, inspired union.

So, when you’re starting a software project, who do you want? Plenty of people out there can play a few chords in time. Do you want Miles’ band? Or would you perhaps prefer [these special guys](https://web.archive.org/web/20090828093327/http://www.jonasbrothers.com/)? Who would you trust to create the customized experience that people will return to time and time again, today, tomorrow, next year?

It’s not unreasonable to make these comparisons. A software project involves art and craft. The less clear the requirements, the more apparent this becomes. Relatively few projects start with a vision of such clarity that the role of technical interpretation is diminished. Even the most precise specification requires improvisation; if the spec provided the literal instructions on what functions to write and how to implement them, we would call it “code” and roll it out for you. For most projects, one must simply assume a profound need for deep technical interpretation; the only real question is how much business interpretation you need first.

Jazz performance is sometimes popularly construed as something like magic; something that can only be explained by “talent” and is fundamentally unfathomable. I remember my great aunt, who came to see my trio perform at a jazz festival in Vermont many years ago, saying “the music is just inside of you!” Well, yes, and the effort to get that little bit of music inside was colossal. There’s nothing magical or unfathomable about it; it’s hard work that takes years of dedicated, focused, consistent effort. It takes ear training, theory training, musical memory development, instrumental technique, improvisational technique, self-assessment and analysis, etc. It is a cultivated tradition of hard work, hard-won experience, that celebrates knowledge gained and skills acquired.

Sound familiar?

Why am I spending so much time on the obvious? Because apparently it’s [not obvious](https://www.backstreetboys.com/). It’s really [not obvious at all](http://www.scriptarchive.com/).

The past few years brought us some great advancements in the webapp framework space, making it easier to design decent-quality web applications with a reasonable separation of concerns. Yet, rather like “Kind of Blue”, they open up this idea that “Hey, anybody can do it!” And it’s true; most anybody can write an app that achieves a minimal separation of presentation, business, and data logic. But what of it? The first problem is a culture that ignores the rest of the software stack, because of a belief that everything that matters is in the application layer. A [decent object-relational mapper](https://metacpan.org/release/Rose-DB-Object) can encourage reasonably good data modeling practices at the relational/structural level, but [effectively encourages a culture of database ignorance and lowest-common-denominator thinking](http://api.rubyonrails.org/classes/ActiveRecord/Base.html). But most problematic of all: the simple idea that because somebody knows [framework X](https://web.archive.org/web/20110923063738/http://en.wikipedia.org/wiki/Apache_Struts#Competing_MVC_frameworks), that somebody can solve your problem.

I can play three chords, and you will [love them forever.](https://www.imdb.com/title/tt0332379/)

If your problem was easy to solve, you wouldn’t need said somebody; the difficulty in your problem isn’t the framework, it’s the business logic and the proper modeling thereof. In which case, you’re best off with people who have built systems both simple and complex, big and small, and thus have a wealth of experience to call upon when interpreting their way to a reasonable technical solution to your problem.

The technical execution of the loose sketches that made up the material on “Kind of Blue” did not pose any particular challenge for Davis and company; the real challenge was in making something worthwhile from it. The answer did indeed lie in the people, and a willingness to let those people exercise their own discretion in pursuit of a common vision, drawing on years of hard-earned experience to find the best expression possible within the established framework.
