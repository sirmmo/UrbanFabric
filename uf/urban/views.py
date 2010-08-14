from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from urban.models import *

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
    for s in t.sold.all():
        filtered.append(s)
    return HttpResponse(simplejson.dumps(filtered), mimetype="application/json")

def by_collection(request, collection_name): 
    t = Collection.objects.get(slug=collection_name)
    filtered = [] #bbox, page, etc...
    for s in t.sold.all():
        filtered.append(s)
    return HttpResponse(simplejson.dumps(filtered), mimetype="application/json")

def by_point(request, point):
    t = Production.objects.get(name=point)
    filtered = [] #bbox, page, etc...
    for s in t.sold.all():
        filtered.append(s)
    return HttpResponse(simplejson.dumps(filtered), mimetype="application/json")


def by_id(request, id):
    t = Production.objects.get(id=id)
    
    return HttpResponse(simplejson.dumps(t), mimetype="application/json")
