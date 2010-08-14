from django.contrib import admin
from django.contrib.gis import admin
from urban.models import *
class PointResourceAdmin(admin.OSMGeoAdmin):
	pass

class LineResourceAdmin(admin.OSMGeoAdmin):
	pass

class PolygonResourceAdmin(admin.OSMGeoAdmin):
	pass

class ElementAdmin(admin.OSMGeoAdmin):
	pass


admin.site.register(PointResource, PointResourceAdmin)
admin.site.register(LineResource, LineResourceAdmin)
admin.site.register(PolygonResource, PolygonResourceAdmin)

admin.site.register(InterestArea)
admin.site.register(Classification)
admin.site.register(Production)
admin.site.register(Venue, ElementAdmin)
admin.site.register(CollectionClassification)
admin.site.register(Link)
admin.site.register(LinkFamily)
admin.site.register(ElementCollection)
admin.site.register(Message)
admin.site.register(Interval)
admin.site.register(TrustedServer)
