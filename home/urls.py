from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from home.views import TimeView, OptionUpdateView, OptionListView, DefaultTextView

router = DefaultRouter()

urlpatterns = router.urls + [
    url(r'^time$', TimeView.as_view(), name='time'),

    url(r'^options/(?P<pk>[0-9]+)$', OptionUpdateView.as_view(), name=''),
    url(r'^options', OptionListView.as_view(), name=''),

    url(r'^defaultTexts/(?P<pk>[0-9]+)$', DefaultTextView.as_view(), name=''),
    url(r'^defaultTexts', DefaultTextView.as_view(), name=''),
]
