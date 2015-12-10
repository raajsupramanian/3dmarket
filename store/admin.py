from django.contrib import admin
from models import Store, Products
from widgets import ImageWidgetAdmin
from django.utils.html import mark_safe

class ProductsInline(ImageWidgetAdmin):
    extra = 0
    model = Products
    fk_name = 'store'
    fieldsets = (
        (None, {
            'fields': (('name', 'price', 'display_image', 'oss_url'),),
        }),)
    verbose_name = "Product"
    verbose_name_plural = "Products"

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    def button(self, obj):
        return mark_safe('<a href="/store/'+str(obj.id)+'">View Store</a>')
    button.short_description = 'Action'
    button.allow_tags = True    
    list_display = ('name', 'created_date', 'updated_date', 'button')
    fieldsets = (
        (None, {
            'fields': (('name', 'created_date', 'updated_date', 'button'),'description')
        }),
       )
    inlines = [ProductsInline,]
    readonly_fields = ('updated_date', 'button')
    def get_queryset(self, request):
        """Limit Pages to those that belong to the request's user."""
        qs = super(StoreAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            # It is mine, all mine. Just return everything.
            return qs
        return qs.filter(user=request.user)
