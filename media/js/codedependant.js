
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
					'z-index': 999,
					events: {
						dblclick: function(e){
							this.options.closeable ? this.hide() : false;
						}.bind(this)
					}
				}
			});
		},
		TrackInstances:false,
		show:function( options ){
			if( options ){ 
				this.setOptions( options );
			}			
			this.element.inject(this.options.element,'top').fade( this.options.opacity );
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
		options:{
		  title:"Modal Box",
		  stage:"<p>hello</p>",
      className: 'smallBox',
      isMaskOn: false,
      onBoxopen: $empty,
      onBoxclose: $empty		  
		},
		initialize:function(options){
			this.setOptions(options);
			this.parent(options);
		},	
		build:function(){
          var m, dim, yscroll, box, titleBar, closebutton, stagewrap, stagecontainer, stage;
          m = this.options._mask;
          dim = getScrollSize();
          //check for fuggin IE people...
          yScroll = self.pageYOffset ? self.pageYOffset : document.documentElement.scrollTop;
          //primary container 
          box = new Element('div', {
              id: 'modalbase',
              styles: {
                  position: 'absolute',
                  top: yScroll + 50, //the users eys tend to reside about 1/3 of the way down.
                  padding: '5px',
                  'z-index': 1000,
                  opacity: 0
              },
              events: {
                  dblclick: function(e){
                      if (this.options.closeable) {
                          this.hide();
                          this.hideBox();
                      }
                  }.bind(this)
              }
          
          });
          
          if (this.options.className) {
              box.addClass(this.options.className);
          }
          box.setStyle('left', (window.getSize().x /2 - box.getSize().x))
          titleBar = new Element('h2', {
              'class': 'title draggable',
              html: this.options.title || ''
          }).inject(box,'top');
          stagewrap = new Element('div', {
              id: "stagewrap",
              'class': 'bg-deep p_all-8'
          }).inject(box);
          stagecontainer = new Element('div', {
              id: 'stagecontainer'
          }).inject(stagewrap);
          stage = new Element('div', {
              id: 'stage',
              'class': 'bg-med border-light p_all-4'
          }).inject(stagecontainer);
          //inject everything into the 'box'
          
          // set the stage contents and save to object
          stage.set('html', this.options.stage || '');
          
          this.setOptions({
              stage: stage,
              titleBar: titleBar,
              modalBox: box,
              closebutton: closebutton
          });
          box.inject(document.body,'top');
          box.setStyle('left', (dim.x / 2) - (box.getSize().x / 1.5));
          new Drag(box, {
              handle: titleBar
          });
		
		}.protect(),
    showBox: function(options){
        if (options) {
            this.setOptions(options);
        }
        this.build();
        this.show();
        this.options.modalBox.fade('in');
        this.setOptions({
            isMaskOn: true
        });
    },
    hideBox: function(){
        this.options.modalBox.fade('out');
        this.hide();
        this.options.modalBox.dispose();
        //            this.hide.delay(1500);
        this.destroy.delay(700, this);
    },		
	});	
	window.cDependant = _cdependant;	
})(window);

document.id(window).addEvent('domready', function(){
  new Fx.SmoothScroll({
    links:'.smoothscroll'
  })
});
