from django.contrib import admin
from .models import College, ClosestCollege, CollegeDomain

class CollegeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'address',)
    search_fields = ['college_name']

admin.site.register(College, CollegeAdmin)
admin.site.register(CollegeDomain)
admin.site.register(ClosestCollege)
