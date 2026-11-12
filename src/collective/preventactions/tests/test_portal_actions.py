"""The portal actions the toolbar shows, as changed by the default profile."""

from collective.preventactions.interfaces import ICollectivePreventActionsLayer
from collective.preventactions.interfaces import IPreventDelete
from collective.preventactions.interfaces import IPreventMoveOrRename
from collective.preventactions.testing import COLLECTIVE_PREVENTACTIONS_INTEGRATION
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface import alsoProvides

import unittest


class TestPortalActions(unittest.TestCase):
    layer = COLLECTIVE_PREVENTACTIONS_INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        alsoProvides(self.request, ICollectivePreventActionsLayer)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.document = api.content.create(
            container=self.portal, type="Document", id="document"
        )

    def action_ids(self, obj, category):
        # plone_context_state memoizes actions per request: call once per test.
        context_state = getMultiAdapter((obj, self.request), name="plone_context_state")
        return {action["id"] for action in context_state.actions(category)}

    def test_unprotected_document(self):
        actions = self.action_ids(self.document, "object_buttons")
        self.assertLessEqual({"cut", "delete", "rename"}, actions)

    def test_prevent_delete_hides_delete(self):
        alsoProvides(self.document, IPreventDelete)
        actions = self.action_ids(self.document, "object_buttons")
        self.assertNotIn("delete", actions)
        self.assertLessEqual({"cut", "rename"}, actions)

    def test_prevent_move_or_rename_hides_cut_and_rename(self):
        alsoProvides(self.document, IPreventMoveOrRename)
        actions = self.action_ids(self.document, "object_buttons")
        self.assertNotIn("cut", actions)
        self.assertNotIn("rename", actions)
        self.assertIn("delete", actions)

    def test_prevents_action_on_type_with_behavior(self):
        # The testing profile enables the behavior on Document only.
        self.assertIn("prevents", self.action_ids(self.document, "object"))

    def test_prevents_action_not_on_type_without_behavior(self):
        folder = api.content.create(container=self.portal, type="Folder", id="folder")
        self.assertNotIn("prevents", self.action_ids(folder, "object"))
