from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer


class UserView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
