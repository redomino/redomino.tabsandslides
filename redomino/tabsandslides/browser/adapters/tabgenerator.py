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
from Products.ATContentTypes.interface import IATTopic
#from zope.component import adapts, getMultiAdapter
from redomino.tabsandslides.utility import filterById

#
# base class
#

class PrototypeTabGenerator(object):

    def __init__(self,context):
        self.context = context

#
# adapters implementation
#

class SimpleTabGenerator(PrototypeTabGenerator):
    """
    >>> class Dummy(object):
    ...    def Title(self):
    ...        return 'Title'
    ...    def absolute_url(self):
    ...        return 'http://nourl'
    >>> dummy = Dummy()
    >>> stg = SimpleTabGenerator(dummy)
    >>> stg.getTab()
    '<a href="http://nourl">Title</a>'
    """

    def getTab(self):
        return ''.join(['<a href="',self.context.absolute_url() ,'">', self.context.Title(), '</a>'])

    def getPane(self):
        layout = self.context.getLayout()
        view = self.context.restrictedTraverse(layout)
#        if ITabbedFolder.providedBy(view) and IATTopic.providedBy(self.context): # see docstring
#            view = self.context.restrictedTraverse('folder_contents')
            
        #danger of infinite recursion !!!
        if IATTopic.providedBy(self.context):
            view = self.context.restrictedTraverse('folder_listing')

        request = self.context.REQUEST # simplify view
        request['ajax_load'] = "1"

        html = view()    

        return filterById(html,'content-core',newclass='template_' + layout)
            
class TabGeneratorImage(PrototypeTabGenerator):
    """
    >>> class Dummy(object):
    ...    def Title(self):
    ...        return 'Title'
    ...    def absolute_url(self):
    ...        return 'http://nourl'
    >>> dummy = Dummy()
    >>> tgi = TabGeneratorImage(dummy)
    >>> tgi.getTab()
    '<a href="http://nourl">Title</a>'
    >>> tgi.getPane()
    '<img src="http://nourl" alt="Title" />'
    
    """
    def getTab(self):
        return ''.join(['<a href="',self.context.absolute_url() ,'">', self.context.Title(), '</a>'])

    def getPane(self):
        return '<img src="%s" alt="%s" />' % (self.context.absolute_url(), self.context.Title() )
   
#
# IImagesTabbedFolder adapters
#

class ImagesTabGenerator(PrototypeTabGenerator):
    """
    >>> class Dummy(object):
    ...    title = 'title'
    ...    def Title(self):
    ...        return 'Title'
    ...    def absolute_url(self):
    ...        return 'http://nourl'
    ...    def Description(self):
    ...        return 'Description'
    >>> dummy = Dummy()
    >>> tgi = ImagesTabGenerator(dummy)
    >>> tgi.getTab()
    '<a href="http://nourl/view"><div style="width:200px;height:200px;background-color:#ccc" >title</div></a>'
    >>> tgi.getPane()
    '<div><h3>Title</h3><p>Description</p></div>'
    
    """
    def getTab(self):
        url = self.context.absolute_url()
        text = self.context.title
        return '<a href="%s/view"><div style="width:200px;height:200px;background-color:#ccc" >%s</div></a>' % (url, text)

    def getPane(self):
        return "<div><h3>%s</h3><p>%s</p></div>" % (self.context.Title(), self.context.Description())


class ImagesImageTabGenerator(PrototypeTabGenerator):
    """
    >>> class Dummy(object):
    ...    title = 'title'
    ...    def Title(self):
    ...        return 'Title'
    ...    def absolute_url(self):
    ...        return 'http://nourl'
    ...    def Description(self):
    ...        return 'Description'
    >>> dummy = Dummy()
    >>> tgi = ImagesImageTabGenerator(dummy)
    >>> tgi.getTab()
    '<a href="http://nourl/view"><img src="http://nourl/@@images/image/mini" /></a>'
    >>> tgi.getPane()
    '<div><h3>Title</h3><p>Description</p></div>'
    """
    def getTab(self):
        url = self.context.absolute_url()
        return '<a href="%s/view"><img src="%s/@@images/image/mini" /></a>' % (url,url)

    def getPane(self):
        return "<div><h3>%s</h3><p>%s</p></div>" % (self.context.Title(), self.context.Description())
   

class ImagesNewsTabGenerator(PrototypeTabGenerator):
    """
    >>> class Dummy(object):
    ...    title = 'title'
    ...    def Title(self):
    ...        return 'Title'
    ...    def absolute_url(self):
    ...        return 'http://nourl'
    ...    def Description(self):
    ...        return 'Description'
    ...    def getText(self):
    ...        return 'Text'
    >>> dummy = Dummy()
    >>> tgi = ImagesNewsTabGenerator(dummy)
    >>> tgi.getTab()
    '<a href="http://nourl"><img src="http://nourl/@@images/image/mini" /></a>'
    >>> tgi.getPane()
    '<div><h3>Title</h3><p>Description</p><div>Text</div></div>'
    """
    def getTab(self):
        url = self.context.absolute_url()
        return '<a href="%s"><img src="%s/@@images/image/mini" /></a>' % (url,url)

    def getPane(self):
        ctx = self.context
        return "<div><h3>%s</h3><p>%s</p><div>%s</div></div>" % (ctx.Title(), ctx.Description(), ctx.getText())


#
# ISlideshowPreviewViewAdapter adapters
#

class PreviewTabGeneratorImage(PrototypeTabGenerator):
    """
    >>> class Dummy(object):
    ...    title = 'title'
    ...    def Title(self):
    ...        return 'Title'
    ...    def absolute_url(self):
    ...        return 'http://nourl'
    ...    def Description(self):
    ...        return 'Description'
    >>> dummy = Dummy()
    >>> tgi = PreviewTabGeneratorImage(dummy)
    >>> tgi.getTab()
    '<a href="http://nourl/view"><img src="http://nourl/@@images/image/tile" /></a>'
    >>> tgi.getPane()
    '<a href="http://nourl/view"><img src="http://nourl" /></a>'
    """
    def getTab(self):
        url = self.context.absolute_url()
        return '<a href="%s/view"><img src="%s/@@images/image/tile" /></a>' % (url,url)

    def getPane(self):
        url = self.context.absolute_url()
        return '<a href="%s/view"><img src="%s" /></a>' % (url,url)
   

class PreviewTabGeneratorNews(PrototypeTabGenerator): 
    """
    >>> class Dummy(object):
    ...    title = 'title'
    ...    def Title(self):
    ...        return 'Title'
    ...    def absolute_url(self):
    ...        return 'http://nourl'
    ...    def Description(self):
    ...        return 'Description'
    ...    def getText(self):
    ...        return 'Text'
    >>> dummy = Dummy()
    >>> tgi = PreviewTabGeneratorNews(dummy)
    >>> tgi.getTab()
    '<div><a href="http://nourl"><img src="http://nourl/@@images/image/tile" /></a></div>'
    >>> tgi.getPane()
    '<div><h3>Title</h3><p>Description</p><div>Text</div></div>'
    """
    def getTab(self):
        url = self.context.absolute_url()
        return '<div><a href="%s"><img src="%s/@@images/image/tile" /></a></div>' % (url,url)

    def getPane(self):
        ctx = self.context
        return "<div><h3>%s</h3><p>%s</p><div>%s</div></div>" % (ctx.Title(), ctx.Description(), ctx.getText())

