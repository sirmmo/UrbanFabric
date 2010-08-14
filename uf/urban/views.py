from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from urban.models import *
from django.core import serializers

def serializable(object):
    o = {}
    for k in object.__dict__:
        if not str(k).startswith('_'):
            val = getattr(object, k, None)
            if  str(val.__class__.__name__) not in ['int', 'unicode', 'bool']:
                val = serializable(val)
            o[k] = val
    return o

def index(request):
    return render_to_response('index.html',{})

def by_tag(request, tag_name):
    t = Production.objects.get(slug=tag_name)
    filtered = [] #bbox, page, etc...
    for s in t.sold.all():
        filtered.append(s)
    return HttpResponse(simplejson.dumps(filtered), mimetype="application/json")
    
def by_classification(request, classification_name):
    t = Classification.objects.get(slug=classification_name)
    filtered = [] #bbox, page, etc...
    for s in t.classifies.all():
        filtered.append(s)
    filtered = serializers.serialize("json", filtered, relations={'classification':{'excludes':('suggested_products','parent',)},'products':{'excludes':('parent',)}},indent=4)
    return HttpResponse(filtered, mimetype="application/json")

def by_collection(request, collection_name): 
    t = ElementCollection.objects.get(slug=collection_name)
    filtered = {} #bbox, page, etc...
    filtered['main'] = serializable(t)
    filtered['elements'] = []
    els = []
    for s in t.elements.all():
        els.append(serializable(s))
    filtered['elements'] = els
    filtered = simplejson.dumps(filtered)
    return HttpResponse(filtered, mimetype="application/json")

def mapstyle(request, collection_name):
    r = ""
    t = ElementCollection.objects.get(slug=collection_name)
    r =  '\
    [\
  {\
    featureType: "road",\
    elementType: "all",\
    stylers: [\
      { hue: "#%s" }\
    ]\
  },{\
    featureType: "transit",\
    elementType: "all",\
    stylers: [\
      { hue: "#%s" }\
    ]\
  },{\
    featureType: "landscape.man_made",\
    elementType: "all",\
    stylers: [\
      { hue: "#%s" }\
    ]\
  },{\
    featureType: "administrative",\
    elementType: "all",\
    stylers: [\
      { hue: "#%s" }   \
    ]\
  },{\
    featureType: "poi.business",\
    elementType: "all",\
    stylers: [\
      { hue: "#0088ff" },\
      { saturation: 16 }\
    ]\
  }\
]' % (self.color_code_back, self.color_code_back, self.color_code_back, self.color_code_back)
    return HttpResponse(r, mimetype="application/json" )

def by_point(request, point):
    t = Production.objects.get(name=point)
    filtered = [] #bbox, page, etc...
    for s in t.sold.all():
        filtered.append(s.__dict__)
    filtered = serializers.serialize("json", filtered, relations={'classification':{'excludes':('suggested_products','parent',)},'products':{'excludes':('parent',)}},indent=4)
    return HttpResponse(filtered, mimetype="application/json")


def by_collection_id(request,collection, id):
    t = Venue.objects.get(id=id)
    t = serializers.serialize("json", t, relations={'classification':{'excludes':('suggested_products','parent',)},'products':{'excludes':('parent',)}},indent=4)
    return HttpResponse(t, mimetype="application/json")

def to_collection_id(request, id):
    return HttpRedirect('')

def xuf_add(request):
    pass

def xuf_ping(request):
    pass


def messages_by_point(request):
    pass
