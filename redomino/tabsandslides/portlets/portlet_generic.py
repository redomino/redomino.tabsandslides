#!/usr/bin/env python
# Authors: Maurizio Lupo <maurizio.lupo@redomino.com> and contributors (see docs/CONTRIBUTORS.txt)
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

import random
from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component import getUtility, getMultiAdapter
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.portlet.collection import PloneMessageFactory as _plone
from Products.CMFPlone import PloneMessageFactory as _plonebase

from plone.app.portlets.portlets import base
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from Products.ATContentTypes.interface import IATTopic
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.app.vocabularies.catalog import SearchableTextSourceBinder

from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ModifyPortalContent

from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import BoundPageTemplate

    
class ICollectionPortlet(IPortletDataProvider):
    """"""
    header = schema.TextLine(
        title=_plone(u"Portlet header"),
        description=_plone(u"Title of the rendered portlet"),
        required=True)

    target_collection = schema.Choice(
        title=_plone(u"Target collection"),
        description=_plone(u"Find the collection which provides the items to list"),
        required=True,
        source=SearchableTextSourceBinder(
            {'object_provides': IATTopic.__identifier__},
            default_query='path:'))

    limit = schema.Int(
        title=_plone(u"Limit"),
        description=_plone(u"Specify the maximum number of items to show in the "
                      u"portlet. Leave this blank to show all items."),
        default=15,
        required=False)

    random = schema.Bool(
        title=_plone(u"Select random items"),
        description=_plone(u"If enabled, items will be selected randomly from the "
                      u"collection, rather than based on its sort order."),
        required=False,
        default=False)


    target_view = schema.Choice(
        title=_plone(u"label_choose_template"),
        required=True, 
        vocabulary="redomino.tabsandslides.portlettemplates", 
        #default=u'portlet_tabs.pt')
        )

    omit_border = schema.Bool(
        title=_plone(u"Omit portlet border"),
        description=_plone(u"Tick this box if you want to render the text above "
                      "without the standard header, border or footer."),
        required=False,
        default=False)



class Assignment(base.Assignment):
    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ICollectionPortlet)

    header = u""
    target_collection = None
    limit = None
    random = False

    def __init__(self, header=u"", target_collection=None, limit=None,
                 random=False, target_view="templates/portlet_tabs.pt", omit_border=False):
        self.header = header
        self.limit = limit
        self.target_collection = target_collection
        self.random = random
        self.target_view = target_view
        self.omit_border = omit_border


    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header

class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

#    _template = ViewPageTemplateFile('portlet_tabs.pt')
    
# 
    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        
    # Cached version - needs a proper cache key
    # @ram.cache(render_cachekey)
    # def render(self):
    #     if self.available:
    #         return xhtml_compress(self._template())
    #     else:
    #         return ''

    def css_class(self):
        """Generate a CSS class from the portlet header
        """
        header = self.data.header
        normalizer = getUtility(IIDNormalizer)
        return "portlet-tabsandslides-%s" % normalizer.normalize(header)

    def render(self):
        _template = ViewPageTemplateFile('templates/%s' % self.data.target_view)
        return BoundPageTemplate(_template, self)()

#    render = _template
    @property
    def footer(self):
        sm = getSecurityManager()       
        context = self.collection()
        if context is not None:
            
            if sm.checkPermission(ModifyPortalContent, context):

                portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
                current_language = portal_state.language()
                # get tool
                tool = getToolByName(context, 'translation_service')

                # this returns type unicode
                editstring = tool.translate(u"edit",
                               'plone',
                                context=context,
                                target_language=current_language) + " " + self.data.header
                
                return u'<div class="managePortletsLink editContent visualClear"><a href="%s">%s</a></div>' % (context.absolute_url(), editstring)
        return None

    @property
    def available(self):
        return len(self.results()) or self.footer

    def object_url(self):
        collection = self.collection()
        if collection is None:
            return None
        else:
            return collection.absolute_url()

    def results(self):
        """ Get the actual result brains from the collection.
            This is a wrapper so that we can memoize if and only if we aren't
            selecting random items."""
        if self.data.random:
            return self._random_results()
        else:
            return self._standard_results()

    @memoize
    def _standard_results(self):
        results = []
        collection = self.collection()
        if collection is not None:
            results = collection.queryCatalog()
            if self.data.limit and self.data.limit > 0:
                results = results[:self.data.limit]
        return results

    # intentionally non-memoized
    def _random_results(self):
        results = []
        collection = self.collection()
        if collection is not None:
            """
            Kids, do not try this at home.

            We're poking at the internals of the (lazy) catalog
            results to avoid instantiating catalog brains
            unnecessarily.

            We're expecting a LazyCat wrapping two LazyMaps as the
            return value from
            Products.ATContentTypes.content.topic.ATTopic.queryCatalog.
            The second of these contains the results of the catalog
            query.  We force sorting off because it's unnecessary and
            might result in a different structure of lazy objects.

            Using the correct LazyMap (results._seq[1]), we randomly
            pick a catalog index and then retrieve it as a catalog
            brain using the _func method.
            """

            results = collection.queryCatalog(sort_on=None)
            if results is None:
                return []
            limit = self.data.limit and min(len(results), self.data.limit) or 1

            if len(results) < limit:
                limit = len(results)
            results = random.sample(results, limit)

        return results

    @memoize
    def collection(self):
        """ get the collection the portlet is pointing to"""

        collection_path = self.data.target_collection
        if not collection_path:
            return None

        if collection_path.startswith('/'):
            collection_path = collection_path[1:]

        if not collection_path:
            return None

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal = portal_state.portal()
        if isinstance(collection_path, unicode):
            #restrictedTraverse accept only strings
            collection_path = str(collection_path)
        return portal.restrictedTraverse(collection_path, default=None)

    def getObjects(self):
        return [b.getObject() for b in self.results()]



class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ICollectionPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget

    label = _plone(u"Add Collection Portlet")
    description = _plone(u"This portlet display a listing of items from a "
                    u"Collection.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    form_fields = form.Fields(ICollectionPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget

    label = _plone(u"Edit Collection Portlet")
    description = _plone(u"This portlet display a listing of items from a "
                    u"Collection.")
