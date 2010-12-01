'''
Created on Nov 22, 2010
@author: Eric
'''

from django.conf.urls.defaults import *

urlpatterns = patterns('codedependant.publisher.views.basic',
    url(r'^$', 'index', name="publisher_index"),
    url(r'^(?P<ct_id>\d+)/(?P<obj_id>\d+)/(?P<slug>[-\w]+)/$', 'content_detail', name="publisher_content_detail"),
)
urlpatterns += patterns('codedependant.publisher.views.management',
    url(r'^(?P<ct_id>\d+)/(?P<obj_id>\d+)/(?P<slug>[-\w]+)/edit/$', 'edit_item', name="publisher_content_edit")
)