from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from .logic.forms import WorkerForm


@login_required
@user_passes_test(lambda u: u.is_superuser)
def index(request, template_name='worker/index.html', context={}):
    context['title'] = 'İşçilər'
    
    context['workers'] = User.objects.filter(is_superuser=False).all()
    
    return render(request, template_name, context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create(request, template_name='worker/create.html', context={}):
    context['title'] = 'İşçi əlavə et'

    form = WorkerForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save(commit=True)
        messages.success(request, 'İşçi əlavə edildi!')
        return redirect('worker:index')

    context['form'] = form
    
    return render(request, template_name, context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def update(request, pk, template_name='worker/create.html', context={}):
    context['title'] = 'İşçi məlumatlarını redaktə et'

    worker = get_object_or_404(User, pk=pk)

    form = WorkerForm(request.POST or None, instance=worker)

    if request.method == 'POST' and form.is_valid():
        form.save(commit=True)
        messages.success(request, 'İşçi məlumatları redaktə edildi!')
        return redirect('worker:index')

    context['form'] = form
    
    return render(request, template_name, context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    if len(user.sales.all()) > 0:
        messages.error(request, 'Bu işçinin satışı müvcud olduğu üçün silinə bilməz!')
    else:
        user.delete()
        messages.success(request, 'İşçi silindi!')
    
    return redirect('worker:index')