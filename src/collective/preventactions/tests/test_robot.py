# -*- coding: utf-8 -*-
from plone.testing import layered
import unittest
import robotsuite

from collective.preventdelete.testing import COLLECTIVE_PREVENTDELETE_ROBOT_TESTING


def test_suite():
    suite = unittest.TestSuite()
    robots_file = [
                'example.robot',
            ]

    for robot_file in robots_file:
        rts = robotsuite.RobotTestSuite(robot_file)
        suite.addTests([
            layered(rts,  layer=COLLECTIVE_PREVENTDELETE_ROBOT_TESTING)
        ])
    return suite