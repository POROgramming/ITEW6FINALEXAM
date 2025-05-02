from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Product, OrderItem

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        # Optional: Make stock readonly if already ordered
        if obj and OrderItem.objects.filter(product=obj).exists():
            return self.readonly_fields + ['stock']
        return self.readonly_fields

    def delete_model(self, request, obj):
        if OrderItem.objects.filter(product=obj).exists():
            self.message_user(
                request,
                f'❌ Cannot delete "{obj.name}". It has already been ordered.',
                level=messages.ERROR
            )
        else:
            super().delete_model(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Optional: disable delete button completely if ordered
        if obj and OrderItem.objects.filter(product=obj).exists():
            return False
        return super().has_delete_permission(request, obj)

admin.site.register(Product, ProductAdmin)
