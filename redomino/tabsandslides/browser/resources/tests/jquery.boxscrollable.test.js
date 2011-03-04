
// test if the plugin is defined

test('boxscrollable plugin', function (){
    ok(jQuery.fn.boxscrollable,'boxscrollable is defined');
});

jQuery(document).ready(function (){

    // fixed number of items
    jQuery('#container0').boxscrollable({horizontal:false, number_items:2});
    jQuery('#container1').boxscrollable({horizontal:true, number_items:2});

    // fixed size
    jQuery('#container2').boxscrollable({horizontal:false, minheight:120});
    jQuery('#container3').boxscrollable({horizontal:true, minwidth:100});

    var button_h = jQuery('.boxscrollable-prev').outerHeight() + jQuery('.boxscrollable-next').outerHeight();


    test('Elements Width', function (){
        // 300 (width) - 100 (buttons width) / 2 (items) = 100
        equals(jQuery('#container1 > .boxscrollable-wrapper').width(),100,'width elements 1 is ok');
        // 300 (width) - 100 (buttons width) / 2 (items) = 100
        equals(jQuery('#container3 > .boxscrollable-wrapper').width(),100,'width elements 3 is ok');
    });

    test('Elements Height', function (){
        // (hcontainer - buttonh) / numelement
        equals(jQuery('#container0 > .boxscrollable-wrapper').height(),(200 - button_h) / 2,'height elements 0 is ok');
        // (hcontainer(min120) - buttonh) / numelement(1)
        equals(jQuery('#container2 > .boxscrollable-wrapper').height(),200 - button_h,'height elements 2 is ok');
    });



    test('Container Width', function (){
        equals(jQuery('#container0').width(),60,'width container0 is ok');
        equals(jQuery('#container1').width(),100*4,'width container1 is ok');
        equals(jQuery('#container2').width(),60,'width container2 is ok');
        equals(jQuery('#container3').width(),100*4,'width container3 is ok');

    });

    test('Container Height', function (){
        equals(jQuery('#container0').height(),((200 - button_h) / 2 ) * 4,'height container0 is ok');
        equals(jQuery('#container1').height(),60,'height container1 is ok');
        equals(jQuery('#container2').height(),(200 - button_h)*4,'height container2 is ok');
        equals(jQuery('#container3').height(),60,'height container3 is ok');

    });

    test('External Container Width', function (){
        equals(jQuery('#container0').parent().width(),60,'width container0 is ok');
        equals(jQuery('#container1').parent().width(),100*2,'width container1 is ok');
        equals(jQuery('#container2').parent().width(),60,'width container2 is ok');
        equals(jQuery('#container3').parent().width(),100 * 2,'width container3 is ok');

    });

    test('External Container Height', function (){
        equals(jQuery('#container0').parent().height(),200 - button_h,'height container0 is ok');
        equals(jQuery('#container1').parent().height(),60,'height container1 is ok');
        equals(jQuery('#container2').parent().height(),200 - button_h,'height container2 is ok');
        equals(jQuery('#container3').parent().height(),60,'height container3 is ok');

    });


    test('Prev class = disabled', function (){
        jQuery(".boxscrollable-prev").each(function (){
            ok(jQuery(this).hasClass('disabled'),"Prev is disabled");
        });
    });

    test('Next class not disabled', function (){
        jQuery(".boxscrollable-next").each(function (){
            ok(!jQuery(this).hasClass('disabled'),"Next is not disabled");
        });
    });


    asyncTest('Click next', function (){
        jQuery(".boxscrollable-next").click();
        setTimeout(function (){
            var delta = (200 - button_h) / 2;
            equals(jQuery('#container0').parent().scrollTop(),delta);
            equals(jQuery('#container0').parent().scrollLeft(),0);

            equals(jQuery('#container1').parent().scrollLeft(),100);
            equals(jQuery('#container1').parent().scrollTop(),0);

            equals(jQuery('#container2').parent().scrollTop(),delta * 2);
            equals(jQuery('#container2').parent().scrollLeft(),0);

            equals(jQuery('#container3').parent().scrollLeft(),100);
            equals(jQuery('#container3').parent().scrollTop(),0);


            ok(!jQuery('#container0').parent().prev().hasClass('disabled'),"Container 0: Prev is not disabled");
            ok(!jQuery('#container0').parent().next().hasClass('disabled'),"Container 0: Next is not disabled");
            ok(!jQuery('#container1').parent().prev().hasClass('disabled'),"Container 1: Prev is not disabled");
            ok(!jQuery('#container1').parent().next().hasClass('disabled'),"Container 1: Next is not disabled");
            ok(!jQuery('#container2').parent().prev().hasClass('disabled'),"Container 2: Prev is not disabled");
            ok(!jQuery('#container2').parent().next().hasClass('disabled'),"Container 2: Next is not disabled");
            ok(!jQuery('#container3').parent().prev().hasClass('disabled'),"Container 3: Prev is not disabled");
            ok(!jQuery('#container3').parent().next().hasClass('disabled'),"Container 3: Next is not disabled");


            start();
        },1000);
    });

    asyncTest('Click next 2', function (){
        jQuery(".boxscrollable-next").click();
        setTimeout(function (){
            var delta = (200 - button_h) / 2;
            equals(jQuery('#container0').parent().scrollTop(),delta * 2);
            equals(jQuery('#container0').parent().scrollLeft(),0);
            equals(jQuery('#container1').parent().scrollLeft(),200);
            equals(jQuery('#container1').parent().scrollTop(),00);
            equals(jQuery('#container2').parent().scrollTop(),delta * 4);
            equals(jQuery('#container2').parent().scrollLeft(),0);
            equals(jQuery('#container3').parent().scrollLeft(),200);
            equals(jQuery('#container3').parent().scrollTop(),0);

            ok(!jQuery('#container0').parent().prev().hasClass('disabled'),"Container 0: Prev is not disabled");
            ok(jQuery('#container0').parent().next().hasClass('disabled'),"Container 0: Next is disabled");
            ok(!jQuery('#container1').parent().prev().hasClass('disabled'),"Container 1: Prev is not disabled");
            ok(jQuery('#container1').parent().next().hasClass('disabled'),"Container 1: Next is disabled");
            ok(!jQuery('#container2').parent().prev().hasClass('disabled'),"Container 2: Prev is disabled");
            ok(!jQuery('#container2').parent().next().hasClass('disabled'),"Container 2: Next is disabled");
            ok(!jQuery('#container3').parent().prev().hasClass('disabled'),"Container 3: Prev is not disabled");
            ok(jQuery('#container3').parent().next().hasClass('disabled'),"Container 3: Next is disabled");

            start();
        },1000);
    });

    asyncTest('Click previous', function (){
        jQuery(".boxscrollable-prev").click();
        setTimeout(function (){
            var delta = (200 - button_h) / 2;
            equals(jQuery('#container0').parent().scrollTop(),delta);
            equals(jQuery('#container0').parent().scrollLeft(),0);

            equals(jQuery('#container1').parent().scrollLeft(),100);
            equals(jQuery('#container1').parent().scrollTop(),0);

            equals(jQuery('#container2').parent().scrollTop(),delta * 2);
            equals(jQuery('#container2').parent().scrollLeft(),0);

            equals(jQuery('#container3').parent().scrollLeft(),100);
            equals(jQuery('#container3').parent().scrollTop(),0);


            ok(!jQuery('#container0').parent().prev().hasClass('disabled'),"Container 0: Prev is not disabled");
            ok(!jQuery('#container0').parent().next().hasClass('disabled'),"Container 0: Next is not disabled");
            ok(!jQuery('#container1').parent().prev().hasClass('disabled'),"Container 1: Prev is not disabled");
            ok(!jQuery('#container1').parent().next().hasClass('disabled'),"Container 1: Next is not disabled");
            ok(!jQuery('#container2').parent().prev().hasClass('disabled'),"Container 2: Prev is not disabled");
            ok(!jQuery('#container2').parent().next().hasClass('disabled'),"Container 2: Next is not disabled");
            ok(!jQuery('#container3').parent().prev().hasClass('disabled'),"Container 3: Prev is not disabled");
            ok(!jQuery('#container3').parent().next().hasClass('disabled'),"Container 3: Next is not disabled");

            start();
        },1000);
    });

});




