from core.forms.models import InsertCodeForm, PhotoUploadForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.template.defaultfilters import slugify
def ajax_code_form(request):
    if request.is_ajax():
        form = InsertCodeForm()
        
        return HttpResponse(form.as_ul(), mimetype="text/html")
    else:
        return HttpResponseBadRequest()
    
def photo_upload(request):
    if request.FILES:
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            # photo upload is meant to be quick and easy
            # so we infer the name of the photo by the name of the file
            bits = photo.image_filename().split('.')
            ext = bits[-1].lower()
            photo.title = bits[0].replace('_', '-').replace('-', ' ').capitalize()
            photo.title_slug = slugify(photo.title)
            photo.save()
            s = photo.get_display_size()
            return HttpResponse(simplejson.dumps({'status':1,
                                                  'width':s[0],
                                                  'height':s[1],
                                                  'mime':ext,
                                                  'preview':photo.get_admin_thumbnail_url()}
            ), mimetype="text/javascript")
    else:
        f = PhotoUploadForm()
        return render_to_response('core/ajax_photoupload.html', {'form':f}, context_instance=RequestContext(request))
    return HttpResponse(simplejson.dumps({'status':1}), mimetype="text/javascript")
def ajax_photo_form(request):
    if request.POST:
        return HttpResponseBadRequest()    
    if request.is_ajax():
        form = PhotoUploadForm()
        html = render_to_string('core/ajax_photoupload.html', {'form':form}, context_instance=RequestContext(request))
        return HttpResponse(html, mimetype='text/html')
    else:
        return HttpResponseBadRequest()    