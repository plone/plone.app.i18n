from zope.component import getGlobalSiteManager
from zope.component import getSiteManager
from zope.component import queryMultiAdapter
from zope.component.interfaces import IComponentRegistry, IComponents
from zope.interface import Interface

from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import _getDottedName
from Products.GenericSetup.utils import _resolveDottedName

class SiteManagerXMLAdapter(XMLAdapterBase):
    """In- and exporter for a local site manager.
    """
    __used_for__ = IComponents
    name = 'sitemanager'

    def _exportNode(self):
        node=self._doc.createElement('utilities')
        node.appendChild(self._extractUtilities())

        self._logger.info('Utilities exported.')
        return node

    def _importNode(self, node):
        if self.environ.shouldPurge():
            self._purgeUtilities()

        self._initUtilities(node)
        self._logger.info('Utilities registered.')

    def _purgeUtilities(self):
        gsm = getGlobalSiteManager()
        global_utilities = gsm.getAllUtilitiesRegisteredFor(Interface)
        utilities = self.context.getAllUtilitiesRegisteredFor(Interface)
        
        for utility in utilities:
            if not utility in global_utilities:
                self.context.unregisterUtility(utility)

    def _initUtilities(self, node):
        for child in node.childNodes:
            if child.nodeName != 'utility':
                continue

            interface = _resolveDottedName(child.getAttribute('interface'))
            class_attr = _resolveDottedName(child.getAttribute('class'))
            name = str(child.getAttribute('name'))
            if name:
                self.context.registerUtility(class_attr(), interface, name)
            else:
                self.context.registerUtility(class_attr(), interface)

    def _extractUtilites(self):
        node=self._doc.createElement('utilities')

        gsm = getGlobalSiteManager()
        global_utilities = gsm.getAllUtilitiesRegisteredFor(Interface)
        utilities = self.context.getAllUtilitiesRegisteredFor(Interface)
        
        for utility in utilities:
            if not utility in global_utilities:
                child=self._doc.createElement('utility')
                interface = _getDottedName('interface')
                obj = _getDottedName(utility)
                name = 'name'
                child.setAttribute('interface', interface)
                child.setAttribute('class', class_attr)
                child.setAttribute('name', name)

                node.appendChild(child)

        return node

def dummyGetId():
    return ''

def importSiteManager(context):
    """Import local components .
    """
    sm = getSiteManager(context.getSite())
    if sm is None or not IComponents.providedBy(sm):
        logger = context.getLogger('utilties')
        logger.info("Can not register utilities, as no site manager was found.")
        return
    # XXX GenericSetup.utils.importObjects expects the object to have a getId
    # function. We provide a dummy one for now, but this should be fixed in GS
    # itself
    sm.getId = dummyGetId
    importObjects(sm, '', context)

def exportSiteManager(context):
    """Export local components.
    """
    sm = getSiteManager(context.getSite())
    if sm is None or not IComponents.providedBy(sm):
        logger = context.getLogger('utilties')
        logger.info("Nothing to export.")
        return

    exportObjects(sm, '', context)
