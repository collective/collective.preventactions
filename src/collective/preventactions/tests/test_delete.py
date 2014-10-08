# -*- coding: utf-8 -*-
import unittest2 as unittest
from collective.preventdelete.testing import (
    COLLECTIVE_PREVENTDELETE_INTEGRATION
)
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import setRoles
from plone.app.testing import login
from plone.dexterity.fti import DexterityFTI
from plone import api

class TestDelete(unittest.TestCase):
    layer = COLLECTIVE_PREVENTDELETE_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        fti = DexterityFTI('dexterity_object')
        self.portal.portal_types._setObject('dexterity_object', fti)
        fti.klass = 'plone.dexterity.content.DexterityContent'
        fti.behaviors = (
            'plone.app.dexterity.behaviors.metadata.IDublinCore',
        )
        self.fti = fti
        self.portal.invokeFactory('Document', 'document')
        self.document = self.portal['document']

    def test_document_delete(self):
        login(self.portal, TEST_USER_NAME)
        view = self.document.restrictedTraverse('@@preventdelete_activation')
        view.enable_not_delete_object()
        self.assertTrue(view.is_enabled)
        self.assertTrue('document' in self.portal.contentIds())
        api.content.delete(obj=self.portal['document'])
        self.assertTrue('document' in self.portal.contentIds())

    def test_dexterity_delete(self):
        view = self.document.restrictedTraverse('@@preventdelete_activation')
        view.enable_not_delete_object()
        self.assertTrue(view.is_enabled)

        view.disable_not_delete_object()
        self.assertFalse(view.is_enabled)
