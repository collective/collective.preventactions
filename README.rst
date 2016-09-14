=========================
collective.preventactions
=========================

.. image:: https://travis-ci.org/imio/collective.preventactions.svg?branch=master
   :target: https://travis-ci.org/imio/collective.preventactions
.. image:: https://coveralls.io/repos/imio/collective.preventactions/badge.svg?branch=master
 :target: https://coveralls.io/github/imio/collective.preventactions?branch=master

This package allows administrateur to marker object which can't be deleted or renamed/moved.


* `Source code @ GitHub <https://github.com/imio/collective.preventactions>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/collective.preventactions>`_
* `Continuous Integration @ Travis-CI <http://travis-ci.org/imio/collective.preventactions>`_

How it works
------------

This package use marker interfaces and subscribe to `IObjectWillBeRemovedEvent` and `IObjectWillBeMovedEvent` events.
If a marker interface is find on modified object, a exception will be raised.


Installation
------------

To install `collective.preventactions` you simply add ``collective.preventactions``
to the list of eggs in your buildout, run buildout and restart Plone.

Then, install `collective.preventactions` using the Add-ons control panel.



License
-------

The project is licensed under the GPLv2.
