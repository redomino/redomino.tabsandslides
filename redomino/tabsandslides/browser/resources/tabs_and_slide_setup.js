/*
*
* slideshow
*
*/

jQuery.fn.init_slideshow = function (){
    var context = this;
    var config = {
	    // enable "cross-fading" effect
	    effect: 'fade',
	    fadeOutSpeed: "slow",
	    rotate: true
    };

    jQuery(".slideshow_tabs",context).tabs(".slideshow_panes > div",config).slideshow({clickable:false});
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
    var config = {
        onClick: function(event, tabIndex) {

		    // the "this" variable is a pointer to the API. You can do a lot with it.
		    var tabPanes = this.getPanes();

             /*
             By returning false here the default behaviour is cancelled.
            This time another tab cannot be clicked when "terms" are not accepted
            */
            tabPanes.each(function (index){

                var $st = jQuery(this).find('.slideshow_tabs');
                if (! $st.length){
                    return
                }
                if(index === tabIndex){
                    $st.data('slideshow').play();
                }
                else {
                    $st.data('slideshow').stop();
                }
            });
	    }    
    };


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
    var config = {
        onClick: function(event, tabIndex) {

		    // the "this" variable is a pointer to the API. You can do a lot with it.
		    var tabPanes = this.getPanes();

             /*
             By returning false here the default behaviour is cancelled.
            This time another tab cannot be clicked when "terms" are not accepted
            */
            tabPanes.each(function (index){

                var $st = jQuery(this).find('.slideshow_tabs');
                if (! $st.length){
                    return
                }
                if(index === tabIndex){
                    $st.data('slideshow').play();
                }
                else {
                    $st.data('slideshow').stop();
                }
            });
	    }    
    };


    jQuery(".imagetabs-tabs",context).tabs("> .imagetabs-panes > div",config);
    jQuery('.imagetabs-tabs',context).boxscrollable({horizontal:true,
//                                                     number_items:4, 
                                                     minheight:200, 
                                                     minwidth:220,
                                                     easing:'easeInOutCirc'});
    return context;

};

/*
*
* imagetabs
*
*/

jQuery.fn.init_gallery = function (){
    var context = this;

    jQuery('.imagegallery',context).boxscrollable({horizontal:true,
//                                                     number_items:4, 
                                                     minheight:200, 
                                                     minwidth:210,
                                                     easing:'easeInOutCirc'});
    return context;

};


/*
*
* init
*
*/

(function($){
$(document).ready(function (){
    $(this).init_slideshow().init_tabs().init_image_tabs().init_gallery();
});
})(jQuery);


