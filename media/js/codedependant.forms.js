
(function(window, undefined){
	var _cdependant = window.cDependant || {};
	_cdependant.Forms = {};
	
	/**
	 * @classDescription: gathers elements matching the passed in CSS selector
	 * 					  removes the value of the element on focus and replaces it
	 * 					  on blur if the user has not entered in any data
	 */
	_cdependant.Forms.FormFocus = new Class({
		Implements:[Events, Options],
		options:{
			formID:null,
			submitID:null,
			errorClass:'',
			handleSubmit:true,
			placeHolderText:'Start Here...',
			onInvalid:Function.from(),
			onValid:Function.from(),
			onFieldFocus:Function.from(),
			onFieldBlur:Function.from()
		},
		initialize:function(selector, options){
			var els, that = this;			
			this.el = document.id(selector);
			this.setOptions(options);
			
			
				this.el.store('initial', that.options.placeHolderText);
				if (this.el.get('value') === "") {
					this.el.set('value',that.options.placeHolderText);
				}
				
				this.el.addEvents({
					focus:function(evt){
						that.set(this);
						if(that.options.formID){
							document.id(that.options.formID).removeClass(that.options.errorClass);
						}
						that.fireEvent('fieldFocus', this);
					},
					blur:function(evt){
						that.reset(this);				
						that.fireEvent('fieldBlur', this);		
					},
					keypress:function(evt){
					if(evt.keyCode === 13 && that.options.handleSubmit){
						evt.stop();
						if (that.validate()) {							
								document.id(that.options.formID).submit();
							}else {
								that.reset(this);
								//el.select();
								return false;
							}
						}		
						
					}
				});			
		},
		set:function(el){
			var e,value, stored;
			
			value = el.get('value');
			stored = el.retrieve('initial');
			if(value.trim() == stored){
				el.set('value');
			}			
		},
		reset:function(el){
			var value, stored;
		
			value = el.get('value').trim();
			stored = el.retrieve('initial');
			
			if (value === ''){
				el.set('value', stored);
			}
		},
		validate:function(){
			var valid = true, val, that = this;
				this.els.each(function(el, index, arr){
				val = el.get('value');
				if (val !== el.retrieve('initial') && val !== '') {
					that.fireEvent('valid');
					valid = true;
				}else{
					valid = false;
					that.fireEvent('invalid');
				}
			});
			return valid;
		},
		toElement:function(){
			return this.els;
		}
	});
	_cdependant.Forms.ValidationQueue = new Class({
		Implements:[Events, Options],
		options:{
			inlineMessages:true,
			onInvalid:Function.from(),
			onValid:Function.from()
		},
		initialize:function(formSelector, validators,options){
			var that = this;
			this.setOptions(options);
			this.queue = validators || [];
			this.form = document.id(formSelector);
			this.form.addEvent('submit',function(evt){ 
				return that.validateForm(that.options.inlineMessages, evt);
			});
		},
		validateForm:function(hardNotice, evt){
			var valid, _notify, invalids, formValid;
			invalids = [];
			valid = formValid= true;			
			_notify = hardNotice || false;
			this.queue.each(function(item, index){
				item.reset();
				valid = item.isValid();
				if(!valid && item.enabled){
					invalids.push(item);					
					formValid = false;				
				}								
				item.validate(_notify);							
			}.bind(this));
			if(invalids.length>0){
				this.fireEvent('invalid', [invalids]);
			}else{
				this.fireEvent('valid', evt);
			}
			return formValid;
		},
		register:function(validator){
			if($type(validator === 'array')){
				validator.each(function(item, index){
					this.queue.push(item);
				}.bind(this));
			}else{
				this.queue.push(validator);	
			}			
		}		
	});
	/**
	 * @classDescription provides the abilty to validate form fields and display the reults in a variety of ways
	 * 					 field validators can be run against each other and use other validators in their own validation
	 */
	_cdependant.Forms.FieldValidator = new Class({
		Implements:[Events, Options],
		
		/**
		 * @property {Regex || Function} validation:  the validation to test user input against. must return true/false
		 * @property {Boolean}  required: 	   	      if not required, empty values are allowed, but is still run against validation, and can be invalid...
		 * @property {String}   errorClassName:       Name of the css class to be applied as an indication of an error
		 * @property {Object}   errors:		          object containing the error messages to display ( required, invalid, formal )
		 * @property {String} 	cleanUp:		      when reset is call, elements matching this css selector will be removed
		 * @property {String}   errorMsg:      	      the default error message if none have been specified
		 * @property {Boolean}  notifications: 	      Whether to display notification messages in the form
		 * @property {Boolean}  inlineWarning:        whether or not to validate as the user types
		 * @method   {Function} onValid:       	      the function to be run when the field is deemed valid
		 * @method   {Function} onInvalid:     	      the function to be run when the field is deemed invalid
		 * @method   {Function} onFieldBlur:   	      the function to be run when the focus leaves the field
		 */
		options:{
			validation:/\w+/,			
			required:false,
			errorClassName:'error',
			errors:{
				required:'This field is required',
				invalid:'The value you entered is invalid',
				formal:'this is your final warning'
			},
			errorMsg:'This is wrong',
			cleanUp:null,				// css selector of elements you want removed when element is reset
			notifications:true,			// show validation messages in form
			inlineWarning:true,			// run validation as user types and adds errorClassName
			onValid:Function.from(),
			onInvalid:Function.from(),
			onFieldBlur:Function.from(),
			onFieldFocus:Function.from()
		},
		/**
		 * @constructor
		 * @param {String} selector: ID of DOM element to watch
		 * @param {Object} options
		 */
		
		initialize:function(selector, options){
			var that = this;
			this.setOptions(options);
			this.EMPTY_VALUES = [null,''];
			this.element = document.id(selector);
			this.notified = false;
			this._error = null;
			this.warned = false;
			this.setEvents();
			this.enabled = true;
		},
		TrackInstances:true,
		setEvents:function(){
			var that = this;
			this.element.addEvents({
				focus:function(){
					that.reset.bind(that);
					that.fireEvent('fieldFocus', that.element);
				},
				blur:function(){
					if(that.options.inlineWarning){
						that.validate(that.options.notification);
					}	
					that.fireEvent('fieldBlur',[that.element, that.isValid()]);
				},
				keyup:function(){
					if ( that.options.inlineWarning ){
						that.validate();	
					}	
				}
			});
		}.protect(),
		/**
		 * @method Runs validation with out any notifications/warnings.
		 * @return {Boolean} true if passes validation.
		 */
		isValid:function(){
			var valid;
			// if not required AND the field is empty
			if ( !this.options.required && this.EMPTY_VALUES.contains(this.element.get('value') ) ){
				this._error = null; 
				return true;
			}
			// if the field is required AND the field is empty
			if( this.options.required && this.EMPTY_VALUES.contains(this.element.get('value')) ){
				this._error='required';
				return false;
			}
			if (typeOf(this.options.validation) == 'function') {
				valid =  this.options.validation.attempt();
			}
			else {
				valid = this.options.validation.test(this.element.get('value').trim());
			}
			
			if(!valid){this._error = 'invalid';}
			return valid;
		},
		/**
		 * @method runs validation and dispatches events. if enabled and required will inject DOM messages 
		 * @param {Boolean} warn if true will add the appropriate class to indicate validation failed
		 * @return{Boolean} returns true if field passes validation
		 */
		validate:function(warn){
			var valid ;
			valid = this.isValid();
			if (valid) {				
				this.fireEvent('valid', this.element);
			}
			else {
				this.fireEvent('invalid', this.element);
				if(this.enabled ){
					this.toElement().getParent().addClass(this.options.errorClassName);
					this.warned = true;
					if(warn){
						this.notify();
					}
				}
			}				
			return valid;
		},
		/**
		 * @method constructs HTML messages based on criteria and injects them into the 
		 * 		   DOM under the element in question
		 */
		notify:function(){
			if(this.notified){return false;}
			var elID, response, that = this;
			if(this.EMPTY_VALUES.contains(this.element.get('value'))){
				response = '<li>{required}</li>'.substitute(that.options.errors);
			}else{
				response = '<li>{invalid}</li>'.substitute(that.options.errors);	
			}
			new Element('ul',{
				className:'errors',
				id:'',
				html: response
			}).inject(that.element,'after');
			this.notified = true;
			return this;
		},
		/**
		 * @method removes any error messages it may have injected into the DOM
		 * 		   and removes the error class from the eleemnt
		 * 
		 * 		   DOES NOT ALTER THE TEXT/VALUE OF THE INPUT
		 */
		reset:function(){
			var that = this;
			this.element.getParent().removeClass(this.options.errorClassName);
			this.element.getSiblings(this.options.errorClassName).destroy();
			
			//jQuery(this.options.identifier).slideUp().remove();
			this.notified = this.warned = false;
			if(this.options.cleanUp){
				this.clean();
			}
			return this;
		},
		toElement:function(){
			return this.element;
		},
		isRequired:function(){
			return this.options.required;
		},
		/**
		 * @method public facing way to get the current error message after validation
		 */
		getErrorMessage:function(){
			return this.options.errors[this._error] || null;
		},
		/**
		 * @method removes siblings of this element who matches the css selector specified in options.cleanUp
		 */
		clean: function(){
			jQuery(this.element.parent().siblings(this.options.cleanUp)).remove();
		},
		/**
		 * @method disables any validation messaging
		 * but can still run validation
		 */
		disable:function(){
			this.enabled = false;
			return this;
		},
		/**
		 * @method enables validation messaging
		 */
		enable:function(){
			this.enabled = true;
			return this;
		}
	});
	_cdependant.Forms.SelectValidator = new Class({
		Extends:_cdependant.Forms.FieldValidator,
		Implements:[Options, Events],
		options:{
			resetValue:-1,
			addValue:-100,
			onElementreset:Function.from(),
			onElementchange:Function.from()		
		},
		initialize:function(selector, options){
			this.element = document.id(selector);
			this.setOptions(options);
			this.parent(selector,options);
		},
		setEvents:function(){
			var that = this;
			this.element.addEvents({
				focus:function(evt){
					that.reset();
					that.fireEvent('elementreset', that.toElement());
					
				},
				blur:function(evt){
					if (this.value != that.options.addValue && that.options.notifications) {
						that.validate(true);					
					}
					
				},
				change:function(evt){
					if (this.value == that.options.resetValue){
						that.fireEvent('elementreset',that.toElement());
						that.fireEvent('elementchange',that.toElement());
						
					}
					else if(this.value == that.options.addValue){
						that.fireEvent('addrequest', that.toElement());
									
					}
					else{
						that.fireEvent('elementchange',that.toElement());
					}				
					
				}
				
			});		
		},
		disable:function(){
			this.enabled = false;
			return this;
		},
		enable:function(){
			this.enabled = true;
			return this;
		},	
		toElement:function(){
			return this.element;
		}
	});	
	/**
	 *   <a>
	 *     <div>{checkbox}</div>
	 *     <div>{label}</div>
	 *   </a>
	 * @classdescription creates a javascript powered checkbox / radio button
	 * supports dependancies
	 * 
	 */
	_cdependant.Forms.JSCheckbox = new Class({
		Extends:_cdependant.Forms.FieldValidator,
		Implements:[Events, Options],
		options:{
			name:'nexus-value',
			checkSelector:'',
			labelSelector:'',
			layout:'inline',
			value:'sample',
			label:'Checkbox',
			baseColor:'#1186D4',
			uncheckedColor:"#999999",
			onChecked:Function.from(),
			onUnchecked:Function.from()
				
		},
		initialize:function(selector,options){
			this.controller = document.id(selector);
			this.setOptions(options);	
			this.build();
			//this.parent(this.element, options);
			this.createColors();
			this.attachEvents();
		},
		
		_baseColor:null,
		TrackInstances:false,
		checked:false,
		enabled:true,
		_dependancies:[],
		attachEvents:function(){
			var that = this;
			this.controller.addEvents({
				click:function(evt){
					evt.stop();
					if(that.enabled){
						that.toggle();
					}
				},
				mouseover:function(){
					that.reset();
					if(that.enabled){
						that.controller.getElement(that.options.checkSelector).tween('background-color', that._hoverColor);	
					}
				},
				mouseout:function(evt){
					
					if(that.enabled){
						if(!that.checked){
							that.controller.getElement(that.options.checkSelector).tween('background-color', that.options.uncheckedColor);
						}else{
							that.controller.getElement(that.options.checkSelector).tween('background-color', that._selectedColor);
						}
					}
				}
			});
		},
		build:function(){
			this.element = new Element('input',{
				id:String.uniqueID(),
				name:this.options.name,
				type:'checkbox',
				value:this.options.value,
				styles:{
					display:'none'	
				}	
			});
			this.controller.getElement( this.options.labelSelector ).set( 'text', this.options.label );
			this.element.inject( this.controller,'after' );
		},
		createColors:function(){
			this._baseColor = 		new Color(this.options.baseColor || '#555555');
			
			this._hoverColor = 		this._baseColor.mix([200,200,200]).rgbToHex();			
			this._selectedColor = 	this._baseColor.mix([100,100,100]).rgbToHex();			
			this._disabledColor = 	this.options.disabledColor || '#444444';
		},	
		isValid:function(){
			var valid;
			// if not required AND the field is empty
			if ( !this.options.required  ){
				this._error = null; 
				valid =  true;
			}
			// if the field is required AND the field is empty
			else if( this.options.required && !this.checked ){
				this._error='required';
				valid =  false;
			}
			else{
				valid = true;
			}
			if(!valid){this._error = 'invalid';}
			return valid;
		},		
		/**
		 * @method runs validation and dispatches events. if enabled and required will inject DOM messages 
		 * @param {Boolean} warn if true will add the appropriate class to indicate validation failed
		 * @return{Boolean} returns true if field passes validation
		 */
		validate:function( warn ){
			var valid ;
			valid = this.isValid();
			if ( valid ) {				
				this.fireEvent('valid', this.controller);
			}
			else {
				this.fireEvent( 'invalid', this.controller );
				if( this.enabled ){
					this.controller.addClass( this.options.errorClassName );
					this.warned = true;
					if( warn ){
						this.notify();
					}
				}
			}				
			return valid;
		},		
		reset:function(){
			var that = this;
			this.controller.removeClass(this.options.errorClassName);
			this.notified = this.warned = false;
			if(this.options.cleanUp){
				this.clean();
			}
			return this;
		},		
		check:function(){
			this.controller.addClass('selected');	
			this.checked = true;
			this.controller.getElement(this.options.checkSelector).tween('background-color',this._selectedColor);
			this.element.set('checked', true);
			this.fireEvent('checked');
			this.checkDependancies();
			return this;
		},
		uncheck:function(){
			this.controller.removeClass('selected');	
			this.checked = false;
			this.controller.getElement(this.options.checkSelector).tween('background-color',this.options.uncheckedColor);
			this.element.set('checked',false);
			this.fireEvent('unchecked');
			return this;
		},
		flash:function(){
			this.controller.getElement(this.options.checkSelector).highlight('#FFF');
		},
		toggle:function(){
			if(this.checked){
				this.uncheck();	
			}else{
				this.check();
			}
			return this;
		},
		checkDependancies:function(){
			
			var deps = this._dependancies || [];
			if(deps.length > 0){
				deps.each(function(item, index){
					if(!item.checked){
						item.check();
					}else{
						item.flash();
					}
				}.bind(this));
			}
			return this;
		}.protect(),
		disable:function(){
			this.enabled = false;
			this.controller.addClass('disabled');
			this.element.set('checked', false);
			this.uncheck();
			return this;
		},
		addDependancy:function(dep){
			if( instanceOf(dep,_cdependant.Forms.JSCheckbox)){
				this._dependancies.push( dep );
			}else{
				throw 'Depenancies must be instances of JSCheckBox';
			}
		},
		addDependancies:function(deps){
			var that = this;
			var d = Array.from(deps);
			stored = this._dependancies || [];
			d.each(function(item, index){
				that.addDependancy(item);
			});
		},
		getDependancies:function(){
			return this._dependancies;
		},
		enable:function(){
			this.enabled = true;
			this.controller.removeClass('disabled');
			return this;	
		},
		toElement:function(){
			return this.controller;	
		},
		value:function(){
			if(!this.enabled){return;}
			return this.element.get('value');	
		}
		
	});
	/*
	 * <label for="check">Check me</label>
	 * <input type="checkbox" name="check" value="checked" id="check" />
	 * 
	 * @classdescription Extends JSCheckbox. Will use existing check box on page to 
	 * create a JSCheckbox instance
	 */
	_cdependant.Forms.GracefullCheckBox = new Class({
		Extends:_cdependant.Forms.JSCheckbox,
		Implements:[Events, Options],
		initialize:function(checkID, options){
			this.element = document.id(checkID);
			this.setOptions(options);
			this.build();
			this.createColors();
			this.attachEvents();
		},
		build:function(){
			var label, labelTxt;
			this.controller = new Element('a', {
				href:"#",
				id:String.uniqueID()
			});
			//find the corresponding lable
			label = $$( 'label[for={id}]'.substitute( {id:this.element.get('id')} ) )[0];
			Boolean(label) ? labelTxt = label.get('text'): labelTxt = this.options.label;
			new Element('div',{
				'class':this.options.checkSelector.split('.')[1]
			}).inject(this.controller);
			
			new Element('div',{
				'class':this.options.labelSelector.split('.')[1],
				text:labelTxt
			}).inject(this.controller);
			
			try {
				label.destroy();
			}catch(e){}
			this.controller.wraps(this.element, 'bottom');
			this.element.setStyle('display', 'none');
		}
	});
	/**
	 * @classDescription Javascript powered replacement for Checkbox inputs. Can be used as individual inputs
	 * 	or can have dependancies which will automatically be checked when this instance is checked.
	 */
	_cdependant.Forms.JSCheckboxGroup = new Class({
		Extends:_cdependant.Forms.FieldValidator,
		Implements:[Events, Options],
		/**
		 * @property {Boolean} stacked:		if the elements should be stacked vertically or allowed to flow inline
		 * @property {Boolean} radio:		if set to true, only 1 element in the group will be allowed
		 * @property {Function} onChange:	function to be run when the state of the element changes
		 * @property {Function} onCheck:	function to be run when the check box is checked
		 * @property {Function} onUncheck:	function to be run when the check box is unchecked
		 * 
		 */
		options:{
			stacked:true,
			radio:true,
			onChange:Function.from(),
			onCheck:Function.from(),
			onUncheck:Function.from()
		},
		name:null,
		elements:null,	
		_checked:[],
		_dependancies:[],	
		initialize:function(groupName, inputs, options){
			this.name = groupName;
			this.elements = new Group(inputs);
			this.setOptions(options);
			this.setEvents();
			this.build();
			if(this.options.radio){
				this.clearInterDepenancy();
			}
		},
		TrackInstances:false,
		setEvents:function(){
			var that = this;
			this.elements.instances.each(function(item, index, obj){
				document.id(item).addEvent('click', function(evt){
					if(that.options.radio){
						that.checked(item).each(function(chk, idx){
							chk.uncheck();
						});						
					}					
					this.checkDependancies();
					this.fireEvent('change', item);
				}.bind(this));
			}.bind(this));
		}.protect(),
		build:function(){
			var els = new Elements(this.elements.instances);
			var maxWidth;
		
			/*
			 * findes the Max width of the parent object of our controller element
			 * so we can set them all to the same width.
			 */
			maxWidth = els
					   .getParent()
					   .getSize()
					   .map(function(item){
   							return item.x;
						}).max() + 2;
						
			els = els.getParent();
			els.setStyles({
				display: 'inline-block',
				'padding-right':'4px'
			});
			if(this.options.stacked){
				els.setStyle('display','block');
			}
			els.setStyle('width', maxWidth);
		}.protect(),
		/**
		 * 
		 * @param {JSCheckbox / Array of JSCheckbox instances } checkbox
		 */
		add:function(checkbox){
			/*
			 * if we get an array, check each to make sure we are getting what we want
			 */
			if ( typeOf(checkbox) === 'array'){									
					checkbox.each(function(item, index){
						if(!instanceOf(item,_cdependant.Forms.JSCheckbox) &&  !instanceOf(item,_cdependant.Forms.GracefullCheckBox)){
							throw "Add function only accepts instances of JSCheckbox or an Array of JSCheckbox instances";
						}else{
							this.elements.instances.push(checkbox);
						}
					});
			/*
			 * else check to make sure we get what we want and add it
			 */
			}else{
				if( !instanceOf(checkbox,_cdependant.Forms.JSCheckbox) && !instanceOf(checkbox,_cdependant.Forms.GracefullCheckBox ) ){
					throw "Add function only accepts instances of JSCheckbox or an Array of JSCheckbox instances";
				}else{				
					this.elements.instances.push(checkbox);					
				}				
			}						
			this.build();
			return this;
		},
		/**
		 * @param {JSCheckBox} jsbox :	The JSCheckbox instance you want to remove from the group. Will also remove it from the DOM
		 */
		remove:function(jsbox){			
			this.elements.instances.erase(jsbox);
			jsbox.controller.getParent().destroy();
		},
		/**
		 * @method checked returns an array of JSCheckbox instances that are currently checked
		 * @param {Object} exclude:	an instance of JSCheckbox that you wish to exclude from the results 
		 * 
		 */
		checked:function(exclude){
			return this.elements.instances.filter(function(item, index){
				if(exclude){
					return ( item.checked && item != exclude);	
				}else{
					return item.checked;	
				}
			});
		},
		/**
		 * @private
		 * 
		 * @method creates a group wide dependancy
		 * @param {JSCheckbox} dep:	the instance you want to add to the group
		 */
		addDependancy:function(dep){
			if (instanceOf(dep,_cdependant.Forms.JSCheckbox)) {
				this._dependancies.push(dep);
			}else {
				throw 'Depenancies must be instances of JSCheckBox';
			}
		}.protect(),
		
		/**
		 * @method adds instances of JSCheckboxes as dependancies of the group
		 * @param {JSCheckbox / Array } deps collection of JSCheckboxes
		 */
		addDependancies:function(deps){
			if (!this.options.radio) {
				var that = this;
				var d = Array.from(deps);
				stored = this._dependancies || [];
				d.each(function(item, index){
					this.addDependancy(item);
				}.bind(this));
			}
		},		
		
		/**
		 * @private
		 * checks dependancies when the user makes a selection in this group
		 */
		checkDependancies:function(){
			var deps = this._dependancies || [];
			if(deps.length > 0){
				deps.each(function(item, index){
					if (!item.checked) {
						item.check();
					}else{
						item.flash();	
					}
				});
			}
			return this;
		}.protect(),		
		
		notify:function(){
			if(this.notified){return false;}
			var elID, response, that = this;
			elID = this.element.attr('id') + 'error';
			if(this.EMPTY_VALUES.contains(this.element.get('value'))){
				response = '<li>{required}</li>'.substitute(that.options.errors);
			}else{
				response = '<li>{invalid}</li>'.substitute(that.options.errors);	
			}
			new Element('ul',{
				className:'errors',
				id:'',
				html: response
			}).inject(that.element,'after');
			this.notified = true;
			return this;
		},
		
		/**
		 * @private
		 * removes all dependancies of this group. 
		 * does not remove from the DOM
		 */
		clearInterDepenancy:function(){
			this.elements.instances.each( function(item, index){
				item._dependancies = [];
			});
		}.protect(),
		isValid:function(){
			var cks,valid;
			cks = this.elements.instances;
			valid = true;
			
						
			if ( !this.options.required ) {
				this._error = null; 
				return true;
			}
			// if the field is required AND the field is empty
			if( this.options.required && this.checked().length === 0 ) {
				this._error='required';
				return false;
			}
			
			Array.each(cks, function(item,index){
				if( !item.isValid() ){
					valid = false;
				}
			});
			
			if(!valid){this._error = 'invalid';}
			return valid;			
		},
		validate:function(){
			var valid ;
			valid = this.isValid();
			if (valid) {				
				this.fireEvent('valid', this.element);
			}
			else {
				this.fireEvent('invalid', this.element);
				if(this.enabled ){
					this.toElement().getParent().addClass(this.options.errorClassName);
					this.warned = true;
					if(warn){
						this.notify();
					}
				}
			}				
			return valid;			
		}
	});
	
	/**
	 * @property {Object} the main Nexus object that holds the classes
	 */
	window.cDependant =_cdependant;
})(window);
