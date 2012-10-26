
/*
*
* slideshow
*
*/

jQuery.fn.init_slideshow = function (){
    var context = this,
        config = tabsandslides.slideshow.config,
        slideshow_config = tabsandslides.slideshow.slideshow_config

    jQuery(".slideshow_tabs",context).tabs(".slideshow_panes > div",config).slideshow(slideshow_config);
    jQuery(".slideshow_tabs",context).each(function (){
        if (jQuery(this).data('slideshow')){
            jQuery(this).data('slideshow').play();
        }
    });

    return context;
};


/*
*
* tabs
*
*/

jQuery.fn.init_tabs = function (){
    var context = this,
        config = tabsandslides.tabs.config;

    jQuery(".tabs",context).tabs("> .panes > div",config);
    return context;

};

/*
*
* imagetabs
*
*/

jQuery.fn.init_image_tabs = function (){
    var context = this,
        config = tabsandslides.image_tabs.config,
        config_boxscrollable = tabsandslides.image_tabs.config_boxscrollable;


    jQuery(".imagetabs-tabs",context).tabs("> .imagetabs-panes > div",config);
    jQuery('.imagetabs-tabs',context).jcarousel(config_boxscrollable);

    jQuery('.imagetabs-panes .image > a')
    .prepOverlay({
         subtype:'image',
         urlmatch:'/image$',
         urlreplace:'/image_large'
        });    

    return context;

};

/*
*
* gallery
*
*/

jQuery.fn.init_gallery = function (){
    var context = this;

    jQuery('.imagegallery',context).jcarousel(tabsandslides.gallery.config_boxscrollable);
    return context;

};

/*
*
* slideshow with previews
*
*/

jQuery.fn.init_slideshowpreview = function (){
    var context = this,
        config = tabsandslides.slideshowpreview.config,
        slideshow_config = tabsandslides.slideshowpreview.slideshow_config;

    jQuery(".slideshow_preview_tabs",context).tabs(".slideshow_preview_panes > div",config).slideshow(slideshow_config);
    jQuery(".slideshow_preview_tabs",context).each(function (){
        jQuery(this).data('slideshow').play();
    });


    return context;
};


/*
*
* accordion
*
*/

jQuery.fn.init_accordion = function (){
    var context = this,
        config = tabsandslides.accordion.config || {};

    jQuery(".tabsandslides-accordion",context).accordion(config);
    return context;

};

/*
*
* init
*
*/

(function($){

$(document).ready(function (){
    $(this)
        .init_image_tabs()
        .init_gallery()
        .init_slideshow()
        .init_tabs()
        .init_accordion()
        .init_slideshowpreview();
});


}(jQuery));




