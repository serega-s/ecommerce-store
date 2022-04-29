from django.contrib import admin

from order.models import Order, ShippingAddress, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "created_at"]
    list_filter = ["status", "created_at"]
    list_editable = ['status']
    search_fields = ["address__first_name", "address__address", "address__place"]
    inlines = [OrderItemInline]


admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
