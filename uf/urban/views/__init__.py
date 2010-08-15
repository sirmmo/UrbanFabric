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

def filter(request, filter, mode):
#    parts = filter.split('/')
#    itm = []
#    for i in range(0, len(parts-1)):
#        itm.append(parts[i].split('+'))
#    if len(itm) == 1 :
#        pass
#    if len(parts) > 1:
#        c = parts[0].split('+')
#        def get_c(el):
#            return Classification.objects.get(el)
#        c = map (get_c,c)
#        p = parts[1].split('+')
#        def get_p(el):
#            return Production.objects.get(el)
#        p = map (get_p,p)
#        pass
#    else: #singlefilter.. normal stuff... but what stuff???
#        if mode.startswith('c'):
#            pass
#        else:
            pass
