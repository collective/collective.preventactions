from collective.preventactions.interfaces import ICollectivePreventActionsLayer
from collective.preventactions.interfaces import IPreventDelete
from collective.preventactions.interfaces import IPreventMoveOrRename
from collective.preventactions.testing import COLLECTIVE_PREVENTACTIONS_INTEGRATION
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.interface import alsoProvides

import unittest


class TestViews(unittest.TestCase):
    layer = COLLECTIVE_PREVENTACTIONS_INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        alsoProvides(self.layer["request"], ICollectivePreventActionsLayer)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.document = api.content.create(
            container=self.portal, type="Document", id="document"
        )

    def test_is_deletable_view(self):
        self.assertTrue(self.document.restrictedTraverse("is_deletable")())
        alsoProvides(self.document, IPreventDelete)
        self.assertFalse(self.document.restrictedTraverse("is_deletable")())

    def test_is_moveable_view(self):
        self.assertTrue(self.document.restrictedTraverse("is_moveable")())
        alsoProvides(self.document, IPreventMoveOrRename)
        self.assertFalse(self.document.restrictedTraverse("is_moveable")())
