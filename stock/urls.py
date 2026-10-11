from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Productos
    path('productos/', views.product_list, name='product_list'),
    path('productos/nuevo/', views.product_create, name='product_create'),
    path('productos/importar/', views.product_import, name='product_import'),
    path('productos/<int:pk>/', views.product_detail, name='product_detail'),
    path('productos/<int:pk>/editar/', views.product_edit, name='product_edit'),
    path('productos/<int:pk>/eliminar/', views.product_delete, name='product_delete'),
    path('productos/<int:pk>/ajuste/', views.product_adjust_stock, name='product_adjust_stock'),

    # Registro de Conteo de Stock (sesión con múltiples áreas/ubicaciones)
    path('conteos/', views.stock_count_session_list, name='stock_count_session_list'),
    path('conteos/nuevo/', views.stock_count_session_create, name='stock_count_session_create'),
    path('conteos/<int:pk>/', views.stock_count_session_detail, name='stock_count_session_detail'),
    path('conteos/<int:pk>/areas/nueva/', views.stock_count_session_add_area, name='stock_count_session_add_area'),
    path('conteos/<int:pk>/areas/<int:audit_pk>/quitar/', views.stock_count_session_remove_area, name='stock_count_session_remove_area'),
    path('conteos/<int:pk>/areas/<int:audit_pk>/reabrir/', views.stock_count_session_reopen_area, name='stock_count_session_reopen_area'),
    path('conteos/<int:pk>/finalizar/', views.stock_count_session_finalize, name='stock_count_session_finalize'),
    path('conteos/<int:pk>/excel/', views.stock_count_session_export_excel, name='stock_count_session_export_excel'),

    # Tomas de Inventario a la Fecha
    path('inventarios/', views.stock_audit_list, name='stock_audit_list'),
    path('inventarios/nuevo/', views.stock_audit_create, name='stock_audit_create'),
    path('inventarios/<int:pk>/contar/', views.stock_audit_count, name='stock_audit_count'),
    path('inventarios/<int:pk>/contar/items/<int:item_pk>/guardar/', views.stock_audit_item_save, name='stock_audit_item_save'),
    path('inventarios/<int:pk>/contar/marcar-pendientes-cero/', views.stock_audit_mark_pending_zero, name='stock_audit_mark_pending_zero'),
    path('inventarios/<int:pk>/reporte-pedido/', views.stock_audit_order_report, name='stock_audit_order_report'),
    path('inventarios/<int:pk>/exportar-csv/', views.stock_audit_export_csv, name='stock_audit_export_csv'),
    path('inventarios/<int:pk>/crear-ordenes/', views.create_orders_from_audit, name='create_orders_from_audit'),
    path('inventarios/<int:pk>/eliminar/', views.stock_audit_delete, name='stock_audit_delete'),

    # Reporte Diario Consolidado Multi-Registro (Bodega, Barra, Cocina)
    path('consolidado/', views.consolidated_selection, name='consolidated_selection'),
    path('consolidado/reporte/', views.consolidated_report_view, name='consolidated_report_view'),
    path('consolidado/exportar-csv/', views.consolidated_export_csv, name='consolidated_export_csv'),
    path('consolidado/crear-pedidos/', views.create_orders_from_consolidated, name='create_orders_from_consolidated'),

    # Pedidos / Órdenes de Compra
    path('pedidos/', views.purchase_order_list, name='purchase_order_list'),
    path('pedidos/<int:pk>/', views.purchase_order_detail, name='purchase_order_detail'),
    path('pedidos/<int:pk>/estado/', views.purchase_order_change_status, name='purchase_order_change_status'),
    path('pedidos/<int:pk>/bloquear/', views.purchase_order_toggle_lock, name='purchase_order_toggle_lock'),
    path('pedidos/express/', views.quick_order_report, name='quick_order_report'),

    # Proveedores
    path('proveedores/', views.supplier_list, name='supplier_list'),
    path('proveedores/nuevo/', views.supplier_create, name='supplier_create'),
    path('proveedores/<int:pk>/editar/', views.supplier_edit, name='supplier_edit'),

    # Categorías / Áreas
    path('categorias/', views.category_list, name='category_list'),
    path('categorias/nueva/', views.category_create, name='category_create'),
    path('categorias/<int:pk>/editar/', views.category_edit, name='category_edit'),

    # Movimientos / Kardex
    path('movimientos/', views.movement_list, name='movement_list'),
]
