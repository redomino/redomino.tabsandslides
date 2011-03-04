# Copyright (c) 2010 Redomino srl (http://redomino.com)
# Authors: Davide Moro <davide.moro@redomino.com> and contributors (see docs/CONTRIBUTORS.txt)
#
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

from redomino.tabsandslides.tests.base import TestCase


class TestPortal(TestCase):
    """ """


    def test_jsinstalled(self):
        """ test if redomino.tabsandslides js is correct installed """
        pjs = self.portal.portal_javascripts
        self.assertTrue("++resource++redomino.tabsandslides_resources/jquery.boxscrollable.js" in pjs.getResourceIds())
        self.assertTrue("++resource++redomino.tabsandslides_resources/jquery-ui-1.8.6.custom.min.js" in pjs.getResourceIds())

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortal))
    return suite


