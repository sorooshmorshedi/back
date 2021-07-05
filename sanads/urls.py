from django.conf.urls import url
from sanads.views import SanadCreateView, SanadDetailView, ReorderSanadsApiView, SanadByPositionView, ConfirmSanad, \
    DefineSanadView

urlpatterns = [

    url(r'^$', SanadCreateView.as_view(), name=''),
    url(r'^(?P<pk>[0-9]+)/$', SanadDetailView.as_view(), name=''),
    url(r'^byPosition$', SanadByPositionView.as_view(), name=''),
    url(r'^(?P<pk>[0-9]+)/confirm/$', ConfirmSanad.as_view(), name=''),
    url(r'^reorder$', ReorderSanadsApiView.as_view(), name=''),
    url(r'^define/$', DefineSanadView.as_view(), name=''),
]
