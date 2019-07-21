from django.conf.urls import url, include

from users.views import UserView, SetActiveCompany, SetActiveFinancialYear

urlpatterns = [
    url(r'^getUser/$', UserView.as_view(), name='retrieve-user'),
    url(r'^setActiveCompany$', SetActiveCompany.as_view(), name='set-active-company'),
    url(r'^setActiveFinancialYear$', SetActiveFinancialYear.as_view(), name='set-active-financial-year'),
]
