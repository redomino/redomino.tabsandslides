"""
Tests the adapters
"""
from redomino.tabsandslides.tests.base import TestCase
from redomino.tabsandslides.browser.adapters.gallerygenerator import GalleryTabGenerator
from redomino.tabsandslides.browser.adapters.tabgenerator import SimpleTabGenerator

class AdapterTestCase(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        #Create Folder
        self.portal.invokeFactory(id='folder', type_name='Folder')
        folder = self.portal.folder
        #Create Content
        folder.invokeFactory(id='doc1', type_name='Document')
        folder.invokeFactory(id='image1', type_name='Image')
        self.doc1 = self.portal.folder.doc1
        self.image1 = self.portal.folder.image1
        #Views
        self.tabbed_view =          folder.restrictedTraverse('@@tabbed_view')
        self.gallery_view =         folder.restrictedTraverse('@@gallery_view')
        self.tabbed_summary_view =  folder.restrictedTraverse('@@tabbed_summary_view')
        self.slideshow_view =       folder.restrictedTraverse('@@slideshow_view')

    def test_get_pane(self):
        """
        Tests the getPane() method in redomino.tabsandslides.browser.adapters.tabgenerator.SimpleTabGenerator
        """      
        adapter = self.tabbed_view.getAdapter(self.doc1)
        self.assertTrue(type(adapter), SimpleTabGenerator)
        self.assertTrue('<div id="" class="tab-content-core template_document_view">' in adapter.getPane())
    
    def test_gallery_get(self):
        """
        Tests the get() method in redomino.tabsandslides.browser.adapters.gallerygenerator.GalleryTabGenerator
        """
        adapter = self.gallery_view.getAdapter(self.image1)
        self.assertTrue(type(adapter), GalleryTabGenerator)
        self.assertTrue('<a href="http://nohost/plone/folder/image1"><img src="http://nohost/plone/folder/image1/@@images/image/mini" alt="" /></a>' in adapter.get())
