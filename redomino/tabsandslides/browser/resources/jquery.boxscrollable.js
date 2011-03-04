/*
*
* boxscrollable
* by Maurizio Lupo
*
* TODO: rotate
*
*/

jQuery.fn.boxscrollable = function (settings){
    var default_config = {
        minheight:null, // get automatically
        minwidth:null, // get automatically
        horizontal: false, //  vertical
        number_items: null, // get automatically from container
        maxbuttonwidth:50, // the max buttons size (it's better to use css)
        rotate: false, // not yet implemented
        easing: 'swing', 
        duration: 'slow'
    }
    var config = jQuery.extend(default_config,settings);

    return this.each(function (index){
        var $this = jQuery(this);
        //$this is my container
        //get the containers
        var $containers = $this.children();
        var max_h = 0, max_w = 0;
        //wrap the external container        
        var $external_wrapper = $this.wrap('<div class="boxscrollable-external-wrapper" />').parent();
        var $next_button = $external_wrapper.after('<div class="boxscrollable-next">next</div>').next();
        var $prev_button = $external_wrapper.before('<div class="boxscrollable-prev">prev</div>').prev();

        if ($next_button.outerWidth() > config.maxbuttonwidth){
            $next_button.css('width', config.maxbuttonwidth + "px");
        }
        if ($prev_button.outerWidth() > config.maxbuttonwidth){
            $prev_button.css('width', config.maxbuttonwidth + "px");
        }

        // set the index
        var index = 0;
        // the animation
        var animate = function (){
            if(config.horizontal){
                $external_wrapper.animate({scrollLeft: index * max_w}, config.duration, config.easing);
            }
            else{
                $external_wrapper.animate({scrollTop: index * max_h}, config.duration, config.easing);
            }
        };

        //get the bigger width and heigth
        $containers.each(function (){
            var $this = jQuery(this);
            var w = $this.outerWidth();
            var h = $this.outerHeight();

            if (w > max_w){
               max_w = w;
            }
            if (h > max_h){
               max_h = h;
            }
        });
        // configuration override what I have discovered
        if(config.minheight){
            max_h = config.minheight;
        }
        if(config.minwidth){
            max_w = config.minwidth;
        }

        // ******************************
        // get container size
        var container_width = $this.outerWidth();
        var container_height = $this.outerHeight();
        var buttons_width = $next_button.outerWidth() + $prev_button.outerWidth();
        var buttons_height = $next_button.outerHeight() + $prev_button.outerHeight();
        
        if(config.horizontal){ //fix prev and next
            container_width = container_width - buttons_width;
        }
        else {
            container_height = container_height - buttons_height;
        }
        // ******************************

        // set the number of items
        if(! config.number_items){ // if number item is not fixed set it to the max possible number 
            if(config.horizontal){
                config.number_items = Math.floor(container_width / max_w);
            }
            else{
                config.number_items = Math.floor(container_height / max_h);
            }
        }

        if(config.horizontal){ // override max_w or max_h
            max_w = Math.floor(container_width / config.number_items);
        }
        else{
            max_h = Math.floor(container_height / config.number_items);
        }
        
        //wrap every container
        $containers.each(function (){
            var $this = jQuery(this);
            
            var $wrapper = $this.css('margin','auto') // center the container
                .wrap('<div class="boxscrollable-wrapper" />').parent(); //wrap the container and get it
            
            if(config.horizontal){ 
                $wrapper.width(max_w); //set the dimensions
                $external_wrapper.css('float','left');
                $next_button.css('float','left');
                $prev_button.css('float','left');
                $wrapper.css('float','left');
            }
            else {
                $wrapper.height(max_h);
            }
            
        });

        //assuming wrapper has no border, padding, margin = 0
        if(config.horizontal){
            $this.width(max_w * $containers.length);
            $this.height(max_h);
            $external_wrapper.width(max_w * config.number_items);
//            $external_wrapper.height(max_h);
        }
        else {
            $this.width(max_w );
            $this.height(max_h* $containers.length);            
            $external_wrapper.width(max_w );
            $external_wrapper.height(max_h * config.number_items);            
        }
        $external_wrapper.css('overflow','hidden'); // test

        $prev_button.addClass('disabled');
        if((index + config.number_items) >= $containers.length){
            $next_button.addClass('disabled');
        }

        var enable_disable_buttons = function (){
            if(index <= 0){
                $prev_button.addClass('disabled');
            }
            else {
                $prev_button.removeClass('disabled');
            }

            if((index + config.number_items) >= $containers.length){
                $next_button.addClass('disabled');            
            }
            else {
                $next_button.removeClass('disabled');            
            }
        }

        $next_button.click(function (){
            if((index + config.number_items) < $containers.length){
                index += 1;
                enable_disable_buttons();
                animate();
            }
            
        });

        $prev_button.click(function (){
            if(index > 0){
                index -= 1;
                enable_disable_buttons();
                animate();
            }
        });

        
    });
};
