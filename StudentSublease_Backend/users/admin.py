from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import Profile, SubleaseUser
from utils.models import College, CollegeDomain

class UserProfileInline(admin.TabularInline):
    model = Profile
    extra = 0

class UserAdmin(BaseUserAdmin):
    # form = SubleaseUserChangeForm
    # add_form = SubleaseUserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'college', 'is_confirmed')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields' : ('college', 'email', 'phone_number', 'password')}),
        ('Personal info', {'fields' : ('first_name', 'last_name')}),
        ('Permissions', {'fields' : ('is_active', 'is_confirmed', 'is_disabled')}),
    )
    add_fieldsets = (
        (None, {
            'classes' : ('wide',),
            'fields' : ('college', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_confirmed'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()
    inlines = (UserProfileInline,)
    

admin.site.register(SubleaseUser, UserAdmin)
admin.site.register(Profile)
admin.site.unregister(Group)
