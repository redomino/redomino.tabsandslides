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
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from Products.ATContentTypes.interface import IATTopic
from Acquisition import aq_inner

from redomino.tabsandslides.browser.interfaces import (ITabGenerator,
                                                       ITabbedFolder,
                                                       ISlideshowFolder,
                                                       IImagesTabbedFolder,
                                                       IGalleryFolder,
                                                       ISlideshowPreviewFolder,
                                                       IBoxView)


class BaseTabbedFolderView(BrowserView):
    """
    base implementation: It is the base of all collection/folder based class with tab or slides
    """

    @property
    def portal_catalog(self):
        return getMultiAdapter((self.context,self.request),name=u"plone_tools").catalog()

    @property
    def portal_types(self):
        return getMultiAdapter((self.context,self.request),name=u"plone_tools").types()


    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def contentsMethod(self):
        context = aq_inner(self.context)
        if IATTopic.providedBy(context):
            contentsMethod = context.queryCatalog
        else:
            contentsMethod = context.getFolderContents
        return contentsMethod
            
    def getViews(self):
        """return a tab and a pane for each object:
        """
        contentsMethod = self.contentsMethod()

        out = []
            
        for b in contentsMethod():
            obj = b.getObject()
            tabGenerator = self.getAdapter(obj)
            out.append({'tab':tabGenerator.getTab(),'pane':tabGenerator.getPane()})

        return out

    def getAdapter(self,obj):
        return getMultiAdapter((obj, self.context, self.request, self), ITabGenerator)

class TabbedFolder(BaseTabbedFolderView):
    implements(ITabbedFolder)

class SlideshowFolder(BaseTabbedFolderView):
    implements(ISlideshowFolder)

class ImagesTabbedFolder(BaseTabbedFolderView):
    implements(IImagesTabbedFolder)

class GalleryFolder(BaseTabbedFolderView):
    implements(IGalleryFolder)

class SlideshowPreviewFolder(BaseTabbedFolderView):
    implements(ISlideshowPreviewFolder)

class BoxView(BaseTabbedFolderView):
    implements(IBoxView)

