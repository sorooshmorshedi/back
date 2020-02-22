from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.exceptions.ConfirmationError import ConfirmationError


class TestView(APIView):
    def get(self, request):
        return Response([])


class ListCreateAPIViewWithAutoFinancialYear(generics.ListCreateAPIView):

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.inFinancialYear(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.instance.financial_year.add(request.user.active_financial_year)
        self.created(serializer.instance, request)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def created(self, instance, request):
        pass


class RetrieveUpdateDestroyAPIViewWithAutoFinancialYear(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.inFinancialYear(self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.financial_year.remove(request.user.active_financial_year)
        if instance.financial_year.count() == 0:
            instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
