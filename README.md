AI Now
======

[![Installability](http://img.shields.io/badge/installability-gold-ffd700.svg)]()

A website for the AI Now Conference.

Local development
-----------------

This project includes a Vagrantfile to make local development easy.
Make sure the `ainow` repo is inside a directory that Vagrant can
mount as an NFS share, eg:

    $ cd ~/Work/AINow
    $ git clone […]
    $ cd ~/Work/AINow/ainow

Then start the VM:

    $ vagrant up

SSH into the vagrant VM and activate the virtualenv:

    $ vagrant ssh
    vagrant@vagrant~$ cd /vagrant/ainow
    vagrant@vagrant~$ source ../virtualenv-ainow/bin/activate

Then run the Django dev server with:

    vagrant@vagrant~$ python manage.py runserver 0.0.0.0:8000

The website will then be running at http://localhost:8000
