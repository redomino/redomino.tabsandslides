A collection of useful views and portlets
=========================================

The main purpose of this product is to provide series of useful views and portlets.
Each of these can be applied to a folder or a collection.

Views
--------------

- **Gallery**: A scrollable carousel.
- **Tabs**: Show the contents inside a tab.
- **Accordion**: Show the contents inside an accordion.
- **Gallery with preview (image top)**: A scrollable carousel that shows a preview of each content.
- **Gallery with preview (image bottom)**: A scrollable carousel that shows a preview of each content.
- **Slideshow**: Shows elements inside a folder (or collection) as a slideshow.

Portlets
------------
This product provides three portlets. For each portlet you can choose among many different views:

- **Gallery**
- **Tabs**
- **Accordion**
- **Slideshow**
- **Gallery with preview (image top)**
- **Gallery with preview (image bottom)**
- **List of items**
- **All items**

The portlets are:

- **TabsAndSlides Collection portlet**: Show the items of a collection. 
- **TabsAndSlides Content portlet**: Show items with a certain ID inside a certain context (usually a folderish object). If the item is a Folder or a collection it returns the contained items.
- **TabsAndSlides Tal portlet**: Show the items using a TAL expression. This expression can return a list of brain of a list of objects. This is a good reference: http://www.owlfish.com/software/simpleTAL/tal-guide.html

For each of that portlet you can limit the elements to be shown, randomize the order of the items, show or not the border of the portlet.

Customize the views
-------------------

It's very easy to customize the look and feel of the views !!!
For example each of the content use a browserview to show its representation. The browserview are registered in the adapters.zcml (inside the browser package)::

    <browser:page
        for="*"
        name="gallery_adapter"
        class=".adapters.Gallery"
        permission="zope2.View"
        />

You can customize the apperance using a more specific Interface::

    <browser:page
        for=".interfaces.IMyCustomContent"
        name="gallery_adapter"
        template="mygallery_adapter.pt"
        permission="zope2.View"
        />

or a layer interface::

    <browser:page
        for="*"
        name="gallery_adapter"
        template="mygallery_adapter.pt"
        permission="zope2.View"
        layer=".interfaces.IThemeSpecific"
        />

Customize javascript configuration
-------------------------------------

The js configuration is overridable (redomino.tabsandslides.config.js).


Javascript documentation
--------------------------

Jcarousel
    - http://sorgalla.com/jcarousel/

JQuerytools tabs
    - http://flowplayer.org/tools/tabs/index.html

JQueryUI
    - http://jqueryui.com/

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
- collective.js.jqueryui

Credits
----------

Author
    - Maurizio Lupo <maurizio.lupo@redomino.com> [sithmel]

Contributors
    - Giacomo Spettoli <giacomo.spettoli@redomino.com> [giacomos]


