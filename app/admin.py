from django.contrib import admin
from app.models import *

# Register your models here.
class UserMasterAdmin(admin.ModelAdmin):
    list_display=('email','password')

# admin.site.register(UserMaster)
admin.site.register(UserMaster, UserMasterAdmin)