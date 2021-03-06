"""students URL Configuration

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
from django.urls import path, include
from django.views.generic.base import RedirectView
from ui.views import index
from accounts.views import signup_view
import django.contrib.auth.urls as auth_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', signup_view, name="signup_view"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('records/', include('records.urls')),
    path('ui/', include('ui.urls')),
    path('classic/', include('classic.urls')),
    path('', RedirectView.as_view(url="/classic/calendar/thismonth/", permanent=False), name="index"),
]
