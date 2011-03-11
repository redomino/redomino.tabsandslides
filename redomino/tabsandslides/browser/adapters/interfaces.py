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

from zope.interface import Interface

# TABS and SLIDES

class ITabGenerator(Interface):
    """general tab adapter interface"""
    def getTab():
        """get the tab"""
    def getPane():
        """get the pane"""

class ITabViewAdapter(ITabGenerator):
    """tabbed folder adapter"""

class ISlideshowViewAdapter(ITabGenerator):
    """slideshow view adapter"""

class IImageTabViewAdapter(ITabGenerator):
    """ImageTab view adapter"""

class ITabPortletAdapter(ITabGenerator):
    """Tab portlet view adapter"""

# GALLERIES

class IGalleryGenerator(Interface):
    """gallery generator interface"""
    def get():
        """get the view"""

class IGalleryAdapter(IGalleryGenerator):
    """gallery view adapter"""
