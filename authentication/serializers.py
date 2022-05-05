
from django.db.models import fields
from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'firstName', 'lastName', 'phoneNumber', 'role','password')



    def validate_date(self,data):
        phone = data['phoneNumber'] 
        true = RegexValidator(regex=r'^\+?1?\d{10,15}$')
        if not true:
            raise serializers.ValidationError({'status':"error", 'message':"Please enter your phonenumber in the format starting with: 09"})   
        return data 


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'firstName', 'lastName', 'phoneNumber', 'role','password')




class Loginserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','phoneNumber', 'role', 'token')
        read_only_fields = ['token']


