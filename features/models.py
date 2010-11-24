from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import datetime
        
class Feature(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    pretty_image = models.ImageField(upload_to='images/features/pretty/', help_text='main image on the home page( dressed up ) - 530x235')
    summary = models.CharField(max_length=150, blank=False)
    date_posted = models.DateTimeField(blank=False, default=datetime.datetime.now, help_text="The date the item was posted to the site. Defaults to today")
    date_modified = models.DateTimeField(auto_now=True, editable=False, help_text='the last time the item was modified. When the item is saved, this is automatically changed to the current day/time')
    sub_heading = models.CharField(max_length=150, blank=True, null=True)
    is_live = models.BooleanField() 

    class Meta:
        ordering = ['-date_posted']    

    def __unicode__(self):
        return '%s' % self.content_object.title
