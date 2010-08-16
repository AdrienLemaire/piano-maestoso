$(function() {
    console.log("yes");     

    $("#right_tabs li").each(function(index) {
        if (index % 2 != 0) {
            $(this).css({
                backgroundColor: "#FFF"
            });
            $(this).children("a").css({
                color: "#000",
            });
        }
    });
});
