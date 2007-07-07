from zope import component
from zope import interface
from zope.i18n.interfaces import ITranslationDomain
from zope.app.i18n.translationdomain import TranslationDomain
from zope.app.i18n.interfaces import ILocalTranslationDomain
from zope.i18n.testmessagecatalog import TestMessageCatalog
from zope.component import getSiteManager

from Products.PlacelessTranslationService import PlacelessTranslationService
from Products.PlacelessTranslationService.utility import PTSTranslationDomain
from Products.PlacelessTranslationService.interfaces import IPlacelessTranslationService
from Products.PlacelessTranslationService.GettextMessageCatalog import translationRegistry

from utils import match

def customize_translation(msgid, msg, domain, language):
    translationdomain = component.getUtility(ITranslationDomain, name=domain)

    # if this domain is not persistent, we're going to register a new
    # local translation domain
    if not ILocalTranslationDomain.providedBy(translationdomain):
        translationdomain = TranslationDomain()
        translationdomain.domain = domain
        sm = getSiteManager()
        sm.registerUtility(translationdomain, ITranslationDomain, name=domain)

    # lookup message catalog for this language
    translationdomain.addMessage(msgid, msg, language)


def query_message(query, language):
    result = []
    for name, util in component.getUtilitiesFor(ITranslationDomain):
        for message in IListMessages(util).filter(language):
            if match(message['msgstr'], query):
                result.append(message)
    return result

class IListMessages(interface.Interface):
    def filter(language):
        """Return list of messages filtered by language."""

    def __iter__(self):
        """
        Return list of messages formatted as dictionary entries:

        - mod_time
        - language
        - msgid
        - msgstr
        - domain

        """

class PTSTranslationDomainMessagesLister(object):
    interface.implements(IListMessages)
    component.adapts(PTSTranslationDomain)

    def __init__(self, td):
        self.td = td
        
    def __iter__(self):
        domain = self.td.domain
        mod_time = 0
        
        pts = component.getUtility(IPlacelessTranslationService)

        import sys
        _pts = sys.modules['Products.PlacelessTranslationService.PlacelessTranslationService']
        catalogRegistry = _pts.catalogRegistry
        
        for (ccode, cdomain), cnames in catalogRegistry.items():
            if cdomain != domain:
                continue

            for cname in cnames:
                catalog = pts._getOb(cname)
                for msgid, msgstr in translationRegistry[catalog.getId()]._catalog.items():
                    if msgid == '':
                        continue
                    yield dict(msgid=msgid,
                               msgstr=msgstr,
                               domain=self.td.domain,
                               language=ccode,
                               mod_time=mod_time)

    def filter(self, language):
        return (message for message in self
                if message['language'] == language)

class GlobalTranslationDomainMessagesLister(object):
    interface.implements(IListMessages)
    component.adapts(ITranslationDomain)
    
    def __init__(self, td):
        self.td = td

    def __iter__(self):
        for catalog in self.td._data.values():
            mod_time = 0
            if isinstance(catalog, TestMessageCatalog):
                continue
            for msgid, msgstr in catalog._catalog._catalog.items():
                if msgid == '':
                    continue
                yield dict(msgid=msgid,
                           msgstr=msgstr,
                           domain=self.td.domain,
                           language=catalog.language,
                           mod_time=mod_time)

    def filter(self, language):
        return (message for message in self
                if message['language'] == language)
    

class LocalTranslationDomainMessagesLister(object):
    interface.implements(IListMessages)
    component.adapts(ILocalTranslationDomain)

    def __init__(self, td):
        self.td = td

    def __iter__(self):
        return (message for message in self.td.getMessages())

    def filter(self, language):
        return (message for message in self
                if message['language'] == language)

