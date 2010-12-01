''' 
    Docstrings go Here 
'''

from diff_match_patch import diff_match_patch
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import striptags
from django_extensions.db.models import TimeStampedModel
from hashlib import md5
from hotsauce.models import EditableItem, ChangeSet
from photologue.models import ImageModel
import redis

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
    def get_ct_proxy(self):
        ''' 
            returns the name of this contenttype as a string without hitting the database 
        '''
        return u'%s' % self.__class__.__name__
    def get_ctype(self):     
        '''returns the ContentType Model that represents this object'''        
        return ContentType.objects.get_for_model(self)
    def get_ctype_id(self):
        '''
            returns the Primary Key of the ContentType model that represents
            this object
        '''
        cid = (md5("%s_%s" %(self.__class__.__name__, self.pk) ).hexdigest())
        mid = self.__REDIS__.get(cid) or None
        if mid:
            return mid
        
        self.__REDIS__.set(cid, self.get_ctype().pk )
        return self.get_ctype().id
    
    def get_app_label(self):
        '''
            returns the name of the application in which this object's class lives
        '''
        return self.get_ctype().app_label

    def get_model_name(self):
        '''returns the model name of this object'''
        return self.get_ctype().model
    
    def get_class_name(self):
        '''return the name of this object's class'''
        return self._meta.verbose_name
        
    class Meta:
        abstract = True    
        
class SelfAwareModel(TimeStampedModel, ContentAwareModel):
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
        
    class Meta:
        abstract = True        

class SiteContentItem(EditableItem, ImageModel, ContentAwareModel):
    '''
        Primary class for content on the site.
        Models should sublcass from here to provide a 
        common API.
    '''
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
    
    def delete(self):
        try:
            self.changes.all().delete()
        except:
            pass
        
    def hit_key(self):
        ''' returns md5 hash key for the instance in question '''
        return md5("%s:%s" %( self.get_ctype_id(), self.pk )).hexdigest()
    def hit(self): 
        ''' increments the internal hit counter by 1 '''
        _RCLIENT = self.__REDIS__
        _RCLIENT.incr(self.hit_key())
    def unhit(self):
        ''' 
            decriments internal hit counter by 1 
        '''
        _RCLIENT = self.__REDIS__
        _RCLIENT.decr(self.hit_key()) 
    def get_hits(self):
        ''' 
            returns the number of times the instance in question has been seen 
        '''
        _RCLIENT = self.__REDIS__
        return _RCLIENT.get(self.hit_key())
    get_hits.short_description = "hits"   
     
    def revert_to(self, revision, author=None):
        '''takes a revision number queries for the changset and returns it '''
        
        #a ChangeSet Instance
        changeset = self.changes.objects.get(version=revision)
        changeset.reapply(author)

    def latest_revision(self):
        '''returns the changeset object '''
        try:
            return self.changes.latest()
        except:
            ChangeSet.objects.none()
    def current_version_number(self):
        ''' returns the numeric revision number of this object'''
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
        '''
            returns the main content with HTML tags striped out
        '''
        return striptags(self.content)
    def see_version_diff(self, revision):        
        '''see the difference of a revision and the previous revision
            if the user wants revision 4, we compare revision 4 & 3
        '''
        _dmp = diff_match_patch()
        if revision == 1:
            return self.latest_changeset().display_change_html()
        else:
            compare = revision -1
        
        rev = Q(revision=revision)
        cmpr = Q(revision=compare)
        changes = self.changes.filter(rev|cmpr)
        #see_item_at_version
        latest = changes[0]
        early = changes[1]
        latest_content = latest.see_item_at_version()
        early_content = early.see_item_at_version()
        
        diffs = _dmp.diff_main(latest_content, early_content)
        return _dmp.diff_prettyHtml(diffs)
    def get_html_content(self):
        ''' returns the full HTML content of the item in question '''
        if self.html_patch is None:
            return self.content
        else:
            _dmp = diff_match_patch()
            patch = _dmp.patch_fromText(self.html_patch)
            return _dmp.patch_apply(patch, self.content)[0]    
                