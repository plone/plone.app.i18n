from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from zope import component

from zope.app.i18n.interfaces import ILocalTranslationDomain

from utils import make_token

class LocalTranslationDomains(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        # local translation domains are local utilities
        tds = [td for name, td in component.getUtilitiesFor(ILocalTranslationDomain)]

        items = []

        for td in tds:
            domain = td.domain
            for language in td.getAvailableLanguages():
                value = make_token(domain, language)
                items.append(SimpleTerm(value, value, '%s (%s)' % (domain, language)))

        return SimpleVocabulary(items)

LocalTranslationDomains = LocalTranslationDomains()
