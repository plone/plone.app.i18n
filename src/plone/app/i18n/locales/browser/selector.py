import zope.deferredimport

zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.viewlets.languageselector import LanguageSelectorViewlet instead.",
    LanguageSelector="plone.app.layout.viewlets.common:LanguageSelectorViewlet",
)
