from django import forms

from .models import Sale

from customers_app.models import Customer

from inventory_app.models import Product

from django import forms

from .models import Sale


class SaleForm(forms.ModelForm):

    customer_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Customer Name'
            }
        )
    )

    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }
        )
    )

    customer_type = forms.ChoiceField(
        choices=[
            ('NORMAL', 'Normal Buyer'),
            ('RETAIL', 'Retailer'),
            ('WHOLESALE', 'Wholesaler'),
        ],
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )
    delivery_address = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Delivery Address'
            }
        )
    )

    distance_km = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Distance KM'
            }
        )
    )

    class Meta:

        model = Sale

        fields = [
            'payment_method',
            'transaction_reference',
            'amount_paid',
        ]

        widgets = {

            'payment_method': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'transaction_reference': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Transaction Reference'
                }
            ),

            'amount_paid': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Amount Paid',
                }
            ),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get(
            'phone_number'
        )
        if not phone:
            return phone
        if not phone.isdigit():
            raise forms.ValidationError(
                'Phone number must contain digits only.'
            )
        
        if len(phone) < 10:
            raise forms.ValidationError(
                'Phone number is too short.'
            )
        return phone
    
    def clean_amount_paid(self):
        amount = self.cleaned_data['amount_paid']
        if amount < 0:
            raise forms.ValidationError(
                'Amount cannot be negative.'
            )
        return amount
    def clean_distance_km(self):
        distance = self.cleaned_data['distance_km']
        if distance and distance < 0:
            raise forms.ValidationError(
                'Distance cannot be negative.'
            )
        return distance
    def clean_transaction_reference(self):
        reference = self.cleaned_data.get(
            'transaction_reference'
        )
        payment_method = self.cleaned_data.get(
            'payment_method'
        )
        # If payment method is not CASH, reference must be provided
        if payment_method != 'CASH':
            if not reference:
                raise forms.ValidationError(
                    'Transaction reference is required.'
                )
        #Only check length if reference exists
        if reference and len(reference) < 5:

            raise forms.ValidationError(
                'Reference must be at least 5 characters long.'
            )
        return reference
    