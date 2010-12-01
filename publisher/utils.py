'''
Created on Nov 29, 2010

@author: Eric
'''

from django import forms
from django.contrib.auth.models import User
from core.forms.widgets import MooEditor
from models import STORY_CHOICES, CD_RATING_OPTIONS

def get_object_form(modelclass):
    ''' 
        Requires: hotsauce.models.EditableItem, codedependant.core.models.SiteContentItem
        Provides: get_object_form:function( models.Model ), ObjectForm:ModelForm
        
        Returns a Django ModelForm based on the Model class passed in
        The form returned will leverage the hotsauce application to make a new
        revision of the object being edited
        
        * modelclass should interface with codedependant.core.models.SiteContentItem
    '''
    class _ObjectForm(forms.ModelForm):
        ''' _ObjectForm modelform class '''
        users = User.objects.filter(is_staff=True)
        comment = forms.CharField(required=False)
        author = forms.ModelChoiceField(users, widget=forms.HiddenInput())
        
        # the singe edge case we may want to edit is on the Review Class
        if 'rating' in [f.name for f in modelclass._meta.fields]:    
            rating = forms.IntegerField(widget=forms.RadioSelect(choices=CD_RATING_OPTIONS))                         
        class Meta:
            model = modelclass
            exclude = ( 'date_created', 'effect' )
            widgets = {
                       'status':forms.RadioSelect(choices=STORY_CHOICES),
                       'content':MooEditor(attrs={'rows':'30'})
                       }
            
        def clean_content(self):
            '''
                creates a place holder for the previous content from the 
                existing object
            '''
            if self.instance.pk is not None:
                self.cleaned_data['old_content'] = self.instance.content
            else:
                self.cleaned_data['old_content'] = ''
            return self.cleaned_data['content']
        
        def clean_title(self):
            '''
                creates a place holder for the previous title from the 
                existing object
            '''

            if self.instance.pk is not None:
                self.cleaned_data['old_title'] = self.instance.title
            else:
                self.cleaned_data['old_title'] = ''
                
            return self.cleaned_data['title']  
                  
        def save(self, *args, **kwargs):
            '''     
                Overides default save method to gather old content
                from the object's instance
            '''
            # get old infor before saving
            comment = self.cleaned_data['comment']
            editor = self.cleaned_data['author']
            old_title = self.cleaned_data['old_title']
            old_content = self.cleaned_data['old_content']
            
            #Save editable item            
            new_item = super(_ObjectForm, self).save(*args, **kwargs)
    
            # create new ChangeSet
            new_item.make_new_revision(old_content, old_title, comment, editor)
            if not new_item.initial_publish and new_item.status in [5, 6]:
                new_item.initial_publish = True
                new_item.save()
    
            return new_item      
#    Return the class, not an instance of the class
    return _ObjectForm