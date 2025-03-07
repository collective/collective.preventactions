# -*- coding: utf-8 -*-
from collective.preventactions.behaviors.prevent_actions import IPreventActionsMarker
from collective.preventactions.testing import COLLECTIVE_PREVENTACTIONS_INTEGRATION
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class PreventActionsIntegrationTest(unittest.TestCase):
    layer = COLLECTIVE_PREVENTACTIONS_INTEGRATION

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Document", "document")
        api.content.create(self.portal, "Folder", "folder")

    def test_prevent_actions_testing_profile(self):
        self.assertTrue(IPreventActionsMarker.providedBy(self.portal["document"]))
        self.assertFalse(IPreventActionsMarker.providedBy(self.portal["folder"]))
