'''
Created on Nov 22, 2010

@author: Eric
'''
from django import forms
from django.contrib.auth.models import User
from publisher.models import STORY_CHOICES, Article
from core.forms.widgets import MooEditor
class EditModeArticleForm(forms.ModelForm):    
    '''
        Docstrings go here
    '''
    users = User.objects.all()
    comment = forms.CharField(required=False, max_length=255)
    author = forms.ModelChoiceField(users, widget=forms.HiddenInput())  
    class Meta:
        model = Article
        widgets = {
                    'status':forms.RadioSelect(choices=STORY_CHOICES),
                    'content':MooEditor(attrs={'rows':'40'})
                   }
        exclude = ( 'date_created' )
    
    def clean_content(self):
        if self.instance.pk is not None:
            self.cleaned_data['old_content'] = self.instance.content
        return self.cleaned_data['content']
    def clean_title(self):
        if self.instance.pk is not None:
            self.cleaned_data['old_title'] = self.instance.title
        return self.cleaned_data['title']
    def save(self, *args, **kwargs):
        ''' DOCSTRING '''
        # get old infor before saving
        comment = self.cleaned_data['comment']
        editor = self.cleaned_data['author']
        if self.instance.id is None:
            old_title = ""
            old_content = ""
            new = True
        else:
            old_title= self.cleaned_data['old_title']
            old_content=self.cleaned_data['old_content']
            new = False
            
        #Save editable item
        
        new_item = super(EditModeArticleForm, self).save(*args, **kwargs)

        # create new ChangeSet
        new_item.make_new_revision(old_content, old_title, comment, editor)
        if not new_item.initial_publish and new_item.status in [5,6]:
            new_item.initial_publish = True
            new_item.save()

        return new_item     
