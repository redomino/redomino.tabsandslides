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

from Products.Five import BrowserView
#from zope.component import getMultiAdapter
#from redomino.tabsandslides.utility import filterById
#from Products.ATContentTypes.interface import IATTopic, IATFolder
#from Acquisition import aq_inner
#from plone.memoize.view import memoize

class CreateObject(BrowserView):
    """create an object (used in content portlet)"""

    def __call__(self):
        ob_id = self.request.form.get('id')
        ob_type = self.request.form.get('type_name')
        
        self.request.RESPONSE.redirect(self.context.absolute_url() + '/createObject?type_name=%s&id=%s' % (ob_type, ob_id))

