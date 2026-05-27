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
    'receipt/<int:sale_id>/',
    views.sale_receipt,
    name='sale_receipt'
    ),

]