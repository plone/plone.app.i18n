import unittest
from Testing import ZopeTestCase
from Testing.ZopeTestCase import ZopeDocFileSuite
from Products.PloneTestCase import ptc

ZopeTestCase.installProduct('PloneTranslations')
ptc.setupPloneSite()

def test_suite():
    return unittest.TestSuite((
        ZopeDocFileSuite(
            'messages.txt',
            test_class=ptc.PloneTestCase,
            ),
        ))
