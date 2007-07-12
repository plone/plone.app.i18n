import unittest

from zope.testing.doctest import DocTestSuite

from zope.interface import implements

from Testing import ZopeTestCase
from Testing.ZopeTestCase import ZopeDocFileSuite

from Products.PloneTestCase import ptc

from zope.annotation import IAttributeAnnotatable
from zope.publisher.browser import TestRequest as ZopeTestRequest
from zope.publisher.interfaces.http import IHTTPRequest
from zope.publisher.interfaces.browser import IBrowserRequest

class TestRequest(ZopeTestRequest):
    implements(IHTTPRequest, IAttributeAnnotatable, IBrowserRequest)

    def set(self, attribute, value):
        setattr(self, attribute, value)

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
