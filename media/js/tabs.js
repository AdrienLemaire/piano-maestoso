// Too slow
//$(function() {
//});
//$("#right_tabs li").each(function(index) {
    //if (index % 2 != 0) {
        //$(this).css({
            //backgroundColor: "#FFF"
        //});
        //$(this).children("a").css({
            //color: "#000",
        //});
    //}
//});
$("#tab_inbox").enableTransforms();
$("#tab_inbox").updateTransform('rotate', 0);
$("#tab_inbox").animate({
    rotate: 45,
    "margin-top": "+=50px"
}, 0);
