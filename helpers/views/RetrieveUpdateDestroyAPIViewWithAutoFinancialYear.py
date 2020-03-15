from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class RetrieveUpdateDestroyAPIViewWithAutoFinancialYear(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.get_serializer_class().Meta.model.objects.all()
