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
# from filebrowser.sites import site
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/filebrowser/', site.urls),
    path('sna_admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='main_login'),
    path('register/', RegistrationView, name='register'),
    path("password-reset", auth_views.PasswordResetView.as_view( template_name="password_reset.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view( template_name="password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view( template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view( template_name="password_reset_complete.html"), name="password_reset_complete"),
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
    path('testimonial/', testimonial, name='testimonial'),
    path('resources/', resources, name='resources'),
    path('errata/', errata, name='errata'),
    path('subscribe/', subscribe, name='subscribe'),
    path('check_answer/', check_answers, name='check_answer'),
    path('add_token/', upload_tokens, name="uploaded_tokens"),
    path('classes/', classes, name='classes'),
    path('classes/sna_winter_22', sna_winter_22, name='sna_winter_22'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
