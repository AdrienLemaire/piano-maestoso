//DATA
// We need radius width = radius height
//var border_radius = 170;
// ul.tabs top : 23px
//var keyboard_top = 23;
// space between pianokeys
//var pianokey_margin = 7;
// Nb of pianokey already existing
//var nb_pianokey = 11;
// pianokey width and height
//var pianokey_innerheight = $(".white").outerHeight();
//var pianokey_height = pianokey_innerheight + pianokey_margin;
//var pianokey_white_width = $(".white").outerWidth();
//var pianokey_black_adjust = pianokey_white_width * 0.11; // Why 0.11 ? mystery


// We define some useful variables
//var max_width = $("#body_block").outerWidth() - border_radius;
//var max_height = $("#body_block").outerHeight() - border_radius;
//var rope_length = Math.sqrt(Math.pow(border_radius, 2) * 2);
//var arc_length = 2 * border_radius * Math.asin(rope_length / (2 * border_radius));
//var piano_length = max_height + arc_length + max_width - (nb_pianokey + 1) * pianokey_height;
//var piano_keys_to_add = piano_length / pianokey_height
var pianokey_sounds = Array("b1", "as1", "a1", "gs1", "g1", "fs1", "f1", "e1", "ds1",
        "d1", "cs1", "c1");


/*// We add new pianokeys to fill the piano keyboard*/
//for (i=0; i<piano_keys_to_add; i++) {
    //note_class = pianokey_sounds[i % pianokey_sounds.length];
    //liClass = (note_class.length == 2) ? "white " + note_class: "black " + note_class;
    //$("#right_tabs ul").append("<li class='" + liClass + "'>&nbsp;</li>");
//}


//// Now we'll move and rotate each pianokey
//$("#right_tabs ul>li").each(function(i){
    //// We define the top value of the pianokey
    //pianokey_class = this.classList[0];
    //pianokey_top = i * pianokey_height;
    //diff_max_height = -(max_height - (pianokey_top + 2 * pianokey_innerheight));
    //// We define the value for moving the pianokey to the left
    //pianokey_left = -(max_height - (pianokey_top + 0.5 * pianokey_height));

    //if (diff_max_height < 0) {
        //diff_max_height = 0;
        //pianokey_left = 0;
    //}

    //// Rotation process
    //deg = 0;
    //if (diff_max_height > 0) {
        //// WORKS VERY BADLY
        //if (diff_max_height < pianokey_height) {
            //pianokey_left = 4;
            //pianokey_top += 10;
            //deg = 8;
        //}
        //else if (diff_max_height < pianokey_height * 2) {
            //pianokey_left = 10;
            //pianokey_top += 16;
            //deg = 15;
        //}
        //else if (diff_max_height < pianokey_height * 3) {
            //pianokey_left = 22;
            //pianokey_top += 15;
            //deg = 22;
        //}
        //else if (diff_max_height < pianokey_height * 4) {
            //pianokey_left = 45;
            //pianokey_top += 25;
            //deg = 30;
        //}
        //else if (diff_max_height < pianokey_height * 5) {
            //pianokey_left = (pianokey_class == "white") ? 71: 68;
            //pianokey_top += (pianokey_class == "white") ? 29: 17;
            //deg = 40;
        //}
        //else if (diff_max_height < pianokey_height * 6) {
            //pianokey_left = (pianokey_class == "white") ? 106: 95;
            //pianokey_top += (pianokey_class == "white") ? 25: 16;
            //deg = 51;
        //}
        //else if (diff_max_height < pianokey_height * 7) {
            //pianokey_left = (pianokey_class == "white") ? 145: 136;
            //pianokey_top += (pianokey_class == "white") ? 20: 5;
            //deg = 66;
        //}
        //else if (diff_max_height < pianokey_height * 8) {
            //pianokey_left = (pianokey_class == "white") ? 192: 175;
            //pianokey_top += (pianokey_class == "white") ? 3: -10;
            //deg = 78;
        //}
        //else if (diff_max_height < pianokey_height * 9) {
            //pianokey_left = (pianokey_class == "white") ? 227: 233;
            //pianokey_top += (pianokey_class == "white") ? -17: -23;
            //deg = 85;
        //}
        //// DOESN'T WORK
        ////rad = Math.atan((border_radius - diff_max_height) / diff_max_height);
        ////deg = 90 - rad * (180 / Math.PI);
        ////if (deg > 0 && deg < 90) {
            ////// We ajust the position due to the rotation
            ////arc_distance = border_radius - Math.sqrt(Math.pow((border_radius - diff_max_height), 2) +
                ////Math.pow((pianokey_top - max_height), 2));
            ////// bad guess to arrange a bit the rotation
            ////pianokey_left -= arc_distance / 2;
            ////pianokey_top += arc_distance / 2;
            ////deg = 0.9 * deg; 
        ////}
        ////else if (deg > 90) {
        //else {
            //// deg and pianokey_top are static values
            //lag = ( pianokey_class == "white") ? 0 : pianokey_black_adjust;
            //pianokey_top = max_height + border_radius + pianokey_height - lag;
            //pianokey_left -= lag;
            //deg = 90;
        //}
    //}

    //$(this).enableTransforms();
    //$(this).updateTransform('rotate', 0);

    //// Animation
    //$(this).animate({
        //"top": "+=" + pianokey_top + "px",
        //left: "-=" + pianokey_left + "px",
        //rotate: deg
    //}, 0);
//});


function Setup() {
    //if (!document.getElementById) return;
    for (i=0; i<pianokey_sounds.length; i++) {
        // embed the appropriate sound using document.write
        document.write('<embed id="' + 'note_' + pianokey_sounds[i] + '"');
        document.write(' src="/site_media/static/sounds/' + pianokey_sounds[i] + '.au" width="1" height="1"');
        document.write(' style="position: fixed; top:0" autostart="false" enablejavascript="true">');
    }
    // Set up event handlers and embed the sounds
    pianokeys_li = $(".whitecontainer>div, .blackcontainer>div>div");
    for (i=0; i<pianokeys_li.length; i++) {
        // set up the event handler
        pianokeys_li[i].onmouseover = PlaySound;
    }
}
function PlaySound(e) {
  if (!e) var e = window.event;
  // which key was clicked?
  thiskey = (e.target) ? e.target: e.srcElement;
  // We absolutely need to put the note class in first position !!!
  var sound = document.getElementById("note_" + thiskey.classList[0]);
  try {
    // RealPlayer
    sound.DoPlay();
  } catch (e) {
    try {
      // Windows Media / Quicktime
      sound.Play();
    } catch (e) {
      //alert("No sound support.");
    }
  }
}
//Run the setup routine when this script executes
Setup();
