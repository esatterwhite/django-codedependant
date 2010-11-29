from core.models import SiteContentItem
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from publisher.managers import LiveArticleManager, CurrentArticleManager, ArchivedArticleManager
STORY_CHOICES = (
    (1, "Needs Edit"),
    (2, "Needs Images"),
    (3, "Needs Approval"),
    (4, "Needs Polish"),
    (5, "Published"),
    (6, "Archived"),
    (7, "OUTDATED"),
    (8, "DENIED"),
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
class Article(SiteContentItem):
    


    status =        models.IntegerField(_("Article Status"),
                                        choices = STORY_CHOICES, default=1)
       
    tag_line =      models.CharField(_('Tag Line'), max_length= 40, 
                                     blank=False, help_text = "A one - liner to grab the reader's attention")
    
    summary =       models.CharField(_('Summary'),
                                     max_length = 255, blank=True, 
                                     null=False, help_text=_("no text"))
    initial_publish = models.BooleanField(editable=False)
    
    admin_objects = models.Manager()
    objects =       CurrentArticleManager()
    live =          LiveArticleManager()
    archived =      ArchivedArticleManager()
    
    class Meta:
        ordering = ('-date_created',)
        get_latest_by ='date_created'
        verbose_name_plural = _('Articles')
    def __unicode__(self):
        return u'%s' % self.title
    
    @permalink
    def get_absolute_url(self):
        return ('codedependant.publisher.views.content_detail', (), {
                                                       "ct_id":self.get_ctype_id(),
                                                       "obj_id":self.pk,
                                                       'slug':self.slug
                                                       })
class Review(SiteContentItem):
    status =        models.IntegerField(_("Review Status"),
                                        choices = STORY_CHOICES, default=1)
     
    tag_line =      models.CharField(_('Tag Line'), max_length= 40, 
                                     blank=False, help_text = "A one - liner to grab the reader's attention")
    
    summary =       models.CharField(_('Summary'),
                                     max_length = 255, blank=True, 
                                     null=False, help_text=_("no text"))    
    class Meta:
        ordering = ('-date_created',)
        get_latest_by ='date_created'
        verbose_name_plural = _("Reviews")
        
    def __unicode__(self):
        return u'%s' % self.title
    
    @permalink
    def get_absolute_url(self):
        return ('', (), {})