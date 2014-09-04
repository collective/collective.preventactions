# -*- coding: utf-8 -*-
from OFS.interfaces import IItem
from zope.container.interfaces import IObjectRemovedEvent
from zope.component import adapter
from plone.app.linkintegrity.interfaces import ILinkIntegrityInfo


@adapter(IItem, IObjectRemovedEvent)
def deleteObject(obj, event):
    request = getattr(obj, 'REQUEST', None)
    info = ILinkIntegrityInfo(request)
    if info.integrityCheckingEnabled():
        pass
