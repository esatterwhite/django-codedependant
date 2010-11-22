
Class.Mutators.TrackInstances = function(track){
	if(!track) return;
	
	var oldInit = this.prototype.initialize;
	var klass = this;
	
	klass.prototype.initialize = function(){
		(klass.instances = klass.instances || []).push(this);
		oldInit.apply( this, arguments);	
	};
};
Array.implement({
	rgbToHex:function(){
		var r = this[0];
		var g = this[1];
		var b = this[2];

		function intToHex(dec){
			var result = (parseInt(dec, 10).toString(16));
			if (result.length == 1) {
				result = ("0" + result);
			}
			return result.toUpperCase();
		}
		
		return "#"+(intToHex(r) + intToHex(g) + intToHex(b));		
	}
});

(function(window, undefined){
	var _cdependant = window.cDependant || {};
	_cdependant.Overlay = new Class({
		Implements:[Events, Options],
		options:{
			bgColor:'#000000',
			opacity:0.6,
			closeable:false,
			element:document.body
		},
		element:null,
		initialize:function(options){
			this.setOptions(options);
			this.element = new Element('div',{
				id:String.uniqueID(),
				styles: {
					position: 'fixed',
					height: '100%',
					width: '100%',
					'background-color': this.options.bgColor,
					opacity: 0,
					top:0,
					left:0,
					'z-index': 9999,
					events: {
						'dblclick': function(e){
							this.options.closeable ? this.hide() : false;
						}.bind(this)
					}
				}
			}).inject(this.options.element,'top');
		},
		TrackInstances:false,
		show:function( options ){
			if( options ){ 
				this.setOptions( options );
			}			
			this.element.fade( this.options.opacity );
			return this;
		},
		hide:function(){
			this.element.fade('out');
			return this;
		},
		destroy:function(){
			this.element.dispose();	
		}
		
	});
	
	_cdependant.ModalBox = new Class({
		Extends:_cdependant.Overlay,
		Implements:[Events, Options],
		options:{},
		initialize:function(options){
			this.setOptions(options);
			this.parent(options);
			this.build();
		},	
		build:function(){
			
		}.protect()
		
	});	
	window.cDependant = _cdependant;	
})(window);

