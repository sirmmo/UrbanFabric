from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models as gismodels

#geographic

class GeoResource(models.Model):
    wkt = models.TextField(blank=True, null=True)
    def __unicode__(self):
        return self.subject.__unicode__()

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
    geolocation = gismodels.PointField(srid=900913)
    objects = gismodels.GeoManager()
   
    def save(self):
        self.wkt = OGRGeometry(str(self.geolocation)).wkt
      
        super(PointResource, self).save() # Call the "real" save() method

class LineResource(GeoResource):
    geolocation = gismodels.LineStringField(srid=900913)
    objects = gismodels.GeoManager()
  
    def save(self):
        self.wkt = OGRGeometry(str(self.geolocation)).wkt
        
        super(LineResource, self).save() # Call the "real" save() method

class PolygonResource(GeoResource):
    geolocation = gismodels.PolygonField(srid=900913)
    objects = gismodels.GeoManager()
 
    def save(self):
        self.wkt = OGRGeometry(str(self.geolocation)).wkt
        
        super(PolygonResource, self).save() # Call the "real" save() method

#interest area

class InterestArea(PointResource):
    radius = models.PositiveIntegerField()

#classifications
class Classification(models.Model):
    name=models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    parent = models.ForeignKey('Classification', blank = True, null=True, default = None)
    suggested_products = models.ManyToManyField('Production', related_name="sold_by")

#production
class Production(models.Model):
    name=models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    parent = models.ForeignKey('Production', blank = True, null=True, default = None)


#elements

class Element(PointResource):
    name = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True)
    description = models.TextField()
    manager = models.ForeignKey(User, related_name="manages_venues")
    intest_area = models.ForeignKey(InterestArea)
    classification = models.ManyToManyField(Classification)
    products = models.ManyToManyField(Production, related_name="sold")

    def save(self):

        super(Element, self).save() # Call the "real" save() method

class CollectionClassification(models.Model):
    name=models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    
class ElementCollection(models.Model):
    name = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True)
    elements = models.ManyToManyField(Element, related_name = "collections")
    manager = models.ForeignKey(User, related_name="manages_groups")
    classification = models.ManyToManyField(CollectionClassification)


class GeoElementCollection(PolygonResource, ElementCollection):
    wiki = models.SlugField(max_length = 250)
    objects = gismodels.GeoManager()

    def save(self):

        super(GeoElementCollection, self).save() # Call the "real" save() method

