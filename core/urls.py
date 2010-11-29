'''
Created on Nov 22, 2010

@author: Eric
'''
from django.conf.urls.defaults import *

urlpatterns = patterns('codedependant.core.views.base',
    url(r'^$','index', name="codedependant_home"),
)
urlpatterns += patterns('codedependant.core.views.ajax',
    url(r'^ajax/insert/code/$','ajax_code_form', name="codedependant_insert_code"),
)

urlpatterns += patterns('codedependant.core.views.search',
    url(r'^search/$', 'ajax_main_search', name='codedependant_core_search'),
    url(r'^search/photos/$', 'photo_search', name='codedependant_photo_search')                        
)