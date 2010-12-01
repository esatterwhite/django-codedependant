/**
 * @author Eric
 */

MooEditable.UI.PhotosearchDialog = function(editor){
	var html = '<input id="photourl" class="search-input" value="" size="15" type="hidden"/> '
			+ 'search <input id="photosearch" class="search-input" value="" size="35" type="text" /> '
			+ 'align <select><option value="fr">Right</option><option value="fl">Left</option></select> '	
			+ '<button class="dialog-button dialog-ok-button">OK</button> '
			+ '<button class="dialog-button dialog-cancel-button">Cancel</button> ';
	var imagesearch, imageElement, photoinput, photourl, anchor, anchorsrc;
	return new MooEditable.UI.Dialog(html,{
		'class':'mooeditable-prompt-dialog',
		onOpen:function(){
			photoinput = $('photosearch');
			photourl = $('photourl');
			imagesearch = new Autocompleter.Request.JSON(photoinput.id, '/search/photos/',{
			'selectMode': 'pick',
			relative:true,
			postVar:'q',
		      injectChoice: function(token){
		      	var choice = new Element('li',{
						events:{
							click:function(e){
								//photoinput.store('image', );
								photourl.set('value',token.thumbnail);
								photoinput.value='';
								anchorsrc = token.image;
								photourl.store('title', token.title);
							}
						}
					});
					//choice.store('displayimg', token.display)
					choice.inputValue = token.title
					new Element('img',{
						src:token.preview,
						'class':'fl mr-6'
					}).inject(choice);
					new Element('div',{
						text:token.title,
					}).inject(choice);
					new Element('br', {
						'class':'clearfloat'
					}).inject(choice);
		            this.addChoiceEvents(choice).inject(this.choices);
		        }
			});
			//Log.log("OPEN!", photoinput);
		},
		onClose:function(e){
			imagesearch.destroy();
		},
		onClick:function(e){
			if (e.target.tagName.toLowerCase() == 'button') e.preventDefault();
			var button = document.id(e.target);
			if (button.hasClass('dialog-cancel-button')) {
				this.close();
				photoinput.value = "";
			}
			else 
				if (button.hasClass('dialog-ok-button')) {
					this.close();
					if (photourl.value !== ""){
						var wrap = new Element('div');
						anchor = new Element('a',{
							src:anchorsrc,
							'class':'remooz',
							title:photourl.retrieve('title')
						});
						imageElement = new Element('img',{
							src:photourl.value,
							'class':'p_all-6 ' + this.el.getElement('select').value
							
						}).inject(anchor);
						anchor.inject(wrap);
						editor.selection.insertContent(wrap.get('html'));
						photourl.value = "";
					}
				}
			
		}
	});
};
Object.append(MooEditable.Actions,{
    photosearch:{
    	title:'Find Image',
    	type:'button',
    	options:{
    		mode:'icon',
    		shortcut:'e'
		}
  	},
  	dialogs:{
  		prompt:function(editor){
  			return MooEditable.UI.PhotosearchDialog(editor);
  		}
  	},
  	command:function(){
  		this.dialogs.photosearch.prompt.open();
  	}
});
