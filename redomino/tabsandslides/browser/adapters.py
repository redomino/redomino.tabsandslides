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
from redomino.tabsandslides.utility import filterById
from Products.ATContentTypes.interface import IATTopic, IATFolder, IATDocument, IATFile, IATImage, IATNewsItem
from zope.component import getMultiAdapter
from Products.Five import BrowserView

class TabsTab(BrowserView):
    def __call__(self):
        return '<a href="%s/view">%s</a>' % (self.context.absolute_url(), self.context.Title())


class GenericPane(BrowserView):
    def __call__(self):
        layout = self.context.getLayout()
        view = self.context.restrictedTraverse(layout)
            
        #danger of infinite recursion
        if IATTopic.providedBy(self.context) or IATFolder.providedBy(self.context):
            view = self.context.restrictedTraverse('folder_listing')

        self.request['ajax_load'] = "1"

        html = view()    

        return filterById(html,'content-core',newclass='template_' + layout)


class ImageTab(BrowserView):
    def __call__(self):
        return '<div class="image"><a href="%s/view"><img src="%s" alt="%s" title="%s"/></a></div>' % (self.context.absolute_url(), 
                                                                         self.context.absolute_url(), 
                                                                         self.context.Title(), 
                                                                         self.context.Title())
    

class GalleryPane(GenericPane):

    def __call__(self):
        if IATDocument.providedBy(self.context) or IATNewsItem.providedBy(self.context):
            return ''.join(['<div class="text">', self.context.getText(), '</div>'])
        if IATImage.providedBy(self.context):
            imageurl = "%s/@@images/image/preview" % (self.context.absolute_url(),)
            return '<div class="image"><a href="%s/image"><img src="%s" alt="%s" title="%s"/></a></div>' % (self.context.absolute_url(),
                                                                                  imageurl,
                                                                                  self.context.Title(),
                                                                                  self.context.Title() )
        
            
        return GenericPane.__call__(self)

class Gallery(BrowserView):
    def portal_url(self):
        return getMultiAdapter((self.context,self.request),name=u"plone_portal_state").portal_url()
        
    def getImage(self):
        portal_url = self.portal_url()

        if IATImage.providedBy(self.context) or IATNewsItem.providedBy(self.context):
            return "%s/@@images/image/thumb" % (self.context.absolute_url(),)
        elif IATTopic.providedBy(self.context) or IATFolder.providedBy(self.context):
            return "%s/++resource++redomino.tabsandslides.folder.png" % (self.portal_url(),)
        else:
            return "%s/++resource++redomino.tabsandslides.page.png" % (self.portal_url(),)
        
