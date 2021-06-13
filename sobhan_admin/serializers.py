from django.contrib.auth import get_user_model
from rest_framework import serializers

from sobhan_admin.models import Profile
from users.models import User
from users.serializers import UserCreateSerializer


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('user',)


class AdminUserListRetrieveSerializer(serializers.ModelSerializer):
    profile = AdminProfileSerializer()

    class Meta:
        model = User
        fields = '__all__'


class AdminUserUpdateSerializer(UserCreateSerializer):
    class Meta:
        model = get_user_model()
        fields = ('max_users', 'max_companies', 'modules')
