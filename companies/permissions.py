from rest_framework.permissions import BasePermission

from companies.models import Company


class CompanyLimit(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            company = request.user.active_company
            user = company.created_by
            return Company.objects.filter(created_by=user).count() < user.max_companies
        return True
