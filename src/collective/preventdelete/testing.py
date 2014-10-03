# -*- coding: utf-8 -*-
from plone.testing import z2
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

import collective.preventdelete


COLLECTIVE_PREVENTDELETE = PloneWithPackageLayer(
    zcml_package=collective.preventdelete,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.preventdelete:testing',
    name='COLLECTIVE_PREVENTDELETE'
)

COLLECTIVE_PREVENTDELETE_INTEGRATION = IntegrationTesting(
    bases=(COLLECTIVE_PREVENTDELETE, ),
    name="COLLECTIVE_PREVENTDELETE_INTEGRATION"
)

COLLECTIVE_PREVENTDELETE_FUNCTIONAL = FunctionalTesting(
    bases=(COLLECTIVE_PREVENTDELETE, ),
    name="COLLECTIVE_PREVENTDELETE_FUNCTIONAL"
)

COLLECTIVE_PREVENTDELETE_ROBOT_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_PREVENTDELETE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name="COLLECTIVE_PREVENTDELETE_ROBOT_TESTING"
)
