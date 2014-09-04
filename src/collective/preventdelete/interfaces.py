# -*- coding: utf-8 -*-
from zope.interface import Interface


class ICollectivePreventdeleteLayer(Interface):
    """Marker interface that defines a Zope 3 browser layer."""


class IPreventDeleteActivated(Interface):
    """Marker interface to enable / disable deleteable object"""
