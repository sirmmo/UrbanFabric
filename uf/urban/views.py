from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from urban.models import *


def serializable(object):
    o = {}
    for k in object.__dict__:
        print str(k)
        if not str(k).startswith('_'):
            val = getattr(object, k, None)
            if  str(val.__class__.__name__) not in ['int', 'unicode', 'bool']:
                print "\n_serial_\n"
                val = serializable(val)
            o[k] = val
    return o


def index(request):
    pass

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
        filtered.append(serializable(s))
    return HttpResponse(simplejson.dumps(filtered), mimetype="application/json")

def by_collection(request, collection_name): 
    t = ElementCollection.objects.get(slug=collection_name)
    filtered = [] #bbox, page, etc...
    for s in t.sold.all():
        filtered.append(s)
    return HttpResponse(simplejson.dumps(filtered), mimetype="application/json")

def by_point(request, point):
    t = Production.objects.get(name=point)
    filtered = [] #bbox, page, etc...
    for s in t.sold.all():
        filtered.append(s.__dict__)
    return HttpResponse(simplejson.dumps(filtered), mimetype="application/json")


def by_id(request, id):
    t = Venue.objects.get(id=id)
    
    return HttpResponse(simplejson.dumps(t), mimetype="application/json")

def xuf_add(request):
    pass

def xuf_ping(request):
    pass

def messages_by_point(request):
    pass
