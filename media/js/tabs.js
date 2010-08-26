//DATA
// We need radius width = radius height
var border_radius = 170;
// ul.tabs top : 23px
var keyboard_top = 23;
// space between pianokeys
var pianokey_margin = 7;
// Nb of pianokey already existing
var nb_pianokey = 11;
// pianokey width and height
var pianokey_height = $(".white").outerHeight();
var pianokey_white_width = $(".white").outerWidth();
var pianokey_black_width = pianokey_white_width * 0.6;


// We define some useful variables
var max_width = $("#body_block").outerWidth() - border_radius;
var max_height = $("#body_block").outerHeight() - border_radius;
var rope_length = Math.sqrt(Math.pow(border_radius, 2) * 2);
var arc_length = 2 * border_radius * Math.asin(rope_length / (2 * border_radius));
var piano_length = max_height + arc_length + max_width - (nb_pianokey + 1) * (pianokey_height + pianokey_margin);


// We add new pianokeys to fill the piano keyboard
for (i=0; i<piano_length; i=i+pianokey_height+pianokey_margin) {
    liClass = "black";
    if (i % ((pianokey_height+pianokey_margin) * 2) == 0) {
        liClass = "white";
    }
    $("#right_tabs ul").append("<li class='" + liClass + "'>&nbsp;</li>");
}


// Now we'll move and rotate each pianokey
$("#right_tabs ul>li").each(function(i){
    // We define the top value of the pianokey
    pianokey_top = i * (pianokey_height + pianokey_margin);
    diff_max_height = -(max_height - (pianokey_top + pianokey_height));
    if (diff_max_height < 0) {
        diff_max_height = 0;
    }

    // We define the value for moving the pianokey to the left
    pianokey_left = diff_max_height;
    
    // Rotation process
    deg = 0;
    if (diff_max_height > 0) {
        rad = Math.atan((border_radius - diff_max_height) / diff_max_height);
        deg = 90 - rad * (180 / Math.PI);
        if (deg > 0 && deg < 90) {
            // We ajust the position due to the rotation
            // TODO NOT WORKING !!!
            arc_distance = border_radius - Math.sqrt(Math.pow((border_radius - diff_max_height), 2) +
                Math.pow((pianokey_top - max_height), 2));
            pianokey_left -= arc_distance;
            pianokey_top += arc_distance;
        }
        else if (deg > 90) {
            // deg and pianokey_top are static values
            lag = 0;
            if (pianokey_top % ((pianokey_height + pianokey_margin) * 2) == 0) {
                lag = (pianokey_white_width - pianokey_black_width) / 4;
            }
            pianokey_top = max_height + border_radius + pianokey_height + pianokey_margin - lag;
            pianokey_left -= lag;
            deg = 90;
        }
    }

    $(this).enableTransforms();
    $(this).updateTransform('rotate', 0);

    // Animation
    $(this).animate({
        "top": "+=" + pianokey_top + "px",
        left: "-=" + pianokey_left + "px",
        rotate: deg
    }, 0);
});
