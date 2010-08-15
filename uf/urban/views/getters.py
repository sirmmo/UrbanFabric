import json

from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect
from urban.forms import *
from urban.models import *
from settings import DEBUG

def serializable(object, level=0, parent=None, ancestor=None):
    o = {}
    if not object == ancestor:
        for k in object.__dict__:
            if not str(k).startswith('_'):
                val = getattr(object, k, None)
                if DEBUG:
                    print "o: " + str(object)
                    print "p: " + str(parent)
                    print "a: " + str(ancestor)
                    print ""
                    print "class: " + val.__class__.__name__
                if  str(val.__class__.__name__) not in ['int', 'unicode', 'bool', 'basestring', 'str']:
                    val = serializable(val, level + 1, object, parent)
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

def on_collection(request, collection_name):
    t = ElementCollection.objects.get(slug=collection_name)
    return HttpResponse(serializers.serialize('json', [t]), mimetype="application/json")

def collection_contents(request, collection_name):
    t = ElementCollection.objects.get(slug=collection_name).elements.all()
    a = [serializable(x) for x in t]
    def polish(stuff):
        del stuff['geolocation']
        del stuff['wkt']
        stuff['url'] = "#%s/%s" %( collection_name, stuff['id'])
        return stuff
    a = map(polish, a)
    return HttpResponse(simplejson.dumps(a), mimetype="application/json")
    


def collection_mapstyle(request, collection_name):
    t = ElementCollection.objects.get(slug=collection_name)
    str = render_to_string('mapstyle.json', {'color':t.color_code_back})
    return HttpResponse(str, mimetype="application/json")

def by_point(request, point):
    t = Production.objects.get(name=point)
    filtered = [] #bbox, page, etc...
    for s in t.sold.all():
        filtered.append(s.__dict__)
    filtered = serializers.serialize("json", filtered, relations={'classification':{'excludes':('suggested_products', 'parent', )}, 'products':{'excludes':('parent', )}}, indent=4)
    return HttpResponse(filtered, mimetype="application/json")


def by_collection_id(request, collection_name, id):
    t = Venue.objects.get(id=id)
    t = simplejson.dumps(serializable(t))
    #serializers.serialize("json", t, relations={'classification':{'excludes':('suggested_products', 'parent', )}, 'products':{'excludes':('parent', )}}, indent=4)
    return HttpResponse(t, mimetype="application/json")

def to_collection_id(request, id):
    return HttpRedirect('')


def messages_by_point(request):
    pass


def ical_by_id(request):
    pass





