from django.urls import path
from . import views

urlpatterns = [
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('access_denied/', views.access_denied,
    name='access_denied'),
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
    path('categories/', views.category_list,
    name='category_list'),
    path('add_category/', views.add_category,
    name='add_category'),
    path('edit_category/<int:id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),
    path('category_details/<int:id>/', views.category_details, name='category_details'),
    path('pricing/',views.pricing_list,
    name='pricing_list'),
    path('pricing/update/<int:id>/',views.update_pricing, name='update_pricing'),
    path('reports/', views.reports_dashboard, name='reports_dashboard'),
    path('low_stock_report/', views.low_stock_report, name='low_stock_report'),
    path('edit_supplier/<int:id>/', views.edit_supplier, name='edit_supplier'),path('delete_supplier/<int:id>/', views.delete_supplier,name='delete_supplier'),
    path('edit_stock_entry/<int:id>/',views.edit_stock_entry,name='edit_stock_entry'),
    
   

]