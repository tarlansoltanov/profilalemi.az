from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request, template_name='core/home.html', context={}):
    context['title'] = 'Ana Səhifə'

    return render(request, template_name, context)


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