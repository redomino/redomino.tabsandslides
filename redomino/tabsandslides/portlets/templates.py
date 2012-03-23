from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements, directlyProvides
from redomino.tabsandslides import tabsandslidesMessageFactory as _

def TemplatesAvailable(context):
    return SimpleVocabulary(
        [
         SimpleTerm(value=u'portlet_tabs.pt', title=_(u'tabs')),
         SimpleTerm(value=u'portlet_slideshow.pt', title=_(u'slideshow')),
         SimpleTerm(value=u'portlet_gallery.pt', title=_(u'gallery'))
         ]
        )

directlyProvides(TemplatesAvailable, IVocabularyFactory)


