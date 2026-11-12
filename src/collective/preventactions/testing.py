# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer

import collective.preventactions


COLLECTIVE_PREVENTACTIONS = PloneWithPackageLayer(
    zcml_package=collective.preventactions,
    zcml_filename="testing.zcml",
    gs_profile_id="collective.preventactions:testing",
    name="COLLECTIVE_PREVENTACTIONS",
)

COLLECTIVE_PREVENTACTIONS_INTEGRATION = IntegrationTesting(
    bases=(COLLECTIVE_PREVENTACTIONS,), name="COLLECTIVE_PREVENTACTIONS_INTEGRATION"
)

COLLECTIVE_PREVENTACTIONS_FUNCTIONAL = FunctionalTesting(
    bases=(COLLECTIVE_PREVENTACTIONS,), name="COLLECTIVE_PREVENTACTIONS_FUNCTIONAL"
)
