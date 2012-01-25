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
--------------------------

Show elements inside a folder (or collection) as a slideshow with a tiny preview.


redomino.tabsandslides.portlet
----------------------------------

This is a portlet that show elements of a collection as a slideshow


Customization
--------------

The views can be customized using adapters. Watch the "browser/adapters" folder.
The js configuration is overridable (redomino.tabsandslides.config.js).


Installation
------------

Add the product to buildout as usual.::

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

1. delete most of the adapters (leave some example only)
2. add a series of content type images to use in galleries and tabbed previews
3. substitute adapter with browserviews (In this way I can customize them using a layer interface)
4. modify boxscrollable plugin (remember to keep the tests updated):
    - do not manage left and right buttons 
    - manage scroll using position relative instead scroll
    - implement cycle between images
    - auto resize
5. use only 2 templates, use only 2 class
    - refactor css
    - refactor js
6. use multiadapters to load js (optional)
