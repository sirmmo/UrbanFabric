from django.contrib import admin
from django.contrib.gis import admin
from urban.models import *
class PointResourceAdmin(admin.OSMGeoAdmin):
	pass

class LineResourceAdmin(admin.OSMGeoAdmin):
	pass

class PolygonResourceAdmin(admin.OSMGeoAdmin):
	pass

class GeoElementCollectionAdmin(admin.OSMGeoAdmin):
	pass

class ElementAdmin(admin.OSMGeoAdmin):
	pass


admin.site.register(PointResource, PointResourceAdmin)
admin.site.register(LineResource, LineResourceAdmin)
admin.site.register(PolygonResource, PolygonResourceAdmin)

admin.site.register(GeoElementCollection,GeoElementCollectionAdmin)
admin.site.register(InterestArea)
admin.site.register(Classification)
admin.site.register(Production)
admin.site.register(Venue, ElementAdmin)
admin.site.register(CollectionClassification)
admin.site.register(ElementCollection)
