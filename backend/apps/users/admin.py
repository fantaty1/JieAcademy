from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'nickname', 'email', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login']
    list_editable = ['is_staff', 'is_superuser', 'is_active']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'nickname']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('扩展信息', {'fields': ('nickname', 'avatar', 'is_admin')}),
    )
