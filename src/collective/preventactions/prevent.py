# -*- coding: utf-8 -*-
from OFS.interfaces import IItem
from OFS.interfaces import IObjectWillBeRemovedEvent
from zope.component import adapter
from plone.app.linkintegrity.interfaces import ILinkIntegrityInfo
from collective.preventactions import _
from plone import api
import logging
logger = logging.getLogger("collective.preventactions.prevent")


@adapter(IItem, IObjectWillBeRemovedEvent)
def deleteObject(obj, event):
    request = getattr(obj, 'REQUEST', None)
    info = ILinkIntegrityInfo(request)
    if info.integrityCheckingEnabled():
        pass
    if True:
        msg = _(u"You can not delete this object")
        logger.info(msg)
        api.portal.show_message(
            message=msg,
            request=request,
            type="info"
        )
        request.response.redirect(obj.absolute_url())
