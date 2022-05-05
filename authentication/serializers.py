
from django.db.models import fields
from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'firstName', 'lastName', 'phoneNumber', 'role','password')