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

redomino.tabsandslides.slideshowportlet
----------------------------------------

This is a portlet that show elements of a collection as a slideshow

redomino.tabsandslides.tabsportlet
---------------------------------------

This is a portlet that show elements of a collection using tabs

How to create new views
------------------------

It's easy !!!: You can create a view extending BaseTabbedFolderView (browser/common.py). The view MUST have an interface !!!
Example:
class MySpecialView(BaseTabbedFolderView):
    implements(IMySpecialView)

The template uses this method to getting the objects:
    tal:repeat="content view/getViews

Every object has a tab and a pane (panel)
    tal:content="structure content/tab"
    tal:content="structure content/pane"

How to customize the look and feel of a object inside a container
------------------------------------------------------------------

Each contained object uses a multiadapter to render its own tab and pane. The multiadapter implements ITabGenerator interface and adapts:

- a context
- a container
- a request 
- a view

Watch the "browser/adapters.py" for examples.

Customize javascript configuration
-------------------------------------

The js configuration is overridable (redomino.tabsandslides.config.js).


Javascript documentation
--------------------------

Jcarousel
    - http://sorgalla.com/jcarousel/

JQuerytools tabs
    - http://flowplayer.org/tools/tabs/index.html


Installation
Add the product to buildout as usual.::

    ...
    eggs =
        redomino.tabsandslides
    ...

redomino.tabsandslides shows up in the "Add-ons" configuration panel.


Dependencies
---------------

- Plone 4.x


Credits
----------

Maurizio Lupo <maurizio.lupo@redomino.com> [sithmel], Author - 2011
Giacomo Spettoli <giacomo.spettoli@redomino.com> [giacomos]

TODO
--------

- fix tests
- add new views
- manage image resizing for mobile sites (next releases ...)

