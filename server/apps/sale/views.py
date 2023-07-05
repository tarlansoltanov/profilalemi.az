from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from server.apps.color.models import Color
from server.apps.customer.models import Customer
from server.apps.product.models import ProductName, Product

from .models import Sale
from .logic.forms import SaleForm



@login_required
def index(request, template_name='sale/index.html', context={}):
    context['title'] = 'Satışlar'

    if not request.user.is_superuser:
        context['sales'] = Sale.objects.filter(user=request.user).order_by('-created_at')
        template_name = 'sale/index_worker.html'

    context['sales'] = Sale.objects.all().order_by('-created_at')

    return render(request, template_name, context)

@login_required
def create(request, template_name='sale/create.html', context={}):
    context['title'] = 'Satış Əlavə Et'

    form = SaleForm(request.POST or None, user=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Satış Əlavə Edildi!')
        return redirect('sale:index')
    
    if form.non_field_errors():
        for error in form.non_field_errors():
            messages.error(request, error)

    products = Product.objects.select_related('name').select_related('color').all()
    product_prices = {}

    for product in products:
        product_prices[product.name.id] = {} if product.name.id not in product_prices else product_prices[product.name.id]
        product_prices[product.name.id][product.color.id] = { 'left' : float(product.left), 'price' : float(product.price) }

    context['product_prices'] = product_prices
    context['form'] = form
    context['colors'] = Color.objects.all()
    context['products'] = ProductName.objects.all()
    context['customers'] = Customer.objects.all()

    return render(request, template_name, context)

@login_required
def update(request, pk, template_name='sale/create.html', context={}):
    context['title'] = 'Satış Məlumatlarını Redaktə Et'

    sale = get_object_or_404(Sale, pk=pk)

    formData = {
        'id': sale.id,
        'name': sale.product.name,
        'color': sale.product.color,
        'quantity': sale.quantity,
        'sell_price': sale.sell_price,
        'customer': sale.customer,
        'paid': sale.paid,
    }

    form = SaleForm(request.POST or None, instance=formData, user=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Satış Əlavə Edildi!')
        return redirect('sale:index')
    
    if form.non_field_errors():
        for error in form.non_field_errors():
            messages.error(request, error)

    products = Product.objects.all()
    product_prices = {}

    for product in products:
        product_prices[product.name.id] = {} if product.name.id not in product_prices else product_prices[product.name.id]
        product_prices[product.name.id][product.color.id] = { 'left' : float(product.left), 'price' : float(product.price) }

    context['product_prices'] = product_prices

    context['form'] = form
    context['colors'] = Color.objects.all()
    context['products'] = ProductName.objects.all()
    context['customers'] = Customer.objects.all()

    return render(request, template_name, context)

@login_required
def delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)

    messages.success(request, 'Satış Silindi!')
    sale.delete()

    return redirect('sale:index')