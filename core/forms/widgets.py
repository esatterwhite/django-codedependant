from django import forms
from django.conf import settings
class MooEditor(forms.Textarea):
    class Media:
        js = ('js/MooEditable.js','js/MooEditable.Urlsearch.js','js/MooEditable.Photosearch.js','js/Swiff.Uploader.js', 'js/FancyUpload2.js')
        css = {'all':('css/MooEditable.css', 'css/MooEditable.Image.css')}
    def __init__(self, attrs={}):
        return super(MooEditor, self).__init__(attrs)
    
    def render (self, name, value, attrs=None):
        rendered = super(MooEditor, self).render(name, value, attrs)
        return rendered + ('''<script>
                                    window.addEvent('domready', function(){
                                        try{
                                          editor =  $('id_%s').mooEditable({
                                            externalCSS:'%scss/editor.css',
                                            paragraphise:false,
                                            actions: 'h2 h4 p | bold italic | insertunorderedlist indent outdent | undo redo refresh-view | createlink urlsearch unlink | urlimage photosearch swfupload | insertcode toggleview'
                                        
                                          });
                                        }
                                        catch(e){}
                                    });
                            </script> ''') % (name, settings.MEDIA_URL)
