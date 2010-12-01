'''
Created on Nov 29, 2010

@author: Eric
'''
from django.shortcuts import render_to_response
from publisher.models import Article
from django.template.context import RequestContext
def index(request):
    object_list = Article.objects.all()
    #object_list  = Article.objects.filter().extra(select={'comment_count':'''SELECT COUNT(*) FROM "django_comments" WHERE "object_pk" = 'publisher_article.id' AND "content_type_id"=%s'''%ContentType.objects.get_for_model(Article).id})
    #c = Comment.objects.filter(object_pk=1, content_type=ContentType.objects.get_for_model(Article)).count()
    return render_to_response('publisher/index.html', 
                                {'object_list':object_list}, 
                                context_instance=RequestContext(request)
                             )

def content_detail(request, ct_id, obj_id, slug):
    article = Article.objects.get(pk=obj_id)
    return render_to_response('publisher/article_detail.html', {'object':article}, context_instance=RequestContext(request))