"""firegoreDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

import asteroid
from asteroid.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include('asteroid.urls')),
    path('', index, name='index'),
    url(r'^((?!(api|admin)).)*$', RedirectView.as_view(url='/', permanent=False), name='index_')
]
#
handler403 = 'asteroid.views.error_400s'
handler400 = 'asteroid.views.error_400s'
handler404 = 'asteroid.views.error_400s'
handler500 = 'asteroid.views.error_400s'