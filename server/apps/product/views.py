from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from server.apps.color.models import Color

from .logic.forms import ProductForm
from .models import Product, ProductName


@login_required
@user_passes_test(lambda u: u.is_superuser)
def index(request, template_name='product/index.html', context={}):
    context['title'] = 'Məhsullar'

    context['products'] = Product.objects.select_related('name').select_related('color').all()

    return render(request, template_name, context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create(request, template_name='product/create.html', context={}):
    context['title'] = 'Məhsul əlavə et'

    form = ProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Məhsul əlavə edildi!')
        return redirect('product:index')

    context['form'] = form
    context['products'] = ProductName.objects.all()
    context['colors'] = Color.objects.all()
    
    return render(request, template_name, context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def update(request, pk, template_name='product/create.html', context={}):
    context['title'] = 'Məhsul məlumatlarını redaktə et'

    product = get_object_or_404(Product, pk=pk)

    form = ProductForm(request.POST or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Məhsul məlumatları redaktə edildi!')
        return redirect('product:index')
    
    context['form'] = form
    context['products'] = ProductName.objects.all()
    context['colors'] = Color.objects.all()
    
    return render(request, template_name, context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.storage.exists():
        messages.error(request, 'Bu məhsul anbarda olduğu üçün silinə bilməz!')
    else:
        messages.success(request, 'Məhsul silindi!')
        product.delete()

    return redirect('product:index')