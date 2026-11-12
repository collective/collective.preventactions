from AccessControl import Unauthorized
from collective.preventactions.browser.preventactions import PreventActionsForm
from collective.preventactions.interfaces import ICollectivePreventActionsLayer
from collective.preventactions.interfaces import IPreventDelete
from collective.preventactions.interfaces import IPreventMoveOrRename
from collective.preventactions.testing import COLLECTIVE_PREVENTACTIONS_INTEGRATION
from plone import api
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

import unittest


class TestForm(unittest.TestCase):
    layer = COLLECTIVE_PREVENTACTIONS_INTEGRATION

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.document = api.content.create(
            container=self.portal, type="Document", id="document"
        )

    def test_form_checked_options(self):
        login(self.portal, TEST_USER_NAME)
        alsoProvides(self.document, IPreventDelete)
        form = PreventActionsForm(self.document, self.request)
        form.updateWidgets()

        widget = form.widgets.get("delete")
        delete_widget_value = widget.items[0]
        self.assertTrue(delete_widget_value["checked"])
        widget = form.widgets.get("move_or_rename")
        move_or_rename_widget_value = widget.items[0]
        self.assertFalse(move_or_rename_widget_value["checked"])

        noLongerProvides(self.document, IPreventDelete)
        form.updateWidgets()

        widget = form.widgets.get("delete")
        delete_widget_value = widget.items[0]
        self.assertFalse(delete_widget_value["checked"])
        widget = form.widgets.get("move_or_rename")
        move_or_rename_widget_value = widget.items[0]
        self.assertFalse(move_or_rename_widget_value["checked"])

        alsoProvides(self.document, IPreventMoveOrRename)
        form.updateWidgets()

        widget = form.widgets.get("delete")
        delete_widget_value = widget.items[0]
        self.assertFalse(delete_widget_value["checked"])
        widget = form.widgets.get("move_or_rename")
        move_or_rename_widget_value = widget.items[0]
        self.assertTrue(move_or_rename_widget_value["checked"])


class TestFormSubmit(unittest.TestCase):
    """Submit the @@prevent-actions form like a browser would."""

    layer = COLLECTIVE_PREVENTACTIONS_INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        alsoProvides(self.request, ICollectivePreventActionsLayer)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.document = api.content.create(
            container=self.portal, type="Document", id="document"
        )

    def submit(self, delete=False, move_or_rename=False):
        for name, checked in (("delete", delete), ("move_or_rename", move_or_rename)):
            self.request.form[f"form.widgets.{name}-empty-marker"] = "1"
            if checked:
                self.request.form[f"form.widgets.{name}"] = ["selected"]
            else:
                self.request.form.pop(f"form.widgets.{name}", None)
        self.request.form["form.buttons.save"] = "Save"
        self.document.restrictedTraverse("@@prevent-actions")()

    def catalog_ids(self, iface):
        brains = api.content.find(object_provides=iface.__identifier__)
        return [brain.getId for brain in brains]

    def test_save_marks_object(self):
        self.submit(delete=True)
        self.assertTrue(IPreventDelete.providedBy(self.document))
        self.assertFalse(IPreventMoveOrRename.providedBy(self.document))

    def test_save_unmarks_object(self):
        alsoProvides(self.document, IPreventDelete, IPreventMoveOrRename)
        self.submit()
        self.assertFalse(IPreventDelete.providedBy(self.document))
        self.assertFalse(IPreventMoveOrRename.providedBy(self.document))

    def test_save_reindexes_object_provides(self):
        # The uninstall profile finds marked objects through the catalog.
        # Query first, so the document is indexed before the form runs.
        self.assertEqual(self.catalog_ids(IPreventDelete), [])
        self.submit(delete=True, move_or_rename=True)
        self.assertEqual(self.catalog_ids(IPreventDelete), ["document"])
        self.assertEqual(self.catalog_ids(IPreventMoveOrRename), ["document"])

        self.submit()
        self.assertEqual(self.catalog_ids(IPreventDelete), [])
        self.assertEqual(self.catalog_ids(IPreventMoveOrRename), [])

    def test_form_requires_manage_portal(self):
        setRoles(self.portal, TEST_USER_ID, ["Editor"])
        with self.assertRaises(Unauthorized):
            self.document.restrictedTraverse("@@prevent-actions")
