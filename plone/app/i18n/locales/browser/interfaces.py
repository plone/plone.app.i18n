from zope.interface import Interface, Attribute

class ILanguageSelector(Interface):
    """ """

    def languages():
        """Returns list of languages."""

    def defaultLanguages():
        """Returns list of possible and selected default languages."""

    def showFlags():
        """Indicates if flags should be used."""

    def useCombined():
        """Indicates if combined language codes should be used."""
