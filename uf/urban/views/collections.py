from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from urban.models import *
from django.core import serializers
from urban.forms import *
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext


def show_all(request):
    pass

def all_tags(request):
    c = Classification.objects.all()
    return HttpResponse(serializers.serialize('json', c), mimetype="application/json")
def all_prods(request):
    c = Production.objects.all()
    return HttpResponse(serializers.serialize('json', c), mimetype="application/json")
def all_colls(request):
    c = ElementCollection.objects.all()
    return HttpResponse(serializers.serialize('json', c), mimetype="application/json")

