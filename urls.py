from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^codedependant/', include('codedependant.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),
     (r'^static_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT,'show_indexes': True}),
    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),

     

)

urlpatterns+=patterns('',
    url(r'^$',include('core.urls')),                      
)


urlpatterns+=patterns('',
    url(r'^photos/',include('photologue.urls')),                      
)
urlpatterns+=patterns('',
    url(r'^articles/',include('codedependant.publisher.urls')),                      
)