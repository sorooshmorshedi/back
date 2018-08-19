from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class ExpenseModelView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, RPTypeListCreate,)
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def list(self, request, *ergs, **kwargs):
        queryset = Expense.objects.all()
        serialized = ExpenseListRetrieveSerializer(queryset, many=True)
        return Response(serialized.data)

    def retrieve(self, request, pk=None):
        queryset = Expense.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serialized = ExpenseListRetrieveSerializer(instance)
        return Response(serialized.data)


class FactorModelView(viewsets.ModelViewSet):
    queryset = Factor.objects.all()
    serializer_class = FactorSerializer

    def list(self, request, *ergs, **kwargs):
        queryset = Factor.objects.all()
        serialized = FactorListRetrieveSerializer(queryset, many=True)
        return Response(serialized.data)

    def retrieve(self, request, pk=None):
        queryset = Factor.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serialized = FactorListRetrieveSerializer(instance)
        return Response(serialized.data)


class FactorItemMass(APIView):
    serializer_class = FactorItemSerializer

    def post(self, request):
        serialized = self.serializer_class(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        for item in request.data:
            instance = FactorItem.objects.get(id=item['id'])
            serialized = FactorItemSerializer(instance, data=item)
            if serialized.is_valid():
                serialized.save()
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, request):
        for itemId in request.data:
            instance = FactorItem.objects.get(id=itemId)
            instance.delete()
        return Response([], status=status.HTTP_200_OK)

