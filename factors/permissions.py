from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from factors.models import Factor


class DefiniteFactorPermission(BasePermission):
    message = 'شما اجازه قطعی کردن این نوع فاکتور را ندارید'

    def has_permission(self, request, view):
        factor = get_object_or_404(Factor, pk=view.kwargs.get('pk'))
        factor_type = factor.type

        base_codename = ''
        if factor_type == Factor.BUY:
            base_codename = 'buy'
        elif factor_type == Factor.SALE:
            base_codename = 'sale'
        elif factor_type == Factor.BACK_FROM_BUY:
            base_codename = 'backFromBuy'
        elif factor_type == Factor.BACK_FROM_SALE:
            base_codename = 'backFromSale'

        return request.user.has_perm("definite.{}Factor".format(base_codename))
