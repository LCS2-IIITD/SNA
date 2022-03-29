"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth.views import LoginView
from token_validation.views import *
from examination.views import *
from django.contrib.auth import views as auth_views
from filebrowser.sites import site
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='main_login'),
    path('register/', RegistrationView, name='register'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('accounts/reset_password/', reset_password, name='reset_password'),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('examination/given/', givenTests, name='given'),
    path('examination/pending/', pendingTests, name='pending'),
    path('givetest/', getTest, name='givetest'),
    path('confirmtest/', confirm_test, name='confirm'),
    path('submit_test/', submit_test, name='submit_test'),
    path('tinymce/', include('tinymce.urls')),
    path('activate/<uidb64>/<token>/',activate, name='activate'),
    path('', index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
