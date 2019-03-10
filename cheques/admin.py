from django.contrib import admin

from .models import *

admin.site.register(Cheque)
admin.site.register(Chequebook)
admin.site.register(StatusChange)

