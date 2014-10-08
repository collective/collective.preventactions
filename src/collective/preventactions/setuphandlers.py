# -*- coding: utf-8 -*-
from zope.interface import noLongerProvides
from Products.CMFCore.utils import getToolByName


def testSetup(context):
    if context.readDataFile('collective.preventactions.txt') is None:
        return


def uninstallPreventAction(context):
    if context.readDataFile('collective.preventactions-uninstall.txt') is None:
        return
    portal = context.getSite()
