// 
//  jquery.animatecss3.js
//  jQuery Animate for CSS3 Transforms
//  
//  Created by Craig Hoover on 2010-06-15.
//  Copyright 2010 Craig Hoover. All rights reserved.
// 
//  This library augments the current jQuery animate function by adding in the ability to
//  control:
//
//		opacity
//		scale
//    rotate
//
// Outside of the jQuery library.  The current jQuery library does not allow for multiple
// DXTransform filters to be applied but this Plugin does!  
//
// NOTE THAT THIS IS ALPHA CODE!  
//
// There are some issues with Internet Explorer and handling the Matrix when applied
// several times.  If someone would like to contribute in helping, please do.
// 
// NOT SUPPORTED AS OF YET: transform-origin
//

// slightly rewrite how jQuery sets these values
jQuery.extend(jQuery.fx.step, {
	opacity: function( fx ) {		   
		CSS3Transform.__updateTransform.call(fx.elem, fx.prop,fx.now);
	},
	
	scale: function( fx ) {
	   CSS3Transform.__updateTransform.call(fx.elem, fx.prop,fx.now);
	},
	
	rotate: function( fx ) {
	   CSS3Transform.__updateTransform.call(fx.elem,fx.prop,fx.now);
	}
});


// proxy the curCSS function so we can change how opacity is handled
var proxiedCurCSS = jQuery.curCSS;

jQuery.extend({
  curCSS: function( elem, name, force ) {
		if(name.match(/opacity|scale|rotate/))
		{
		   return CSS3Transform.__getTransform.call(elem, name);   		
		}
		else
		{		      		
		   return proxiedCurCSS.apply(elem, arguments);   		   
		}
	}
});   

// our meat and potatoes
var CSS3Transform = {
   
   initialized:false,
   implementation: null,
   dxfilters: ['DXImageTransform.Microsoft.Alpha','DXImageTransform.Microsoft.Matrix'],      
   
   setup:function()
   {
      switch(true)
      {
         case ($.browser.msie): this.implementation = 'msie'; break;
         case ($.browser.webkit): this.implementation = 'webkit'; break;
         case ($.browser.mozilla): this.implementation = 'moz'; break;
      }
      
      CSS3Transform.initialized = true;
   },
   
   filterMap : {
      'opacity': {
         defaultValue:1,
         implementations:{
            'moz': {
               __get:function(){return this.style.MozOpacity}, 
               __set:function(value){ this.style.MozOpacity = value }
            },
            'webkit': {
               __get:function(){ return this.style.opacity}, 
               __set:function(value){ this.style.opacity = value}
            },
            'msie': {
               __get:function(){ return parseFloat(this.filters.item('DXImageTransform.Microsoft.Alpha').opacity)/100},
               __set:function(value){
                  var f = this.filters.item('DXImageTransform.Microsoft.Alpha');
                  f.Opacity = parseFloat(value) * 100;
                  f.enabled = true;
                  f.style = 0;
               }
            }
         }
      },
      'scale': {
         defaultValue:1,
         implementations:{
            'moz' : {
               __get:function(){ 
                  var match = this.style.MozTransform.match(/scale\((.[^\)]*)\)/);
                  if(match[1]) {return match[1] }else{ return CSS3Transform.filterMap['scale'].defaultValue };
               },
               __set:function(value){                      
                  var text = this.style.MozTransform.replace(/^\s+|\s$|none|off/g,'');
                  var value = isNaN(value) ? 'none' : 'scale('+parseFloat(value)+')';
                  var match = text.match(/scale\((.[^\)]*)\)/);
                  this.style.MozTransform = match ? text.replace(/scale\((.[^\)]*)\)/, value) : (text == '' ? value : text + ' '+ value);
               }
            },
            'webkit' : {
               __get:function(){
                  var match = this.style.WebkitTransform.match(/scale\((.[^\)]*)\)/);
                  if(match[1]) { return parseFloat(match[1]) }else{ return CSS3Transform.filterMap['scale'].defaultValue;}                     
               },
               __set:function(value){
                  var text = this.style.WebkitTransform.replace(/^\s+|\s$|none|off/,'');
                  var value = isNaN(value) ? 'none' : 'scale('+parseFloat(value)+')';
                  var match = text.match(/scale\((.[^\)]*)\)/);
                  this.style.WebkitTransform = match ? text.replace(/scale\((.[^\)]*)\)/, value) : (text == '' ? value : text + ' '+ value);                     
               }
            },
            'msie' : {
               __get:function(){
                  var f = this.filters.item('DXImageTransform.Microsoft.Matrix');
                  return this.CSS3Transform['Scale'];      
               },
               __set:function(value){
                  var f = this.filters.item('DXImageTransform.Microsoft.Matrix');
                  var value = parseFloat(value);
                	var M12 = 0, M21 = 0;
                	var curRotate = this.curRotate || 0;
                  this.scaleX = value;
                  this.scaleY = value;                                   
                  
                	if(curRotate > 0)
                	{                     
               		var rad = curRotate * (Math.PI * 2 / 360), costheta = Math.cos(rad), sintheta = Math.sin(rad);
               		var M12 = -sintheta * this.scaleX, M21 = sintheta * this.scaleY, M11 = costheta * this.scaleX, M22 = costheta * this.scaleY;
                  }
                  else
                  {
                     M11 = this.scaleX;
                     M22 = this.scaleY;
                  }
                  
                	f.M11 = M11; // scaling (in all honesty, I still don't get the matrix concept very well)
                	f.M22 = M22; // scaling 
                	f.M12 = M12; // rotating
                	f.M21 = M21; // rotating                  
                	 
                  f.sizingMethod = 'auto expand';   
                  f.enabled = true;             
               }
            }
         }
      },
      'rotate': {
         defaultValue:0,
         implementations:{
            'moz' : {
               __get:function(){
                  var match = this.style.MozTransform.match(/rotate\((.[^\)]*)\)/);
                  if(match[1]) { return parseFloat(match[1]) } else { return CSS3Transform.filterMap['rotate'].defaultValue };                     
               },
               __set:function(value){
                  var text = this.style.MozTransform.replace(/^\s+|\s$|none|off/g,'');
                  var value = isNaN(parseFloat(value)) ? 'none' : 'rotate('+parseFloat(value)+'deg)';                                    
                  var match = text.match(/rotate\((.[^\)]*)\)/);
                  this.style.MozTransform = match ? text.replace(/rotate\((.[^\)]*)\)/, value) : (text == '' ? value : text + ' '+ value);                    
               }
            },
            'webkit' : {
               __get:function(){
                  var match = this.style.WebkitTransform.match(/rotate\((.[^\)]*)\)/);
                  if(match[1]) { return parseFloat(match[1]) } else { returnCSS3Transform.filterMap['rotate'].defaultValue;}                  
               },
               __set:function(value){
                  var text = this.style.WebkitTransform.replace(/^\s+|\s$|none|off/,'');
                  var value = isNaN(parseFloat(value)) ? 'none' : 'rotate('+parseFloat(value)+'deg)';
                  var match = text.match(/rotate\((.[^\)]*)\)/);
                  this.style.WebkitTransform = match ? text.replace(/rotate\((.[^\)]*)\)/, value) : (text == '' ? value : text + ' '+ value);                     
               }
            },
            'msie' : {
               __get:function(){
                  var f = this.filters.item('DXImageTransform.Microsoft.Matrix');
                  return this.scaleX + 'deg';
               },
               __set:function(value){
                  var f = this.filters.item('DXImageTransform.Microsoft.Matrix');
                  var value = parseFloat(value);   
                  this.curRotate = value;
                                 
            		var rad = value * (Math.PI * 2 / 360), costheta = Math.cos(rad), sintheta = Math.sin(rad);
                  
                	this.scaleX	= this.scaleX || 1;
                	this.scaleY	= this.scaleY || 1;
             	
                	f.M11 = costheta * this.scaleX;
                	f.M22 = costheta * this.scaleY;
                	f.M12 = -sintheta * this.scaleX;
                	f.M21 = sintheta * this.scaleY;    
             	
                	this.scaleM11 = f.M11;
                	this.scaleM12 = f.M12;
                	this.scaleM21 = f.M21;
                	this.scaleM22 = f.M22; 

                	f.sizingMethod = 'auto expand'; 
                	f.enabled = true; 
               }
            }
         }
      }
   },

	/*
	 * apply IE transforms to elements per element
	 * @params (element)
	 */
   __setupIETransforms:function()
   {
      var element = $(this);
      var str = '';
      var domel = element.get(0);
      $(CSS3Transform.dxfilters).each(function(){
         str += str != '' ? ' ' : '';
         str += 'progid:'+this+'()';
      });   
      domel.style.filter = str;   
      domel.CSS3Transform = ['Scale','Opacity','Rotate'];
      $.each(element.get(0).filters, function(f){ this.enabled = false; });      
   },     
      
	/*
	 * apply an update to a transform value
	 * @param (element)
	 * @param string name of property
	 * @param integer value of new property
	 */
   __updateTransform : function(name, value){
      if(typeof value != 'undefined')
      {
         var element = $(this).get(0);
         CSS3Transform.filterMap[name].implementations[CSS3Transform.implementation].__set.call(element,value);
      }                
   },   
   
	/*
	 * get value of a transform property
	 * @param (element)
	 * @param string property name
	 * @return string | integer
	 */
   __getTransform: function(name)
   {         
      var element = $(this).get(0);
      return CSS3Transform.filterMap[name].implementations[CSS3Transform.implementation].__get.call(element, name);         
   },

	/*
	 * allow an element to be "transformable"
	 * @param (element)
	 */ 
   __enableTransforms : function(){      
      if(!CSS3Transform.initialized) CSS3Transform.setup();
      $(this).each(function(){
         var element = this, str = '', ops = '';
         if(CSS3Transform.implementation == 'msie') CSS3Transform.__setupIETransforms.call(element);
         $.each(CSS3Transform.filterMap,function(name, obj){
            if(obj.implementations && typeof obj.implementations[CSS3Transform.implementation] != 'undefined')
            {
                $(element).updateTransform(name, obj.defaultValue);
            }
         });         
      });      
   }
}

// attach to jquery
$.fn.enableTransforms = function()
{
	$(this).each(function(){
   	CSS3Transform.__enableTransforms.call(this);
	});
}

// attach to jquery
$.fn.updateTransform = function(filter, value)
{
	$(this).each(function(){
   	CSS3Transform.__updateTransform.call(this, filter, value);	
	});
}

// attach to jquery
$.fn.getTransform = function(filter)
{
	$(this).each(function(){
   	return CSS3Transform.__getTransform.call(this, filter);
	});
}
