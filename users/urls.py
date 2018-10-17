from django.conf.urls import url, include

from users.views import UserView

urlpatterns = [

    url(r'^getUser/$', UserView.as_view(), name=''),
    # url(r'^transactions/(?P<pk>[0-9]+)$', TransactionDetail.as_view(), name=''),
]
