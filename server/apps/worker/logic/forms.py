from django import forms
from django.contrib.auth.models import User


class WorkerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

        error_messages = {
            'username': {
                'required': 'İstifadəçi adı boş ola bilməz!',
                'unique': 'Bu istifadəçi adı artıq mövcuddur!',
            },
            'password': {
                'required': 'Şifrə boş ola bilməz!',
            },
            'first_name': {
                'required': 'Ad boş ola bilməz!',
            },
            'last_name': {
                'required': 'Soyad boş ola bilməz!',
            },
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['password'].required = False
            self.initial['password'] = None

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password'] not in [None, '']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user