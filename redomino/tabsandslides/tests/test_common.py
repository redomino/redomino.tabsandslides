"""Integration test for redomino.tabsandslides.browser.common"""

from redomino.tabsandslides.tests.base import TestCase
from redomino.tabsandslides.browser.adapters.tabgenerator import SimpleTabGenerator, ImagesTabGenerator
from redomino.tabsandslides.browser.adapters.gallerygenerator import GalleryTabGenerator


class TestCommonFolder(TestCase):
    
    def afterSetUp(self):
        self.loginAsPortalOwner()
        #Create Folder
        self.portal.invokeFactory(id='folder', type_name='Folder')
        folder = self.portal.folder
        #Create Content
        folder.invokeFactory(id='doc1', type_name='Document')
        folder.invokeFactory(id='image1', type_name='Image')
        doc1 = self.portal.folder.doc1
        image1 = self.portal.folder.image1
        #Views
        self.tabbed_view =          folder.restrictedTraverse('@@tabbed_view')
        self.gallery_view =         folder.restrictedTraverse('@@gallery_view')
        self.tabbed_summary_view =  folder.restrictedTraverse('@@tabbed_summary_view')
        self.slideshow_view =       folder.restrictedTraverse('@@slideshow_view')
        self.slideshow_preview_view =       folder.restrictedTraverse('@@slideshow_preview_view')

    def test_has_view(self):
        """
        Tests if the views are registered for Folder
        """
        pt = self.portal.portal_types
        self.assertTrue('tabbed_view' in pt['Folder'].view_methods)
        self.assertTrue('gallery_view' in pt['Folder'].view_methods)
        self.assertTrue('tabbed_summary_view' in pt['Folder'].view_methods)
        self.assertTrue('slideshow_view' in pt['Folder'].view_methods)
        self.assertTrue('slideshow_preview_view' in pt['Folder'].view_methods)

    def test_get_views(self):
        """
        Tests if the views are returning values
        """
        #tabbed_view
        self.assertTrue(self.tabbed_view.getViews()[0]['pane'])
        self.assertTrue(self.tabbed_view.getViews()[0]['tab'])
        #gallery_view

        self.assertTrue('template_document_view' in self.gallery_view.getViews()[0])
        self.assertTrue('img' in self.gallery_view.getViews()[1])
        #tabbed_summary_view
        self.assertTrue(self.tabbed_summary_view.getViews()[0]['pane'])
        self.assertTrue(self.tabbed_summary_view.getViews()[0]['tab'])
        #slideshow_view
        self.assertTrue(self.slideshow_view.getViews()[0]['pane'])
        self.assertTrue(self.slideshow_view.getViews()[0]['tab'])
        #slideshow_view
        self.assertTrue(self.slideshow_preview_view.getViews()[0]['pane'])
        self.assertTrue(self.slideshow_preview_view.getViews()[0]['tab'])

    def test_get_adapter(self):
        ##Folder
        #tabbed_view
        self.assertEqual(SimpleTabGenerator, type(self.tabbed_view.getAdapter(self.portal.folder)))
        #gallery_view
        self.assertEqual(GalleryTabGenerator, type(self.gallery_view.getAdapter(self.portal.folder)))
        #tabbed_summary_view
        self.assertEqual(ImagesTabGenerator, type(self.tabbed_summary_view.getAdapter(self.portal.folder)))
        #slideshow_view
        self.assertEqual(SimpleTabGenerator, type(self.slideshow_view.getAdapter(self.portal.folder)))
        #slideshow_preview_view
        self.assertEqual(SimpleTabGenerator, type(self.slideshow_view.getAdapter(self.portal.folder)))
        ##Doc1
        #tabbed_view
        self.assertEqual(SimpleTabGenerator, type(self.tabbed_view.getAdapter(self.portal.folder.doc1)))
        #gallery_view
        #self.assertEqual(GalleryTabGenerator, type(self.gallery_view.getAdapter(self.portal.folder.doc1)))
        #tabbed_summary_view
        self.assertEqual(ImagesTabGenerator, type(self.tabbed_summary_view.getAdapter(self.portal.folder.doc1)))
        #slideshow_view
        self.assertEqual(SimpleTabGenerator, type(self.slideshow_view.getAdapter(self.portal.folder.doc1)))
        #slideshow_preview_view
        self.assertEqual(SimpleTabGenerator, type(self.slideshow_view.getAdapter(self.portal.folder.doc1)))


      ##Image
        #tabbed_view
        #self.assertEqual(SimpleTabGenerator, type(self.tabbed_view.getAdapter(self.portal.folder.image1)))
        #gallery_view
        #self.assertEqual(GalleryTabGenerator, type(self.gallery_view.getAdapter(self.portal.folder.image1)))
        #tabbed_summary_view
        #self.assertEqual(ImagesTabGenerator, type(self.tabbed_summary_view.getAdapter(self.portal.folder.image1)))
        #slideshow_view
        #self.assertEqual(SimpleTabGenerator, type(self.slideshow_view.getAdapter(self.portal.folder.image1)))
 
class TestCommonTopic(TestCase):
    
    def afterSetUp(self):
        self.loginAsPortalOwner()
        #Create Topic
        self.portal.invokeFactory(id='topic', type_name='Topic')
        topic = self.portal.topic
        #Views
        self.tabbed_view =          topic.restrictedTraverse('@@tabbed_view')
        self.gallery_view =         topic.restrictedTraverse('@@gallery_view')
        self.tabbed_summary_view =  topic.restrictedTraverse('@@tabbed_summary_view')
        self.slideshow_view =       topic.restrictedTraverse('@@slideshow_view')

    def test_has_view(self):
        """
        Tests if the views are registered for Topic
        """
        pt = self.portal.portal_types
        #Folder
        self.assertTrue('tabbed_view' in pt['Topic'].view_methods)
        self.assertTrue('gallery_view' in pt['Topic'].view_methods)
        self.assertTrue('tabbed_summary_view' in pt['Topic'].view_methods)
        self.assertTrue('slideshow_view' in pt['Topic'].view_methods)
        self.assertTrue('slideshow_preview_view' in pt['Topic'].view_methods)


    def test_get_adapter(self):
        ##Folder
        #tabbed_view
        self.assertEqual(SimpleTabGenerator, type(self.tabbed_view.getAdapter(self.portal.topic)))
        #gallery_view
        #self.assertEqual(GalleryTabGenerator, type(self.gallery_view.getAdapter(self.portal.topic)))
        #tabbed_summary_view
        self.assertEqual(ImagesTabGenerator, type(self.tabbed_summary_view.getAdapter(self.portal.topic)))
        #slideshow_view
        self.assertEqual(SimpleTabGenerator, type(self.slideshow_view.getAdapter(self.portal.topic)))
        #slideshow_preview_view
        self.assertEqual(SimpleTabGenerator, type(self.slideshow_view.getAdapter(self.portal.topic)))        
