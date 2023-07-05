from django import forms

from server.apps.color.models import Color

from ..models import Product, ProductName


class ProductForm(forms.ModelForm):
    name = forms.CharField(label="Ad", max_length=255, required=True)
    color = forms.CharField(label="Rəng", max_length=255, required=True)

    class Meta:
        model = Product
        fields = ['name', 'color']

        error_messages = {
            'name': {
                'required': "Ad boş ola bilməz.",
                'max_length': "Ad 255 simvoldan çox ola bilməz.",
            },
            'color': {
                'required': "Rəng boş ola bilməz.",
                'max_length': "Rəng 255 simvoldan çox ola bilməz.",
            },
        }

    def __init__(self, *args, **kwargs):
        self.check = kwargs.pop('check', True)
        super(ProductForm, self).__init__(*args, **kwargs)
        self.check = not self.instance.pk if self.check is None else self.check
    
    def clean_name(self):
        return self.get_or_create('name', ProductName)
    
    def clean_color(self):
        return self.get_or_create('color', Color)

    def clean(self):
        if self.check:
            name = self.cleaned_data.get('name')
            color = self.cleaned_data.get('color')
            if Product.objects.filter(name=name, color=color).exists():
                raise forms.ValidationError('Bu ad və rəngdə məhsul artıq mövcuddur!')
        return self.cleaned_data
    
    def get_or_create(self, field, model):
        name = self.cleaned_data.get(field)
        try:
            name = int(name)
            if temp := model.objects.filter(pk=name).first():
                return temp
            else:
                raise ValueError
        except ValueError:
            return model.objects.create(name=name)
        
    def save(self, commit=True):
        name = self.cleaned_data['name']
        color = self.cleaned_data['color']
        product = Product.objects.filter(name=name, color=color).first()
        return product or super(ProductForm, self).save(commit=commit)
    