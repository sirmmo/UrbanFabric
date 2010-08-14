from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from urban.models import *
from django.core import serializers
from urban.forms import *
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

def add(request):
    addr = request.REQUEST.get('remote_url', "")
    if addr != "":
        s = TrustedServer ()
        s.ping_url = addr
        s.save()

        #send XUF trust request
    pass

def ping(request):
    #receive XUF ping
    pass
