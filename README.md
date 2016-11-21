AI Now
======

[![Installability](http://img.shields.io/badge/installability-gold-ffd700.svg)]()

A website for the AI Now Conference.

Local development
-----------------

This project includes a Vagrantfile to make local development easy.
Simply run:

    $ vagrant up

To get a fully configured vagrant development environment. The code is
installed into `/vagrant/ainow` inside the VM, and you can run
the Django dev server with:

    $ source virtualenv-ainow/bin/activate
    $ python manage.py runserver 0.0.0.0:8000

The website will then be running at http://localhost:8000

Creating content
----------------

The basic steps to creating content for a conference are:

* Create a Schedule or Schedules
* Add Slots to the Schedule for when talks are happening
* Create Speakers.
* Create a Presentation for each talk and associate it with a Slot
* Associate Speakers with Presentations

Note that not all the items below may be relevant depending on the
design of the site.

### Schedules

A Schedule represents a series of talks or sessions. Schedules are the
underlying organising concept of the site. Broadly speaking if an item
isn't associated with a schedule then it won't appear on the site.

### Slots

A Slot is a period of time and is used to both set out when things are
happening and also to link a Presentation to a Schedule.

If you have a Slot in which mutiple talks are happening - e.g. Lightning
Talks - then you can include the talks by setting the Slot type to Other
and linking to them in the Slot description. Note that the Presentations
will still need to be associated with a Schedule to be displayed on the
site.

### Presentations

A Presentations can have a main speaker and associated speakers. If a talk is
associated with a Slot then it will automatically appear in the
Schedule.

For a Presentation to be displayed on the site it must either be associated
with a Slot or a Schedule. You should use the latter for talks that
appear as part of a session - e.g. Lightning Talks or Poster sessions.

### Speakers

People giving talks. Note that a speaker will only appear on the
Speakers page if they are associated with a Presentation.

### Resources

The resources pages are used for collecting sets of documents together.
You can create a resource and then associated a set of documements with
it to have them listed on that Resource page.

### Pages

Pages are used for content that does not fit in the categories above -
e.g. Call for Papers.

# Blocks

Blocks are for small editiable pieces of text that are used in otherwise
hardcoded templates. The content of them will depend on the design of
the site.

### Trouble shooting

#### Missing content

If something does not appear on the site - i.e. you get a Page Not Found
error - then check that is associated with a Slot.

#### Speaker not appearing in list

For a speaker to appear in the automatically generated list of speakers
then they need to be associated with a Presentation either as a main or
secondary speaker.

If they are associated with a Presentation and still not appearing check
that the Presentation is associated with a Slot or a Schedule.
