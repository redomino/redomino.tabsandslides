/*
*
* slideshow
*
*/

jQuery.fn.init_slideshow = function (){
    var context = this;
    var config = tabsandslides.slideshow.config;
    var slideshow_config = tabsandslides.slideshow.slideshow_config

    jQuery(".slideshow_tabs",context).tabs(".slideshow_panes > div",config).slideshow(slideshow_config);
    jQuery(".slideshow_tabs",context).each(function (){
        jQuery(this).data('slideshow').play();
    });

    return context;
};


/*
*
* tabs
*
*/

jQuery.fn.init_tabs = function (){
    var context = this;
    var config = tabsandslides.tabs.config;

//    jQuery(".tabs",context).tabs("div.panes > div",config);
    jQuery(".tabs",context).tabs("> .panes > div",config);
    return context;

};

/*
*
* imagetabs
*
*/

jQuery.fn.init_image_tabs = function (){
    var context = this;
    var config = tabsandslides.image_tabs.config;
    var config_boxscrollable = tabsandslides.image_tabs.config_boxscrollable;


    jQuery(".imagetabs-tabs",context).tabs("> .imagetabs-panes > div",config);
    jQuery('.imagetabs-tabs',context).jcarousel(config_boxscrollable);
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
    var context = this;
    var config = tabsandslides.slideshowpreview.config;
    var slideshow_config = tabsandslides.slideshowpreview.slideshow_config

    jQuery(".slideshow_preview_tabs",context).tabs(".slideshow_preview_panes > div",config).slideshow(slideshow_config);
    jQuery(".slideshow_preview_tabs",context).each(function (){
        jQuery(this).data('slideshow').play();
    });

    return context;
};

/*
*
* init
*
*/

(function($){
$(document).ready(function (){
    $(this).init_slideshow().init_tabs().init_image_tabs().init_gallery().init_slideshowpreview();
});
})(jQuery);


