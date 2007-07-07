from zope.component import getUtility
from zope.i18n.interfaces import ITranslationDomain
from zope.app.i18n.translationdomain import TranslationDomain
from zope.app.i18n.interfaces import ILocalTranslationDomain

from zope.component import getSiteManager

def customize_translation(msgid, msg, domain, language):
    translationdomain = getUtility(ITranslationDomain, name=domain)

    # if this domain is not persistent, we're going to register a new
    # local translation domain
    if not ILocalTranslationDomain.providedBy(translationdomain):
        translationdomain = TranslationDomain()
        translationdomain.domain = domain
        sm = getSiteManager()
        sm.registerUtility(translationdomain, ITranslationDomain, name=domain)

    # lookup message catalog for this language
    translationdomain.addMessage(msgid, msg, language)
