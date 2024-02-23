from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

from .models import Product

admin.site.unregister(User)
admin.site.unregister(Group)


class ReadOnlyAdminMixin:
    def has_add_permission(self, request):
        is_superuser = request.user.is_superuser
        if is_superuser:
            return True
        return False
    def has_change_permission (self, request, obj=None):
        is_superuser = request.user.is_superuser
        if is_superuser:
            return True
        
        elif request.user.has_perm("inventory.change_product"):
            return True
        
        return False
    def has_delete_permission (self, request, obj=None):
        is_superuser = request.user.is_superuser
        if is_superuser:
            return True
        return False
    def has_view_permission (self, request, obj=None):
        is_superuser = request.user.is_superuser
        if is_superuser:
            return True
        return True


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['username'].disabled = True
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['user_permissions'].disabled = True
            form.base_fields['groups'].disabled = True
        return form

@admin.register(Product)
class ProductAdmin(ReadOnlyAdminMixin ,admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "web_id",
        'slug',
        "is_active",
        "created_at"
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['name'].disabled = True
        
        return form

    