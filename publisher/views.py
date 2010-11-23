# Create your views here.
from django.shortcuts import render_to_response
from publisher.models import Article
from publisher.forms import EditModeArticleForm
from django.template.context import RequestContext
from codedependant.core.utils import get_admin_object
from django.http import HttpResponseForbidden, HttpResponseRedirect
def index(request):
    object_list = Article.objects.all()
    return render_to_response('publisher/index.html', 
                                {'object_list':object_list}, 
                                context_instance=RequestContext(request)
                             )

def content_detail(request, ct_id, obj_id, slug):
    
    return render_to_response()

def edit_item(request, ct_id,obj_id, slug):
    obj = Article.objects.get(pk=obj_id)
    if request.POST:
        form = EditModeArticleForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            item = form.save()
            return HttpResponseRedirect('/')
        else:
            return render_to_response('publisher/editor.html', {'form':form}, context_instance=RequestContext(request))
    else:
        if request.user.is_staff:
            
            form = EditModeArticleForm(instance=obj)
            return render_to_response('publisher/editor.html', {'form':form}, context_instance=RequestContext(request))
        else:
            return HttpResponseForbidden()