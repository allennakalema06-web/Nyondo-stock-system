from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from inventory_app.decorators import allowed_roles
from .models import Receipt
import uuid
from django.db.models import Sum, F
from django.utils import timezone
from .models import Sale, SaleItem, PendingCreditSale, Receipt
from customers_app.models import TransportDelivery, Customer
from inventory_app.models import Product
from .forms import SaleForm
from decimal import Decimal
# Create your views here.

@login_required
@allowed_roles(['ADMIN', 'ATTENDANT'])
def attendant_dashboard(request):

    today = timezone.now().date()

    todays_sales = Sale.objects.filter(
        created_at__date=today
    )

    total_sales = todays_sales.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    total_transactions = todays_sales.count()

    total_paid = todays_sales.aggregate(
        total=Sum('amount_paid')
    )['total'] or 0

    total_items_sold = SaleItem.objects.filter(
        sale__created_at__date=today
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    low_stock_products = Product.objects.filter(
        quantity__lte=F('reorder_level')
    ).order_by('quantity')[:5]

    approved_sales = PendingCreditSale.objects.filter(
        approved_for_sale=True
    ).count()

    recent_sales = todays_sales.order_by(
        '-created_at'
    )[:10]

    top_products = Product.objects.order_by(
        '-quantity'
    )[:5]

    pending_deliveries = TransportDelivery.objects.filter(
        delivery_status='PENDING'
    ).count()
    
    total_transport_money = TransportDelivery.objects.aggregate(
        total=Sum('transport_fee')
    )['total'] or 0

    context = {

        'total_sales': total_sales,

        'total_transactions': total_transactions,

        'total_paid': total_paid,

        'total_items_sold': total_items_sold,

        'low_stock_products': low_stock_products,

        'approved_sales': approved_sales,
        'pending_deliveries': pending_deliveries,'total_transport_money': total_transport_money,

        'recent_sales': recent_sales,

        'top_products': top_products,

    }

    return render(
        request,
        'attendant/attendant_dashboard.html',
        context
    )

@login_required
@allowed_roles(['ADMIN', 'ATTENDANT'])
def create_sale(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            customer_name = form.cleaned_data['customer_name']
            phone_number = form.cleaned_data['phone_number']
            customer_type = form.cleaned_data['customer_type']
            distance_km = form.cleaned_data['distance_km'] or Decimal('0')
            customer, created = Customer.objects.get_or_create(
                customer_name=customer_name,
                defaults={
                    'phone_number': phone_number,
                    'customer_type': customer_type,
                }
            )
            product_ids = request.POST.getlist('product')
            quantities = request.POST.getlist('quantity')
            prices = request.POST.getlist('price')
            subtotals = request.POST.getlist('subtotal')
            subtotal_amount = Decimal('0')

            for subtotal in subtotals:
                if subtotal:
                    subtotal_amount += Decimal(subtotal)

            for product_id, quantity in zip(product_ids, quantities):
                if not product_id:
                    continue
                product = Product.objects.get(id=product_id)
                quantity = int(quantity)
                if quantity > product.quantity:
                    messages.error(
                        request,
                        f'Not enough stock for {product.product_name}'
                    )
                    return redirect('create_sale')

            transport_fee = Decimal('0')
            if distance_km > 0:
                if distance_km <= 10 and subtotal_amount >= 500000:
                    transport_fee = Decimal('0')
                else:
                    transport_fee = Decimal('30000')

            grand_total = subtotal_amount + transport_fee
            sale = form.save(commit=False)
            sale.customer = customer
            sale.attendant = request.user
            sale.subtotal_amount = subtotal_amount
            sale.transport_charge = transport_fee
            sale.total_amount = grand_total
            sale.balance = grand_total - sale.amount_paid
            sale.payment_status = 'PAID'
            sale.sale_source = 'DIRECT'
            if distance_km > 0:
                sale.requires_delivery = True
            sale.save()

            for product_id, quantity, price, subtotal in zip(product_ids, quantities, prices, subtotals):
                if not product_id:
                    continue
                product = Product.objects.get(id=product_id)
                quantity = int(quantity)
                price = Decimal(price)
                subtotal_decimal = Decimal(subtotal) if subtotal else Decimal('0')
                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    selling_price=price,
                    subtotal=subtotal_decimal
                )
                product.quantity -= quantity
                product.save()

            receipt_number = (
                f"RCPT-{sale.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            )
            Receipt.objects.create(sale=sale, receipt_number=receipt_number)
            if sale.requires_delivery:
                TransportDelivery.objects.create(
                    customer=customer,
                    sale=sale,
                    delivery_address='Not Provided',
                    distance_km=distance_km,
                    transport_fee=transport_fee,
                    delivery_status='PENDING'
                )
            messages.success(request, 'Sale recorded successfully.')
            return redirect('sale_receipt', sale_id=sale.id)
    else:
        form = SaleForm()

    context = {
        'form': form,
        'products': products,
    }
    return render(request, 'attendant/create_sale.html', context)


@login_required
@allowed_roles(['ADMIN', 'ATTENDANT'])
def sales_history(request):

    sales = Sale.objects.select_related(
        'customer',
        'attendant'
    ).order_by('-created_at')

    context = {
        'sales': sales
    }

    return render(
        request,
        'attendant/sales_history.html',
        context
    )

@login_required
@allowed_roles(['ADMIN', 'ATTENDANT'])
def sale_details(request, sale_id):

    sale = Sale.objects.get(id=sale_id)

    sale_items = SaleItem.objects.filter(
        sale=sale
    )

    context = {

        'sale': sale,

        'sale_items': sale_items,

    }

    return render(
        request,
        'attendant/sale_details.html',
        context
    )

@login_required
@allowed_roles(['ADMIN', 'ATTENDANT'])
def edit_sale(request, sale_id):

    sale = Sale.objects.get(id=sale_id)

    if request.method == 'POST':

        payment_method = request.POST.get('payment_method')

        transaction_reference = request.POST.get(
            'transaction_reference'
        )

        amount_paid = request.POST.get('amount_paid')

        sale.payment_method = payment_method

        sale.transaction_reference = transaction_reference

        sale.amount_paid = Decimal(amount_paid)

        sale.balance = (
            sale.total_amount -
            sale.amount_paid
        )

        if sale.balance <= 0:

            sale.payment_status = 'PAID'

            sale.balance = 0

        else:

            sale.payment_status = 'PARTIAL'

        sale.save()

        messages.success(
            request,
            'Sale record updated successfully.'
        )

        return redirect('sales_records')

    context = {
        'sale': sale,
    }

    return render(
        request,
        'attendant/edit_sale.html',
        context
    )

@login_required
@allowed_roles(['ADMIN', 'ATTENDANT'])
def sale_receipt(request, sale_id):

    sale = Sale.objects.get(id=sale_id)

    items = sale.items.all()

    context = {
        'sale': sale,
        'items': items,
    }

    return render(
        request,
        'attendant/sale_receipt.html',
        context
    )