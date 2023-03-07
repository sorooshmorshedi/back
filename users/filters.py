import django_filters
from django_filters import rest_framework as filters
from django_jalali.db import models as jmodels

from helpers.filters import BASE_FIELD_FILTERS
from users.models import UserNotification, Notification


class UserNotificationFilter(filters.FilterSet):
    class Meta:
        model = UserNotification
        fields = {
            'notification__title': ['exact', 'contains'],
            'notification__explanation': ['exact', 'contains'],
            'notification__created_at': ['exact', 'gte', 'lte'],
        }
        filter_overrides = {
            jmodels.jDateTimeField: {
                'filter_class': django_filters.CharFilter,
            },
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }


class NotificationFilter(filters.FilterSet):
    class Meta:
        model = Notification
        fields = {
            'title': BASE_FIELD_FILTERS,
            'explanation': BASE_FIELD_FILTERS,
            'created_at': BASE_FIELD_FILTERS,
            'send_date': BASE_FIELD_FILTERS,
        }
        filter_overrides = {
            jmodels.jDateTimeField: {
                'filter_class': django_filters.CharFilter,
            },
            jmodels.jDateField: {
                'filter_class': django_filters.CharFilter,
            },
        }

