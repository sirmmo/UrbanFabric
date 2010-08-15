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
