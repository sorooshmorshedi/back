from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.filters import UserNotificationFilter
from users.models import UserNotification
from users.serializers import UserNotificationSerializer


class UserNotificationListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserNotificationSerializer
    filterset_class = UserNotificationFilter
    ordering_fields = '__all__'
    pagination_class = LimitOffsetPagination

    def get_queryset(self) -> QuerySet:
        return UserNotification.objects.filter(user=self.request.user).order_by('-status', 'id')


class ChangeUserNotificationStatusView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        user = request.user

        user_notification = get_object_or_404(UserNotification, user=user, pk=data.get('id'))
        user_notification.status = data.get('new_status')
        user_notification.save()

        return Response([])
