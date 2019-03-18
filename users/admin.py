from django.contrib import admin
from django.contrib.auth.models import Permission

from users.models import User, Access

admin.site.register(User)
admin.site.register(Permission)
admin.site.register(Access)

