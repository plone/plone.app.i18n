from plone.fieldsets import FormFieldsets

from zope.interface import implements
from zope.interface import Interface
from zope.component import adapts

import zope.cachedescriptors.property

from Acquisition import aq_inner

from zope.schema import TextLine
from zope.schema import Choice

from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from zope.formlib import form

from zope.app.form.browser import RadioWidget

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_unicode

from plone.app.controlpanel.form import ControlPanelForm
from plone.app.i18n.messages import query_message, customize_translation
from plone.app.form.widgets import LanguageDropdownChoiceWidget

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from utils import make_msg_token, split_msg_token

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
                     description=_(u"Enter a search string to find existing translation messages."),
                     required=False,
                     default=u'')

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
    pass

class ITranslationsSchema(ITranslationQuerySchema,
                          ITranslationQueryResultSchema,
                          IManageTranslationsSchema):
    """Combined schema for the adapter lookup."""
    
class TranslationsControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(ITranslationsSchema)

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

    @form.action(_(u'Save translation'), translationquery_actions)
    def handle_add(self, action, data):
        language = data['language']

        try:
            # we need to get these directly from the request
            token = self.request['form.result']
            translation = self.request['form.translation']
        except:
            # try running a query instead
            return self.handle_query.success(data)
            
        domain, msgid = split_msg_token(token)

        # register translation
        customize_translation(msgid, translation, domain, language)

        self.status = _(u'Translation customized.')
            
    handle_add.visible_condition = lambda form, action: form.show_search_results

    @form.action(_(u'Search'), translationquery_actions)
    def handle_query(self, action, data):
        query = data['query']
        language = data['language']

        if query:
            messages = query_message(query, language)
            if messages:
                # set up result field
                self.form_fields = setup_form_fields(managetranslationsset,
                                                     translationresultset)
                
                self.show_search_results = True
                self.form_fields['result'].field.vocabulary = SimpleVocabulary(
                    [SimpleTerm(make_msg_token(msg['domain'], msg['msgid']),
                                make_msg_token(msg['domain'], msg['msgid']),
                                msg['msgstr']) for msg in messages])
            else:
               self.status = _(u'No translations matched your query.')
        else:
            self.status = _(u'Empty query submitted. Please type in a query before searching.')

    @form.action(_(u'Remove'), managetranslations_actions)
    def handle_remove(self, action, data):
        self.status = _(u'Translation removed.')

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
