from django import forms
from .models import Expense
from customers_app.models import Customer, DepositPayment
from sales_app.models import PendingCreditSale
import re


class ExpenseForm(forms.ModelForm):

    class Meta:

        model = Expense

        fields = [

            'expense_type',

            'payment_method',

            'transaction_reference',

            'amount',

            'description',

        ]

        widgets = {

            'expense_type': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'payment_method': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'transaction_reference': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Transaction Reference'
                }
            ),

            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter amount'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Expense description'
                }
            ),

        }



class SchemeCustomerForm(forms.ModelForm):

    class Meta:

        model = Customer

        fields = [

            'customer_name',

            'phone_number',

            'nin',

            'address',

            'customer_type',

            'employer_name',

            'next_of_kin',
            'next_of_kin_contact',

        ]

        widgets = {

            'address': forms.Textarea(
                attrs={'rows': 3}
            ),

        }  

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        pattern = r'^(07\d{8}|2567\d{8})$'
        if not re.match(pattern, phone):
            raise forms.ValidationError(
                'Enter a valid Ugandan phone number.'
            )
        return phone
    
    def clean_next_of_kin_contact(self):
        contact = self.cleaned_data.get('next_of_kin_contact')

        if not contact:
            return contact

        pattern = r'^(07\d{8}|2567\d{8})$'

        if not re.match(pattern, contact):
            raise forms.ValidationError(
                'Enter a valid Ugandan phone number.'
            )

        return contact

    def clean_nin(self):
        nin = self.cleaned_data['nin'].upper()
        pattern = r'^[A-Z]{2}[0-9]{10}[A-Z]{3}$'
        if not re.match(pattern, nin):
            raise forms.ValidationError(
                'Enter a valid Ugandan NIN.'
            )
        existing = Customer.objects.filter(nin=nin)

        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise forms.ValidationError(
                'This NIN already exists.'
            )
        return nin



class DepositPaymentForm(forms.ModelForm):

    class Meta:

        model = DepositPayment

        fields = [

            'pending_sale',

            'amount_paid',

            'payment_method',

            'transaction_reference',

        ]

class PendingCreditSaleForm(forms.ModelForm):

    class Meta:

        model = PendingCreditSale

        fields = [
            'customer',
            'amount_paid',
            'transport_charge',
        ]

    customer = forms.ModelChoiceField(
        queryset=Customer.objects.filter(
            is_scheme_customer=True
        )
    )        