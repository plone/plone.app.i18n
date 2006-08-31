#
# PAITestCase
#

from Products.PloneTestCase.ptc import *

from zope.app.component.hooks import setSite, clearSite, setHooks

installProduct('GSLocalAddons')
setupPloneSite(
    extension_profiles=['Products.GSLocalAddons:default',
                        'plone.app.i18n:default'])

class PAITestCase(PloneTestCase):

    def afterSetUp(self):
        setHooks()
        setSite(self.portal)

    def beforeTearDown(self):
        clearSite()

class FunctionalTestCase(Functional, PAITestCase):
    """This is a stub.
    """
