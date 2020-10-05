from rest_framework import serializers

from sobhan_admin.models import Profile
from users.models import User


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('user',)


class AdminUserListRetrieveSerializer(serializers.ModelSerializer):
    profile = AdminProfileSerializer()

    class Meta:
        model = User
        fields = '__all__'
