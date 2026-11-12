from collective.preventactions.interfaces import IPreventDelete
from collective.preventactions.interfaces import IPreventMoveOrRename
from collective.preventactions.testing import COLLECTIVE_PREVENTACTIONS_INTEGRATION
from OFS.ObjectManager import BeforeDeleteException
from plone import api
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

import unittest

MOVE_REFUSED = "You can not move or rename this object"


class TestActions(unittest.TestCase):
    layer = COLLECTIVE_PREVENTACTIONS_INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        login(self.portal, TEST_USER_NAME)
        self.document = api.content.create(
            container=self.portal, type="Document", id="document"
        )
        self.folder = api.content.create(
            container=self.portal, type="Folder", id="folder"
        )

    def test_delete_document(self):
        alsoProvides(self.document, IPreventDelete)
        with self.assertRaises(BeforeDeleteException):
            api.content.delete(self.document)
        self.assertIn("document", self.portal.contentIds())

    def test_delete_unprotected_document(self):
        api.content.delete(self.document)
        self.assertNotIn("document", self.portal.contentIds())

    def test_delete_folder_containing_protected_document(self):
        inner = api.content.create(container=self.folder, type="Document", id="inner")
        alsoProvides(inner, IPreventDelete)
        with self.assertRaises(BeforeDeleteException):
            api.content.delete(self.folder)
        self.assertIn("folder", self.portal.contentIds())

    def test_move_document(self):
        alsoProvides(self.document, IPreventMoveOrRename)

        with self.assertRaisesRegex(Exception, MOVE_REFUSED):
            api.content.move(source=self.document, target=self.folder)
        with self.assertRaisesRegex(Exception, MOVE_REFUSED):
            api.content.rename(obj=self.document, new_id="changed-doc")
        self.assertEqual(self.document.absolute_url(), "http://nohost/plone/document")

        noLongerProvides(self.document, IPreventMoveOrRename)
        api.content.rename(obj=self.document, new_id="old-doc")
        self.assertEqual(self.document.getId(), "old-doc")

        alsoProvides(self.document, IPreventMoveOrRename)
        with self.assertRaisesRegex(Exception, MOVE_REFUSED):
            api.content.move(source=self.document, target=self.folder)
        with self.assertRaisesRegex(Exception, MOVE_REFUSED):
            api.content.rename(obj=self.document, new_id="changed-doc")
        self.assertEqual(self.document.absolute_url(), "http://nohost/plone/old-doc")

    def test_move_folder_containing_protected_document(self):
        inner = api.content.create(container=self.folder, type="Document", id="inner")
        alsoProvides(inner, IPreventMoveOrRename)
        target = api.content.create(container=self.portal, type="Folder", id="target")
        with self.assertRaisesRegex(Exception, MOVE_REFUSED):
            api.content.move(source=self.folder, target=target)
        self.assertIn("folder", self.portal.contentIds())

    def test_prevent_delete_does_not_prevent_move_or_rename(self):
        alsoProvides(self.document, IPreventDelete)
        api.content.rename(obj=self.document, new_id="renamed")
        api.content.move(source=self.document, target=self.folder)
        self.assertIn("renamed", self.folder.contentIds())

    def test_prevent_move_or_rename_does_not_prevent_delete(self):
        alsoProvides(self.document, IPreventMoveOrRename)
        api.content.delete(self.document)
        self.assertNotIn("document", self.portal.contentIds())

    def test_copy_delete_protected_document(self):
        alsoProvides(self.document, IPreventDelete)
        copy = api.content.copy(source=self.document, target=self.folder)
        self.assertIn("document", self.portal.contentIds())
        # The copy inherits the marker.
        self.assertTrue(IPreventDelete.providedBy(copy))

    def test_copy_move_protected_document_is_refused(self):
        # Current behaviour, not necessarily the wanted one: the copy inherits
        # the marker, and adding it fires an ObjectWillBeAddedEvent, which is an
        # IObjectWillBeMovedEvent with a new name.
        alsoProvides(self.document, IPreventMoveOrRename)
        with self.assertRaisesRegex(Exception, MOVE_REFUSED):
            api.content.copy(source=self.document, target=self.folder)
        self.assertNotIn("document", self.folder.contentIds())
