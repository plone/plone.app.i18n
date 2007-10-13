from zope import interface

class ICustomizableTranslationsTool(interface.Interface):
    """Adapts the portal object and provides a number of utility
    methods for managing and listing translations."""
    
    def addMessage(msgid, msg, domain, language):
        pass
    
    def removeMessage(msgid, domain, language):
        pass

    def queryMessage(query, language, include_global=True):
        pass

    def listMessages(domain, language):
        pass

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
