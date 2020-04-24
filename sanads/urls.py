from django.conf.urls import url
from sanads.views import SanadListCreate, SanadDetail, newCodeForSanad, ReorderSanadsApiView, GetSanadByCodeView

urlpatterns = [

    url(r'^$', SanadListCreate.as_view(), name=''),
    url(r'^(?P<pk>[0-9]+)$', SanadDetail.as_view(), name=''),
    url(r'^newCode$', newCodeForSanad, name=''),
    url(r'^getSanadByCode$', GetSanadByCodeView.as_view(), name=''),
    url(r'^reorder$', ReorderSanadsApiView.as_view(), name=''),
]
