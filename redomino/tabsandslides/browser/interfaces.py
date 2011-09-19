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

class ITabGenerator(Interface):
    """Generate tabs"""
    def getTab():
        """return a tab (label, image or whatever)"""
    def getPane():
        """return a pane (usually the content)"""

class ITabbedFolder(Interface):
    """tabbed_folder view interface"""

class ISlideshowFolder(Interface):
    """slideshow_folder view interface"""
class IImagesTabbedFolder(Interface):
    """images_tabbed_folder view interface"""
class IGalleryFolder(Interface):
    """gallery_tabbed_folder view interface"""
class ISlideshowPreviewFolder(Interface):
    """slideshow_preview_folder view interface"""
class IBoxView(Interface):
    """box view view interface"""


