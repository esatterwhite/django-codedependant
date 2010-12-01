from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse

def index(request):
    return render_to_response('core/home.html', {}, context_instance=RequestContext(request))

def server_error(request):
    return HttpResponse('500')