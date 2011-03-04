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

import lxml.html

def filterById(html,id,newclass=None):
    """ filter an xml by id. Example:
    
    >>> html = u'<?xml version="1.0"> <html><head></head><body><div id="content">Hello!</div><div>other content</div></body></html>'
    >>> filterById(html,'content')
    u'<div id="content">Hello!</div>'

    """

    classes = ['tab-content-core']
    if newclass:
        classes.append(newclass)

    doc = lxml.html.fromstring(html)
    try:
        nodes = doc.get_element_by_id(id)
    except:
        return ""
    nodes.set('id','')
    nodes.set('class'," ".join(classes))
    
    return lxml.html.tostring(nodes)
    


