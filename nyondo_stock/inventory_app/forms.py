from django import forms
from .models import StockEntry, Product, StockEntryItem, StockAdjustment, Supplier, Category, SupplierPayment
from django.forms import inlineformset_factory


class StockEntryForm(forms.ModelForm):

    class Meta:

        model = StockEntry

        fields = [
            'supplier',
            'supplied_on_credit',
            'stock_date',
            'invoice_number',
            'notes',
        ]
        widgets = {

    'supplier': forms.Select(attrs={
        'class': 'form-control'
    }),

    'invoice_number': forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter invoice number'
    }),

    'stock_date': forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }),

    'supplied_on_credit': forms.CheckboxInput(attrs={
        'class': 'checkbox-input'
    }),

    'notes': forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3,
        'placeholder': 'Additional notes'
    }),

}
  




class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [

    'category',

    'sku',

    'product_name',

    'unit',

    'unit_cost',

    'normal_percentage',

    'retail_percentage',

    'wholesale_percentage',

    'normal_price',

    'retail_price',

    'wholesale_price',

    'quantity',

    'reorder_level',

]

        widgets = {

            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

            'sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter SKU'
            }),

            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),

            'unit': forms.Select(attrs={
                'class': 'form-control'
            }),

            'unit_cost': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'normal_percentage': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'retail_percentage': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'wholesale_percentage': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'retail_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),

            'wholesale_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),

            'normal_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'reorder_level': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

        }


class StockEntryItemForm(forms.ModelForm):
    normal_percentage = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control percentage-input',
            'placeholder': 'Normal %'
        }),
        initial=25
    )
    
    retail_percentage = forms.DecimalField(

        widget=forms.NumberInput(attrs={
            'class': 'form-control percentage-input',
            'placeholder': 'Retail %'
        }),
        initial=20
    )

    wholesale_percentage = forms.DecimalField(

        widget=forms.NumberInput(attrs={
            'class': 'form-control percentage-input',
            'placeholder': 'Wholesale %'
        }),
        initial=10
    )

    class Meta:

        model = StockEntryItem

        fields = [
            'product',
            'quantity',
            'unit_cost',
        ]

        widgets = {

            'product': forms.Select(attrs={
                'class': 'form-control product-select'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control quantity-input'
            }),

            'unit_cost': forms.NumberInput(attrs={
                'class': 'form-control cost-input'
            }),
            
            'normal_percentage': forms.NumberInput(attrs={'class': 'form-control percentage-input'}),'retail_percentage': forms.NumberInput(attrs={'class': 'form-control percentage-input'}),'wholesale_percentage': forms.NumberInput(attrs={'class': 'form-control percentage-input'}),

        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({
            'class': 'form-control product-select'
        })
        self.fields['quantity'].widget.attrs.update({
            'class': 'form-control quantity-input'
        })
        self.fields['unit_cost'].widget.attrs.update({
            'class': 'form-control cost-input'
        })
        products = self.fields['product'].queryset
        choices = [('', 'Select Product')]
        for product in products:
            choices.append(
                (
                    product.id,
                    f"{product.product_name}"
                )
            )

        self.fields['product'].choices = choices

StockEntryItemFormSet = inlineformset_factory(

    StockEntry,
    StockEntryItem,

    form=StockEntryItemForm,

    extra=1,

    can_delete=True
)


class StockAdjustmentForm(forms.ModelForm):

    class Meta:

        model = StockAdjustment

        fields = [
            'product',
            'quantity_changed',
            'reason',
        ]

        widgets = {

            'product': forms.Select(attrs={
                'class': 'form-control'
            }),

            'quantity_changed': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Use negative for damaged/lost stock'
            }),

            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explain why stock is being adjusted'
            }),

        }


class SupplierForm(forms.ModelForm):

    class Meta:

        model = Supplier

        fields = [
            'supplier_name',
            'contact_person',
            'job_title',
            'phone_number',
            'alternative_phone',
            'email',
            'company_type',
            'business_registration_number',
            'tin_number',
            'website',
            'address',
            'city',
            'country',
        ]


        widgets = {

            'supplier_name': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter supplier or company name'
            }),

            'contact_person': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter contact person'
            }),

            'job_title': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Sales Manager / Director'
            }),

            'phone_number': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Primary phone number'
            }),

            'alternative_phone': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Alternative phone number'
            }),

            'email': forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'supplier@email.com'
            }),

            'company_type': forms.Select(attrs={
                'class':'form-control'
            }),

            'business_registration_number': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Business registration number'
            }),

            'tin_number': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'TIN number'
            }),

            'website': forms.URLInput(attrs={
                'class':'form-control',
                'placeholder':'https://example.com'
            }),

            'address': forms.Textarea(attrs={
                'class':'form-control',
                'rows':3,
                'placeholder':'Supplier address'
            }),

            'city': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Kampala'
            }),

            'country': forms.TextInput(attrs={
                'class':'form-control'
            }),

        }

class CategoryForm(forms.ModelForm):

    class Meta:

        model = Category

        fields = ['category_name']

        widgets = {

            'category_name': forms.TextInput(attrs={

                'class': 'form-control',

                'placeholder': 'Enter category name'

            })

        }


class PricingForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = [

            'normal_percentage',
            'retail_percentage',
            'wholesale_percentage'

        ]

        widgets = {

            'normal_percentage': forms.NumberInput(attrs={

                'class': 'form-control',

                'step': '0.01'

            }),

            'retail_percentage': forms.NumberInput(attrs={

                'class': 'form-control',

                'step': '0.01'

            }),

            'wholesale_percentage': forms.NumberInput(attrs={

                'class': 'form-control',

                'step': '0.01'

            }),

        }
class SupplierPaymentForm(forms.ModelForm):

    class Meta:

        model = SupplierPayment

        fields = [

            'supplier',

            'amount_paid',

            'payment_method',

            'transaction_reference',

        ]

        widgets = {

            'supplier': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'amount_paid': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter amount paid'
                }
            ),

            'payment_method': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'transaction_reference': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Transaction reference'
                }
            ),

        }       