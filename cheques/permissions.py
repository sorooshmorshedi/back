from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from cheques.models.ChequeModel import Cheque


class SubmitChequePermission(BasePermission):
    def has_permission(self, request, view):
        is_paid = request.data.get('is_paid', False) == 'true'
        if is_paid:
            codename = "submit.paidCheque"
        else:
            codename = "submit.receivedCheque"
        return request.user.has_perm(codename)


class ChangeChequeStatusPermission(BasePermission):
    def has_permission(self, request, view):
        cheque = get_object_or_404(Cheque, pk=view.kwargs.get('pk'))
        user = request.user
        if cheque.is_paid:
            codename = "changeStatus.paidCheque"
        else:
            codename = "changeStatus.receivedCheque"
        return user.has_object_perm(cheque, codename)

