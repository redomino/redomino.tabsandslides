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

from zope.interface import implements
from zope.component import getUtility, getMultiAdapter

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.portlet.collection.collection import Renderer as CollectionRenderer
from plone.portlet.collection.collection import Assignment as CollectionAssignment
from plone.portlet.collection.collection import AddForm as CollectionAddForm
from plone.portlet.collection.collection import ICollectionPortlet as CollectionICollectionPortlet

from redomino.tabsandslides.browser.adapters.interfaces import ITabPortletAdapter

class ICollectionPortlet(CollectionICollectionPortlet):
    """"""

class Renderer(CollectionRenderer):
    """Portlet renderer.
    
    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    _template = ViewPageTemplateFile('portlet_slideshow.pt')
    render = _template

    def getViews(self):
        out = []
            
        for b in self.results():
            obj = b.getObject()
            tabGenerator = ITabPortletAdapter(obj)
            out.append({'tab':tabGenerator.getTab(),'pane':tabGenerator.getPane()})

        return out

class Assignment(CollectionAssignment):
    """"""
    implements(ICollectionPortlet)

class AddForm(CollectionAddForm):
    """"""
    def create(self, data):
        return Assignment(**data)

class EditForm(CollectionAddForm):
    """"""

