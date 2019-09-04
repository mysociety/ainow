# TICTeC

A website for the TICTeC Conference.

## Local development

This project includes a `Vagrantfile` to make local development easier.

This includes a trigger that runs `script/bootstrap-dev` on `vagrant up` 
which will attempt to download up-to-date test data for the environment.
Note that triggers require Vagrant >= 2.1.0.

It relies on your having key-based SSH access to git.mysociety.org which
most people working on Tictec should have.

If it encounters a problem, it will halt and output an error message. 

To start work on your local machine, simply run:

    $ vagrant up

To get a fully configured vagrant development environment. The code is
installed into `/vagrant/ainow` inside the VM, and you can run
the Django dev server from within the Vagrant machine with:

    $ script/server

The website will then be running at http://localhost:8000

The virtualenv can be sourced with:

    $ source ../virtualenv-ainow/bin/activate

## Administration

Administration happens through Django's in-built admin interface. For production, this lives at https://tictec.mysociety.org/admin/.

### Schedules

The basis of each instance of a conference is the `Schedule`. Without this, nothing will work.

### Conference Timetable

#### Slots

A `Slot` represents a discrete period of time within a conference schedule in which one or more things may happen.

#### Sessions

A `Session` is an occurence of zero or more `Presentations`, in a `Room`, in a specific `Slot`. This is the closest thing that exists to the concept of a 'timetable slot'.

In the case of a `Session` for lunch or similar, there will be no `Presentations`. A keynote would have one `Presentation`, and a regular slot may have many.

#### Presentations

A presentation represents a talk by one or more `Speakers`, and occurs within a `Session`. They may have resources attached to them such as YouTube videos, or SlideShare presentations.

#### Rooms

A physical location in which `Sessions` occur.

### Speakers & Attendees

Each `Schedule` will likely have many people attending. These are represented by `Attendees` and `Speakers`. Please note that these do _not_ relate to each other - details for someone as a `Speaker` will be presented in a different context on the website to any details they may have as an `Attendee`.

#### Attendees

People who will appear in the list of attendees for a `Schedule`. May be linked to `Users` if we want them to be able to edit their own profile, but this is not necessary.

A person may attend (in theory) multiple `Schedules`, but this can cause administrative woes if someone moves jobs (for example) between conferences.

#### Speakers

Speakers are fundamentally attendees who can be linked to `Presentations`.

##### Keynote Speakers

Keynote speakers are specified in the view for the `Schedule`, and not in the database.

### Blocks

Some elements of the site source their content from the `Blocks`, based on slug.

Blocks are parsed as Markdown in most contexts.

## Important Code Locations

### Schedule Front Pages

Each schedule has its own front page template which lives in the `ainow/templates/ainow` folder, its own view which lives in `conference/views.py`, and a URL which lives in `conference/urls.py`.

### Conference-specific Speaker Pages

Some conferences have a custom speaker page view, for example where they have keynote speakers. These have URLs hardcoded in `conference/urls.py` and a matching view in `conference/views.py.
