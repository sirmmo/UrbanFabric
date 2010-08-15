from django.conf.urls.defaults import *


urlpatterns = patterns('',


    (r'^forms/add/user$', 'urban.views.forms.add_user'),
    (r'^forms/login/user$', 'urban.views.forms.login_user'),
    (r'^forms/delete/user/(?P<username>\w*)$', 'urban.views.forms.del_user'),

    (r'^forms/add/venue$', 'urban.views.forms.add_venue'),
    (r'^forms/add/group$', 'urban.views.forms.add_group'),

    (r'^forms/edit/venue/(?P<id>\d+)$', 'urban.views.forms.edit_venue'),
    
    (r'^forms/delete/venue/(?P<id>\d+)$', 'urban.views.forms.edit_group'),

    (r'^$', 'urban.views.index'),
    (r'^show/tags/$', 'urban.views.collections.all_tags'),
    (r'^show/prods/$', 'urban.views.collections.all_prods'),
    (r'^show/collections/$', 'urban.views.collections.all_colls'),

    (r'^tag/(?P<tag_name>\w*)/$', 'urban.views.getters.by_tag'),
    (r'^prod/(?P<classification_name>\w*)/$', 'urban.views.getters.by_classification'),
    (r'^cf/(?P<id>\d+)$', 'urban.views.getters.to_collection_id'),
    (r'^collection/(?P<collection_name>\w*)/$', 'urban.views.getters.on_collection'),
    (r'^collection/(?P<collection_name>\w*)/contents$', 'urban.views.getters.collection_contents'),
    (r'^collection/(?P<collection_name>\w*)/mapstyle$', 'urban.views.getters.collection_mapstyle'),
    
    (r'^c/(?P<collection_name>\w*)/(?P<id>\d+)$', 'urban.views.getters.by_collection_id'),
    (r'^c/(?P<collection_name>\w*)/(?P<id>\d+)/ical$', 'urban.views.getters.ical_by_id'),
    (r'^p/(?P<point>\.*)$', 'urban.views.getters.by_point'),

    (r'^messages/$', 'urban.views.getters.messages_by_point'),

    (r'^xuf/addurl/$', 'urban.views.xuf.add'),
    (r'^xuf/ping/$', 'urban.views.xuf.ping'),
)
