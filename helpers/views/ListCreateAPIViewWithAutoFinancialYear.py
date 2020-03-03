from rest_framework import generics, status
from rest_framework.response import Response


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