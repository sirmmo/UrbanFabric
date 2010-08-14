from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from urban.models import *
from django.core import serializers



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
        filtered.append(s)
    filtered = serializers.serialize("json", filtered, relations={'classification':{'excludes':('suggested_products','parent',)},'products':{'excludes':('parent',)}},indent=4)
    return HttpResponse(filtered, mimetype="application/json")

def by_collection(request, collection_name): 
    t = ElementCollection.objects.get(slug=collection_name)
    filtered = [] #bbox, page, etc...
    for s in t.sold.all():
        filtered.append(s)
    filtered = serializers.serialize("json", filtered, relations={'classification':{'excludes':('suggested_products','parent',)},'products':{'excludes':('parent',)}},indent=4)
    return HttpResponse(filtered, mimetype="application/json")

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
