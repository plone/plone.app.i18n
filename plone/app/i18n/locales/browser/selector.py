from zope.interface import implements
from zope.viewlet.interfaces import IViewlet

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile


class LanguageSelector(BrowserView):
    """Language selector.

      >>> ls = LanguageSelector(None, dict(), None, None)
      >>> ls
      <plone.app.i18n.locales.browser.selector.LanguageSelector object at ...>

      >>> ls.update()
      >>> ls.available()
      False
      >>> ls.languages()
      []
      >>> ls.showFlags()
      False

      >>> class Tool(object):
      ...     use_cookie_negotiation = False
      ...
      ...     def __init__(self, **kw):
      ...         self.__dict__.update(kw)
      ...
      ...     def showFlags(self):
      ...         return True
      ...
      ...     def getAvailableLanguageInformation(self):
      ...         return dict(en={'selected' : True}, de={'selected' : False},
      ...                     nl={'selected' : True})
      ...
      ...     def getLanguageBindings(self):
      ...         # en = selected by user, nl = default, [] = other options
      ...         return ('en', 'nl', [])

      >>> ls.tool = Tool()
      >>> ls.available()
      False

      >>> ls.tool = Tool(use_cookie_negotiation=True)
      >>> ls.available()
      True
      >>> ls.languages()
      [{'code': 'nl', 'selected': False}, {'code': 'en', 'selected': True}]
      >>> ls.showFlags()
      True

      >>> class NewTool(Tool):
      ...     always_show_selector = False
      ...
      ...     def showSelector(self):
      ...         return bool(self.use_cookie_negotiation or self.always_show_selector)

      >>> ls.tool = NewTool()
      >>> ls.available()
      False

      >>> ls.tool = NewTool(use_cookie_negotiation=True)
      >>> ls.available()
      True

      >>> ls.tool = NewTool(always_show_selector=True)
      >>> ls.available()
      True

      >>> class Dummy(object):
      ...     def getPortalObject(self):
      ...         return self
      ...
      ...     def absolute_url(self):
      ...         return 'absolute url'

      >>> context = Dummy()
      >>> context.portal_url = Dummy()
      >>> ls = LanguageSelector(context, dict(), None, None)
      >>> ls.portal_url
      'absolute url'
    """
    implements(IViewlet)

    render = ZopeTwoPageTemplateFile('languageselector.pt')

    def __init__(self, context, request, view, manager):
        super(LanguageSelector, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.tool = getToolByName(context, 'portal_languages', None)
        portal_tool = getToolByName(context, 'portal_url', None)
        self.portal_url = None
        if portal_tool is not None:
            self.portal_url = portal_tool.getPortalObject().absolute_url()

    def update(self):
        pass

    def available(self):
        if self.tool is not None:
            # Ask the language tool. Using getattr here for BBB with older
            # versions of the tool.
            showSelector = getattr(aq_base(self.tool), 'showSelector', None)
            if showSelector is not None:
                return self.tool.showSelector() # Call with aq context
            # BBB
            return bool(self.tool.use_cookie_negotiation)
        return False

    def languages(self):
        """Returns list of languages."""
        if self.tool is None:
            return []

        bound = self.tool.getLanguageBindings()
        current = bound[0]

        def merge(lang, info):
            info["code"]=lang
            if lang == current:
                info['selected'] = True
            else:
                info['selected'] = False
            return info

        return [merge(lang, info) for (lang,info) in
                    self.tool.getAvailableLanguageInformation().items()
                    if info["selected"]]

    def showFlags(self):
        """Do we use flags?."""
        if self.tool is not None:
            return self.tool.showFlags()
        return False
