from rest_framework.permissions import BasePermission


class AccountListCreate(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.has_perm('accounts.get_account')
        if request.method == 'POST':
            return request.user.has_perm('accounts.add_account')


class AccountDetail(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('PUT', 'PATCH'):
            return request.user.has_perm('accounts.change_account')
        if request.method == 'DELETE':
            return request.user.has_perm('accounts.delete_account')
        if request.method == 'GET':
            return request.user.has_perm('accounts.get_account')


