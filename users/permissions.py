from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from users.models import User


class ChangePasswordPermission(BasePermission):
    def has_permission(self, request, view):
        current_user = request.user
        target_user = get_object_or_404(User, pk=request.data.get('user'))
        return current_user.is_staff or current_user == target_user


class DeleteUserPermission(BasePermission):
    def has_permission(self, request, view):
        user = get_object_or_404(User, pk=view.kwargs.get('pk'))
        return not (user.is_staff or user.is_superuser)
