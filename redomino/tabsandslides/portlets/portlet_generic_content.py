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
from plone.portlet.collection import PloneMessageFactory as _plone
from redomino.tabsandslides import tabsandslidesMessageFactory as _

from plone.app.portlets.portlets import base
from Products.ATContentTypes.interface import IATTopic
from plone.app.layout.navigation.interfaces import INavigationRoot 
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Acquisition import aq_inner, aq_parent
from Products.Archetypes.utils import shasattr
from plone.app.layout.navigation.defaultpage import isDefaultPage

from AccessControl import getSecurityManager
from Products.CMFCore.permissions import ModifyPortalContent

from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import BoundPageTemplate

class IContentPortlet(IPortletDataProvider):
    """"""
    header = schema.TextLine(
        title=_plone(u"Portlet header"),
        description=_plone(u"Title of the rendered portlet"),
        required=True)

    content_id = schema.TextLine(
        title=_(u"Content Id"),
        description=_(u"The id of the content."),
        required=True)

    contentType = schema.Choice(
        title=_(u"Which content type"),
        description=_(u"Pick the content type you want to add to this portlet. If you choose a folderish content the portlet show the elements inside. If you choose a collection the portlet shows the objects that fit the criteria."),
        vocabulary="redomino.tabsandslides.contenttypes", 
        required=True,
#        default=False
)

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

    implements(IContentPortlet)

    header = u""
    limit = None
    relative_to_ct_inherit = False
    def __init__(self, header=u"", content_id='', contentType='Document',
                 relative_to_contenttype=None, relative_to_ct_inherit = False,
                 limit = 15, random = None, target_view="templates/portlet_tabs.pt", omit_border=False):
        self.header = header
        self.content_id = content_id
        self.contentType = contentType
        self.relative_to_contenttype = relative_to_contenttype
        self.relative_to_ct_inherit = relative_to_ct_inherit 
        self.limit = limit
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
        _template = ViewPageTemplateFile("templates/%s" % self.data.target_view)
        return BoundPageTemplate(_template, self)()

#    render = _template

    @property
    def footer(self):
        footer = []
        sm = getSecurityManager()       
        context = self.get_context()

        if sm.checkPermission(ModifyPortalContent, context):
            portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
            current_language = portal_state.language()
            # get tool
            tool = getToolByName(context, 'translation_service')

            
            #THERE IS A DESCENDANT ACQUIRED BY CONTEXT (USE ACQUISITION)
            if not shasattr(context, self.data.content_id) and hasattr(context, self.data.content_id) :
                # this returns type unicode
                editstring = tool.translate(u"edit",
                               'plone',
                                context=context,
                                target_language=current_language) + " " + self.data.header
                footer.append(u'<div class="managePortletsLink editContent visualClear"><a href="%s/view">%s</a></div>' % (self.get_item().absolute_url(), editstring))

            #THERE IS A DIRECT DESCENDANT
            if shasattr(context, self.data.content_id):
                # this returns type unicode
                editstring = tool.translate(u"edit",
                               'plone',
                                context=context,
                                target_language=current_language) + " " + self.data.header
                footer.append(u'<div class="managePortletsLink editContent visualClear"><a href="%s/view">%s</a></div>' % (self.object_url(), editstring))

            #THERE ISN'T A DIRECT DESCENDANT
            if not shasattr(context, self.data.content_id) and not hasattr(context, self.data.content_id) :
                addstring = tool.translate(u"add",
                               'plone',
                                context=context,
                                target_language=current_language) + " " + self.data.header

                footer.append(u'<div class="managePortletsLink editContent visualClear"><a href="%s/createTabsandSlidesContent?type_name=%s&id=%s">%s</a></div>' % (
                        context.absolute_url(),
                        self.data.contentType,
                        self.data.content_id,
                        addstring))

        
        return ''.join(footer)

    @property
    def available(self):
#        if self.context.id == self.data.content_id:
#            return False # don't show for the content id

        context_state = getMultiAdapter((self.get_context(), self.request), name=u'plone_context_state')
        if not context_state.is_folderish():
            return False # show for folderish content type only
        return len(self.getObjects()) or self.footer

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

    def get_item(self):
        context = self.get_context()
#        if shasattr(context, self.data.content_id):
#            return getattr(context, self.data.content_id)
        return getattr(context, self.data.content_id, None)
#        return None

    def getObjects(self):
        """ Get the actual result brains from the folder"""
        context = self.get_item()

        if context:
            limit = self.data.limit
            view = getMultiAdapter((context, self.request),name=u'tabsandslides_view')
            results = view.getObjects()
            if self.data.random:
                if len(results) < limit:
                    limit = len(results)
                results = random.sample(results, limit)
        
            return results[:limit]
        return []

    def object_url(self):
        return '%s/%s' % (self.get_context().absolute_url(),self.data.content_id)

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IContentPortlet)

    label = _(u"Add a Content Portlet")
    description = _(u"This portlet display one item or all items inside a folder.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    form_fields = form.Fields(IContentPortlet)

    label = _(u"Edit Content Portlet")
    description = _(u"This portlet display one item or all items inside a folder.")

