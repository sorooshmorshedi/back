from rest_framework.permissions import BasePermission


class CompanyListCreate(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.has_perm('companies.get_company')
        if request.method == 'POST':
            return request.user.has_perm('companies.add_company')


class CompanyDetail(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('PUT', 'PATCH'):
            return request.user.has_perm('companies.change_company')
        if request.method == 'DELETE':
            return request.user.has_perm('companies.delete_company')
        if request.method == 'GET':
            return request.user.has_perm('companies.get_company')

