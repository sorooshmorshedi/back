import django_filters
from django_filters import rest_framework as filters
from django_jalali.db import models as jmodels
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
        }


class NotificationFilter(filters.FilterSet):
    class Meta:
        model = Notification
        fields = {
            'title': ['exact', 'contains'],
            'explanation': ['exact', 'contains'],
            'created_at': ['exact', 'gte', 'lte'],
        }
        filter_overrides = {
            jmodels.jDateTimeField: {
                'filter_class': django_filters.CharFilter,
            },
        }
