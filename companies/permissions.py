from rest_framework.permissions import BasePermission


class CompanyLimit(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            user = request.user.get_superuser()
            return user.companies.count() < user.max_companies
        return True

