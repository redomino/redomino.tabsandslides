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

from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component import getUtility, getMultiAdapter
from plone.memoize.instance import memoize

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.portlet.collection import PloneMessageFactory as _plone
from redomino.tabsandslides import tabsandslidesMessageFactory as _

from plone.app.portlets.portlets import base
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from Products.ATContentTypes.interface import IATTopic
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.Expression import Expression, getExprContext

from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import BoundPageTemplate
    
class IFolderPortlet(IPortletDataProvider):
    """"""
    header = schema.TextLine(
        title=_plone(u"Portlet header"),
        description=_plone(u"Title of the rendered portlet"),
        required=True)

    talexp = schema.TextLine(
        title=_(u"Tal expression"),
        description=_(u"For example: python:object.portal_type == 'News Item'"),
        required=False)

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
        required=True,
        default=False)


class Assignment(base.Assignment):
    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IFolderPortlet)

    header = u""
    limit = None

    def __init__(self, header=u"", talexp='', target_view="templates/portlet_tabs.pt", omit_border=False):
        self.header = header
        self.talexp = talexp
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
    def available(self):
        return len(self.results())

    @memoize
    def get_context(self):
        context = aq_inner(self.context)
        ctxstate =  getMultiAdapter((context, self.request), name=u'plone_context_state')
        if not ctxstate.is_folderish():
            context = aq_parent(context)
        return context

    def results(self):
        """ Get the actual result brains from the folder"""
        
        return self.get_context().getFolderContents()

    def evaluate_exp(self, ctx, expression):
        expression_context = getExprContext(self, ctx)
        # works but It's not perfectly clear how
        # http://collective-docs.readthedocs.org/en/latest/functionality/expressions.html
        value = expression(expression_context)
        if hasattr(value, 'strip') and value.strip() == "":
            # Usually empty expression field means that
            # expression should be True
            value = True
        if value:
            # Expression succeeded
            return True
        else:
            return False

    def getObjects(self):
        objects = [b.getObject() for b in self.results()]
        
        #exclude self
        objects = [o for o in objects if o != self.context]
        
        if self.data.talexp and self.data.talexp.strip():
            expression = Expression(self.data.talexp)
            objects = [ctx for ctx in objects if self.evaluate_exp(ctx, expression)]
        return objects

    def object_url(self):
        return self.get_context().absolute_url()

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IFolderPortlet)

    label = _(u"Add a Folder Portlet")
    description = _(u"This portlet display items from the current "
                    u"Folder.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    form_fields = form.Fields(IFolderPortlet)

    label = _(u"Edit Folder Portlet")
    description = _(u"This portlet display items from the current "
                    u"Folder.")

