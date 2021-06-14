from django.contrib import admin

from distributions.models import Visitor, CommissionRange, Path
from distributions.models.car_model import Car
from distributions.models.distribution_model import Distribution
from distributions.models.distributor_model import Distributor
from distributions.models.driver_model import Driver

admin.site.register(Visitor)
admin.site.register(Car)
admin.site.register(CommissionRange)
admin.site.register(Distribution)
admin.site.register(Distributor)
admin.site.register(Driver)
admin.site.register(Path)
