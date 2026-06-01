from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts_app.decorators import allowed_roles
from .models import Expense, DailyReport
from .forms import ExpenseForm, DepositPaymentForm
from sales_app.models import Sale
from inventory_app.models import Product, Supplier, StockEntry, SupplierPayment
from customers_app.models import Customer, TransportDelivery
from customers_app.models import Customer
from .forms import SchemeCustomerForm
from sales_app.models import PendingCreditSale, PendingCreditSaleItem
from customers_app.models import DepositPayment
from decimal import Decimal
from django.db.models import Sum
from inventory_app.forms import SupplierPaymentForm
from django.shortcuts import get_object_or_404

from django.db.models import Sum, F
# Create your views here.

@login_required
@allowed_roles(['ADMIN'])
def admin_dashboard(request):

    # REVENUE

    total_revenue = Sale.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    # EXPENSES

    total_expenses = Expense.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    # NET PROFIT

    net_profit = total_revenue - total_expenses

    # STOCK VALUE

    stock_value = Product.objects.aggregate(
        total=Sum(
            F('quantity') * F('unit_cost')
        )
    )['total'] or 0

    # CUSTOMERS

    total_customers = Customer.objects.count()

    # PENDING DELIVERIES

    pending_deliveries = TransportDelivery.objects.filter(
        delivery_status='PENDING'
    ).count()

    # LOW STOCK

    low_stock_products = Product.objects.filter(
        quantity__lte=F('reorder_level')
    ).count()

    # RECENT SALES

    recent_sales = Sale.objects.select_related(
        'customer'
    ).order_by('-created_at')[:5]

    # RECENT EXPENSES

    recent_expenses = Expense.objects.select_related(
        'recorded_by'
    ).order_by('-created_at')[:5]

    context = {

        'total_revenue': total_revenue,

        'total_expenses': total_expenses,

        'net_profit': net_profit,

        'stock_value': stock_value,

        'total_customers': total_customers,

        'pending_deliveries': pending_deliveries,

        'low_stock_products': low_stock_products,

        'recent_sales': recent_sales,

        'recent_expenses': recent_expenses,

    }

    return render(
        request,
        'admin/admin_dashboard.html',
        context
    )

@login_required
@allowed_roles(['ADMIN'])
def expense_records(request):

    expenses = Expense.objects.select_related(
        'recorded_by'
    ).order_by('-created_at')

    total_expenses = Expense.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    context = {

        'expenses': expenses,

        'total_expenses': total_expenses,

    }

    return render(
        request,
        'admin/expense_records.html',
        context
    )


@login_required
@allowed_roles(['ADMIN'])
def add_expense(request):

    if request.method == 'POST':

        form = ExpenseForm(request.POST)

        if form.is_valid():

            expense = form.save(commit=False)

            expense.recorded_by = request.user

            expense.save()
            
            messages.success(
                request,
                'Expense recorded successfully.'
            )

            return redirect('expense_records')

    else:

        form = ExpenseForm()

    context = {

        'form': form

    }

    return render(
        request,
        'admin/add_expense.html',
        context
    )

@login_required
@allowed_roles(['ADMIN'])
def admin_sales_overview(request):

    sales = Sale.objects.select_related(
        'customer',
        'attendant'
    ).order_by('-created_at')

    total_sales = Sale.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    total_transactions = Sale.objects.count()

    paid_sales = Sale.objects.filter(
        payment_status='PAID'
    ).count()

    partial_sales = Sale.objects.filter(
        payment_status='PARTIAL'
    ).count()

    context = {

        'sales': sales,

        'total_sales': total_sales,

        'total_transactions': total_transactions,

        'paid_sales': paid_sales,

        'partial_sales': partial_sales,

    }

    return render(
        request,
        'admin/admin_sales_overview.html',
        context
    )

@login_required
@allowed_roles(['ADMIN'])
def admin_stock_overview(request):

    products = Product.objects.all().order_by(
        'product_name'
    )

    total_products = products.count()

    low_stock_count = products.filter(
        quantity__lte=F('reorder_level')
    ).count()

    stock_value = products.aggregate(
        total=Sum(
            F('quantity') * F('unit_cost')
        )
    )['total'] or 0

    context = {

        'products': products,

        'total_products': total_products,

        'low_stock_count': low_stock_count,

        'stock_value': stock_value,

    }

    return render(
        request,
        'admin/admin_stock_overview.html',
        context
    )

@login_required
@allowed_roles(['ADMIN'])
def admin_reports_center(request):

    reports = DailyReport.objects.select_related(
        'generated_by'
    ).order_by('-report_date')

    total_sales = DailyReport.objects.aggregate(
        total=Sum('total_sales')
    )['total'] or 0

    total_expenses = DailyReport.objects.aggregate(
        total=Sum('total_expenses')
    )['total'] or 0

    total_profit = DailyReport.objects.aggregate(
        total=Sum('net_profit')
    )['total'] or 0

    total_deposits = DailyReport.objects.aggregate(
        total=Sum('total_deposits')
    )['total'] or 0

    context = {

        'reports': reports,

        'total_sales': total_sales,

        'total_expenses': total_expenses,

        'total_profit': total_profit,

        'total_deposits': total_deposits,

    }

    return render(
        request,
        'admin/admin_reports_center.html',
        context
    )

@login_required
@allowed_roles(['ADMIN'])
def deposit_dashboard(request):

    scheme_customers = Customer.objects.filter(
        is_scheme_customer=True
    )

    total_scheme_customers = scheme_customers.count()

    total_deposits = DepositPayment.objects.aggregate(
        total=Sum('amount_paid')
    )['total'] or 0

    pending_pickups = PendingCreditSale.objects.filter(
        status='PENDING'
    ).count()

    approved_pickups = PendingCreditSale.objects.filter(
        approved_for_sale=True
    ).count()

    recent_deposits = DepositPayment.objects.select_related(
        'pending_sale',
        'pending_sale__customer'
    ).order_by('-payment_date')[:8]

    context = {

        'total_scheme_customers': total_scheme_customers,

        'total_deposits': total_deposits,

        'pending_pickups': pending_pickups,

        'approved_pickups': approved_pickups,

        'recent_deposits': recent_deposits,

    }

    return render(
        request,
        'admin/deposit_dashboard.html',
        context
    )

@login_required
@allowed_roles(['ADMIN'])
def register_scheme_customer(request):

    if request.method == 'POST':

        form = SchemeCustomerForm(request.POST)

        if form.is_valid():

            customer = form.save(commit=False)

            customer.is_scheme_customer = True

            customer.save()

            messages.success(
                request,
                'Scheme customer registered successfully.'
            )

            return redirect(
                'scheme_customers'
            )

    else:

        form = SchemeCustomerForm()

    context = {

        'form': form

    }

    return render(
        request,
        'admin/register_scheme_customer.html',
        context
    )

@login_required
@allowed_roles(['ADMIN'])
def scheme_customers(request):

    customers = Customer.objects.filter(
        is_scheme_customer=True
    ).order_by('-registered_at')

    context = {

        'customers': customers

    }

    return render(
        request,
        'admin/scheme_customers.html',
        context
    )


@login_required
@allowed_roles(['ADMIN'])
def deposit_history(request):

    deposits = DepositPayment.objects.select_related(
        'pending_sale',
        'pending_sale__customer'
    ).order_by('-payment_date')

    total_deposits = deposits.aggregate(
        total=Sum('amount_paid')
    )['total'] or 0

    context = {

        'deposits': deposits,

        'total_deposits': total_deposits,

    }

    return render(
        request,
        'admin/deposit_history.html',
        context
    )

@login_required
@allowed_roles(['ADMIN'])
def pending_pickups(request):

    pickups = PendingCreditSale.objects.select_related(
        'customer'
    ).order_by('-created_at')

    pending_count = pickups.filter(
        approved_for_sale=False
    ).count()

    approved_count = pickups.filter(
        approved_for_sale=True
    ).count()

    context = {

        'pickups': pickups,

        'pending_count': pending_count,

        'approved_count': approved_count,

    }

    return render(
        request,
        'admin/pending_pickups.html',
        context
    )

@login_required
@allowed_roles(['ADMIN'])
def temporary_receipt(request, pending_id):

    pending_sale = PendingCreditSale.objects.get(
        id=pending_id
    )

    items = pending_sale.items.all()

    context = {

        'pending_sale': pending_sale,

        'items': items,

    }

    return render(
        request,
        'admin/temporary_receipt.html',
        context
    )

@login_required
@allowed_roles(['ADMIN'])
def supplier_credit_dashboard(request):

    suppliers_with_credit = Supplier.objects.filter(
        balance_due__gt=0
    ).order_by('-balance_due')

    total_supplier_credit = suppliers_with_credit.aggregate(
        total=Sum('balance_due')
    )['total'] or 0

    recent_credit_stock = StockEntry.objects.filter(
        supplied_on_credit=True
    ).select_related(
        'supplier'
    ).order_by('-date_added')[:8]

    recent_payments = SupplierPayment.objects.select_related(
        'supplier'
    ).order_by('-payment_date')[:8]

    context = {

        'suppliers_with_credit': suppliers_with_credit,

        'total_supplier_credit': total_supplier_credit,

        'recent_credit_stock': recent_credit_stock,

        'recent_payments': recent_payments,

    }

    return render(
        request,
        'admin/supplier_credit_dashboard.html',
        context
    )

@login_required
@allowed_roles(['ADMIN'])
def supplier_credit_list(request):

    suppliers = Supplier.objects.filter(
        balance_due__gt=0
    ).order_by('-balance_due')

    total_credit = suppliers.aggregate(
        total=Sum('balance_due')
    )['total'] or 0

    context = {

        'suppliers': suppliers,

        'total_credit': total_credit,

    }

    return render(
        request,
        'admin/supplier_credit_list.html',
        context
    )

@login_required
@allowed_roles(['ADMIN'])
def supplier_credit_details(request, supplier_id):

    supplier = get_object_or_404(
        Supplier,
        id=supplier_id
    )

    stock_entries = StockEntry.objects.filter(
        supplier=supplier,
        supplied_on_credit=True
    ).order_by('-date_added')

    payments = SupplierPayment.objects.filter(
        supplier=supplier
    ).order_by('-payment_date')

    total_credit_stock = stock_entries.aggregate(
        total=Sum('total_cost')
    )['total'] or 0

    total_paid = payments.aggregate(
        total=Sum('amount_paid')
    )['total'] or 0

    context = {

        'supplier': supplier,

        'stock_entries': stock_entries,

        'payments': payments,

        'total_credit_stock': total_credit_stock,

        'total_paid': total_paid,

    }

    return render(
        request,
        'admin/supplier_credit_details.html',
        context
    )



@login_required
@allowed_roles(['ADMIN'])
def record_supplier_payment(request):

    if request.method == 'POST':

        form = SupplierPaymentForm(request.POST)

        if form.is_valid():

            payment = form.save(commit=False)

            payment.recorded_by = request.user

            supplier = payment.supplier

            if payment.amount_paid > supplier.balance_due:

                messages.error(
                    request,
                    'Payment exceeds supplier balance.'
                )

                return redirect(
                    'record_supplier_payment'
                )

            supplier.balance_due -= payment.amount_paid

            supplier.save()

            payment.save()

            messages.success(
                request,
                'Supplier payment recorded successfully.'
            )

            return redirect(
                'supplier_credit_dashboard'
            )

    else:

        form = SupplierPaymentForm()

    context = {

        'form': form

    }

    return render(
        request,
        'admin/record_supplier_payment.html',
        context
    )

@login_required
@allowed_roles(['ADMIN'])
def supplier_payment_history(request):

    payments = SupplierPayment.objects.select_related(
        'supplier',
        'recorded_by'
    ).order_by('-payment_date')

    total_paid = payments.aggregate(
        total=Sum('amount_paid')
    )['total'] or 0

    context = {

        'payments': payments,

        'total_paid': total_paid,

    }

    return render(
        request,
        'admin/supplier_payment_history.html',
        context
    )

@login_required
@allowed_roles(['ADMIN'])
def transport_overview(request):

    deliveries = TransportDelivery.objects.all()

    total_deliveries = deliveries.count()

    pending_deliveries = deliveries.filter(
        delivery_status='PENDING'
    ).count()

    completed_deliveries = deliveries.filter(
        delivery_status='DELIVERED'
    ).count()

    total_transport_income = deliveries.aggregate(
        total=Sum('transport_fee')
    )['total'] or 0

    context = {

        'total_deliveries': total_deliveries,

        'pending_deliveries': pending_deliveries,

        'completed_deliveries': completed_deliveries,

        'total_transport_income': total_transport_income,

    }

    return render(
        request,
        'admin/transport_overview.html',
        context
    )


@login_required
@allowed_roles(['ADMIN'])
def pending_deliveries(request):

    deliveries = TransportDelivery.objects.filter(
        delivery_status='PENDING'
    ).order_by('-created_at')

    context = {

        'deliveries': deliveries

    }

    return render(
        request,
        'admin/pending_deliveries.html',
        context
    )

@login_required
@allowed_roles(['ADMIN'])
def completed_deliveries(request):

    deliveries = TransportDelivery.objects.filter(
        delivery_status='DELIVERED'
    ).order_by('-created_at')

    context = {

        'deliveries': deliveries

    }

    return render(
        request,
        'admin/completed_deliveries.html',
        context
    )


@login_required
@allowed_roles(['ADMIN'])
def approve_pickup(request, pending_id):

    pickup = PendingCreditSale.objects.get(
        id=pending_id
    )

    if pickup.balance_remaining > 0:

        messages.error(
            request,
            'Customer has not completed payment.'
        )

        return redirect(
            'pending_pickups'
        )

    pickup.approved_for_sale = True

    pickup.save()

    messages.success(
        request,
        'Pickup approved successfully.'
    )

    return redirect(
        'pending_pickups'
    )

@login_required
@allowed_roles(['ADMIN'])
def record_deposit_payment(request):

    if request.method == 'POST':

        form = DepositPaymentForm(request.POST)

        if form.is_valid():

            deposit = form.save(commit=False)

            pending_sale = deposit.pending_sale

            # Add payment to the order

            pending_sale.amount_paid += deposit.amount_paid

            # Update remaining balance

            pending_sale.balance_remaining = (
                pending_sale.total_amount -
                pending_sale.amount_paid
            )

            pending_sale.save()

            # Save balance snapshot on deposit record

            deposit.remaining_balance = (
                pending_sale.balance_remaining
            )

            deposit.verified = True

            deposit.save()

            messages.success(
                request,
                'Deposit payment recorded successfully.'
            )

            return redirect(
                'deposit_dashboard'
            )

    else:

        form = DepositPaymentForm()

    context = {

        'form': form

    }

    return render(
        request,
        'admin/record_deposit_payment.html',
        context
    )

@login_required
@allowed_roles(['ADMIN'])
def create_scheme_order(request):

    customers = Customer.objects.filter(
        is_scheme_customer=True
    )

    products = Product.objects.filter(
        eligible_for_scheme=True
    )

    if request.method == 'POST':

        customer_id = request.POST.get('customer')

        product_ids = request.POST.getlist('product')

        quantities = request.POST.getlist('quantity')

        prices = request.POST.getlist('price')

        subtotals = request.POST.getlist('subtotal')

        customer = get_object_or_404(
            Customer,
            id=customer_id
        )

        total_amount = Decimal('0')

        for subtotal in subtotals:

            if subtotal:

                total_amount += Decimal(subtotal)

        pending_sale = PendingCreditSale.objects.create(

            customer=customer,

            total_amount=total_amount,

            amount_paid=Decimal('0'),

            balance_remaining=total_amount,

            approved_for_sale=False,

            created_by=request.user

        )

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

            PendingCreditSaleItem.objects.create(

                pending_sale=pending_sale,

                product=product,

                quantity=int(quantity),

                selling_price=Decimal(price),

                subtotal=Decimal(subtotal)

            )

        messages.success(
            request,
            'Scheme order created successfully.'
        )

        return redirect(
            'pending_pickups'
        )

    context = {

        'customers': customers,

        'products': products,

    }

    return render(
        request,
        'admin/create_scheme_order.html',
        context
    )