from Products.CMFCore.utils import ToolInit

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
