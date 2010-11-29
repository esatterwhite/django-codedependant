from django import template
from django.contrib import comments
from django.contrib.comments.models import Comment
from django.contrib.comments.templatetags.comments import *
from django.core.cache import cache
from django.template import Library, Node, TemplateSyntaxError, Variable
from django.utils.encoding import smart_unicode
from hashlib import sha1
register = template.Library()
class CacheCommentCount(Node):
    def __init__(self, comment_object, var_name='count'):
        self.comment_object = Variable(comment_object)
        self.as_var = var_name
    def render(self, context):
        cache_count = None
        the_object = self.comment_object.resolve(context)
        key = sha1('comment_count_%s_%s' % (the_object.__unicode__(), the_object.pk)).hexdigest()
        cache_count = cache.get(key)
        if cache_count is None:
            cache_count = Comment.objects.filter(
                content_type=the_object.get_ct(),
                object_pk=smart_unicode(the_object.pk),
                site__pk=settings.SITE_ID,
                is_public=True,
                is_removed=False
            ).count()
            cache_count
            cache.set(key, cache_count, 1500)
        context[self.as_var] = cache_count
        return ""
def DoCacheCommentCount(parser, token):

    '''{% cache_comment_count [object] as [varname] %} '''
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError, "cache_comment_count takes exactly 3 arguments"
    elif bits[2] != 'as':
        raise TemplateSyntaxError, "second argument of cache_comment_count tage must be 'as'"
    else:
        return CacheCommentCount(bits[1], bits[3])

register.tag('get_cached_comment_count', DoCacheCommentCount)
register.tag('get_comment_count', get_comment_count)
register.tag('get_comment_list', get_comment_list)
register.tag('get_comment_form', get_comment_form)
register.tag('render_comment_form', render_comment_form)
register.simple_tag(comment_form_target)

