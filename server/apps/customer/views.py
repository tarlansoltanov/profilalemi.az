from django.contrib import messages
from django.db.models import OuterRef, Subquery
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from server.apps.sale.models import Sale

from .models import Customer
from .logic.forms import CustomerForm


@login_required
@user_passes_test(lambda u: u.is_superuser)
def index(request, template_name='customer/index.html', context={}):
    context['title'] = 'Müştərilər'

    last_sale_date = Sale.objects.filter(id=OuterRef('id')).order_by('-created_at').values('created_at')[:1]

    context['customers'] = Customer.objects.annotate(last_sale_date=Subquery(last_sale_date)).order_by('-last_sale_date')

    return render(request, template_name, context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create(request, template_name='customer/create.html', context={}):
    context['title'] = 'Müştəri əlavə et'

    form = CustomerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Müştəri əlavə edildi!')
        return redirect('customer:index')

    context['form'] = form
    
    return render(request, template_name, context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def update(request, pk, template_name='customer/create.html', context={}):
    context['title'] = 'Müştəri məlumatlarını redaktə et'

    customer = get_object_or_404(Customer, pk=pk)

    form = CustomerForm(request.POST or None, instance=customer)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Müştəri məlumatları redaktə edildi!')
        return redirect('customer:index')
    
    context['form'] = form
    
    return render(request, template_name, context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if customer.sales.exists():
        messages.error(request, 'Bu müştəri satış etdiyi üçün silinə bilməz!')
    else:
        messages.success(request, 'Müştəri silindi!')
        customer.delete()

    return redirect('customer:index')