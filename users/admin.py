from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from users.models import User, Role, PhoneVerification

UserAdmin.fieldsets += (('ماژول ها', {'fields': ('modules',)}),)
UserAdmin.fieldsets += (('active financial company', {'fields': ('active_company',)}),)
UserAdmin.fieldsets += (('محدودیت ها', {'fields': ('max_companies', 'max_users',)}),)
UserAdmin.fieldsets += (('Secrets', {'fields': ('secret_key',)}),)


class PermissionAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name', 'codename')


admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(PhoneVerification)
