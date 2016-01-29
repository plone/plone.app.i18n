# -*- coding: UTF-8 -*-

import unittest

from zope.component.testing import setUp, tearDown
import doctest


def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite('plone.app.i18n.locales.browser.selector',
                     setUp=setUp(),
                     tearDown=tearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        ))
