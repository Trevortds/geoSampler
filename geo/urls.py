"""geo URL Configuration

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
from django.contrib import admin
from django.urls import path, include, reverse
from .views import home_page
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import login_page, register_page, password_change_page
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect

import samples

urlpatterns = [
    # path('', home_page, name="home"),
    path('', lambda r: HttpResponseRedirect(reverse("samples:index")), name="home"),
    path('admin/', admin.site.urls),
    path('login/', login_page, name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('samples/', include(('samples.urls', "samples")), name="samples"),
    path('jobs/', include(('jobs.urls', "jobs")), name="jobs"),
    path('register/', register_page, name="register"),
    path('change_password/', password_change_page, name="password_change"),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)