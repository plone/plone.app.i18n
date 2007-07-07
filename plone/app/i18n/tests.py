import unittest
from zope.testing.doctest import DocTestSuite

from Testing import ZopeTestCase
from Testing.ZopeTestCase import ZopeDocFileSuite
from Products.PloneTestCase import ptc

ZopeTestCase.installProduct('PloneTranslations')
ZopeTestCase.installProduct('PlacelessTranslationService')
ptc.setupPloneSite()

def test_suite():
    return unittest.TestSuite((
        ZopeDocFileSuite(
            'messages.txt',
            test_class=ptc.PloneTestCase,
            ),
        DocTestSuite(
            'plone.app.i18n.utils'
            ),
        ))
