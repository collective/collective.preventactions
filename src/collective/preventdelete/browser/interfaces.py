# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface
from collective.preventdelete import _


class IPreventDeleteActivationView(Interface):
    """ Prevent Delete activation """
    can_enable_not_delete_object = schema.Bool(
        _(u'Can not delete this object'),
        readonly=True
    )

    can_disable_not_delete_object = schema.Bool(
        _(u'Can delete this object'),
        readonly=True
    )

    def enable_not_delete_object():
        """ Enable not delete object
        """

    def disable_not_delete_object():
        """ Disable not delete object
        """
