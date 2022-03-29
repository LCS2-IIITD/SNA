from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http.response import HttpResponse
from .models import Account, Tokens, Subscription
from .forms import UserCreationForm, UserChangeForm
import csv 

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

# Register your models here.
class AccountAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model =  Account

    list_display = ('first_name', 'last_name', 'email', 'is_active', 'is_admin', 'token')
    list_filter = ('is_admin', 'is_active',)

    fieldsets = (
        (None, {'fields': ('email', 'token',  'password', 'is_active', 'is_admin')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),'fields': ('email', 'token',  'password1', 'password2', 'is_active', 'is_admin')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('first_name', 'last_name', 'email', 'token__token',)
    ordering = ('first_name',)
    filter_horizontal = ('groups', 'user_permissions',)
    # list_filter = ()
    # fieldsets = ()

class TokenAdmin(admin.ModelAdmin):
    list_display    = ['id', 'token', 'active']
    list_filter = ('active',)
    search_fields = ('token',)

class SubscriptionAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display    = ['email']
    search_fields = ('email',)
    actions = ["export_as_csv"]

admin.site.register(Tokens, TokenAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Subscription, SubscriptionAdmin)