"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from server.apps.core import urls as core_urls
from server.apps.worker import urls as worker_urls
from server.apps.product import urls as product_urls
from server.apps.storage import urls as storage_urls
from server.apps.customer import urls as customer_urls
from server.apps.authentication import urls as auth_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(core_urls, namespace='core')),
    path('auth/', include(auth_urls, namespace='auth')),
    path('worker/', include(worker_urls, namespace='worker')),
    path('product/', include(product_urls, namespace='product')),
    path('storage/', include(storage_urls, namespace='storage')),
    path('customer/', include(customer_urls, namespace='customer')),
]

handler400 = 'server.apps.core.views.handler400'
handler403 = 'server.apps.core.views.handler403'
handler404 = 'server.apps.core.views.handler404'
handler500 = 'server.apps.core.views.handler500'
handler503 = 'server.apps.core.views.handler503'

# Health check
urlpatterns += [
    path("health/", include("health_check.urls")),
]

# Django Debug Toolbar
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
