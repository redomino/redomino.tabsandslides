#!/usr/bin/env python
# Authors: Giacomo Spettoli <giacomo.spettoli@redomino.com> and contributors (see docs/CONTRIBUTORS.txt)
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
from zope.component import getUtility

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.portlet.collection import PloneMessageFactory as _plone
from plone.memoize.instance import memoize

from plone.app.portlets.portlets import base
from plone.i18n.normalizer.interfaces import IIDNormalizer

from plone.app.layout.navigation.interfaces import INavigationRoot 
from Acquisition import aq_inner, aq_parent
from plone.app.layout.navigation.defaultpage import isDefaultPage

from Products.CMFCore.Expression import Expression, getExprContext

from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import BoundPageTemplate
from redomino.tabsandslides import tabsandslidesMessageFactory as _
from Products.ZCatalog.Lazy import LazyMap
    
class ITalExpPortlet(IPortletDataProvider):
    """"""
    header = schema.TextLine(
        title=_plone(u"Portlet header"),
        description=_plone(u"Title of the rendered portlet"),
        required=True)

    talexp = schema.TextLine(
        title=_(u"Tal expression"),
        description=_(u"Tal expression description", default="""This tal expression can returns a list of brain or objects. For example:
- subject example:  python:portal.portal_catalog.searchResults(Subject=object.Subject())
- path example:  python:portal.portal_catalog.searchResults(path='/'.join(object.getPhysicalPath()))
- path example2: python:portal.portal_catalog.searchResults(path={query='/'.join(object.getPhysicalPath(), depth = 1}))
- type example:  python: portal.portal_catalog.searchResults(Type='Document')
- sort example:  portal.portal_catalog.searchResults(sort_order="reverse", sort_limit = 5, sort_on="Date")
- related items: python: object.getRelatedItems()
- related backreference: python: [ b.getSourceObject() for b in portal.reference_catalog.getBackReferences(object, relationship="relatesTo")]
"""),
        required=False)

    relative_to_contenttype = schema.Choice(
        title=_(u"Context content type"),
        description=_(u"If you use this option, the portlet picks the content relative to the closest parent of the specified content type. If not, the content is relative to the current object."),
        vocabulary="redomino.tabsandslides.contenttypes", 
        required=False
#        default=False
)
    relative_to_ct_inherit = schema.Bool(
        title=_plone(u"Allow inheritance from parent"),
        description=_(u"If enabled, the portlet will be visible on objects contained by the context choosen. "
                      u"This option is used only if the portlet is relative to a specific content type (using the option above)."),
        required=False,
        default=False)

    limit = schema.Int(
        title=_plone(u"Limit"),
        description=_plone(u"Specify the maximum number of items to show in the "
                      u"portlet. Leave this blank to show all items."),
        default=15,
        required=False)

    random = schema.Bool(
        title=_plone(u"Select random items"),
        description=_plone(u"If enabled, items will be selected randomly from the "
                      u"TAL expression, rather than based on its sort order."),
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

    implements(ITalExpPortlet)

    header = u""
    talexp = False
    limit = None
    random = False

    relative_to_ct_inherit = False

    def __init__(self, header=u"", talexp='', relative_to_contenttype = None,relative_to_ct_inherit = False, limit=None,
                 random=False, target_view="templates/portlet_tabs.pt", omit_border=False):
        self.header = header
        self.limit = limit
        self.talexp = talexp
        self.relative_to_contenttype = relative_to_contenttype
        self.relative_to_ct_inherit = relative_to_ct_inherit 
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

    def css_class(self):
        """Generate a CSS class from the portlet header
        """
        header = self.data.header
        normalizer = getUtility(IIDNormalizer)
        return "portlet-tabsandslides-%s" % normalizer.normalize(header)

    def render(self):
        _template = ViewPageTemplateFile('templates/%s' % self.data.target_view)
        return BoundPageTemplate(_template, self)()

    @property
    def available(self):
        return len(self.results())

    def object_url(self):
        return None

    @memoize
    def results(self):
        """ Get the actual result brains from the collection.
            This is a wrapper so that we can memoize if and only if we aren't
            selecting random items."""
        results = []
        context = self.get_context()

        if self.data.talexp and self.data.talexp.strip() and context:
            expression = Expression(self.data.talexp)
            expression_context = getExprContext(context, object = context)
            expresult = expression(expression_context)
            if isinstance(expresult, LazyMap): # case 1: talexp returns brains
                results = [brain.getObject() for brain in expresult]
            else:
                results = expresult # case 2: talexp returns objects

            results = [res for res in results if res.UID() != context.UID()]
                
        return results

    @memoize
    def getObjects(self):
        limit = self.data.limit

        results = self.results()

        if self.data.random:
            if len(results) < limit:
                limit = len(results)
            results = random.sample(results, limit)
        
        return results[:limit]

    @memoize
    def get_context(self):
        context = aq_inner(self.context)
        container = aq_parent(context)

        if isDefaultPage(container, context):
            context = container

        if self.data.relative_to_contenttype:
            if hasattr(self.data, 'relative_to_ct_inherit') and self.data.relative_to_ct_inherit:
                while context.portal_type != self.data.relative_to_contenttype:
                    if INavigationRoot.providedBy(context):
                        return None # parent not found
                    context = aq_parent(context)
            else:
                if context.portal_type != self.data.relative_to_contenttype:
                    return None # parent not found


        return context


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ITalExpPortlet)
#    form_fields['target_collection'].custom_widget = UberSelectionWidget

    label = _plone(u"Add TalExp Portlet")
    description = _plone(u"This portlet display a listing of items from a "
                    u"TAL expression.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    form_fields = form.Fields(ITalExpPortlet)

    label = _plone(u"Edit Collection Portlet")
    description = _plone(u"This portlet display a listing of items from a "
                    u"TAL expression.")
