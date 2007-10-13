from plone.fieldsets import FormFieldsets

from zope.interface import implements
from zope.interface import Interface
from zope.component import adapts

import zope.cachedescriptors.property

from zope.schema import TextLine
from zope.schema import Choice
from zope.schema import Bool

from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from zope.formlib import form

from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_unicode

from zope.app.form.browser import RadioWidget

from Products.CMFCore.utils import getToolByName

from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase

from plone.app.controlpanel.form import ControlPanelForm
from plone.app.form.widgets import LanguageDropdownChoiceWidget

from Acquisition import aq_inner

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from utils import make_token, split_token
from export import po_export
from interfaces import ICustomizableTranslationsTool

class SearchResultsWidget(RadioWidget):
    _displayItemForMissingValue = False
    
    def __init__(self, field, request):
        """Initialize the widget."""
        super(SearchResultsWidget, self).__init__(field,
            field.vocabulary, request)

class NonRequiredLanguageDropDownChoiceWidget(LanguageDropdownChoiceWidget):
    _displayItemForMissingValue = False
        
class ITranslationQuerySchema(Interface):
    language = Choice(title=_(u'Language'),
                      description=_(u'Choose language.'),
                      required=False,
                      vocabulary="plone.app.vocabularies.SupportedContentLanguages")

    query = TextLine(title=_(u'Query'),
                     description=_(u"Enter a search string to find translation messages. "
                                   "You can leave this field empty and retrieve all messages "
                                   "if you choose to query custom translations only."),
                     required=False,
                     default=u'')

    local_only = Bool(title=_(u'Custom translations only'),
                      required=False,
                      description=_(u'Search custom translation messages only.'))

class ITranslationQueryResultSchema(Interface):
    result = Choice(title=_(u'Search results'),
                    description=_(u"Select the message that best matches your query."),
                    vocabulary=SimpleVocabulary.fromItems([]),
                    required=False)

    translation = TextLine(title=_(u'Translation'),
                     description=_(u"Type in new translation."),
                     required=False,
                     default=u'')

class IManageTranslationsSchema(Interface):
    domain = Choice(title=_(u'Domains'),
                    description=_(u'Choose a local translation domain'),
                    required=False,
                    vocabulary="plone.app.i18n.vocabularies.LocalTranslationDomains")

class ITranslationsSchema(ITranslationQuerySchema,
                          ITranslationQueryResultSchema,
                          IManageTranslationsSchema):
    """Combined schema for the adapter lookup."""
    
class TranslationsControlPanelAdapter(SchemaAdapterBase):
    def __init__(self, context):
        super(TranslationsControlPanelAdapter, self).__init__(context)
        
    def get_language(self):
        ltool = getToolByName(self.context, 'portal_languages')
        return ltool.getDefaultLanguage()

    def set_language(self):
        pass

    query = ''
    translation = ''
    language = property(get_language,
                        set_language)    
    local_only = False
    domain = ''
    result = ''

managetranslationsset = FormFieldsets(IManageTranslationsSchema)

translationresultset = FormFieldsets(ITranslationQuerySchema,
                                     ITranslationQueryResultSchema)

translationqueryset = FormFieldsets(ITranslationQuerySchema)

def setup_form_fields(managetranslationset,
                      translationqueryset):
    # set up fieldsets
    managetranslationsset.id = 'managetranslationsset'
    managetranslationsset.label = _(u'Manage existing translations')
    translationqueryset.id = 'translationqueryset'
    translationqueryset.label = _(u'Add custom translation')

    # set up custom widgets
    try:
        translationqueryset['result'].custom_widget = SearchResultsWidget
    except:
        pass
    translationqueryset['language'].custom_widget = NonRequiredLanguageDropDownChoiceWidget

    return FormFieldsets(translationqueryset,
                         managetranslationsset)

class TranslationsControlPanel(ControlPanelForm):
    template = ZopeTwoPageTemplateFile('controlpanel.pt')

    form_fields = setup_form_fields(managetranslationsset,
                                    translationqueryset)
    
    label = _("Translations")
    description = _("Manage custom translations.")
    form_name = _("Translations")

    translationquery_actions = form.Actions()
    managetranslations_actions = form.Actions()
    
    show_search_results = False

    @zope.cachedescriptors.property.Lazy
    def actions(self):
        return list(self.managetranslations_actions)+list(self.translationquery_actions)

    @form.action(_(u'Save'), translationquery_actions)
    def handle_add(self, action, data):
        language = data['language']

        try:
            # we need to get these directly from the request
            token = self.request['form.result']
            translation = self.request['form.translation']
        except:
            # try running a query instead
            return self.handle_query.success(data)
            
        domain, msgid = split_token(token)

        # register translation
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        tool = ICustomizableTranslationsTool(portal)
        tool.addMessage(msgid, translation, domain, language)

        self.status = _(u'Translation customized.')
            
    handle_add.visible_condition = lambda form, action: form.show_search_results

    @form.action(_(u'Delete'), translationquery_actions)
    def handle_delete(self, action, data):
        language = data['language']

        try:
            # we need to get these directly from the request
            token = self.request['form.result']
            translation = self.request['form.translation']
        except:
            # try running a query instead
            return self.handle_query.success(data)
            
        domain, msgid = split_token(token)

        # remove message
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        tool = ICustomizableTranslationsTool(portal)
        tool.removeMessage(msgid, domain, language)

        self.status = _(u'Translation deleted.')

    handle_delete.visible_condition = lambda form, action: form.show_search_results

    @form.action(_(u'Search'), translationquery_actions)
    def handle_query(self, action, data):
        query = data['query']
        local_only = data['local_only']
        language = data['language']

        if local_only or query:
            portal = getToolByName(self.context, 'portal_url').getPortalObject()
            tool = ICustomizableTranslationsTool(portal)
                
            messages = tool.queryMessage(query,
                                         language,
                                         include_global=not local_only)
            if messages:
                # set up result field
                self.form_fields = setup_form_fields(managetranslationsset,
                                                     translationresultset)
                
                self.show_search_results = True
                self.form_fields['result'].field.vocabulary = SimpleVocabulary(
                    [SimpleTerm(make_token(msg['domain'], msg['msgid']),
                                make_token(msg['domain'], msg['msgid']),
                                msg['msgstr']) for msg in messages])
            else:
               self.status = _(u'No translations matched your query.')
        else:
            self.status = _(u'Empty query submitted. Please type in a query before searching.')

    @form.action(_(u'Export as .po-file'), managetranslations_actions)
    def handle_export(self, action, data):
        domain, language = split_token(data['domain'])

        response = self.request.response
        
        # set response header to plain text
        response.setHeader('Content-Type', 'text/plain')        

        # set filename
        response.setHeader('Content-Disposition', 
                           'attachment; filename=%s-%s.po' % (domain, language))

        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        tool = ICustomizableTranslationsTool(portal)

        messages = tool.listMessages(domain, language)

        return po_export(domain,
                         language,
                         messages)
        
    def getActionsFor(self, fieldset):
        """Helper method to allow displaying actions inside each
        fieldset."""

        actions = (self.translationquery_actions, self.managetranslations_actions)
        fieldsets = self.form_fields.fieldsets
        
        for fs, actions in [(fieldsets[i], actions[i]) for i in range(len(fieldsets))]:
            if fieldset is fs:
                # return only visible actions
                return [a for a in actions if \
                        not getattr(a, 'visible_condition', None) or \
                        a.visible_condition(self, a)]
