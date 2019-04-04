from django.conf.urls import url, include

from users.views import UserView, setActiveCompany, setActiveFinancialYear

urlpatterns = [
    url(r'^getUser/$', UserView.as_view(), name=''),
    url(r'^setActiveCompany$', setActiveCompany, name=''),
    url(r'^setActiveFinancialYear$', setActiveFinancialYear, name=''),
]
