from plone.i18n.locales.interfaces import IContentLanguageAvailability
from plone.app.i18n.locales.browser.interfaces import ILanguageSelector

from zope.interface import implements
from zope.component import queryUtility

from Products.CMFPlone import utils

class ContentLanguageSelector(utils.BrowserView):

    implements(ILanguageSelector)

    def __init__(self, context, request):
        super(LanguageSelector, self).__init__(context, request)
        self.util = queryUtility(IContentLanguageAvailability)

    def languages(self):
        """Returns list of languages."""
        languages = self.util.getLanguages()

        new_langs = []
        for lang in languages:
            if lang in self.util.getSupportedLanguages():
                languages[lang]['selected'] = True
            else:
                languages[lang]['selected'] = False
            # add language-code to dict
            langs[lang][u'code'] = lang
            # flatten outer dict to list to make it sortable
            new_langs.append(langs[lang])
        
        new_langs.sort(lambda x, y: cmp(x.get(u'native', x.get(u'name')), y.get(u'native', y.get(u'name'))))
        return new_langs

    def defaultLanguages(self):
        """Returns list of possible and selected default languages."""
        languages = self.util.getSupportedLanguages()
        for lang in languages:
            if lang == self.util.getDefaultLanguage():
                languages[lang]['selected'] = True
            else:
                languages[lang]['selected'] = False
        return languages

    def showFlags(self):
        """Indicates if flags should be used."""
        return self.util.showFlags()

    def useCombined(self):
        """Indicates if combined language codes should be used."""
        return self.util.useCombined()
