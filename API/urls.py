"""API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from .journal import views

import rest_framework.authtoken.views as authtoken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/<meal>/<location>/<year>/<month>/<day>/', views.get_menu),
    path('fetch_menus/', views.fetch_menus),
    path('user/', views.create_user),
    path('api-token-auth/', authtoken.obtain_auth_token),
    path('get_journal/', views.get_journal),
    path('add_dishes_to_journal/', views.add_dishes_to_journal),
]
