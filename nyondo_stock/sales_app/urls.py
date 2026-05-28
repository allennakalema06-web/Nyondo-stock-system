from django.urls import path
from . import views

urlpatterns = [

    path(
        'attendant_dashboard/',
        views.attendant_dashboard,
        name='attendant_dashboard'
    ),
    path(
        'create/',
        views.create_sale,
        name='create_sale'
    ),
    path(
    'sales_history/',
    views.sales_history,
    name='sales_history'
    ),
    path(
    'sale_details/<int:sale_id>/',
    views.sale_details,
    name='sale_details'
    ),
    path(
    'edit_sale/<int:sale_id>/',
    views.edit_sale,
    name='edit_sale'
    ),
    path(
    'sale_receipt/<int:sale_id>/',
    views.sale_receipt,
    name='sale_receipt'
    ),
    path( 
        'receipt_records/', 
        views.receipt_records, name='receipt_records' 
    ), 
    path( 
        'transport_records/', 
        views.transport_records, name='transport_records' 
    ), 
    path( 
        'stock-check/', 
        views.stock_check, 
        name='stock_check' 
    ),
    path(
        'pending_deposit_sales/',
        views.pending_deposit_sales,name='pending_deposit_sales'
    ),
    path(
        'complete_pending_sale/[int:pending_id](int:pending_id)/',
        views.complete_pending_sale,
        name='complete_pending_sale'
    ),
    



]