from django import forms

from ..models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['name']
        
        error_messages = {
            'name': {
                'required': "Ad boş ola bilməz.",
                'max_length': "Ad 255 simvoldan çox ola bilməz.",
                'unique': "Bu adda müştəri artıq mövcuddur.",
            },
        }
    