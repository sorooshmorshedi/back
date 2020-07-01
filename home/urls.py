from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from home.views import TimeView, OptionUpdateView, OptionListView

router = DefaultRouter()

urlpatterns = router.urls + [
    url(r'^time$', TimeView.as_view(), name='time'),

    url(r'^options/(?P<pk>[0-9]+)$', OptionUpdateView.as_view(), name=''),
    url(r'^options', OptionListView.as_view(), name=''),
]
