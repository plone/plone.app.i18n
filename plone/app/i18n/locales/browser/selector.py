from zope.interface import implements
from zope.viewlet.interfaces import IViewlet

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile


class LanguageSelector(BrowserView):
    """Language selector.
    """
    implements(IViewlet)

    render = ZopeTwoPageTemplateFile('languageselector.pt')

    def __init__(self, context, request, view, manager):
        super(BrowserView, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.tool = getToolByName(context, 'portal_languages', None)
        portal_tool = getToolByName(context, 'portal_url')
        self.portal_url = portal_tool.getPortalObject().absolute_url()

    def update(self):
        pass

    def available(self):
        if self.tool.use_cookie_negotiation:
            return True
        return False

    def languages(self):
        """Returns list of languages."""
        if self.tool is None:
            return []

        bound = self.tool.getLanguageBindings()
        current = bound[0]

        supported = self.tool.getSupportedLanguages()
        languages = []
        for lang in supported:
            data = {}
            data['code'] = lang
            if lang == current:
                data['selected'] = True
            else:
                data['selected'] = False
            data['flag'] = self.tool.getFlagForLanguageCode(lang)
            data['name'] = self.tool.getNameForLanguageCode(lang)
            languages.append(data)

        return languages

    def showFlags(self):
        """Do we use flags?."""
        if self.tool is not None:
            return self.tool.showFlags()
        return False
