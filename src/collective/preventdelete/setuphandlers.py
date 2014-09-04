# -*- coding: utf-8 -*-
from zope.interface import noLongerProvides
from Products.CMFCore.utils import getToolByName


def testSetup(context):
    if context.readDataFile('collective.preventdelete.txt') is None:
        return


def uninstallPreventDelete(context):
    if context.readDataFile('collective.preventdelete-uninstall.txt') is None:
        return
    portal = context.getSite()
    unregisterProvidesInterfaces(portal)


def unregisterProvidesInterfaces(portal):
    from collective.preventdelete.interfaces import IPreventDeleteActivate
    interfaces = IPreventDeleteActivate
    for interface in interfaces:
        catalog = getToolByName(portal, 'portal_catalog')
        brains = catalog({"object_provides": interface.__identifier__})
        for brain in brains:
            obj = brain.getObject()
            noLongerProvides(obj, interface)
            obj.reindexObject()
