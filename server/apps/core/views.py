from django.shortcuts import render

def home(request, template_name='core/home.html', context={}):
    context['title'] = 'Ana Səhifə'

    return render(request, template_name, context)