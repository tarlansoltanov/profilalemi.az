from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def login_page(request, template_name='authentication/login.html', context={}):
    context['title'] = 'Giriş'

    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if remember:
                request.session.set_expiry(1209600)

            return redirect('core:home')
        else:
            messages.error(request, 'İstifadəçi adı və ya şifrə yanlışdır!')
    return render(request, template_name, context)

def logout_page(request):
    logout(request)
    return redirect('core:home')