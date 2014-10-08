# -*- coding: utf-8 -*-
from plone.browserlayer.utils import registered_layers
from plone.app.testing import applyProfile
import unittest2 as unittest
from zope.event import notify
from zope.traversing.interfaces import BeforeTraverseEvent

from Products.CMFCore.utils import getToolByName

from collective.preventdelete.testing import COLLECTIVE_PREVENTDELETE_INTEGRATION
from collective.preventdelete.interfaces import  ICollectivePreventdeleteLayer

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import setRoles
from plone.app.testing import login


class TestInstall(unittest.TestCase):
    layer = COLLECTIVE_PREVENTDELETE_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        notify(BeforeTraverseEvent(self.portal, self.request))

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        qi_tool = getToolByName(self.portal, 'portal_quickinstaller')
        pid = 'collective.preventdelete'
        installed = [p['id'] for p in qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')

    def test_layer_installed(self):
        self.assertTrue(ICollectivePreventdeleteLayer in registered_layers())

    def test_uninstall_product(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Document', 'document')
        self.document = self.portal['document']
        view = self.document.restrictedTraverse('@@preventdelete_activation')
        view.enable_not_delete_object()
        self.assertTrue(view.is_enabled)

        applyProfile(self.portal, 'collective.preventdelete:uninstall')
        self.assertFalse(ICollectivePreventdeleteLayer in registered_layers())

        self.assertFalse(view.is_enabled)
