import xapian
from djapian.indexer import CompositeIndexer
from publisher.index import Article
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import simplejson
from photologue.models import Photo


def ajax_main_search(request):
    if xapian is None:
        result =[]
        return HttpResponse(simplejson.dumps(result, mimetype="text/javascript"))
    if request.is_ajax():     
        if request.POST:
           # try:
            search = request.POST['q']
            if " " in search:
                search = search.replace(" ", " OR ")
            if "." in search:
                search = search.replace(".", ' AND ')
            flags= xapian.QueryParser.FLAG_PARTIAL|xapian.QueryParser.FLAG_WILDCARD \
                |xapian.QueryParser.FLAG_BOOLEAN |xapian.QueryParser.FLAG_PHRASE
            indexers = [Article.indexer]
            comp = CompositeIndexer(*indexers)
            res = comp.search(search).flags(flags)
            rlist = [dict(name=x.instance.__unicode__(), 
                          ct_id=x.instance.get_ctype_id(),
                          ct=x.instance.get_ct_proxy(),
                          obj_id=x.instance.pk,
                          image=x.instance.get_search_url(),
                          url=x.instance.get_absolute_url() or None) for x in res]
            return HttpResponse(simplejson.dumps(rlist), 
                            mimetype='text/javascript')
            #except:
            #    return HttpResponseBadRequest()
        else:
            return HttpResponse(simplejson.dumps({'error':True}, mimetype="text/javascript"))
    else:
        # can probably change to redirect to a search
        # page view as well
        return HttpResponseBadRequest()
    
def photo_search(request):
    term = request.POST.get('q') or None
    photos = []
    if term:
        photos = Photo.objects.filter(title__icontains = term)
        photos = [dict(
                        preview = photo.get_search_url(),
                        thumbnail = photo.get_article_url(),
                        image = photo.get_display_url(),
                        title = photo.title,
                        ct = "photo",
                        caption = photo.caption,
                       ) for photo in photos ]
        
    return HttpResponse(simplejson.dumps(photos), mimetype="text/javascript")