from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.GenericSetup import EXTENSION, profile_registry

def initialize(context):
    """Intializer called when used as a Zope 2 product."""

    profile_registry.registerProfile('default',
        'plone.app.i18n default profile',
        'Extension profile including plone.app.i18n configuration.',
        'profiles/default',
        'plone.app.i18n',
        EXTENSION,
        for_=IPloneSiteRoot)
