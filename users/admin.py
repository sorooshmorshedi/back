from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from users.models import User, Role, PhoneVerification

UserAdmin.fieldsets += (('ماژول ها', {'fields': ('modules',)}),)
UserAdmin.fieldsets += (('active financial company', {'fields': ('active_company',)}),)

admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(PhoneVerification)
