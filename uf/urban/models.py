from django.contrib.auth.models import User
from django.db import models

#geographic

class GeoResource(models.Model):
    wkt = models.TextField(blank=False, null=True)
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


class PointResource(GeographicResource):
    geolocation = gismodels.PointField(srid=900913)
    objects = gismodels.GeoManager()
   
    def save(self):
        self.wkt = OGRGeometry(str(self.geolocation)).wkt
      
        super(PointResource, self).save() # Call the "real" save() method

class LineResource(GeographicResource):
    geolocation = gismodels.LineStringField(srid=900913)
    objects = gismodels.GeoManager()
  
    def save(self):
        self.wkt = OGRGeometry(str(self.geolocation)).wkt
        
        super(LineResource, self).save() # Call the "real" save() method

class PolygonResource(GeographicResource):
    geolocation = gismodels.PolygonField(srid=900913)
    objects = gismodels.GeoManager()
 
    def save(self):
        self.wkt = OGRGeometry(str(self.geolocation)).wkt
        
        super(PolygonResource, self).save() # Call the "real" save() method

#interest area

class InterestArea(PointResource):
    radius = models.PositiveItegerField()

#classifications
class Classification(models.Model):
    name=models.CharField(max_length=200)
    parent = models.ForeignKey('Classification', blank = True, null=True, default = None)
    suggested_products = models.ManyToManyField('Production', related_name="produced_by")

#production
class Production(models.Model):
    name=models.CharField(max_length=200)
    parent = models.ForeignKey('Production', blank = True, null=True, default = None)


#elements

class Element(PointResource):
    name = models.CharField(max_length=200)
    description = models.TextField()
    manager = models.ForeignKey(User, related_name="manages")
    intest_area = models.ForeignKey(InterestArea)
    

class ElementCollection(models.Model):
    elements = models.ManyToManyField(Element, related_name = "collections")
    manager = models.ForeignKey(User, related_name="manages")


