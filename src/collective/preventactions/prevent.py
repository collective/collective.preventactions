# -*- coding: utf-8 -*-
from collective.preventactions import _
from collective.preventactions.interfaces import IPreventDelete
from collective.preventactions.interfaces import IPreventMoveOrRename
from OFS.interfaces import IItem
from OFS.interfaces import IObjectWillBeMovedEvent
from OFS.interfaces import IObjectWillBeRemovedEvent
from plone.app.linkintegrity.interfaces import ILinkIntegrityInfo
from plone.app.linkintegrity.exceptions import LinkIntegrityNotificationException
from plone import api
from zope.component import adapter

import logging
import zExceptions
logger = logging.getLogger("collective.preventactions.prevent")


@adapter(IItem, IObjectWillBeMovedEvent)
def deleteObject(obj, event):
    request = getattr(obj, 'REQUEST', None)
    info = ILinkIntegrityInfo(request)
    if info.integrityCheckingEnabled():
        pass
    # import ipdb; ipdb.set_trace()
    if IPreventDelete.providedBy(obj):
        msg = _(u"You can not delete this object")
        logger.info(msg)
        api.portal.show_message(
            message=msg,
            request=request,
            type="info"
        )
        request.response.redirect(obj.absolute_url())
        raise LinkIntegrityNotificationException(obj)
        return False
        # raise zExceptions.Redirect(obj.absolute_url())


@adapter(IItem, IObjectWillBeRemovedEvent)
def moveOrRenameObject(obj, event):
    request = getattr(obj, 'REQUEST', None)
    # info = ILinkIntegrityInfo(request)
    # if info.integrityCheckingEnabled():
    #     pass

    # If it's a object deleted: do nothing, IObjectWillBeRemovedEvent is fire
    if getattr(event, 'newName', None) is None:
        # request.response.redirect(obj.absolute_url())
        return
    else:
        if IPreventMoveOrRename.providedBy(obj):
            msg = _(u"You can not move or rename this object")
            logger.info(msg)
            api.portal.show_message(
                message=msg,
                request=request,
                type="info"
            )
            request.response.redirect(obj.absolute_url())
