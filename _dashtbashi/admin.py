from django.contrib import admin
from _dashtbashi.models import Car, Driver, Driving, Remittance, Lading, OtherDriverPayment

admin.site.register(Car)
admin.site.register(Driver)
admin.site.register(Driving)
admin.site.register(Remittance)
admin.site.register(Lading)
admin.site.register(OtherDriverPayment)
