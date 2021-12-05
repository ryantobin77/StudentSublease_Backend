from django.contrib import admin
from .models import Conversation

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tenant', 'lister', 'message_count', 'date_started', 'date_last_active', 'last_notified')
    readonly_fields = ('message_count', 'date_started', 'date_last_active')
    search_fields = ('tenant__email', 'tenant__first_name', 'tenant__last_name', 'listing__lister__email', 'listing__lister__first_name', 'listing__lister__last_name')

    def message_count(self, obj):
        return obj.message_set.count()

    def date_started(self, obj):
        if obj.message_set.count() > 0:
            return obj.message_set.order_by('date').first().date
        else:
            return None

    def date_last_active(self, obj):
        if obj.message_set.count() > 0:
            return obj.message_set.order_by('date').last().date
        else:
            return None

    def tenant(self, obj):
        return obj.tenant.email
    tenant.short_description = "Tenant"
    tenant.admin_order_field = 'tenant__email'

    def lister(self, obj):
        return obj.listing.lister.email
    lister.short_description = "Lister"
    lister.admin_order_field = 'listing__lister__email'

admin.site.register(Conversation, ConversationAdmin)
