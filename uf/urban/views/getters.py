from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect
from urban.forms import *
from urban.models import *




def serializable(object):
    o = {}
    for k in object.__dict__:
        if not str(k).startswith('_'):
            val = getattr(object, k, None)
            if  str(val.__class__.__name__) not in ['int', 'unicode', 'bool']:
                val = serializable(val)
            o[k] = val
    return o

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
    filtered = serializers.serialize("json", filtered, relations={'classification':{'excludes':('suggested_products', 'parent', )}, 'products':{'excludes':('parent', )}}, indent=4)
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



def by_point(request, point):
    t = Production.objects.get(name=point)
    filtered = [] #bbox, page, etc...
    for s in t.sold.all():
        filtered.append(s.__dict__)
    filtered = serializers.serialize("json", filtered, relations={'classification':{'excludes':('suggested_products', 'parent', )}, 'products':{'excludes':('parent', )}}, indent=4)
    return HttpResponse(filtered, mimetype="application/json")


def by_collection_id(request, collection, id):
    t = Venue.objects.get(id=id)
    t = serializers.serialize("json", t, relations={'classification':{'excludes':('suggested_products', 'parent', )}, 'products':{'excludes':('parent', )}}, indent=4)
    return HttpResponse(t, mimetype="application/json")

def to_collection_id(request, id):
    return HttpRedirect('')


def messages_by_point(request):
    pass


def ical_by_id(request):
    pass