from django.urls import path
from . import views

urlpatterns = [

    path(
        'admin_dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),
    path(
        'expense_records/',
        views.expense_records,
        name='expense_records'
    ),

    path(
        'add_expense/',
        views.add_expense,
        name='add_expense'
    ),
    path(
        'admin_sales_overview/',
        views.admin_sales_overview,
        name='admin_sales_overview'
    ),
    path(
        'admin_stock_overview/',
        views.admin_stock_overview,
        name='admin_stock_overview'
    ),
    path(
        'admin_reports_center/',
        views.admin_reports_center,
        name='admin_reports_center'
    ),
    path(
        'deposit_dashboard/',
        views.deposit_dashboard,
        name='deposit_dashboard'
    ),
    path(
        'register_scheme_customer/',
        views.register_scheme_customer,
        name='register_scheme_customer'
    ),

    path(
        'scheme_customers/',
        views.scheme_customers,
        name='scheme_customers'
    ),
    path(
        'record_deposit-payment/',
        views.record_deposit_payment,
        name='record_deposit_payment'
    ),
    path(
        'deposit_history/',
        views.deposit_history,
        name='deposit_history'
    ),

    path(
        'pending_pickups/',
        views.pending_pickups,
        name='pending_pickups'
    ),

    path(
        'approve_pickup/<int:pending_id>/',
        views.approve_pickup,
        name='approve_pickup'
    ),
    path(
        'create_pending_pickup/',
        views.create_pending_pickup,name='create_pending_pickup'
    ),
    path(
        'temporary_receipt/<int:pending_id>/',
        views.temporary_receipt,
        name='temporary_receipt'
    ),
    path(
        'supplier_credit_dashboard/',
        views.supplier_credit_dashboard,
        name='supplier_credit_dashboard'
    ),
    path(
        'supplier_credit_list/',
        views.supplier_credit_list,
        name='supplier_credit_list'
    ),

    path(
        'supplier_credit_details/<int:supplier_id>/',
        views.supplier_credit_details,
        name='supplier_credit_details'
    ),

    path(
        'record_supplier_payment/',
        views.record_supplier_payment,
        name='record_supplier_payment'
    ),

    path(
        'supplier_payment_history/',
        views.supplier_payment_history,
        name='supplier_payment_history'
    ),
    path(
        'transport_overview/',
        views.transport_overview,
        name='transport_overview'
    ),

    path(
        'pending_deliveries/',
        views.pending_deliveries,
        name='pending_deliveries'
    ),

    path(
        'completed_deliveries/',
        views.completed_deliveries,
        name='completed_deliveries'
    ),


]