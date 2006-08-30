# -*- coding: UTF-8 -*-
"""
    Country tests.
"""

import unittest
from Testing import ZopeTestCase

from Products.PloneTestCase import PloneTestCase
from Testing.ZopeTestCase import ZopeDocTestSuite

PloneTestCase.installProduct('GSLocalAddons')

PloneTestCase.setupPloneSite(
    extension_profiles=['Products.GSLocalAddons:default',
                        'plone.app.i18n:default'])

from plone.app.i18n.locales.interfaces import ICountries
from zope.testing import doctest
from zope.testing.doctestunit import DocTestSuite

def testAvailableCountries():
    """
      >>> from zope.app.component.hooks import setSite, clearSite, setHooks
      >>> setHooks()

      >>> setSite(self.portal)

      >>> from zope.component import queryUtility
      >>> from plone.app.i18n.locales.interfaces import ICountries

      >>> util = queryUtility(ICountries)
      >>> util
      <Countries at ...>

      >>> countrycodes = util.getAvailableCountries()
      >>> len(countrycodes)
      1

      >>> u'en' in countrycodes
      True

      >>> countries = util.getCountries()
      >>> len(countries)
      243

      >>> de = countries[u'de']
      >>> de[u'name']
      u'Germany'

      >>> de[u'flag']
      u'/@@/country-flags/de.gif'

      >>> clearSite()
    """

def test_suite():
    return unittest.TestSuite((
        DocTestSuite('plone.app.i18n.locales.countries'),
        ZopeDocTestSuite(
            test_class=PloneTestCase.FunctionalTestCase,
            optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
        ))

if __name__ == '__main__':
    unittest.main(defaultTest="test_suite")
