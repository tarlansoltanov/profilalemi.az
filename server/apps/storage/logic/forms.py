from django import forms

from ..models import Storage


class StorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = ['quantity', 'buy_price', 'sell_price']

        error_messages = {
            'quantity': {
                'required': "Miqdar boş ola bilməz.",
                'value': "Miqdar 0-dan böyük olmalıdır.",
            },
            'buy_price': {
                'required': "Maya qiyməti boş ola bilməz.",
                'value': "Maya qiyməti 0-dan böyük olmalıdır.",
            },
            'sell_price': {
                'required': "Satış qiyməti boş ola bilməz.",
                'value': "Satış qiyməti 0-dan böyük olmalıdır.",
            },
        }

    def clean(self):
        cleaned_data = super(StorageForm, self).clean()
        quantity = cleaned_data.get("quantity")
        buy_price = cleaned_data.get("buy_price")
        sell_price = cleaned_data.get("sell_price")

        if quantity <= 0:
            self.add_error('quantity', "Miqdar 0-dan böyük olmalıdır.")
        if buy_price <= 0:
            self.add_error('buy_price', "Maya qiyməti 0-dan böyük olmalıdır.")
        if sell_price <= 0:
            self.add_error('sell_price', "Satış qiyməti 0-dan böyük olmalıdır.")

        if quantity and buy_price and sell_price:
            if buy_price > sell_price:
                self.add_error('sell_price', "Satış qiyməti maya qiymətindən böyük və ya bərabər olmalıdır.")

    def save(self, commit=True, product=None):
        instance = super(StorageForm, self).save(commit=False)
        instance.product = product
        if commit:
            instance.save()
        return instance