from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import *

# Register your models here.

admin.site.site_header = "Administrator Panel"
admin.site.site_title = "Inventory"
admin.site.index_title = "Dashboard"

class ItemConfigAdmin(admin.ModelAdmin):
    list_display = ("item","name","category","quantity","room")
    list_filter = ["category","room"]

    readonly_fields = ('item',)
    
class LendingConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False 
    
    list_display = ("client","item","category","room","lending_quantity","date_lending","return_time","status")
    list_filter = ["status"]

    readonly_fields = ["description"]

class CustomUserAdmin(UserAdmin):
    model = Account
    list_display = ['username','is_staff', 'is_active', 'date_joined']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phonenumber')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'phonenumber', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('email', 'username', 'firstname', 'lastname', 'phonenumber')
    ordering = ('email',)

admin.site.unregister(Group)
admin.site.register(Account, CustomUserAdmin)
admin.site.register(Barang, ItemConfigAdmin)
admin.site.register(Peminjaman, LendingConfigAdmin)