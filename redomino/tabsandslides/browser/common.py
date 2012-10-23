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

from zope.interface import implements, Interface

from Products.Five import BrowserView
from zope.component import getMultiAdapter
from redomino.tabsandslides.utility import filterById
from Products.ATContentTypes.interface import IATTopic, IATFolder
from Acquisition import aq_inner
from plone.memoize.view import memoize

class SingleView(BrowserView):
    """utility view for non folderish content (used in content portlet)"""

    @memoize   
    def getObjects(self):
        """return the context
        """
        return [self.context]

class BaseView(BrowserView):
    """
    base implementation: It is the base of all collection/folder based class with tab or slides
    """

    @property
    def portal_catalog(self):
        return getMultiAdapter((self.context,self.request),name=u"plone_tools").catalog()

    def contentsMethod(self):
        context = aq_inner(self.context)
        if IATTopic.providedBy(context):
            contentsMethod = context.queryCatalog
        else:
            contentsMethod = context.getFolderContents
        return contentsMethod

    @memoize   
    def getObjects(self):
        """return all the objects
        """
        contentsMethod = self.contentsMethod()
        return [b.getObject() for b in contentsMethod()]


class OriginalView(BrowserView):
    def __call__(self):
        layout = self.context.getLayout()
        view = self.context.restrictedTraverse(layout)
            
        #danger of infinite recursion
        if IATTopic.providedBy(self.context) or IATFolder.providedBy(self.context):
            view = self.context.restrictedTraverse('folder_listing')

        self.request['ajax_load'] = "1"

        html = view()

        filtered = filterById(html,'content-core',newclass='template_' + layout)

        if filtered:
            return filtered

        # old styles views
        return filterById(html,'content',newclass='template_' + layout)


