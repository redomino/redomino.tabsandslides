from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements, directlyProvides
from redomino.tabsandslides import tabsandslidesMessageFactory as _

def TemplatesAvailable(context):
    return SimpleVocabulary(
        [
         SimpleTerm(value=u'portlet_tabs.pt', title=_(u'tabs')),
         SimpleTerm(value=u'portlet_accordion.pt', title=_(u'accordion')),
         SimpleTerm(value=u'portlet_slideshow.pt', title=_(u'slideshow')),
         SimpleTerm(value=u'portlet_gallery.pt', title=_(u'gallery')),
         SimpleTerm(value=u'portlet_imagetab.pt', title=_(u'Gallery with preview (Image top)')),
         SimpleTerm(value=u'portlet_imagetab2.pt', title=_(u'Gallery with preview (Image bottom)')),
         SimpleTerm(value=u'portlet_list.pt', title=_(u'List')),
         SimpleTerm(value=u'portlet_allitems.pt', title=_(u'All Items'))
         ]
        )

directlyProvides(TemplatesAvailable, IVocabularyFactory)


