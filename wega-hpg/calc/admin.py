from django.contrib import admin

# Register your models here.
from .models import PlantProfile, PlantTemplate, PlantProfileHistory
from django.contrib.auth.admin import UserAdmin


from import_export import resources


from import_export.admin import  ImportExportModelAdmin

admin.site.register(PlantProfile,ImportExportModelAdmin)
admin.site.register(PlantTemplate,ImportExportModelAdmin)
admin.site.register(PlantProfileHistory,ImportExportModelAdmin)