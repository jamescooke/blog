Auto-generated vs Manual API Documentation Strategies
=====================================================

:date: 2016-05-04 12:00
:tags: documentation
:category: Code
:summary: 
:scm_path: content/1605-api-documentation.rst


Background
----------

Benefits of manual documentation

* Frameworks provide large amounts of power with only a few lines of
  configuration. For example, this configuration in Django Rest Framework will
  set up a CRUD endpoint for Accounts:

  .. code-block:: python

      >>> from

  In this situation it's hard to see where the documentation would fit if a 


The communication illusion
--------------------------

I'll take a lot in this post about the illusion of communication. This is a
quote often `misattributed to George Bernard Shaw
<https://en.wikiquote.org/wiki/George_Bernard_Shaw#Misattributed>`_, but it's
helpful, so here it is:

    The single biggest problem in communication is the illusion that it has
    taken place.

Past experience
---------------

To me this seems like a problem we often faced at my old business Fublo when
approaching a new website build. Our builds often consisted of `brochureware
<https://en.wiktionary.org/wiki/brochureware>`_ sites on top of a simple CMS
system, so they were not complex. However, conversation within our team would
often happen like this:

    "We know the solution to the problem, so instead of drawing out the design,
    let's just jump straight into HTML and code it up. This will save time."

However, we often found that inevitably this didn't save time at all. We would
often have to burn much of our initial work because we couldn't fit the final
client requirements into it, or rework major structural elements because they
turned out not to be suitable.

I see the this eventual inefficiency as the result of three illusions:

* **The illusion within ourselves:** It turns out it's just an illusion that
  what we thought was the solution was suitable and or workable. We often
  thought we "knew" the client problem and how to solve it, but in the end it
  turned out, more often than not, we didn't.

* **The illusion within the team:** This illusion was also in full effect
  within our small team. We found that what we described as the problem to each
  other would fit with our own distorted view.  

* **The illusion that we knew what the client wanted:** We also didn't often
  fully understand the client need, even though we thought that we did at the
  outset. Sometimes there would be omissions in their brief or
  misunderstandings about how content would be provided or managed.

 The only real way to get a
  unified plan was to flesh out our ideas rather than descr


Applying this to API design
---------------------------

Based on my past experiences
