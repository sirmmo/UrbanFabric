from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from urban.models import *
from django.core import serializers
from urban.forms import *
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext


def index(request):
    return render_to_response('index.html',{})

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



