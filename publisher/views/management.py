'''
Created on Nov 29, 2010

@author: Eric
'''
from codedependant.core.utils import get_admin_object
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden, HttpResponseRedirect, \
    HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from publisher.utils import get_object_form
from django.contrib.contenttypes.models import ContentType


#@staff_member_required
def create_item(request, ct_id):
    ctype = ContentType.objects.get(pk=ct_id)
    formclass = get_object_form(ctype.model_class())
    
    return render_to_response('publisher/editor.html', {'form':formclass()}, context_instance=RequestContext(request))


@staff_member_required
def edit_item(request, ct_id,obj_id, slug, template_name='publisher/editor.html'):
    obj = get_admin_object(ct_id, obj_id)
    formclass = get_object_form(obj.__class__)
    if request.POST:        
        form = formclass(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            item = form.save()
            messages.add_message(request, messages.SUCCESS, 
                                 'the {type}: {title} has been saved'.format(type=item.get_ct_proxy(),
                                 title=item.title))            
            return HttpResponseRedirect(item.get_absolute_url())
        else:
            return render_to_response(template_name, 
                                      {'form':form}, 
                                      context_instance=RequestContext(request))
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
                return render_to_response(template_name, 
                                          {'form':form}, 
                                          context_instance=RequestContext(request))
        else:
            return HttpResponseForbidden()
        