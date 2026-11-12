Changelog
=========

0.4.0 (unreleased)
------------------

- Fix: the "Prevent actions" form now reindexes ``object_provides``, so the
  uninstall profile also unmarks objects protected through the form.
  [remdub]

- Fix: the uninstall profile now removes the "Prevent actions" object action.
  [remdub]

- Configure the package with ``plone.meta``: move package metadata to
  ``pyproject.toml``, replace buildout and ruff with tox and pre-commit
  (tested on Plone 6.2.3 and 6.1), add GitHub Actions workflows.
  [remdub]

- Import ``INonInstallable``, ``IPloneSiteRoot`` and ``get_installer`` from
  ``plone.base`` instead of the deprecated ``Products.CMFPlone`` locations.
  [remdub]

- Add tests for the event subscribers, the form, the portal actions and the
  uninstall profile.
  [remdub]

- Switch to PEP 420 native namespace package.
  [remdub]

- Add Plone 6 compatibility.
  [remdub]

- Add french locales.
  [remdub]

- Remove robot tests.
  [remdub]

- Add behavior to choose which content types to prevent.
  [remdub]


0.3.0 (2019-11-26)
------------------

- Remove Archetypes dependency.
  [bsuttor]


0.2.1 (2018-07-10)
------------------

- Typo.
  [bsuttor]


0.2 (2018-07-09)
----------------

- Fix check render of PreventActionForm.
  [bsuttor]


0.1 (2016-09-20)
----------------

- Package created using mr.bob
  [bsuttor]
