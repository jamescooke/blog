API Documentation and the Communication Illusion
================================================

:date: 2016-05-04 12:00
:tags: topic:api, topic:documentation
:category: Code
:summary: How can documenting an API help us to communicate with our team and
          API consumer developers efficiently?
:scm_path: content/1605-api-documentation.rst


In this post I talk quite a lot about the "Communication Illusion" - a quote
often `misattributed to George Bernard Shaw
<https://en.wikiquote.org/wiki/George_Bernard_Shaw#Misattributed>`_:

    The single biggest problem in communication is the illusion that it has
    taken place.

Now let's talk about documenting APIs...

API documentation and my current workflow
-----------------------------------------

When I'm building an API, I usually have a client in mind that will be
consuming its resources. That means a developer or team of developers will be
writing code against the API that I build and so my current workflow for
updating or creating new API services focuses on providing API documentation.

It works like this:

* Manually document the endpoint using `REST API documentation templates
  <https://github.com/jamescooke/restapidocs>`_. Highlight any side effects,
  requirements and illustrate required data and responses.

  Alternatively, if there is a change to be made to the service, then the
  documentation edit can be provided as an SCM diff which can be easily
  reviewed.

* Ask for sign off on the API documentation from the API consumer development
  team. Incorporate any feedback and repeat until team are happy.

* Build out new endpoint using test cases written from the documentation.

* Once complete, export server responses back from the test suite into the
  documentation. Note any changes that were required to the signed off document
  and flag them to the consumer developers during the release process, if not
  beforehand.

Past experience of Communications Illusions
-------------------------------------------

In conversations with other developers about my process it's been called
"tedious". I can agree that it seems like extra effort at first, however, I
believe that it pays off in the long run and that belief is based on my past
experience at my old web development business, Fublo.

At Fublo, we often produced `brochureware
<https://en.wiktionary.org/wiki/brochureware>`_ sites on top of a simple CMS
system. When starting a new project, conversation within our team would often
happen like this:

    We know the solution to the problem, so instead of drawing out the design,
    let's just jump straight into HTML and code it up. This will save time.

Inevitably this didn't save time at all. We would often have to burn much of
our initial work because we couldn't fit the final client requirements into it,
or rework major structural elements because they turned out to be unsuitable.

This inefficiency is the result of three illusions:

* **The illusion with ourselves:** When we thought that we knew the solution
  and that it would be suitable and workable, this was just an illusion. Our
  minds tricked us into thinking that we knew the answer but we didn't.

* **The Communications Illusion within the team:** This was in full effect
  within our small team. We found that what we described as the problem to each
  other would fit with our own distorted view and we would only find out that
  our opinions were not the same some significant time after starting the
  build - sometimes too late to make changes.

* **The Communications Illusion with the client:** We also didn't often fully
  understand the client need, even though we thought we did at the outset.
  Sometimes there would be omissions in the brief or misunderstandings about
  how content would be provided, presented or managed.

Those three illusions sum up to one big Communications Illusion - we believe
that we, our team and our clients all have tallying opinions and ideas, when
there is no proof that that is the case.

Pretty quickly, but probably not as quickly as we would have liked, we realised
that the "tedious" way of producing flat designs before starting coding was
often the most efficient, even though it felt like it wasn't. It provided the
quickest route to a communication feedback loop, within ourselves, our team and
with our clients and that destroys the Communication Illusion. On top of that
it meant that we were not making any accidental, hard to refactor, architectural
decisions on the fly without all the required information.

Applying this to API design
---------------------------

So it's my opinion that producing a flat API document without touching a line
of code or writing a single test is the most efficient way of destroying the
potential Communications Illusions when creating APIs.

This means that providing static API documentation first is the most efficient
path to a place where API producers and consumers have a joint shared opinion
about how the API will operate and perform.

Tooling wishlist
----------------

On the flip side of those benefits in the long term, there is still a part of
me that finds some of my manual process a little slow. My inner need for
efficiency feels unfulfilled every time I copy and paste an API response into a
document.

In an ideal world I would have tools that would:

* Extract from the API documentation a set of tests that could be run against
  the built API to assert that the documentation features were all adhered to.

* A tool that would extract from the server responses made to these tests the
  response payloads so that they could be added back in or matched with the API
  document that they came from.

However, even if those tools did exist, the starting point would still be some
form of static documentation that describes what the API does.

I've seen that there are tools like `Apiary <https://apiary.io/>`_ which might
make this process easier, but I would want to hear some positive experience and
read a case study before I committed to using such a service for client work.

Final thoughts
--------------

So, I hope in this post I've been able to convince you that it's most
efficient to document your API before you build or change it. I hope that, like
me, you find that that efficiency comes from the increase in communication that
the documentation creates as a side-effect, destroying the Communication
Illusion that can ruin a project build.

Unfortunately, I've not found a way to ensure that the consumer programmers of
my APIs read and understand what's in the documentation before coding starts.
That's a second layer of Communication Illusion that I'll maybe get to tackle
another day.

Happily, I still agree with `this Tweet
<https://twitter.com/jamesfublo/status/518017851224227840>`_ that I posted more
than 18 months ago:

.. raw:: html

    <blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Building an API... All that matters is the docs.</p>&mdash; James Cooke (@jamesfublo) <a href="https://twitter.com/jamesfublo/status/518017851224227840">October 3, 2014</a></blockquote>
    <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

...and in fact, after working on more API builds and writing this post, I
believe it's even more true than before.

Happy API building!

* `Read comments on Hacker News <https://news.ycombinator.com/item?id=11666301>`_
