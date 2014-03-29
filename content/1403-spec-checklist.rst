Flat designs to website specification - a checklist
###################################################

:date: 2014-03-29 16:00
:category: Code
:summary: Agencies often provide flat designs to web developers as a
          specification, but these only scratch the surface of a true website
          functional specification. This is a check-list of features which can
          be fleshed out to start the journey towards a full functional spec.


Isolated design has problems
============================

Since many web projects are approached from the visual aspect, often the *seen*
elements are designed first. This can be fine if it's integrated with well
thought out feedback from developers, but can create more work for the project
if it's completed and signed off in isolation.

* **Results in more development work** when a design might have some serious
  development implications when compared to a slightly different solution that
  could also have been acceptable.
* **Work estimates will be less accurate** since the flat designs just start to
  scratch the surface of the development required - they are not a full
  specification.
* **Can lead to frustration within the design team** as they are asked to
  redesign elements during the production process that they thought were
  already signed off.
* **Potentially leads to uncertainty with the client** if 'signed off' designs
  are presented again for sign off with changes that were not previously
  foreseen.


How to use this checklist
=========================

Next time you see a software project being discussed just via flat designs, let
your alarm bells ring. Open up conversation about the features on this list to
break down the isolation that the design team is operating in.


For Developers
--------------

This basic list can start a journey of specification exploration. Start to ask
questions about all these features before you agree on a specification or
timeline since some of these items can become heavy or project effecting.

This list is very back-end focused, but hopefully can be helpful for
front-enders too.


For Website owners
------------------

If you're being asked to sign off a project on flat designs alone, then it
might be beneficial to check that the team you're working with have these
aspects of the development on their radar. They might not have the answer to
them yet, but should have a plan to find them.


For Designers
-------------

You are often stuck in the middle of the process. Continue to involve your
development team, they will be able to point out things that will require more
effort to build before your client signs off the visuals, saving the project
work in the long term.

You can help to ensure you get good value feedback by asking them questions
about items on this checklist - ensure they're not lulled into a false sense of
"it'll be easy" by your fantastic design work!


The Checklist
=============

The following details are often missing from flat web designs, but should be
provided in a full specification.

* **Page titles** - Standard and often missed by designers that use a generic
  image of a web browser frame to wrap their designs. Loved by content managers
  and search engines. Do they have a format and can be auto-generated? Does the
  content database need an extra field?

* **Hidden HTML data** - What about all the data in the HTML `<head>`? Meta
  description, icon, Facebook data? Also for each image what will be the `<img>
  alt` tag?

* **URLs** - Also missed by designers when using generic browser frames, what
  are the URLs of each page being shown? Remember to check the URLs of pages
  that have pagination.

* **Data field requirements** - Designs often show the 'best case' for content,
  but ensuring good data is entering the database is essential for a successful
  web project. What are the limits - shortest names?  Longest ones?  Are spaces
  allowed? Should content be trimmed? Emails should be validated, but on what
  level? Semantically, or with a request to a DNS or mail server?

* **Form fields, validation and error messages** - If you're looking at a
  design that shows a web form, are there are error messages in the design?
  Expanding on the requirements for the data above, what will happen to the
  form when invalid data is entered? How will fields be flagged for errors?
  Which data elements will be sent back to the form and which will be cleaned
  out? Are there any fields (like address) that need to be localised?

* **User sign up requirements** - If the site will be accepting registrations,
  what will users need to provide to register? Email address? User name (how
  long)? Are there any blocked words in user names (like 'admin', the project
  brand name or profanities)? Password (how long)? Are there any password
  strength requirements? How will users reset their passwords?

* **Transactional emails** - What emails will need to be sent by the system?
  What is their content and design? Can users manage these notifications?

* **Security** - Will the site have any functions that will protect the data of
  its users? For example, will the user login page throttle access on multiple
  incorrect passwords? Will there be 'https' required?

* **Private data** - Since flat designs will show the public end user view of a
  project, what data is hidden from the user but essential for the project?
  Latest login dates? Number of logins? IP address of last visit or
  registration? Banned, active, subscriber flags? Active or dormant flags on
  content?

* **Click and hover behaviours** - What will happen when elements like links
  are hovered? Are there any menus functions that are hidden behind clicks? Are
  there any titles to be shown when the user hovers an item?

* **Error pages** - What is the design for the 404 page? What about 503 and any
  other error pages? Will there need to be a holding page when the site is
  being updated and is offline?

* **Analytics configuration** - How should the analytics be configured to track
  behaviours on the site? Is it required? Will a simple configuration suffice
  or will there need to be funnels and or events configured? Analytics can be
  complex enough to require as much work as the original build out of a
  project, so ensuring that the specification is defined and covers the
  business needs early is a benefit.

* **Translation requirements** - Will any of the content in the designs require
  translation? This also effects the items mentioned above in the checklist.
  Remember that any image elements that have been prepared that contain text
  will need to be generated in each target language - will each of those
  translated texts fit within the design?


Feedback and thoughts
=====================

I hope that the list above helps someone who's working through the design of a
site. Any time that I've worked on a project where developers and stakeholders
have been involved in the design stages early on have always been successful.

If there are items you think should be added you can contribute on GitHub, or
mention them in the comments below.

Thanks for reading.
