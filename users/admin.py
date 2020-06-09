from django.contrib import admin
from django.contrib.auth.models import Permission

from users.models import User, Role, PhoneVerification

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(PhoneVerification)
