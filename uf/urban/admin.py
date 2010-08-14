from django.contrib import admin
from django.contrib.gis import admin

class PointResourceAdmin(admin.OSMGeoAdmin):
	pass

class LineResourceAdmin(admin.OSMGeoAdmin):
	pass

class PolygonResourceAdmin(admin.OSMGeoAdmin):
	pass



admin.site.register(PointResource, PointResourceAdmin)
admin.site.register(LineResource, LineResourceAdmin)
admin.site.register(PolygonResource, PolygonResourceAdmin)


