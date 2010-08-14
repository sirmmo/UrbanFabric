from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.gdal import *
from django.contrib.gis.geos import *

#geographic

class GeoResource(models.Model):
    wkt = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return self.wkt

    @classmethod
    def from_wkt(self, wkt, ctype, oid):
        gel = WKTReader().read(wkt)
        gt = style[str(gel.geom_type)]
        gg = gt()
        gg.content_type = ctype
        gg.object_id = oid
        gg.geolocation = gel
        gg.save()


class PointResource(GeoResource):
    geolocation = gismodels.PointField(srid=4326)
    objects = gismodels.GeoManager()

    def save(self):
        self.wkt = OGRGeometry(str(self.geolocation)).wkt
      
        super(PointResource, self).save() # Call the "real" save() method

class LineResource(GeoResource):
    geolocation = gismodels.LineStringField(srid=4326)
    objects = gismodels.GeoManager()
  
    def save(self):
        self.wkt = OGRGeometry(str(self.geolocation)).wkt
        
        super(LineResource, self).save() # Call the "real" save() method

class PolygonResource(GeoResource):
    geolocation = gismodels.MultiPolygonField(srid=4326)
    objects = gismodels.GeoManager()
 
    def save(self):
        self.wkt = OGRGeometry(str(self.geolocation)).wkt
        
        super(PolygonResource, self).save() # Call the "real" save() method

#interest area

class InterestArea(models.Model):
    wkt = models.TextField(blank = True, null=True)
    geolocation = gismodels.PointField(srid=4326, blank = True, null=True)
    element = models.ForeignKey('Venue', related_name="interest_area")
    radius = models.PositiveIntegerField()
    def save(self):
        self.geolocation = self.element.geolocation
        self.wkt = OGRGeometry(str(self.geolocation)).wkt
        super(InterestArea, self).save() # Call the "real" save() method

    def __unicode__(self):
        return self.element.name + ": radius = " + str(self.radius)
#classifications
class Classification(models.Model):
    icon = models.ImageField(upload_to = "img/class/")
    name=models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    parent = models.ForeignKey('Classification', blank = True, null=True, default = None)
    suggested_products = models.ManyToManyField('Production', related_name="sold_by")

    commercial = models.BooleanField(default=True)
    public_service = models.BooleanField(default = False)
    abstract = models.BooleanField(default = False)

    def __unicode__(self):
        return self.name
#production
class Production(models.Model):
    icon = models.ImageField(upload_to = "img/prod/")
    name=models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    parent = models.ForeignKey('Production', blank = True, null=True, default = None)

    def __unicode__(self):
        return self.name

#elements

class Venue(PointResource):
    name = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True)
    description = models.TextField()
    manager = models.ForeignKey(User, related_name="manages_venues")
    classification = models.ManyToManyField(Classification, related_name="classifies")
    products = models.ManyToManyField(Production, related_name="sold")
    
    def __unicode__(self):
        return self.name
    def save(self):

        super(Venue, self).save() # Call the "real" save() method

class CollectionClassification(models.Model):
    name=models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name
    
class ElementCollection(models.Model):
    name = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True)
    elements = models.ManyToManyField(Venue, related_name = "collections")
    manager = models.ForeignKey(User, related_name="manages_groups")
    classification = models.ManyToManyField(CollectionClassification)
    color_code_back = models.CharField(max_length = 10, default="ff8c00")
    color_code_front = models.CharField(max_length = 10, default="000000")
    def __unicode__(self):
        return self.name

class GeoElementCollection(PolygonResource, ElementCollection):
    wiki = models.SlugField(max_length = 250)
    objects = gismodels.GeoManager()

    def save(self):

        super(GeoElementCollection, self).save() # Call the "real" save() method


#horrible... to make better asap
class Message(models.Model):
    daily = models.BooleanField(default=False)
    weekly = models.BooleanField(default=False)
    monthly = models.BooleanField(default=False)
    yearly = models.BooleanField(default=False)

    time_start = models.PositiveSmallIntegerField()
    time_end = models.PositiveSmallIntegerField()

    day_start = models.PositiveSmallIntegerField()
    day_end = models.PositiveSmallIntegerField()

    month_start = models.PositiveSmallIntegerField()
    month_end = models.PositiveSmallIntegerField()

    year_start = models.PositiveIntegerField()
    year_end = models.PositiveIntegerField()

    text = models.CharField(max_length=400)