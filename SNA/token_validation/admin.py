from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Tokens
from .forms import UserCreationForm, UserChangeForm

# Register your models here.
class AccountAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model =  Account

    list_display = ('first_name', 'last_name', 'email', 'is_active', 'is_admin')
    list_filter = ('is_admin', 'is_active',)

    fieldsets = (
        (None, {'fields': ('email', 'token',  'password', 'is_active', 'is_admin')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        # ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),'fields': ('email', 'token',  'password1', 'password2', 'is_active', 'is_admin')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        # ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('first_name',)

class TokenAdmin(admin.ModelAdmin):
    list_display    = ['id', 'token', 'active']

admin.site.register(Tokens, TokenAdmin)
admin.site.register(Account, AccountAdmin)