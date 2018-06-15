# -*- coding: UTF-8 -*-
from zope.component.testing import setUp, tearDown

import doctest
import re
import six
import unittest


class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if six.PY2:
            got = re.sub("u'(.*?)'", "'\\1'", got)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite(
            'plone.app.i18n.locales.browser.selector',
            setUp=setUp(),
            tearDown=tearDown,
            optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
            checker=Py23DocChecker(),
            )
        ))
