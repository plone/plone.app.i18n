# -*- coding: UTF-8 -*-

import unittest
import doctest

from plone.app.testing.bbb import PTC_FUNCTIONAL_TESTING
from plone.testing import layered

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite('plone.app.i18n.locales.countries'),
        doctest.DocTestSuite('plone.app.i18n.locales.languages'),
        layered(doctest.DocFileSuite('countries.txt',
            optionflags=OPTIONFLAGS,
            package='plone.app.i18n.locales.tests',
            ), layer=PTC_FUNCTIONAL_TESTING),
        layered(doctest.DocFileSuite('languages.txt',
            optionflags=OPTIONFLAGS,
            package='plone.app.i18n.locales.tests',
            ), layer=PTC_FUNCTIONAL_TESTING)
        ))
