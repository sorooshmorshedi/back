from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from cheques.models.ChequeModel import Cheque


class SubmitChequePermission(BasePermission):
    def has_permission(self, request, view):
        received_or_paid = request.data.get('received_or_paid')
        if received_or_paid == Cheque.RECEIVED:
            codename = "submit.receivedCheque"
        else:
            codename = "submit.paidCheque"
        return request.user.has_perm(codename)


class ChangeChequeStatusPermission(BasePermission):
    def has_permission(self, request, view):
        cheque = get_object_or_404(Cheque, pk=view.kwargs.get('pk'))
        user = request.user
        if cheque.received_or_paid == Cheque.RECEIVED:
            codename = "changeStatus.receivedCheque"
        else:
            codename = "changeStatus.paidCheque"
        return user.has_object_perm(cheque, codename)

