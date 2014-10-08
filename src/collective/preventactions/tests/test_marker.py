# -*- coding: utf-8 -*-
import unittest2 as unittest
from collective.preventdelete.testing import (
    COLLECTIVE_PREVENTDELETE_INTEGRATION
)
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import setRoles
from plone.app.testing import login


class TestMarker(unittest.TestCase):
    layer = COLLECTIVE_PREVENTDELETE_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', 'document')
        self.document = self.portal['document']

    def test_enable_marker(self):
        login(self.portal, TEST_USER_NAME)
        view = self.document.restrictedTraverse('@@preventdelete_activation')
        view.enable_not_delete_object()
        self.assertTrue(view.is_enabled)

    def test_disable_marker(self):
        view = self.document.restrictedTraverse('@@preventdelete_activation')
        view.enable_not_delete_object()
        self.assertTrue(view.is_enabled)

        view.disable_not_delete_object()
        self.assertFalse(view.is_enabled)
