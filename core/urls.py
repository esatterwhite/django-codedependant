'''
Created on Nov 22, 2010

@author: Eric
'''
from django.conf.urls.defaults import *

urlpatterns = patterns('codedependant.core.views.ajax',
#    url(r'^ajax/$','', name=""),
)
urlpatterns += patterns('codedependant.core.views.base',
    url(r'^$','index', name="codedependant_home"),
)
rlpatterns = patterns('codedependant.core.views.search',
#    url(r'^search/$','', name=""),
)