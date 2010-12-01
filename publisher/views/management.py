'''
Created on Nov 29, 2010

@author: Eric
'''
from django.shortcuts import render_to_response
from publisher.models import Article
from publisher.forms import EditModeArticleForm
from django.template.context import RequestContext
from codedependant.core.utils import get_admin_object
from django.http import HttpResponseForbidden, HttpResponseRedirect,\
    HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from publisher.utils import get_object_form



@staff_member_required
def edit_item(request, ct_id,obj_id, slug):
    obj = get_admin_object(ct_id, obj_id)
    formclass = get_object_form(obj.__class__)
    if request.POST:
        
        form = formclass(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return render_to_response('publisher/editor.html', {'form':form}, context_instance=RequestContext(request))
    else:
        if request.user.is_staff:
            
            form = formclass(initial={
                                'title':obj.title,
                                'tag_line':obj.tag_line,
                                'content':obj.get_html_content(),
                                'summary':obj.summary,
                                'status':obj.status,
                                'author':obj.author.pk,
                                'image':obj.image,
                                'crop_from':obj.crop_from       
                             })        
            if request.is_ajax():
                return HttpResponse(form.as_ul(), mimetype='text/html')
            else:
                return render_to_response('publisher/editor.html', {'form':form}, context_instance=RequestContext(request))
        else:
            return HttpResponseForbidden()