# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.Five.browser import BrowserView
from plone import api
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import noLongerProvides

from collective.preventdelete import _

from collective.preventdelete.interfaces import IPreventDeleteActivated
from collective.preventdelete.browser.interfaces import IPreventDeleteActivationView


class PreventDeleteActivationView(BrowserView):
    """
    PreventDelete activation helper view
    """
    implements(IPreventDeleteActivationView)

    def _redirect(self, msg=''):
        if self.request:
            if msg:
                api.portal.show_message(message=msg,
                                        request=self.request,
                                        type='info')
            self.request.response.redirect(self.context.absolute_url())
        return msg

    def _get_real_context(self):
        context = self.context
        plone_view = getMultiAdapter((context, self.request), name="plone")
        if plone_view.isDefaultPageInFolder():
            context = aq_parent(context)
        context = aq_inner(context)
        return context

    @property
    def is_enabled(self):
        context = self._get_real_context()
        if IPreventDeleteActivated.providedBy(context):
            return True
        return False

    @property
    def can_enable_not_delete_object(self):
        return not self.is_enabled

    @property
    def can_disable_not_delete_object(self):
        context = self._get_real_context()
        return(IPreventDeleteActivated.providedBy(context))

    def enable_not_delete_object(self):
        """ Enable the PreventDelete """
        context = self._get_real_context()
        portal_type = context.portal_type
        alsoProvides(context, IPreventDeleteActivated)
        catalog = api.portal.get_tool('portal_catalog')
        catalog.reindexObject(context)
        msg = _(u'This object is no more deleteable')
        msg += (': {}'.format(portal_type))
        self._redirect(msg)

    def disable_not_delete_object(self):
        """ Disable the PreventDelete """
        context = self._get_real_context()
        portal_type = context.portal_type
        noLongerProvides(context, IPreventDeleteActivated)
        catalog = api.portal.get_tool('portal_catalog')
        catalog.reindexObject(context)
        msg = _(u'This object is now deleteable')
        msg += (': {}'.format(portal_type))
        self._redirect(msg)
