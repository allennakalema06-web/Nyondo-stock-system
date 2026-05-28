from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from inventory_app.decorators import allowed_roles
from .models import Receipt
from django.db.models import Sum, F
from django.utils import timezone
from .models import Sale, SaleItem, PendingCreditSale
from customers_app.models import TransportDelivery, Customer, DeliveryLocation
from inventory_app.models import Product
from .forms import SaleForm
from decimal import Decimal
# Create your views here.

@login_required
@allowed_roles(['ADMIN', 'ATTENDANT'])
def attendant_dashboard(request):
    today = timezone.now().date()

    # TODAY SALES

    todays_sales = Sale.objects.filter(
        created_at__date=today
    )

    today_sales = todays_sales.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    transaction_count = todays_sales.count()

    total_items_sold = SaleItem.objects.filter(
        sale__created_at__date=today
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    # OVERALL BUSINESS TOTALS

    overall_revenue = Sale.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    overall_transactions = Sale.objects.count()

    overall_items_sold = SaleItem.objects.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    total_customers = Customer.objects.count()


    # LOW STOCK

    low_stock_queryset = Product.objects.filter(
        quantity__lte=F('reorder_level')
    )

    low_stock_products = low_stock_queryset.count()

    # APPROVED DEPOSITS

    approved_deposits = PendingCreditSale.objects.filter(
        approved_for_sale=True
    ).count()

    # RECENT SALES

    recent_sales = Sale.objects.select_related(
        'customer'
    ).order_by(
        '-created_at'
    )[:8]

    # TOP PRODUCTS

    top_products = SaleItem.objects.values(
        'product__product_name'
    ).annotate(
        total=Sum('quantity')
    ).order_by(
        '-total'
    )[:5]

    # DELIVERIES

    pending_deliveries = TransportDelivery.objects.filter(
        delivery_status='PENDING'
    ).count()

    delivered_count = TransportDelivery.objects.filter(
        delivery_status='DELIVERED'
    ).count()

    # TRANSPORT REVENUE

    total_transport_money = TransportDelivery.objects.filter(
        transport_fee__gt=0
    ).aggregate(
        total=Sum('transport_fee')
    )['total'] or 0

    # STOCK VALUE

    stock_value = Product.objects.aggregate(
        total=Sum(
            F('quantity') * F('unit_cost')
        )
    )['total'] or 0

    context = {

        # TODAY
        'today_sales': today_sales,
        'transaction_count': transaction_count,
        'total_items_sold': total_items_sold,

        # OVERALL
        'overall_revenue': overall_revenue,
        'overall_transactions': overall_transactions,
        'overall_items_sold': overall_items_sold,
        'total_customers': total_customers,

        # OTHER
        'approved_deposits': approved_deposits,
        'pending_deliveries': pending_deliveries,
        'delivered_count': delivered_count,
        'low_stock_products': low_stock_products,
        'recent_sales': recent_sales,
        'top_products': top_products,
        'total_transport_money': total_transport_money,
        'stock_value': stock_value,

    }
    return render(
        request,
        'attendant/attendant_dashboard.html',context
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
            distance_km = (form.cleaned_data['distance_km'] or Decimal('0')
            )
            
            # PHONE VALIDATION 
            if len(phone_number) < 10: 
                messages.error( 
                    request, 
                    'Enter a valid phone number.' 
                    ) 
                return redirect('create_sale') 
            # CREATE CUSTOMER
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
            # VALIDATE PRODUCTS EXIST 
            if not product_ids: 
                messages.error( 
                    request, 
                    'Add at least one product.' 
                    ) 
                return redirect('create_sale')
            subtotal_amount = Decimal('0')

            for subtotal in subtotals:
                if subtotal:
                    subtotal_amount += Decimal(subtotal)

            #VALIDATE STOCK + QUANTITIES

            for product_id, quantity in zip(product_ids, quantities):
                if not product_id:
                    continue
                product = Product.objects.get(id=product_id)
                quantity = int(quantity)
                #QUANTITY VALIDATION
                if quantity <= 0:
                    messages.error(
                         request,
                         'Quantity must be greater than zero.'
                    )
                    return redirect('create_sale')

                #STOCK VALIDATION
                if quantity > product.quantity:
                    messages.error(
                        request,
                        f'Not enough stock for {product.product_name}'
                    )
                    return redirect('create_sale')
            #TRANSPORT LOGIC
            transport_fee = Decimal('0')
            if distance_km > 0:
                if distance_km <= 10 and subtotal_amount >= 500000:
                    transport_fee = Decimal('0')
                else:
                    transport_fee = Decimal('30000')

            grand_total = (subtotal_amount + transport_fee)

            #CREATE SALE
            sale = form.save(commit=False)
            sale.customer = customer
            sale.attendant = request.user
            sale.subtotal_amount = subtotal_amount
            sale.transport_charge = transport_fee
            sale.total_amount = grand_total
            sale.balance = (grand_total - sale.amount_paid)
            sale.payment_status = 'PAID'
            sale.sale_source = 'DIRECT'
            
                
            # FULL PAYMENT VALIDATION
            if sale.amount_paid < grand_total:
                    messages.error(request,'Attendant sales must be fully paid.'
                    )
                    return redirect('create_sale')
            
            # TRANSACTION REFERENCE VALIDATION

            if ( 
                sale.payment_method != 'CASH' and 
                not sale.transaction_reference 
                ): 
                messages.error( 
                    request, 
                    'Transaction reference is required.' 
                    ) 
                return redirect('create_sale')
            #DELIVERY FLAG
            if distance_km > 0:
                sale.requires_delivery = True

            sale.save()

            # CREATE SALE ITEM
            for product_id, quantity, price, subtotal in zip(
                product_ids, 
                quantities, 
                prices, 
                subtotals
            ):
                if not product_id:
                    continue
                product = Product.objects.get(
                    id=product_id
                )
                quantity = int(quantity)

                price = Decimal(price)

                subtotal_decimal = (
                    Decimal(subtotal) 
                    if subtotal 
                    else Decimal('0')
                )
                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    selling_price=price,
                    subtotal=subtotal_decimal
                )
                
                #UPDATE STOCK
                product.quantity -= quantity
                product.save()
            #CREATE RECEIPT
            receipt_number = (
                f"RCPT-{sale.id}-"
                f"{timezone.now().strftime('%Y%m%d%H%M%S')}"
            )
            Receipt.objects.create(
                sale=sale, receipt_number=receipt_number
            )
            #CREATE DELIVERY
            if sale.requires_delivery:
                delivery_address = request.POST.get(
                    'delivery_address'
                ) or 'Unknown Location'
                delivery_location, created = (
                    DeliveryLocation.objects.get_or_create(
                        customer=customer,location_name=delivery_address,
                        defaults={
                            'distance_km': distance_km,'transport_charge': transport_fee,
                        }
                    )
                )
                
                TransportDelivery.objects.create(
                    customer=customer,

                    sale=sale,

                    delivery_address=delivery_address,

                    delivery_location=delivery_location,

                    transport_fee=transport_fee,

                    delivery_status='PENDING',

                    truck_number='Not Assigned',

                    driver_name='Not Assigned',

                    recorded_by=request.user

                )
                messages.success(
                    request, 
                    'Sale recorded successfully.'
                )
                return redirect(
                    'sale_receipt', sale_id=sale.id
                )
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

@login_required
@allowed_roles(['ADMIN', 'ATTENDANT'])
def receipt_records(request):
    receipts = Receipt.objects.select_related(
        'sale',
        'sale__customer'
    ).order_by('-generated_at')
    context = {
        'receipts': receipts
    }
    return render(
        request, 'attendant/receipt_records.html', context
    )


@login_required
@allowed_roles(['ADMIN', 'ATTENDANT'])
def stock_check(request):
    products = Product.objects.all().order_by(
        'product_name'
    )
    
    low_stock_products = Product.objects.filter(
        quantity__lte=F('reorder_level')
    )
    context = {
        'products': products,'low_stock_products': low_stock_products,
    }
    return render(
    request,
    'attendant/stock_check.html',
    context
    )

@login_required
@allowed_roles(['ADMIN', 'ATTENDANT'])
def pending_deposit_sales(request):
    pending_sales = PendingCreditSale.objects.filter(
        approved_for_sale=True,
        status='PENDING'
    ).select_related(
        'customer'
    ).order_by('-created_at')

    context = {
        'pending_sales': pending_sales

    }
    
    return render(
        request, 
        'attendant/pending_deposit_sales.html', context
    )

@login_required
@allowed_roles(['ADMIN', 'ATTENDANT'])
def complete_pending_sale(request, pending_id):
    pending_sale = PendingCreditSale.objects.get(
        id=pending_id
    )
    
    if pending_sale.status == 'COMPLETED':
        messages.warning(
        request,
        'This deposit sale is already completed.'
        )
        return redirect('pending_deposit_sales')

    # CREATE FINAL SALE

    sale = Sale.objects.create(
        customer=pending_sale.customer,

        attendant=request.user,

        sale_source='DEPOSIT',

        deposit_reference=pending_sale,

        subtotal_amount=pending_sale.total_amount,

        transport_charge=pending_sale.transport_charge,

        total_amount=pending_sale.total_amount,

        amount_paid=pending_sale.amount_paid,

        balance=0,

        payment_status='PAID',

        payment_method='CASH',

        completed_sale=True

    )

    # CREATE SALE ITEMS

    pending_items = pending_sale.items.all()

    for item in pending_items:
        
        SaleItem.objects.create(
            
            sale=sale,

            product=item.product,

            quantity=item.quantity,

            selling_price=item.selling_price,

            subtotal=item.subtotal

        )

        # REDUCE STOCK

        product = item.product

        product.quantity -= item.quantity

        product.save()

    # CREATE RECEIPT

    receipt_number = f"RCPT-{sale.id}"

    Receipt.objects.create(
        
        sale=sale,
        receipt_number=receipt_number

    )

    # MARK DEPOSIT COMPLETE

    pending_sale.status = 'COMPLETED'

    pending_sale.save()

    messages.success(
        request,
        'Pending deposit successfully completed.'
    )

    return redirect(
        'sale_receipt',
        sale.id
    )


@login_required
@allowed_roles(['ADMIN', 'ATTENDANT'])
def transport_records(request):
    deliveries = TransportDelivery.objects.select_related(
        'customer',
        'sale',
        'delivery_location',
        'recorded_by'
    ).order_by('-created_at')
    
    pending_count = deliveries.filter(
        delivery_status='PENDING'
    ).count()
    
    delivered_count = deliveries.filter(
        delivery_status='DELIVERED'
    ).count()
    
    total_transport_money = deliveries.aggregate(
        total=Sum('transport_fee')
    )['total'] or 0
    
    context = {
        'deliveries': deliveries,

        'pending_count': pending_count,

        'delivered_count': delivered_count,

        'total_transport_money': total_transport_money,

    }
    
    return render(
        request, 'attendant/transport_records.html', context
    )


