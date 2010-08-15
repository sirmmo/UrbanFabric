from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from urban.models import *
from django.core import serializers
from urban.forms import *
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
import httplib, urllib
def add(request):
    addr = request.REQUEST.get('remote_url', "")
    if addr != "":
        s = TrustedServer ()
        s.ping_url = addr
        s.save()

def ping(request):
    if request.method == 'GET':
        return HttpResponse('I ping, therefore I am')
    else:
        pass
    

def send_ping(content):
    for server in TrustedServer.objects.all():
        params = urllib.urlencode({'payload':content})
        conn = httplib.HTTPConnection(server.ping_url)
        conn.request("POST", "/cgi-bin/query", params, headers)