from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.viewlet.interfaces import IViewlet


@implementer(IViewlet)
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
    ...     supported_langs = ['de', 'en', 'ar']
    ...     always_show_selector = False
    ...
    ...     def __init__(self, **kw):
    ...         self.__dict__.update(kw)
    ...         self.showFlags = True
    ...
    ...     def getSupportedLanguages(self):
    ...         return self.supported_langs
    ...
    ...     def getAvailableLanguageInformation(self):
    ...         return dict(en={'selected' : True}, de={'selected' : False},
    ...                     nl={'selected' : True}, ar={'selected': True})
    ...
    ...     def getLanguageBindings(self, request):
    ...         # en = selected by user, nl = default, [] = other options
    ...         return ('en', 'nl', [])
    ...
    ...     def showSelector(self):
    ...         return bool(self.use_cookie_negotiation or self.always_show_selector)

    >>> ls.tool = Tool()
    >>> ls.available()
    False

    >>> ls.tool = Tool(use_cookie_negotiation=True)
    >>> ls.available()
    True

    >>> result = [{'code': 'en', 'selected': True}, {'code': 'ar', 'selected': False},
    ...           {'code': 'nl', 'selected': False}]
    >>> ls.languages() == result
    True

    >>> ls.showFlags()
    True

    >>> ls.tool = Tool(use_cookie_negotiation=True)
    >>> ls.available()
    True

    >>> ls.tool = Tool(always_show_selector=True)
    >>> ls.available()
    True

    >>> from zope.interface import implementer
    >>> from OFS.interfaces import IItem
    >>> @implementer(IItem)
    ... class Dummy(object):
    ...     def getPortalObject(self):
    ...         return self
    ...     def absolute_url(self):
    ...         return 'absolute url'

    >>> context = Dummy()
    >>> context.portal_url = Dummy()
    >>> ls = LanguageSelector(context, dict(), None, None)
    >>> ls.portal_url()
    'absolute url'
    """

    def __init__(self, context, request, view, manager):
        super().__init__(context, request)
        self.view = view
        self.manager = manager

    def update(self):
        self.tool = getToolByName(self.context, "portal_languages", None)

    def available(self) -> bool:
        if self.tool is None:
            return False
        selector = self.tool.showSelector()
        languages = len(self.tool.getSupportedLanguages()) > 1
        return selector and languages

    def portal_url(self):
        portal_tool = getToolByName(self.context, "portal_url", None)
        if portal_tool is not None:
            return portal_tool.getPortalObject().absolute_url()
        return None

    def languages(self):
        """Returns list of languages."""
        if self.tool is None:
            return []

        bound = self.tool.getLanguageBindings(self.request)
        current = bound[0]

        def merge(lang, info):
            info["code"] = lang
            info["selected"] = lang == current
            return info

        languages = [
            merge(lang, info)
            for (lang, info) in self.tool.getAvailableLanguageInformation().items()
            if info["selected"]
        ]

        # sort supported languages by index in portal_languages tool
        supported_langs = self.tool.getSupportedLanguages()

        def index(info):
            try:
                return supported_langs.index(info["code"])
            except ValueError:
                return len(supported_langs)

        return sorted(languages, key=index)

    def showFlags(self):
        """Do we use flags?."""
        if self.tool is None:
            return False
        return self.tool.showFlags
