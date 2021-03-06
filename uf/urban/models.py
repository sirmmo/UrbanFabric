from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.gdal import *
from django.contrib.gis.geos import *
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

#geographic
class GeoResource(models.Model):
    wkt = models.TextField(blank=True, null=True)
    def __unicode__(self):
        return self.wkt
    class Meta:
        abstract = True

class PointResource(GeoResource):
    geolocation = gismodels.PointField(srid=4326)
    latitude = models.TextField(blank = True, null=True)
    longitude = models.TextField(blank = True, null=True)
    objects = gismodels.GeoManager()

    def save(self):
        self.wkt = OGRGeometry(str(self.geolocation)).wkt
        self.latitude = OGRGeometry(str(self.geolocation)).y
        self.longitude = OGRGeometry(str(self.geolocation)).x
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
    latitude = models.TextField(blank = True, null=True)
    longitude = models.TextField(blank = True, null=True)
    geolocation = gismodels.PointField(srid=4326, blank = True, null=True)
    element = models.ForeignKey('Venue', related_name="interest_area")
    radius = models.PositiveIntegerField()
    def save(self):
        self.geolocation = self.element.geolocation
        self.wkt = OGRGeometry(str(self.geolocation)).wkt
        self.latitude = OGRGeometry(str(self.geolocation)).y
        self.longitude = OGRGeometry(str(self.geolocation)).x
        super(InterestArea, self).save() # Call the "real" save() method

    def __unicode__(self):
        return self.element.name + ": radius = " + str(self.radius)

#classifications
class Classification(models.Model):
    icon = models.ImageField(upload_to = "img/class/")
    name=models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    parent = models.ForeignKey('Classification', blank = True, null=True, default = None)
    suggested_products = models.ManyToManyField('Production', related_name="sold_by")

    commercial = models.BooleanField(default=True)
    public_service = models.BooleanField(default = False)
    abstract = models.BooleanField(default = False)

    def save(self):
        self.slug = slugify(self.name)
        super( Classification, self ).save()
        
    def __unicode__(self):
        return self.name

#production
class Production(models.Model):
    icon = models.ImageField(upload_to = "img/prods/")
    name=models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank = True)
    parent = models.ForeignKey('Production', blank = True, null=True, default = None)

    def __unicode__(self):
        return self.name
    def save(self):
        self.slug = slugify(self.name)
        super( Production, self ).save()

#elements
class Venue(PointResource):
    name = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank = True)
    description = models.TextField()
    manager = models.ForeignKey(User, related_name="manages_venues")
    classification = models.ManyToManyField(Classification, related_name="classifies")
    sold_products = models.ManyToManyField(Production, related_name="sold", null=True, blank=True)
    bought_products = models.ManyToManyField(Production, related_name="bought", null=True, blank=True)
    opening = models.ManyToManyField('Interval', null=True, blank=True)
    links = models.ManyToManyField('Link', null=True, blank=True)
    server = models.ForeignKey('TrustedServer', blank = True, null=True, default = None)

    objects = gismodels.GeoManager()

    def __unicode__(self):
        return self.name
    def save(self):
        self.slug = slugify(self.name)
        super(Venue, self).save() # Call the "real" save() method
        if self.id:
            d = InterestArea.objects.filter(element__id = self.id)
            if len(d)== 1:
                d = d[0]
                d.save()

class Link(models.Model):
    url = models.URLField(verify_exists=True)
    type = models.ForeignKey('LinkFamily')
    def __unicode__(self):
        return self.url

class LinkFamily(models.Model):
    name=models.CharField(max_length = 150)
    icon = models.ImageField(upload_to = "img/links/")
    def __unicode__(self):
        return self.name

class CollectionClassification(models.Model):
    name=models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank = True)
    private = models.BooleanField(default = True)
    
    def __unicode__(self):
        return self.name
    def save(self):
        self.slug = slugify(self.name)
        super(CollectionClassification, self).save() # Call the "real" save() method
        
class ElementCollection(models.Model):
    name = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank = True)
    elements = models.ManyToManyField(Venue, related_name = "collections")
    manager = models.ForeignKey(User, related_name="manages_groups")
    classification = models.ManyToManyField(CollectionClassification)
    color_code_back = models.CharField(max_length = 10, default="ff8c00")
    color_code_front = models.CharField(max_length = 10, default="000000")
    url = models.URLField()
    icon = models.ImageField(upload_to = 'img/colls/')
    def __unicode__(self):
        return self.name

    def save(self):

        self.slug = slugify(self.name)
        super(ElementCollection, self).save() # Call the "real" save() method


#horrible... to make better asap
class Message(models.Model):
    area = models.ForeignKey(InterestArea)
    timing = models.ManyToManyField('Interval')
    text = models.CharField(max_length=400)



DOW = (
    (0,_('Monday')),
    (1,_('Tuesday')),
    (2,_('Wednesday')),
    (3,_('Thursday')),
    (4,_('Friday')),
    (5,_('Saturday')),
    (6,_('Sunday')),
)

MOY = (
    (1,_('January')),
    (2,_('February')),
    (3,_('March')),
    (4,_('April')),
    (5,_('May')),
    (6,_('June')),
    (7,_('July')),
    (8,_('August')),
    (9,_('September')),
    (10,_('October')),
    (11,_('November')),
    (12,_('December')),
)

class Interval(models.Model):
    repeats = models.BooleanField(default= True)

    daily = models.BooleanField(default=False)
    weekly = models.BooleanField(default=False)
    monthly = models.BooleanField(default=False)
    yearly = models.BooleanField(default=False)

    time_start = models.TimeField()
    time_end = models.TimeField()

    day_start = models.PositiveSmallIntegerField(choices = DOW)
    day_end = models.PositiveSmallIntegerField(choices = DOW)

    month_start = models.PositiveSmallIntegerField(choices = MOY)
    month_end = models.PositiveSmallIntegerField(choices = MOY)

    year_start = models.PositiveIntegerField()
    year_end = models.PositiveIntegerField()

    

class TrustedServer(models.Model):
    ping_url = models.URLField(max_length = 1024, verify_exists = True);
    accepted = models.BooleanField(default = False)
