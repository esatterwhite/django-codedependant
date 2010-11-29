MooEditable.UI.SearchDialog = function(editor){
	var html = '<input type="hidden" id="plainurl" value="" size="35"> '
			 + 'search <input type="text" id="globalsearch" value="" size="35" class="search-input"/> '
			 + '<button class="dialog-ok-button">OK</button>'
			 + '<button class="dialog-cancel-button">Cancel</button>';
	var sitesearch, searchinput, urlinput;
	return new MooEditable.UI.Dialog(html,{
		'class':'mooeditable-prompt-dialog',
		onOpen:function(e){
			searchinput = $('globalsearch');
			urlinput = $('plainurl');
			sitesearch = new Autocompleter.Request.JSON(searchinput.id, '/search/',{
				postVar:'q',
				selectMode:true,
				relative:true,
				minLength: 2,
				injectChoice:function(token){
					var choice = new Element('li',{
						events:{
							'click':function(e){
								urlinput.set('value', token.url);
							}
						}
					});
					choice.inputValue = token.name;
					new Element('img',{
						src:token.image,
						'class':'fl pr-6'
					}).inject(choice);
					new Element('div', {
						html:this.markQueryValue(token.name),
						'class':'small'
					}).inject(choice);
					new Element('div',{
						'class':'compact-text',
						text:token.ct
					}).inject(choice);
					new Element('br',{'class':'clearfloat'}).inject(choice);
					this.addChoiceEvents(choice).inject(this.choices);
				}
			});
		},
		onClose:function(e){
			sitesearch.destroy();
			urlinput.set('value', '');
			searchinput.set('value','');
		},
		onClick:function(e){
			if (e.target.tagName.toLowerCase() == 'button') {
				e.preventDefault();
			}
			var button = document.id(e.target);
			if (button.hasClass('dialog-cancel-button')) {
				this.close();
			}
			else 
				if (button.hasClass('dialog-ok-button')) {
					if (urlinput.value !== '') {
						var txt = editor.selection.getText();
						var link_wrap= new Element('div');
						new Element('a',{
							href:urlinput.value,
							text:txt
						}).inject(link_wrap);
						editor.selection.insertContent(link_wrap.get('html'));
					}
					this.close();
				}			
		}
	});
	
};
MooEditable.Actions.urlsearch={
	title:'Find URL',
	type:'button',
	options:{
		mode:'icon',
		shortcut:'h'
	},
	dialogs:{	
		alert: MooEditable.UI.AlertDialog.pass('Please select the text you wish to hyperlink.'),
		prompt:function(editor){
			return MooEditable.UI.SearchDialog(editor);
		}
	},
	command:function(){
		if (this.selection.isCollapsed()) {
			this.dialogs.urlsearch.alert.open();
		}
		else {
			this.dialogs.urlsearch.prompt.open();
		}
	}
	
};