(function ($){

$(document).ready(function (){

$('#formfield-form-talexp').each(function (){

    var $this = $(this),
        $input = $this.find('input'),
        $menu = $('<div class="talexp_help" />').load('@@talexp_portlet_help').hide().appendTo($this);

    $menu.click(function (evt){
        var $target = $(evt.target);
        if ($target.is('dt')){
            $input.val($target.next('dd').text());
//            $menu.fadeOut('fast');
        }
        
    });

    $input
    .attr('autocomplete','off')
    .focus(function (){
       $menu.fadeIn('fast');
    })
    .blur(function (){
       setTimeout(function (){
           $menu.fadeOut('fast');
       }, 200);
    });

});

});

}(jQuery));
