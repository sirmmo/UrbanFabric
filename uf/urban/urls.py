from django.conf.urls.defaults import *


urlpatterns = patterns('',


    (r'^forms/add/user$', 'urban.views.form_add_user'),

    (r'^$', 'urban.views.index'),
    (r'^show/tags/$', 'urban.views.all_tags'),
    (r'^show/prods/$', 'urban.views.all_prods'),
    (r'^show/collections/$', 'urban.views.all_colls'),

    (r'^tag/(?P<tag_name>\w*)/$', 'urban.views.by_tag'),
    (r'^prod/(?P<classification_name>\w*)/$', 'urban.views.by_classification'),
    (r'^cf/(?P<id>\d+)$', 'urban.views.to_collection_id'),
    (r'^collection/(?P<collection_name>\w*)/$', 'urban.views.by_collection'),
    
    (r'^c/(?P<collection_name>\w*)/(?P<id>\d+)$', 'urban.views.by_collection_id'),
    (r'^c/(?P<collection_name>\w*)/(?P<id>\d+)/ical$', 'urban.views.ical_by_id'),
    (r'^p/(?P<point>\.*)$', 'urban.views.by_point'),

    (r'^messages/$', 'urban.views.messages_by_point'),

    (r'^xuf/addurl/$', 'urban.views.xuf_add'),
    (r'^xuf/ping/$', 'urban.views.xuf_ping'),
)
