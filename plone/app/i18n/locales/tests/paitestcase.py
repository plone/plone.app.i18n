#
# PAITestCase
#

from Products.PloneTestCase.ptc import *

from zope.app.component.hooks import setSite, clearSite, setHooks

installProduct('GSLocalAddons')
setupPloneSite(
    extension_profiles=['Products.GSLocalAddons:default'])

site_dependent_extension_profiles=['plone.app.i18n:default']

class PAITestCase(PloneTestCase):

    def afterSetUp(self):
        setHooks()
        setSite(self.portal)
        # We need the site to be set during the application of this profile.
        # As this has to happen after the site object itself is created,
        # there's no way to do this easily in PloneTestCase, as it creates
        # and applies extension profiles in the same external method call.
        setup_tool = self.portal.portal_setup
        current_context = setup_tool.getImportContextID()
        for extension in site_dependent_extension_profiles:
            setup_tool.setImportContext('profile-%s' % extension)
            setup_tool.runAllImportSteps()
        # Restore import context again
        setup_tool.setImportContext(current_context)

    def beforeTearDown(self):
        clearSite()

class FunctionalTestCase(Functional, PAITestCase):
    """This is a stub.
    """
