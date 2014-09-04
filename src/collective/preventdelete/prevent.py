# -*- coding: utf-8 -*-
from OFS.interfaces import IItem
from zope.container.interfaces import IObjectRemovedEvent
from zope.component import adapter
from plone.app.linkintegrity.interfaces import ILinkIntegrityInfo
from collective.preventdelete.interfaces import IPreventDeleteActivated
from collective.preventdelete import _
from plone import api


@adapter(IItem, IObjectRemovedEvent)
def deleteObject(obj, event):
    request = getattr(obj, 'REQUEST', None)
    info = ILinkIntegrityInfo(request)
    if info.integrityCheckingEnabled():
        pass
    if IPreventDeleteActivated.providedBy(obj):
        msg = _(u"You can not delete this object")
        api.portal.show_message(
            message=msg,
            request=request,
            type="info"
        )
        request.response.redirect(obj.absolute_url())
