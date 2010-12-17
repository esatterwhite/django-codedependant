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



MooEditable.Actions.swfupload ={
  title:"Upload Images",
  type:'button',
  options:{
    mode:'icon',
    shortcut:'k'
  },
  command:function(button, e){
    var uploader, req, box;
    req = new Request.HTML({
      url:'/ajax/photo/upload/',
      method:'get',
      onFailure:function(){},
      onSuccess:function(responseHTML, responseElements, responseText){
        box = new cDependant.ModalBox({
          title:'Upload Images',
          stage:responseText,
          className:'',
          closeable:true
        });
        box.showBox();
        $('photo-close').addEvent('click', function(evt){
          evt.stop();
          box.hideBox();
        });
        uploader = new FancyUpload2(document.id('photo-status'), document.id('photo-list'), { // options object
          queued:false,
          fieldName:'image',
          // we console.log infos, remove that in production!!
          verbose: true,
       
          // url is read from the form, so you just have to change one place
          url: '/core/photo_upload/',
       
          // path to the SWF file
          path: 'http://127.0.0.1:8000/static_media/swf/Swiff.Uploader.swf',
 
          // remove that line to select all files, or edit it, add more items
          typeFilter: {
            'Images (*.jpg, *.jpeg, *.gif, *.png)': '*.jpg; *.jpeg; *.gif; *.png'
          },
       
          // this is our browse button, *target* is overlayed with the Flash movie
          target: 'photo-browse',
       
          // graceful degradation, onLoad is only called if all went well with Flash
          onLoad: function() {
            $('photo-status').removeClass('hide'); // we show the actual UI
            $('photo-fallback').destroy(); // ... and hide the plain form
       
            // We relay the interactions with the overlayed flash to the link
            this.target.addEvents({
              click: function() {
                return false;
              },
              mouseenter: function() {
                this.addClass('hover');
              },
              mouseleave: function() {
                this.removeClass('hover');
                this.blur();
              },
              mousedown: function() {
                this.focus();
              }
            });
       
            // Interactions for the 2 other buttons
       
            $('photo-clear').addEvent('click', function() {
              uploader.remove(); // remove all files
              return false;
            });
       
            $('photo-upload').addEvent('click', function() {
              uploader.start(); // start upload
              return false;
            });
          },
       
          // Edit the following lines, it is your custom event handling
       
          /**
           * Is called when files were not added, "files" is an array of invalid File classes.
           * 
           * This example creates a list of error elements directly in the file list, which
           * hide on click.
           */ 
          onSelectFail: function(files) {
            files.each(function(file) {
              new Element('li', {
                'class': 'validation-error',
                html: file.validationErrorMessage || file.validationError,
                title: MooTools.lang.get('FancyUpload', 'removeTitle'),
                events: {
                  click: function() {
                    this.destroy();
                  }
                }
              }).inject(this.list, 'top');
            }, this);
          },
       
          /**
           * This one was directly in FancyUpload2 before, the event makes it
           * easier for you, to add your own response handling (you probably want
           * to send something else than JSON or different items).
           */
          onFileSuccess: function(file, response) {
            var json = new Hash(JSON.decode(response, true) || {});
       
            if (json.get('status') == '1') {
              Log.log(file);
              Log.log(response);
              file.element.addClass('file-success');
              file.info.set('html', '<strong>Image was uploaded:</strong> ' + json.get('width') + ' x ' + json.get('height') + 'px, <em>' + json.get('mime') + '</em>');
            } else {
              file.element.addClass('file-failed');
              file.info.set('html', '<strong>An error occured:</strong> ' + (json.get('error') ? (json.get('error') + ' #' + json.get('code')) : response));
            }
          },
       
          /**
           * onFail is called when the Flash movie got bashed by some browser plugin
           * like Adblock or Flashblock.
           */
          onFail: function(error) {
            switch (error) {
              case 'hidden': // works after enabling the movie and clicking refresh
                alert('To enable the embedded uploader, unblock it in your browser and refresh (see Adblock).');
                break;
              case 'blocked': // This no *full* fail, it works after the user clicks the button
                alert('To enable the embedded uploader, enable the blocked Flash movie (see Flashblock).');
                break;
              case 'empty': // Oh oh, wrong path
                alert('A required file was not found, please be patient and we fix this.');
                break;
              case 'flash': // no flash 9+ :(
                alert('To enable the embedded uploader, install the latest Adobe Flash plugin.')
            }
          }
       
        }); 
            
      }
    }).send();
    
  }
};
