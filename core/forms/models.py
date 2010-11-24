'''
Created on Nov 22, 2010

@author: Eric
'''
from django import forms
from photologue.models import Photo

class InsertCodeForm(forms.Form):
    LANGUAGES = (
         ('js', 'JavaScript'),
         ('html', 'HTML'),
         ('css','CSS'),
         ('php','PHP'),
         ('ruby','Ruby'),
         ('sql', 'SQL'),
         ('shell','Shell'),
         ('python', 'Python')
    )
    
    language = forms.ChoiceField(choices=LANGUAGES)
    code = forms.CharField(widget=forms.Textarea(attrs={'rows':'10'}))
    
    
class PhotoUploadForm(forms.ModelForm):
    
    class Meta:
        model = Photo
        fields=['image']
            