A collection of useful views
===================================
The main purpose of this product is to provide series of useful views (and a portlet).
Every view can be applied to a folder or a collection.

gallery_view
--------------
Show elements inside a folder (or collection) in a gallery.

tabbed_view
--------------
Show elements inside a folder (or collection) inside tabs.

tabbed_summary_view
----------------------
Show elements inside a folder (or collection) inside tabs. Instead of strings each tab can be a structure of html (scrollable)

slideshow_view
------------------
Show elements inside a folder (or collection) as a slideshow.

slideshow_preview_view
------------------
Show elements inside a folder (or collection) as a slideshow with a tiny preview.


redomino.tabsandslides.portlet
----------------------------------
This is a portlet that show elements of a collection as a slideshow


How to create new views
------------------------
It's easy !!!: create a view extending BaseTabbedFolderView (browser/common.py). The view MUST has an interface !!!
Example:
class MySpecialView(BaseTabbedFolderView):
    implements(IMySpecialView)

The template uses this method to getting the objects:
    tal:repeat="content view/getViews

Every object has a tab and a pane (panel)
    tal:content="structure content/tab"
    tal:content="structure content/pane"

How to customize the way the container objects look
----------------------------------------------------
Each contained object uses a multiadapter to render its own tab and pane. The multiadapter implements ITabGenerator interface and adapts:
- a context
- a container
- a request 
- a view

Watch the "browser/adapters.py" for examples.

Customize javascript configuration
-------------------------------------
The js configuration is overridable (redomino.tabsandslides.config.js).


Installation
------------
Add the product to buildout as usual.


....
eggs =
    redomino.tabsandslides
...

redomino.tabsandslides shows up in the "Add-ons" configuration panel.


Dependencies
------------

- Plone 4.x


Credits
-------

Created by Maurizio Lupo for redomino in 2011.

TODO
--------
- Replace boxscrollable plugin with jcarousel
- Replace slideshow plugin with something better
- manage image resizing for mobile sites
- add views: better gallery, box view
- fix portlet (crash editing properties )
- Download panes when requested with ajax (and add a js hook to execute javascript code on pages)

