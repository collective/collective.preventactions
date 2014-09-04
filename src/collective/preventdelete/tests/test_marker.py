# -*- coding: utf-8 -*-
import unittest2 as unittest
from collective.prenventdelete.testing import COLLECTIVE_PRENVENTDELETE_INTEGRATION


class TestMarker(unittest.TestAdapter):
    layer = COLLECTIVE_PRENVENTDELETE_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_active_marker(self):
        pass

    def test_unactive_marker(self):
        pass
