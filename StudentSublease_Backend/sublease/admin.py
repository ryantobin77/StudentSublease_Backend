from django.contrib import admin
from .models import Address, Amenity, StudentListing, StudentListingImages


class StudentListingImagesInline(admin.TabularInline):
    model = StudentListingImages
    extra = 0


class StudentListingAdmin(admin.ModelAdmin):
    date_hierarchy = 'listed_date'
    filter_horizontal = ('amenities',)
    inlines = (StudentListingImagesInline,)
    list_display = ('__str__', 'lister', 'num_tenants')
    list_filter = ('num_tenants',)

    def num_tenants(self, object):
        return object.num_tenants
    num_tenants.short_description = "NUM TENANTS"
    num_tenants.admin_order_field = "num_tenants"


admin.site.register(Address)
admin.site.register(Amenity)
admin.site.register(StudentListingImages)
admin.site.register(StudentListing, StudentListingAdmin)
