from rest_framework import serializers

from sobhan_admin.models import Profile
from users.models import User


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class AdminUserSerializer(serializers.ModelSerializer):
    profile = AdminProfileSerializer(allow_null=True, required=False)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')

        user = super().create(validated_data)
        password = validated_data.get('password')
        user.set_password(password)
        user.save()

        Profile.objects.create(**profile_data, user=user)

        return user

    def update(self, instance: User, validated_data):
        profile_data = validated_data.pop('profile')
        res = super().update(instance, validated_data)
        instance.profile.update(**profile_data)
        return res
