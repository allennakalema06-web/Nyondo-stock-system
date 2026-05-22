from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Product, StockEntry, StockEntryItem, Category, Supplier, StockAdjustment
from django.db import models
from .forms import StockEntryForm, ProductForm, StockEntryItemFormSet, StockAdjustmentForm, SupplierForm
from decimal import Decimal
from django.db.models import Sum, F, DecimalField

# Create your views here.

def manager_dashboard(request):

    total_products = Product.objects.count()

    total_stock_quantity = 0

    total_inventory_value = 0

    products = Product.objects.all()

    for product in products:

        total_stock_quantity += product.quantity

        total_inventory_value += (
            product.quantity * product.unit_cost
        )

    low_stock_products = Product.objects.filter(
        quantity__lte=models.F('reorder_level')
    ).count()

    supplier_credit = Supplier.objects.filter(
        balance_due__gt=0
    )

    total_supplier_credit = 0

    for supplier in supplier_credit:

        total_supplier_credit += supplier.balance_due

    recent_stock = StockEntry.objects.select_related(
        'supplier'
    ).order_by('-date_added')[:5]

    top_products = Product.objects.order_by(
        '-quantity'
    )[:5]

    context = {

        'total_products': total_products,

        'total_stock_quantity': total_stock_quantity,

        'total_inventory_value': total_inventory_value,

        'low_stock_products': low_stock_products,

        'total_supplier_credit': total_supplier_credit,

        'recent_stock': recent_stock,

        'top_products': top_products,

    }

    return render(
        request,
        'manager/dashboard.html',
        context
    )
def product_list(request):

    products = Product.objects.select_related(
        'category'
    ).all().order_by('product_name')

    search_query = request.GET.get('search')

    category_id = request.GET.get('category')

    if search_query:

        products = products.filter(
            product_name__icontains=search_query
        )

    if category_id:

        products = products.filter(
            category_id=category_id
        )

    categories = Category.objects.all()

    total_products = products.count()

    low_stock_count = products.filter(
        quantity__lte=F('reorder_level')
    ).count()

    context = {

        'products': products,

        'categories': categories,

        'total_products': total_products,

        'low_stock_count': low_stock_count,

    }

    return render(
        request,
        'manager/product_list.html',
        context
    )




def register_stock(request):

    if request.method == 'POST':

        form = StockEntryForm(request.POST)

        formset = StockEntryItemFormSet(
            request.POST,
            prefix='items'
    )

        if form.is_valid() and formset.is_valid():

            stock_entry = form.save(commit=False)

            stock_entry.added_by = request.user

            stock_entry.save()

            total_cost = 0

            items = formset.save(commit=False)

            for item in items:

                item.stock_entry = stock_entry

                item.subtotal = (
                    item.quantity * item.unit_cost
                )

                total_cost += item.subtotal

                item.save()
            for deleted_form in formset.deleted_forms:

                    if deleted_form.instance.pk:

                       deleted_form.instance.delete()

            product = item.product

            product.quantity += item.quantity

            product.unit_cost = item.unit_cost

            wholesale_markup = formset.cleaned_data[
                    items.index(item)
                ]['wholesale_markup']

            normal_markup = formset.cleaned_data[
                     items.index(item)
                ]['normal_markup']

            retail_markup = formset.cleaned_data[
                    items.index(item)
                ]['retail_markup']
            
            
            product.wholesale_price = (
                    item.unit_cost *
                    (1 + (wholesale_markup / 100))
                )

            product.normal_price = (
                    item.unit_cost *
                    (1 + (normal_markup / 100))
                )

            product.retail_price = (
                    item.unit_cost *
                    (1 + (retail_markup / 100))
                )
            
            product.normal_percentage = form.cleaned_data[
                'normal_percentage'
                ]

            product.retail_percentage = form.cleaned_data[
                'retail_percentage'
                ]

            product.wholesale_percentage = form.cleaned_data[
                'wholesale_percentage'
                ]
            
            product.save()

            stock_entry.total_cost = total_cost

            stock_entry.save()

            if stock_entry.supplied_on_credit:

                supplier = stock_entry.supplier

                supplier.balance_due += total_cost

                supplier.save()

            return redirect('product_list')

    else:

        form = StockEntryForm()

        formset = StockEntryItemFormSet(
            prefix='items'
        )

    context = {
        'form': form,
        'formset': formset
    }

    return render(
        request,
        'manager/register_stock.html',
        context
    )

def stock_history(request):

    stock_entries = StockEntry.objects.all().order_by(
        '-date_added'
    )

    context = {
        'stock_entries': stock_entries
    }

    return render(
        request,
        'manager/stock_history.html',
        context
    )

def stock_details(request, id):

    stock_entry = get_object_or_404(
        StockEntry,
        id=id
    )

    items = stock_entry.items.select_related('product')

    context = {
        'stock_entry': stock_entry,
        'items': items,
    }

    return render(
        request,
        'manager/stock_details.html',
        context
    )


def low_stock(request):

    products = Product.objects.filter(
        quantity__lte=models.F('reorder_level')
    ).order_by('quantity')

    total_low_stock = products.count()

    context = {
        'products': products,
        'total_low_stock': total_low_stock
    }

    return render(
        request,
        'manager/low_stock.html',
        context
    )

def stock_adjustments(request):

    adjustments = StockAdjustment.objects.select_related('product', 'adjusted_by').order_by(
        '-adjusted_at'
    )

    if request.method == 'POST':

        form = StockAdjustmentForm(request.POST)

        if form.is_valid():

            adjustment = form.save(commit=False)

            adjustment.adjusted_by = request.user

            adjustment.save()

            product = adjustment.product

            product.quantity += adjustment.quantity_changed

            if product.quantity < 0:

                product.quantity = 0

            product.save()

            return redirect('stock_adjustments')

    else:

        form = StockAdjustmentForm()

    context = {
        'form': form,
        'adjustments': adjustments
    }

    return render(
        request,
        'manager/stock_adjustments.html',
        context
    )

def add_product(request):

    if request.method == 'POST':

        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('product_list')

    else:
        form = ProductForm()

    context = {
        'form': form
    }

    return render(request, 'manager/add_product.html', context)

def edit_product(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':

        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()

            return redirect('product_list')

    else:
        form = ProductForm(instance=product)

    context = {
        'form': form
    }

    return render(request, 'manager/edit_product.html', context)

def delete_product(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':

        product.delete()

        return redirect('product_list')

    context = {
        'product': product
    }

    return render(request, 'manager/delete_product.html', context)


def supplier_list(request):

    suppliers = Supplier.objects.all().order_by(
        'supplier_name'
    )

    context = {
        'suppliers': suppliers
    }

    return render(
        request,
        'manager/supplier_list.html',
        context
    )


def add_supplier(request):

    if request.method == 'POST':

        form = SupplierForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('supplier_list')

    else:

        form = SupplierForm()

    context = {
        'form': form
    }

    return render(
        request,
        'manager/add_supplier.html',
        context
    )


def supplier_details(request, id):

    supplier = get_object_or_404(
        Supplier,
        id=id
    )

    stock_entries = StockEntry.objects.filter(
        supplier=supplier
    ).order_by('-date_added')

    context = {
        'supplier': supplier,
        'stock_entries': stock_entries
    }

    return render(
        request,
        'manager/supplier_details.html',
        context
    )


def supplier_credit(request):

    suppliers = Supplier.objects.filter(
        balance_due__gt=0
    ).order_by('-balance_due')

    total_credit = 0

    for supplier in suppliers:

        total_credit += supplier.balance_due

    recent_credit_stock = StockEntry.objects.filter(
        supplied_on_credit=True
    ).select_related(
        'supplier'
    ).order_by('-date_added')[:10]

    context = {

        'suppliers': suppliers,

        'total_credit': total_credit,

        'recent_credit_stock': recent_credit_stock,

    }

    return render(
        request,
        'manager/supplier_credit.html',
        context
    )