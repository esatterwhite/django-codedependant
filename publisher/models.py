from core.models import SiteContentItem
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from publisher.managers import LiveArticleManager, CurrentArticleManager, ArchivedArticleManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
STORY_CHOICES = (
    (1, _("Needs Edit")),
    (2, _("Needs Images")),
    (3, _("Needs Approval")),
    (4, _("Needs Polish")),
    (5, _("Published")),
    (6, _("Archived")),
    (7, _("OUTDATED")),
    (8, _("DENIED")),
)
MODERATION_OPTIONS = (
    ('approval', _('Approve')),
    ('denial', _('Deny'))
) 

CD_RATING_OPTIONS = (
     (0, _('0 Stars')),                     
     (1, _('1 Star')),
     (2, _('2 Stars')),
     (3, _('3 Stars')),
     (4, _('4 Stars')),
     (5, _('5 Stars')),
)

class ArticleBase(SiteContentItem):
    status =          models.IntegerField(_("Status"),
                                        choices = STORY_CHOICES, default=1)
       
    tag_line =        models.CharField(_('Tag Line'), max_length= 40, 
                                     blank=False, help_text = "A one - liner to grab the reader's attention")
    
    summary =         models.CharField(_('Summary'),
                                     max_length = 255, blank=True, 
                                     null=False, help_text=_("no text"))
    initial_publish = models.BooleanField(editable=False, default=False)

    class Meta:
        abstract = True
        
class Article(ArticleBase):
        
    admin_objects =   models.Manager()
    objects =         CurrentArticleManager()
    live =            LiveArticleManager()
    archived =        ArchivedArticleManager()
    
    class Meta:
        ordering = ('-date_created',)
        get_latest_by ='date_created'
        verbose_name_plural = _('Articles')
    def __unicode__(self):
        return u'%s' % self.title
    
    @permalink
    def get_absolute_url(self):
        return ('codedependant.publisher.views.basic.content_detail', (), {
                                                       "ct_id":self.get_ctype_id(),
                                                       "obj_id":self.pk,
                                                       'slug':self.slug
                                                       })
class Review(ArticleBase):
    content_type =  models.ForeignKey(ContentType, null=True)
    object_id =     models.IntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')  
    rating =        models.SmallIntegerField(_('Rating'),
                                             blank=False, null=True,
                                             choices=CD_RATING_OPTIONS) 
    class Meta:
        ordering = ('-date_created',)
        get_latest_by ='date_created'
        verbose_name_plural = _("Reviews")
        
    def __unicode__(self):
        return u'%s' % self.title
    
    @permalink
    def get_absolute_url(self):
        return ('', (), {})