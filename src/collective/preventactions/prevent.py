# -*- coding: utf-8 -*-
from collective.preventactions import _
from collective.preventactions.interfaces import IPreventDelete
from collective.preventactions.interfaces import IPreventMoveOrRename
from OFS.interfaces import IItem
from OFS.interfaces import IObjectWillBeMovedEvent
from OFS.interfaces import IObjectWillBeRemovedEvent
from OFS.ObjectManager import BeforeDeleteException
from plone import api
from zope.component import adapter

import logging
logger = logging.getLogger('collective.preventactions.prevent')


@adapter(IItem, IObjectWillBeMovedEvent)
def deleteObject(obj, event):

    if IPreventDelete.providedBy(obj):
        msg = _(u'You can not delete this object')
        logger.info(msg)
        raise BeforeDeleteException()


@adapter(IItem, IObjectWillBeRemovedEvent)
def moveOrRenameObject(obj, event):
    request = getattr(obj, 'REQUEST', None)
    if IPreventMoveOrRename.providedBy(obj) \
            and not IPreventDelete.providedBy(obj):
        msg = _(u'You can not move or rename this object')
        # logger.info(msg)
        api.portal.show_message(
            message=msg,
            request=request,
            type='info'
        )
        request.response.redirect(obj.absolute_url())
        raise Exception(msg)
