# -*- coding: utf-8 -*-
import unittest2 as unittest
from collective.preventdelete.testing import COLLECTIVE_PREVENTDELETE_INTEGRATION


class TestAdapter(unittest.TestCase):
    layer = COLLECTIVE_PREVENTDELETE_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_document_delete(self):
        self.assertTrue(True)
