from django.contrib import admin
from .models import (
    Category, Supplier, Product, StockAudit, StockAuditItem, StockCountSession,
    PurchaseOrder, PurchaseOrderItem, StockMovement, AppSettings,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'product_count')
    search_fields = ('name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_name', 'phone', 'email')
    search_fields = ('name', 'contact_name', 'phone')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'presentation', 'locations_display', 'supplier', 'current_stock', 'unit', 'min_stock', 'ideal_stock', 'cost_price', 'is_active')
    list_filter = ('location', 'group', 'supplier', 'unit', 'is_active')
    search_fields = ('name', 'sku', 'detalle_ubicacion', 'group', 'presentation')
    list_editable = ('min_stock', 'ideal_stock', 'cost_price')


class StockAuditItemInline(admin.TabularInline):
    model = StockAuditItem
    extra = 0
    fields = ('product', 'previous_stock', 'min_stock', 'counted_stock', 'suggested_order', 'final_order', 'notes')
    readonly_fields = ('previous_stock', 'min_stock', 'suggested_order')


class StockAuditInline(admin.TabularInline):
    model = StockAudit
    extra = 0
    fields = ('title', 'category', 'location_area', 'responsible', 'status', 'completed_at')
    readonly_fields = ('completed_at',)


@admin.register(StockCountSession)
class StockCountSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'count_date', 'status', 'responsible', 'total_areas', 'completed_areas', 'total_counted_products')
    list_filter = ('status', 'count_date')
    search_fields = ('title', 'responsible')
    inlines = [StockAuditInline]


@admin.register(StockAudit)
class StockAuditAdmin(admin.ModelAdmin):
    list_display = ('title', 'audit_date', 'status', 'session', 'responsible', 'total_products_in_audit', 'total_counted_products', 'items_to_order_count')
    list_filter = ('status', 'audit_date', 'category')
    search_fields = ('title', 'responsible')
    inlines = [StockAuditItemInline]


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 0
    fields = ('product', 'quantity', 'unit', 'unit_price', 'subtotal', 'notes')
    readonly_fields = ('subtotal',)


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('code', 'date', 'supplier', 'status', 'responsible', 'total_items', 'total_cost')
    list_filter = ('status', 'date', 'supplier')
    search_fields = ('code', 'responsible', 'notes')
    inlines = [PurchaseOrderItemInline]


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'product', 'movement_type', 'quantity', 'previous_stock', 'new_stock', 'reference')
    list_filter = ('movement_type', 'created_at')
    search_fields = ('product__name', 'reference')


@admin.register(AppSettings)
class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ('hide_previous_field', 'hide_minimum_field')
