from django.contrib import admin
from .models import User
# Register your models here.

admin.site.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['id','email','date_of_birth', 'is_active', 'is_admin']