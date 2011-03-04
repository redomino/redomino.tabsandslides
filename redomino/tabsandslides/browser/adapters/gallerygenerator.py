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

#from zope.interface import implements, Interface
from Products.ATContentTypes.interface import  IATTopic
#from redomino.tabsandslides.browser.interfaces import IGalleryFolder, IGalleryGenerator
#from zope.component import adapts, getMultiAdapter
from redomino.tabsandslides.utility import filterById

#
# base class
#

class PrototypeGalleryGenerator(object):

    def __init__(self,context):
        self.context = context

#
# IGalleryFolder adapters
#

class GalleryTabGenerator(PrototypeGalleryGenerator):
    """

    """
    def get(self):
        layout = self.context.getLayout()
        view = self.context.restrictedTraverse(layout)
            
        #danger of infinite recursion
        if IATTopic.providedBy(self.context):
            view = self.context.restrictedTraverse('folder_listing')

        request = self.context.REQUEST # simplify view
        request['ajax_load'] = "1"

        html = view()    

        return filterById(html,'content-core',newclass='template_' + layout)

class GalleryImageTabGenerator(PrototypeGalleryGenerator):
    """
    >>> class Dummy(object):
    ...    def Title(self):
    ...        return 'Title'
    ...    def absolute_url(self):
    ...        return 'http://nourl'
    >>> dummy = Dummy()
    >>> stg = GalleryImageTabGenerator(dummy)
    >>> stg.get()
    '<a href="http://nourl"><img src="http://nourl/@@images/image/mini" alt="Title" /></a>'
    """
    def get(self):
        ctx = self.context
        return '<a href="%s"><img src="%s/@@images/image/mini" alt="%s" /></a>' % (ctx.absolute_url(), ctx.absolute_url(), ctx.Title() )

#class GalleryNewsTabGenerator(PrototypeGalleryGenerator):
#    """"""
#    def get(self):
#        ctx = self.context
#        return '<a href="%s"><img src="%s/@@images/image/mini" alt="%s" /></a>' % (ctx.absolute_url(), ctx.absolute_url(), ctx.Title() )

