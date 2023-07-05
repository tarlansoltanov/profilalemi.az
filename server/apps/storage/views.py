from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from server.apps.color.models import Color
from server.apps.product.models import Product, ProductName
from server.apps.product.logic.forms import ProductForm

from .models import Storage
from .logic.forms import StorageForm


@login_required
@user_passes_test(lambda u: u.is_superuser)
def index(request, template_name='storage/index.html', context={}):
    context['title'] = 'Anbardakı məhsullar'

    context['storage'] = Storage.objects.select_related('product__name').select_related('product__color').all().order_by('-created_at')
    
    return render(request, template_name, context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create(request, template_name='storage/create.html', context={}):
    context['title'] = 'Anbara məhsul əlavə et'

    product_form = ProductForm(request.POST or None, check=False)
    form = StorageForm(request.POST or None)

    if request.method == 'POST' and product_form.is_valid() and form.is_valid():
        product = product_form.save()
        form.save(commit=True, product=product)
        messages.success(request, 'Anbara məhsul əlavə edildi!')
        return redirect('storage:index')

    context['form'] = form
    context['product_form'] = product_form
    context['products'] = ProductName.objects.all()
    context['colors'] = Color.objects.all()
    
    return render(request, template_name, context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def update(request, pk, template_name='storage/create.html', context={}):
    context['title'] = 'Anbardakı məhsul məlumatlarını redaktə et'

    storage = get_object_or_404(Storage, pk=pk)

    product_form = ProductForm(request.POST or None, check=False, instance=storage.product)
    form = StorageForm(request.POST or None, instance=storage)

    if request.method == 'POST' and product_form.is_valid() and form.is_valid():
        product = product_form.save()
        form.save(commit=True, product=product)
        messages.success(request, 'Anbardakı məhsul məlumatları redaktə edildi!')
        return redirect('storage:index')

    context['form'] = form
    context['product_form'] = product_form
    context['products'] = ProductName.objects.all()
    context['colors'] = Color.objects.all()
    
    return render(request, template_name, context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete(request, pk):
    storage = get_object_or_404(Storage, pk=pk)

    if storage.sold > 0:
        messages.error(request, 'Bu məhsuldan satıldığı üçün silinə bilməz!')
    else:
        storage.delete()
        messages.success(request, 'Anbardakı məhsul silindi!')
    
    return redirect('storage:index')