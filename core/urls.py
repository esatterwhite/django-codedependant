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