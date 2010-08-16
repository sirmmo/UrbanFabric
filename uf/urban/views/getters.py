from cmath import sqrt
import json

from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect
from settings import DEBUG
from uf.urban.models import InterestArea
from urban.forms import *
from urban.models import *

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
        stuff['url'] = "#%s/%s" % (collection_name, stuff['id'])
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

from django.contrib.gis.measure import D
from django.contrib.gis.geos import *
from django.contrib.gis.gdal import *
from django.db.models import F
import math
def messages_by_point(request):
    point = request.REQUEST.get('point', None)
    if not point == None:
        
        point = simplejson.loads(point)
        point = Point(point['c'], point['b'])
        time = request.REQUEST.get('time', None)
        if not (point == None or time == None):
            ias = InterestArea.objects.all().values('wkt', 'element_id', 'radius', 'id', )
            print point

            def proc(el):
                #                print point.x
                #                print point.y
                p2 = fromstr(el['wkt'])
                #                print p2.x
                #                print p2.y
                dist = sqrt((point.y-p2.y) ** 2 + ((point.x-p2.x) * math.cos(point.y * 2 * math.pi / 360)) ** 2) * 111000
                dist = dist.real
                #                print      dist
                if dist < el['radius']:
                    el['geo'] = fromstr(el['wkt'])
                    return el
            ias = map(proc, ias)
            #            print ias
            ms = Message.objects.filter(area__id__in=[i['id'] for i in ias]).values('text', 'area__element__name')
            def resp(el):
                el['name'] = str(el['area__element__name'])
                del el['area__element__name']
                el['text'] = str(el['text'])
                return el
            ms = map(resp, ms)

            return HttpResponse(ms)
    return HttpResponse()


def ical_by_id(request):
    pass


def area(request):
    ne = request.REQUEST.get('ne')
    ne = simplejson.loads(ne)
    ne = Point(ne['c'], ne['b'])
    sw = request.REQUEST.get('sw')
    sw = simplejson.loads(sw)
    sw = Point(sw['c'], sw['b'])
    print ne
    print sw
    nw = Point(ne.x, sw.y)
    print nw
    se = Point(sw.x, ne.y)
    print se
    p = Polygon([ne, se, sw, nw, ne])
    print p
    t = Venue.objects.filter(geolocation__contained = p)
    a = [serializable(x) for x in t]
    def polish(stuff):
        del stuff['geolocation']
        del stuff['wkt']
        return stuff
    a = map(polish, a)
    return HttpResponse(simplejson.dumps(a), mimetype="application/json")
    



