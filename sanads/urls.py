from django.conf.urls import url
from sanads.views import SanadListCreate, SanadDetail, ReorderSanadsApiView, SanadByPositionView, ConfirmSanad

urlpatterns = [

    url(r'^$', SanadListCreate.as_view(), name=''),
    url(r'^(?P<pk>[0-9]+)/$', SanadDetail.as_view(), name=''),
    url(r'^byPosition$', SanadByPositionView.as_view(), name=''),
    url(r'^(?P<pk>[0-9]+)/confirm/$', ConfirmSanad.as_view(), name=''),
    url(r'^reorder$', ReorderSanadsApiView.as_view(), name=''),
]
