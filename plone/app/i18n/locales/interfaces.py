from plone.i18n.locales.interfaces import ICountryAvailability
from plone.i18n.locales.interfaces import IContentLanguageAvailability
from plone.i18n.locales.interfaces import IMetadataLanguageAvailability
from plone.i18n.locales.interfaces import IModifiableCountryAvailability
from plone.i18n.locales.interfaces import IModifiableLanguageAvailability
from zope.interface import Interface


class ICountries(ICountryAvailability, IModifiableCountryAvailability):
    """A modifiable list of countries."""

class IContentLanguages(IContentLanguageAvailability,
                        IModifiableLanguageAvailability):
    """A modifiable list of available content languages."""

class IMetadataLanguages(IMetadataLanguageAvailability,
                         IModifiableLanguageAvailability):
    """A modifiable list of available metadata languages."""

class ISelectorAdapter(Interface):
    """A marker interface for the selector viewlet"""

    def languages(self):
        """ Getting the list of languages available """

    def urlForLanguage(self, code):
        """ Getting the url for a language code """
