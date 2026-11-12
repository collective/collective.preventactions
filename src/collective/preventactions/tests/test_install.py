from collective.preventactions.interfaces import ICollectivePreventActionsLayer
from collective.preventactions.interfaces import IPreventDelete
from collective.preventactions.interfaces import IPreventMoveOrRename
from collective.preventactions.testing import COLLECTIVE_PREVENTACTIONS_INTEGRATION
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.base.interfaces import INonInstallable
from plone.base.utils import get_installer
from plone.browserlayer.utils import registered_layers
from zope.component import getAllUtilitiesRegisteredFor
from zope.interface import alsoProvides

import unittest

PACKAGE = "collective.preventactions"


class TestSetup(unittest.TestCase):
    layer = COLLECTIVE_PREVENTACTIONS_INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        self.assertTrue(self.installer.is_product_installed(PACKAGE))

    def test_browserlayer_installed(self):
        self.assertIn(ICollectivePreventActionsLayer, registered_layers())

    def test_uninstall_profile_hidden(self):
        hidden = [
            profile
            for utility in getAllUtilitiesRegisteredFor(INonInstallable)
            for profile in utility.getNonInstallableProfiles()
        ]
        self.assertIn(f"{PACKAGE}:uninstall", hidden)


class TestUninstall(unittest.TestCase):
    layer = COLLECTIVE_PREVENTACTIONS_INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.document = api.content.create(
            container=self.portal, type="Document", id="document"
        )
        self.document2 = api.content.create(
            container=self.portal, type="Document", id="document2"
        )
        alsoProvides(self.document, IPreventDelete)
        alsoProvides(self.document2, IPreventDelete, IPreventMoveOrRename)
        self.document.reindexObject()
        self.document2.reindexObject()

        self.installer = get_installer(self.portal, self.layer["request"])
        self.installer.uninstall_product(PACKAGE)

    def test_product_uninstalled(self):
        self.assertFalse(self.installer.is_product_installed(PACKAGE))

    def test_browserlayer_removed(self):
        self.assertNotIn(ICollectivePreventActionsLayer, registered_layers())

    def test_markers_removed(self):
        for obj in (self.document, self.document2):
            self.assertFalse(IPreventDelete.providedBy(obj))
            self.assertFalse(IPreventMoveOrRename.providedBy(obj))
        for iface in (IPreventDelete, IPreventMoveOrRename):
            brains = api.content.find(object_provides=iface.__identifier__)
            self.assertEqual(len(brains), 0)

    def test_object_buttons_restored(self):
        object_buttons = self.portal.portal_actions.object_buttons
        self.assertNotIn(
            "is_deletable", object_buttons.delete.getProperty("available_expr")
        )
        for name in ("cut", "rename"):
            self.assertNotIn(
                "is_moveable", object_buttons[name].getProperty("available_expr")
            )

    def test_prevents_action_removed(self):
        self.assertNotIn("prevents", self.portal.portal_actions.object.objectIds())
