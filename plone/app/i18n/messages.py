from zope import component
from zope import interface

from zope.i18n.interfaces import ITranslationDomain
from zope.i18n import interpolate

from zope.app.i18n.translationdomain import TranslationDomain
from zope.app.i18n.interfaces import ILocalTranslationDomain

from zope.i18n.testmessagecatalog import TestMessageCatalog

from zope.component import getSiteManager

from Products.PlacelessTranslationService.utility import PTSTranslationDomain
from Products.PlacelessTranslationService.interfaces import IPlacelessTranslationService
from Products.PlacelessTranslationService.GettextMessageCatalog import translationRegistry

import sys
_pts = sys.modules['Products.PlacelessTranslationService.PlacelessTranslationService']
catalogRegistry = _pts.catalogRegistry

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot

from utils import match, make_token, normalize_language_token

query_accuracy_threshold = 0.8

from interfaces import ICustomizableTranslationsTool, IListMessages

class LocalTranslationDomainAdapter(object):
    component.adapts(IPloneSiteRoot)
    interface.implements(ICustomizableTranslationsTool)

    def __init__(self, portal):
        self.context = portal
        
    def addMessage(self, msgid, msg, domain, language):
        translationdomain = component.queryUtility(ILocalTranslationDomain, name=domain)
    
        # if this domain is not persistent, we're going to register a new
        # local translation domain
        if not translationdomain:
            sm = component.getSiteManager()
            translationdomain = TranslationDomain()
            translationdomain.domain = domain
            translationdomain.__parent__ = sm
            sm.registerUtility(translationdomain,
                               provided=ILocalTranslationDomain,
                               name=str(domain))
        
        # add message to td
        translationdomain.addMessage(msgid, msg, language)

        # work-around for bug in zope.app.i18n.translationdomain
        translationdomain[language].domain = domain

    def removeMessage(self, msgid, domain, language):
        translationdomain = component.getUtility(ILocalTranslationDomain, name=domain)
        
        translationdomain.deleteMessage(msgid, language)
    
    def queryMessage(self, query, language, include_global=True):
        tokens = []
        result = []

        # get translation domains, local first
        tds = [td for name, td in component.getUtilitiesFor(ILocalTranslationDomain)]

        if include_global:
            tds += list(component.getAllUtilitiesRegisteredFor(ITranslationDomain))

            # create PTS translation domain objects on the fly
            for cat in translationRegistry.values():
                info = cat.info()
                try:
                    td = PTSTranslationDomain(info['domain'])
                    tds.append(td)
                except KeyError:
                    # catalog record broken; ignore.
                    pass
                
        for util in tds:
            messages = IListMessages(util)
            messages.context = self.context
            for message in messages.filter(language):
                # keep track of domain/msgid combinations (tokens) already added
                token = make_token(message['domain'], message['msgid'])
                if token in tokens:
                    continue

                msg = message['msgid'] + " " + message['msgstr']

                accuracy = match(msg, query)
            
                if accuracy > query_accuracy_threshold:
                    if token not in tokens:
                        result.append(message)
                        tokens.append(token)

        return result

    def listMessages(self, domain, language):
        translationdomain = component.getUtility(ILocalTranslationDomain, name=domain)

        return IListMessages(translationdomain)

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

class MessagesLister(object):
    interface.implements(IListMessages)

    def __init__(self, td):
        self.td = td
        
    def filter(self, language):
        token = normalize_language_token(language)
        return (message for message in self if \
                normalize_language_token(message['language']) == token)

class PTSTranslationDomainMessagesLister(MessagesLister):
    component.adapts(PTSTranslationDomain)

    def __iter__(self):
        #portal = getToolByName(self.context, 'portal_url').getPortalObject()
        #pts = portal.aq_inner.aq_parent.Control_Panel.TranslationService
        pts = component.getUtility(IPlacelessTranslationService)
        
        for (ccode, cdomain), cnames in catalogRegistry.items():
            if cdomain != self.td.domain:
                continue

            for cname in cnames:
                catalog = pts._getOb(cname)
                yield ccode, translationRegistry[catalog.getId()]._catalog
            

    def filter(self, language):
        token = normalize_language_token(language)
        mod_time = 0

        for lang, catalog in self:
            if normalize_language_token(lang) != token: continue

            for msgid, msgstr in catalog.items():
                if msgid == '': continue

                yield dict(msgid=msgid,
                           msgstr=msgstr,
                           domain=self.td.domain,
                           language=language,
                           mod_time=mod_time)

class GlobalTranslationDomainMessagesLister(MessagesLister):
    component.adapts(ITranslationDomain)
    
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

class LocalTranslationDomainMessagesLister(MessagesLister):
    component.adapts(ILocalTranslationDomain)

    def __iter__(self):
        return (message for message in self.td.getMessages())

    
