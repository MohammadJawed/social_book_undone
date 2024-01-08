from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import UploadedFile, CustomUser

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = '__all__'

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'        