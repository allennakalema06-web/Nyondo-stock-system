from django.urls import path
from . import views

urlpatterns = [
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('register_stock/', views.register_stock, name='register_stock'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('stock_history/', views.stock_history,name='stock_history'),
    path('stock_details/<int:id>/', views.stock_details, name='stock_details'),
    path('low_stock/', views.low_stock,name='low_stock'),
    path('stock_adjustments/', views.stock_adjustments, name='stock_adjustments'),
    path('suppliers/', views.supplier_list,name='supplier_list'),
    path('add_supplier/', views.add_supplier,name='add_supplier'),
    path('supplier_details/<int:id>/', views.supplier_details, name='supplier_details'),
    path('supplier_credit/', views.supplier_credit, name='supplier_credit'),

]