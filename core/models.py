from diff_match_patch import diff_match_patch
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import striptags
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel
from hotsauce.models import EditableItem, ChangeSet

from sorl.thumbnail.fields import ImageField
from hashlib import md5
import redis

class TestModel(models.Model):
    title = models.CharField(max_length=255, blank=False,null=False)
    slug =  AutoSlugField(populate_from=('title'),db_index=True, unique=True)
    thumbnail = ImageField(upload_to="images/")
    

# generic - can go on anything
class ContentAwareModel(models.Model):
    '''
        An Abstract model: models which subclass the SelfAwareModel
        will have a series of methods that give quick access to that
        model's meta information:
        
        Content Type & it's ID
        App Label
        Model Name
        Class Name
        
        The aim is to make working with generic models easier from a
        template as generic relations offer a good deal of information
        about the related object, but accessing information about the 
        target object/model itself can be frustrating.
        
        Way to add Standarized functionality with out changing model strucure
    '''
    __REDIS__ = redis.Redis(
        host=getattr(settings, 'REDIS_HOST', 'localhost'),
        port=getattr(settings, 'REDIS_PORT', 6379),
        db=getattr(settings, 'REDIS_DB', 0),
    )

    def get_ct(self):
        '''returns the ContentType Model that represents this object'''
        return ContentType.objects.get_for_model(self)
    
    def get_ct_id(self):
        '''
            returns the Primary Key of the ContentType model that represents
            this object
        '''
        return self.get_ct().id
    
    def get_app_label(self):
        '''returns the name of the application in which this object's class lives'''
        return self.get_ct().app_label

    def get_model_name(self):
        '''returns the model name of this object'''
        return self.get_ct().model
    
    def get_class_name(self):
        '''return the name of this object's class'''
        return self._meta.verbose_name
        
    class Meta:
        abstract = True    
        
class SelfAwareModel(TimeStampedModel):
    '''
        An Abstract model: models which subclass the SelfAwareModel
        will have a series of methods that give quick access to that
        model's meta information:
        
        Content Type & it's ID
        App Label
        Model Name
        Class Name
        created - datetime object
        modified - datetime object

        The aim is to make working with generic models easier from a
        template as generic relations offer a good deal of information
        about the related object, but accessing information about the 
        target object/model itself can be frustrating.
        
        Way to add Standarized functionality with out changing model strucure
    '''
    __REDIS__ = redis.Redis(
        host=getattr(settings, 'REDIS_HOST', 'localhost'),
        port=getattr(settings, 'REDIS_PORT', 6379),
        db=getattr(settings, 'REDIS_DB', 0),
    )
    def get_ct(self):
        return ContentType.objects.get_for_model(self)
    
    def get_ct_id(self):
        return self.get_ct().id
    
    def get_app_label(self):
        return self.get_ct().app_label
    
    def get_model_name(self):
        return self.get_ct().model
    
    def get_class_name(self):
        return self._meta.verbose_name
        
    class Meta:
        abstract = True        

from photologue.models import ImageModel
class SiteContentItem(EditableItem, ImageModel, ContentAwareModel):
    html_patch = models.TextField(blank = True, 
                                  null = True, 
                                  editable = False)    
    enable_comments = models.BooleanField()   
    changes = generic.GenericRelation(ChangeSet)
    objects = models.Manager()
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return (u"%s" % self.title )
    
    def hit_key(self):
        return md5("%s:%s" %( self.get_ct(), self.pk )).hexdigest()
    def hit(self):
        _RCLIENT = self.__REDIS__
        _RCLIENT.incr(self.hit_key())
    def unhit(self):
        _RCLIENT = self.__REDIS__
        _RCLIENT.decr(self.hit_key()) 
    def get_hits(self):
        _RCLIENT = self.__REDIS__
        return _RCLIENT.get(self.hit_key())
    get_hits.short_description = "hits"    
    def revert_to(self, revision, author=None):
        '''takes a revision number queries for the changset and returns it '''
        
        #a ChangeSet Instance
        changeset = self.changes.objects.get(version=revision)
        changeset.reapply(author)

    def current_version(self):
        '''DOCSTRINGS'''
        try:
            return self.changes.latest().revision
        except:
            None
    def current_version_number(self):
        try:
            return self.changes.latest().revision
        except:
            return 'initial'
        
    def make_new_revision(self, old_content, old_title, comment, editor):
        '''
            Function to be overridden
            
            This is the function that is called from the form that 
            is responsible for saving and editable item.
            
            This creates a new ChangeSet related to the object that called
            this function
        '''
        from hotsauce.utils import make_difPatch
        ctype = ContentType.objects.get_for_model(self)
        diff_text = make_difPatch(self.content, old_content)
        change = ChangeSet.objects.create(content_diff=diff_text, 
                                      content_type=ctype, 
                                      object_id=self.id, 
                                      comment=comment,
                                      old_title=old_title,
                                      editor=editor)
        return change     
    def make_indexable(self):
        '''
            Incoming content is assumed to be HTML
            We want to index plain text, not html
            
            If the current content is already plain text, 
            we don't do anything
            
            else convert the html to plain text make 
            a patch to convert the text back to html
            save the plain text, save the patch as 
            text string save the object 
        '''
        _dmp = diff_match_patch()
        html = self.content
        plain_text = striptags(html)
        
        if not self.content == plain_text:
            patch = _dmp.patch_make(plain_text, html)
            self.content = plain_text
            self.html_patch = _dmp.patch_toText(patch)
    
    def as_plain_text(self):
        return striptags(self.content)
    def see_version_diff(self, revision):
        _dmp = diff_match_patch()
        '''see the difference of a revision and the previous revision
            if the user wants revision 4, we compare revision 4 & 3
        '''
        if revision == 1:
            return self.latest_changeset().display_change_html()
        else:
            compare = revision -1
        
        r = Q(revision=revision)
        c = Q(revision=compare)
        changes = self.changes.filter(r|c)
        #see_item_at_version
        latest = changes[0]
        early = changes[1]
        latest_content = latest.see_item_at_version()
        early_content = early.see_item_at_version()
        
        diffs = _dmp.diff_main(latest_content, early_content)
        return _dmp.diff_prettyHtml(diffs)
    def get_html_content(self):
        if self.html_patch is None:
            return self.content
        else:
            _dmp = diff_match_patch()
            patch = _dmp.patch_fromText(self.html_patch)
            return _dmp.patch_apply(patch, self.content)[0]    
                