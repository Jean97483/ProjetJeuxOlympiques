from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser





class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Keys', {'fields': ('unique_key', 'purchase_key', 'final_key', 'qr_code')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'unique_key', 'purchase_key','final_key'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'unique_key', 'purchase_key', 'final_key')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'unique_key', 'purchase_key', 'final_key')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)