from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from plone.app.portlets.storage import PortletAssignmentMapping

from redomino.tabsandslides.tests.base import TestCase
from redomino.tabsandslides.portlets import portlet_slideshow as collection


class TestPortlet(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager',))

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='redomino.tabsandslides.portlet')
        self.assertEquals(portlet.addview, 'redomino.tabsandslides.portlet')

    def testInterfaces(self):
        portlet = collection.Assignment(header=u"title")
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portlet = getUtility(IPortletType, name='redomino.tabsandslides.portlet')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={'header' : u"test title"})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], collection.Assignment))

    def testInvokeEditView(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = collection.Assignment(header=u"title")
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, collection.EditForm))

    def testRenderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = collection.Assignment(header=u"title")

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, collection.Renderer))

class TestRenderer(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager',))

    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = assignment or collection.Assignment(header=u"title")

        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)

    def test_render(self):
        r = self.renderer(context=self.portal, assignment=collection.Assignment(header=u"title"))
        r = r.__of__(self.folder)
        r.update()
        output = r.render()

        self.assertTrue('slideshow_panes' in output)
        self.assertTrue('slideshow_tabs' in output)
        self.assertTrue('control_slideshow' in output)


    def test_collection_path_unicode(self):
        """
        Cover problem in #9184
        """
        r = self.renderer(context=self.portal,
                          assignment=collection.Assignment(header=u"title",
                                                           target_collection=u"/events"))
        r  = r.__of__(self.folder)
        self.assertEqual(r.collection().id, 'events')

        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite
