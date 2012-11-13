from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements, directlyProvides
from redomino.tabsandslides import tabsandslidesMessageFactory as _
from zope.component import getMultiAdapter
from Products.CMFDynamicViewFTI.interfaces import IDynamicViewTypeInformation

def ContentTypes(context):
#    portal_state = getMultiAdapter((context, context.REQUEST), name=u'plone_portal_state')
#    allowedCT = portal_state.friendly_types()
#    allowedCT = portal_types.listContentTypes()
    portal_types = getMultiAdapter((context, context.REQUEST), name=u'plone_tools').types()
#    allowedCT = [t for t in portal_types.listTypeInfo() if t.global_allow]
    allowedCT = [t for t in portal_types.listTypeInfo() if IDynamicViewTypeInformation.providedBy(t)]

    return SimpleVocabulary(
        [SimpleTerm(value=t.getId(), title=t.Title()) for t in allowedCT])

directlyProvides(ContentTypes, IVocabularyFactory)


