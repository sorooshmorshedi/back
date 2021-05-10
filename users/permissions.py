from django.db.models.aggregates import Sum, Count
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from companies.models import CompanyUser
from users.models import User


class ChangePasswordPermission(BasePermission):
    def has_permission(self, request, view):
        current_user = request.user
        target_user = get_object_or_404(User, pk=request.data.get('user'))
        return current_user.is_staff or current_user == target_user or current_user.has_perm('changePassword.user')


class DeleteUserPermission(BasePermission):
    message = "کاربر ادمین غیر قابل حذف می باشد"

    def has_permission(self, request, view):
        user = get_object_or_404(User, pk=view.kwargs.get('pk'))
        return not (user.is_staff or user.is_superuser)


class UserLimit(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            company = request.user.active_company
            user = company.created_by

            users_count = CompanyUser.objects.filter(company__created_by=user).count()

            return users_count + 1 < user.max_users
        return True
