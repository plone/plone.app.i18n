from Products.CMFCore.utils import ToolInit
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.GenericSetup import EXTENSION, profile_registry

from plone.app.i18n.locales.countries import Countries
from plone.app.i18n.locales.languages import ContentLanguages
from plone.app.i18n.locales.languages import MetadataLanguages

tools = (Countries, ContentLanguages, MetadataLanguages)

def initialize(context):
    """Intializer called when used as a Zope 2 product."""

    ToolInit('plone.app.i18n',
             tools=tools,
             icon='tool.gif',
    ).initialize(context)

# XXX this needs to move back into initialize, but right now this doesn't
# play nicely with the layered test setup, as the initialize method is
# called more than once, but has a side-effect that is not cleaned up by the
# CA cleanUp call
profile_registry.registerProfile('default',
        'plone.app.i18n default profile',
        'Extension profile including plone.app.i18n configuration.',
        'profiles/default',
        'plone.app.i18n',
        EXTENSION,
        for_=IPloneSiteRoot)
