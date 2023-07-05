from django.db.models import Sum, F
from django.shortcuts import render, redirect
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required

from ..sale.models import Sale
from ..storage.models import Storage


@login_required
def home(request, template_name='core/home.html', context={}):
    context['title'] = 'Ana Səhifə'

    sales = Sale.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(income=Sum(F('quantity')*F('sell_price'))).order_by('-month')

    storage = Storage.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(outcome=Sum(F('quantity')*F('buy_price'))).order_by('-month')

    context['report'] = {dict(s)['month']: { 'outcome' : dict(s)['outcome'], 'income': 0 } for s in storage}

    for sale in sales:
        if dict(sale)['month'] in context['report']:
            context['report'][dict(sale)['month']]['income'] = dict(sale)['income']
        else:
            context['report'][dict(sale)['month']] = { 'outcome' : 0, 'income': dict(sale)['income'] }

    context['report'] = [ { 'month': k, 'income': v['income'], 'outcome': v['outcome'], 'total' : v['income'] - v['outcome'] } for k, v in context['report'].items() ]
        
    return render(request, template_name, context) if request.user.is_superuser else redirect('sale:index')


def handler400(request, exception=None, template_name='core/error-400.html'):
    return render(request, template_name, status=400)

def handler403(request, exception=None, template_name='core/error-403.html'):
    return render(request, template_name, status=403)

def handler404(request, exception=None, template_name='core/error-404.html'):
    return render(request, template_name, status=404)

def handler500(request, exception=None, template_name='core/error-500.html'):
    return render(request, template_name, status=500)

def handler503(request, exception=None, template_name='core/error-503.html'):
    return render(request, template_name, status=503)