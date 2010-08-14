from django.conf.urls.defaults import *


urlpatterns = patterns('',
   
    (r'^$', 'urban.views.index'),
    (r'^tag/(?P<tag_name>\w*)/$', 'urban.views.by_tag'),
    (r'^prod/(?P<classification_name>\w*)/$', 'urban.views.by_classification'),
    (r'^cf/(?P<id>\d+)$', 'urban.views.to_collection_id'),
    (r'^collection/(?P<collection_name>\w*)/$', 'urban.views.by_collection'),
    
    (r'^c/(?P<collection_name>\w*)/(?P<id>\d+)$', 'urban.views.by_collection_id'),
    (r'^p/(?P<point>\.*)$', 'urban.views.by_point'),

    (r'^messages/$', 'urban.views.messages_by_point'),

    (r'^xuf/addurl/$', 'urban.views.xuf_add'),
    (r'^xuf/ping/$', 'urban.views.xuf_ping'),
)
