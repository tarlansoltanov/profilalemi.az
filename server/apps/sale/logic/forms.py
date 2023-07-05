from django import forms

from server.apps.color.models import Color
from server.apps.product.models import ProductName, Product
from server.apps.customer.models import Customer

from ..models import Sale


class SaleForm(forms.Form):
    name = forms.ModelChoiceField(queryset=ProductName.objects.all())
    color = forms.ModelChoiceField (queryset=Color.objects.all())
    quantity = forms.IntegerField()
    sell_price = forms.DecimalField(max_digits=10, decimal_places=2)
    customer = forms.CharField(max_length=255)
    paid = forms.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.instance:
            self.id = self.instance['id']
            self.fields['name'].initial = self.instance['name'].id
            self.fields['color'].initial = self.instance['color'].id
            self.fields['quantity'].initial = self.instance['quantity']
            self.fields['sell_price'].initial = self.instance['sell_price']
            self.fields['customer'].initial = self.instance['customer'].id
            self.fields['paid'].initial = self.instance['paid']
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        color = cleaned_data.get('color')
        quantity = cleaned_data.get('quantity')
        sell_price = cleaned_data.get('sell_price')
        paid = cleaned_data.get('paid')

        products = Product.objects.filter(name=name, color=color)

        if quantity * sell_price < paid:
            raise forms.ValidationError("Ödənilən məbləğ satış qiymətindən çox ola bilməz!")
        if products.count() == 0:
            raise forms.ValidationError("Bu məhsul mövcud deyil!")
        if products.first().left < quantity:
            if self.id:
                sale = Sale.objects.filter(pk=self.id).first()
                if sale.quantity + products.first().left < quantity:
                    raise forms.ValidationError("Bu məhsuldan yetərli sayda mövcud deyil!")
            else:
                raise forms.ValidationError("Bu məhsuldan yetərli sayda mövcud deyil!")
        return cleaned_data
        
    def clean_customer(self):
        customer = self.cleaned_data.get('customer')
        try:
            customer = int(customer)
            if temp := Customer.objects.filter(pk=customer).first():
                return temp
            else:
                raise ValueError
        except ValueError:
            return Customer.objects.create(name=customer)
    
    def save(self):
        cleaned_data = self.cleaned_data
        name = cleaned_data.get('name')
        color = cleaned_data.get('color')
        quantity = cleaned_data.get('quantity')
        sell_price = cleaned_data.get('sell_price')
        customer = cleaned_data.get('customer')
        paid = cleaned_data.get('paid')

        product = Product.objects.filter(name=name, color=color).first()

        if self.instance:
            sale = Sale.objects.filter(pk=self.instance['id']).first()
            sale.customer = customer
            sale.quantity = quantity
            sale.sell_price = sell_price
            sale.paid = paid
        else:
            sale = Sale.objects.create(
                customer=customer,
                quantity=quantity,
                sell_price=sell_price,
                paid=paid,
                user=self.user,
            )

        sale.save(product=product)
    