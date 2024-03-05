from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . models import CustomUser
from . custom_auth import CustomAuth
from django.contrib.auth import get_user_model
User = get_user_model()


# class UserRegisterSerializer(serializers.ModelSerializer):
#     confirm_password = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = CustomUser
#         fields = ['first_name', 'last_name', 'login', 'password', 'confirm_password']
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def validate(self, data):
#         if data['password'] != data.pop('confirm_password'):
#             raise serializers.ValidationError('Passwords do not match')
#         return data
#
#     def create(self, validated_data):
#         return User.objects.create(**validated_data)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name', 'photo', 'password']


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    username_field = 'login'
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')
        if login and password:
            user = self.authenticate_user(login, password)
            if user:
                refresh = self.get_token(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
                return data
            else:
                raise serializers.ValidationError('user not found')
        else:
            raise serializers.ValidationError('must include login and password')


    def authenticate_user(self, login, password):
        user = CustomAuth().authenticate(request=None, login=login, password=password)
        return user

