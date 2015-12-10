from django.contrib import admin
from models import Store, Products

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_date', 'updated_date')
    fieldsets = (
        (None, {
            'fields': (('name', 'created_date', 'updated_date'),)
        }),
       )
    readonly_fields = ('created_date','updated_date')
    def get_queryset(self, request):
        """Limit Pages to those that belong to the request's user."""
        qs = super(StoreAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            # It is mine, all mine. Just return everything.
            return qs
        return qs.filter(user=request.user)
