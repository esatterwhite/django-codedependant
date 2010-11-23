from django import forms
from django.conf import settings
class MooEditor(forms.Textarea):
    class Media:
        js = ('js/MooEditable.js',)
        css = {'all':('css/MooEditable.css', 'css/MooEditable.Image.css')}
    def __init__(self, attrs={}):
        return super(MooEditor, self).__init__(attrs)
    
    def render (self, name, value, attrs=None):
        rendered = super(MooEditor, self).render(name, value, attrs)
        return rendered + ('''<script>
                                    window.addEvent('domready', function(){
                                       editor =  $('id_%s').mooEditable({
                            externalCSS:'%scss/MooEditable.css',
                            actions: 'bold italic | insertunorderedlist indent outdent | undo redo refresh-view | unlink | urlimage | toggleview'
                          })
                                    });
                            </script> ''') % (name, settings.MEDIA_URL)
