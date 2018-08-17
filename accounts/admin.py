from django.contrib import admin

from .accounts.models import *

admin.site.register(Account)
admin.site.register(FloatAccount)
