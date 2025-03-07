#!/bin/bash

locales_directory=src/collective/preventactions/locales

domain=collective.preventactions
bin/i18ndude rebuild-pot --exclude profiles.zcml --pot $locales_directory/$domain.pot --create $domain .
bin/i18ndude sync --pot $locales_directory/$domain.pot $locales_directory/*/LC_MESSAGES/$domain.po