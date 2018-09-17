# -*- coding: UTF-8 -*-
from plone.app.testing import PLONE_INTEGRATION_TESTING
from plone.testing import layered

import doctest
import re
import six
import unittest

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if six.PY2:
            got = re.sub("u'(.*?)'", "'\\1'", got)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite('plone.app.i18n.locales.countries'),
        doctest.DocTestSuite('plone.app.i18n.locales.languages'),
        layered(doctest.DocFileSuite('countries.txt',
            optionflags=OPTIONFLAGS,
            package='plone.app.i18n.locales.tests',
            checker=Py23DocChecker(),
            ), layer=PLONE_INTEGRATION_TESTING),
        layered(doctest.DocFileSuite('languages.txt',
            optionflags=OPTIONFLAGS,
            package='plone.app.i18n.locales.tests',
            checker=Py23DocChecker(),
            ), layer=PLONE_INTEGRATION_TESTING)
        ))
