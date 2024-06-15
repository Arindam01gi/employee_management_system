from .models import User,UserDetails
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username','active']

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['user_id', 'firstname', 'lastname', 'email', 'phone', 'user_role', 'profile_pic', 'designation', 'salary', 'joining_date', 'created_on', 'updated_on']