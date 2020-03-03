from rest_framework import generics, status
from rest_framework.response import Response


class RetrieveUpdateDestroyAPIViewWithAutoFinancialYear(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.inFinancialYear(self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.financial_year.remove(request.user.active_financial_year)
        if instance.financial_year.count() == 0:
            instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)