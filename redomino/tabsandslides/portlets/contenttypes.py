from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements, directlyProvides
from redomino.tabsandslides import tabsandslidesMessageFactory as _

def ContentTypes(context):
    allowedCT = context.allowedContentTypes()
    return SimpleVocabulary(
        [SimpleTerm(value=t.getId(), title=t.Title()) for t in allowedCT])

directlyProvides(ContentTypes, IVocabularyFactory)


