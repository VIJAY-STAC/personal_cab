from django.contrib import admin
from .models import Cars, File, Trips, City, Booking, TripTimeTable, TripStatus, ProfitLoss
# Register your models here.

admin.site.register(Cars)
class UserAdmin(admin.ModelAdmin):
    list_display=['id','name','milege']


admin.site.register(Trips)
class TripsAdmin(admin.ModelAdmin):
    list_display=['id','name','milege']

admin.site.register(City)
class TripsAdmin(admin.ModelAdmin):
    list_display=['id',]

admin.site.register(Booking)
class TripsAdmin(admin.ModelAdmin):
    list_display=['id']

admin.site.register(TripTimeTable)
class TripsAdmin(admin.ModelAdmin):
    list_display=['id']

admin.site.register(TripStatus)
class TripsAdmin(admin.ModelAdmin):
    list_display=['id']


admin.site.register(ProfitLoss)
class TripsAdmin(admin.ModelAdmin):
    list_display=['id']

admin.site.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display=['id','created_by','name','key','url','size','file_type']