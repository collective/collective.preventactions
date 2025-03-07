.. image:: https://coveralls.io/repos/collective/collective.preventactions/badge.svg?branch=master
   :target: https://coveralls.io/github/collective/collective.preventactions?branch=master

=========================
collective.preventactions
=========================

This package allows administrators to mark objects which can't be deleted or renamed/moved.

.. image:: https://raw.githubusercontent.com/imio/collective.preventactions/master/docs/screenshot.png
    :alt: The map on a collection.
    :width: 388
    :height: 276
    :align: center

* `Source code @ GitHub <https://github.com/collective/collective.preventactions>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/collective.preventactions>`_


Versions
--------

- Version 0.4 is for Plone 6 and Python 3
- Version 0.3 is for Plone 5.2 and Python 3
- Versions < 0.3 are compatible with Archetypes (branch 0.2.x)


How it works
------------

This package use marker interfaces and subscribe to `IObjectWillBeRemovedEvent` and `IObjectWillBeMovedEvent` events.
If a marker interface is find on modified object, a exception will be raised.

You can also set some contents not deleteable (for example) like this in your setuphandler : ::

   from collective.preventactions.interfaces import IPreventDelete
   from plone import api
   from zope.interface import alsoProvides


   def post_install(context):
       obj = api.content.get('/Plone/content-not-deleteable')
       alsoProvides(obj, IPreventDelete)

Installation
------------

To install `collective.preventactions` you simply add ``collective.preventactions``
to the list of eggs in your buildout, run buildout and restart Plone.

Then, install `collective.preventactions` using the Add-ons control panel.



License
-------

The project is licensed under the GPLv2.
