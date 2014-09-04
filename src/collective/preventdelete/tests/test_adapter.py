# -*- coding: utf-8 -*-
import unittest2 as unittest
from collective.prenventdelete.testing import COLLECTIVE_PRENVENTDELETE_INTEGRATION


class TestAdapter(unittest.TestAdapter):
    layer = COLLECTIVE_PRENVENTDELETE_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_document_delete(self):
        pass
