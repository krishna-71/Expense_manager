from django.contrib import auth
from django.utils.encoding import force_str
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.exceptions import TokenError

from .models import *


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, Please try again..!!')

        if not user.is_active:
            raise AuthenticationFailed('Account Disabled, Please contact Admin..!!')

        if not user.is_verified:
            raise AuthenticationFailed('Account is not verified, Please click the link sent to '
                                       'your email to activate the account..!!')

        return {
            'email': user.email,
            'password': user.password,
            'tokens': user.tokens()
        }
        return super().validate(attrs)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=560)

    class Meta:
        model = User
        fields = ['token']


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:

        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=58, min_length=6, write_only=True)
    token = serializers.CharField(max_length=255,  write_only=True)
    uidb4 = serializers.CharField(max_length=58, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb4']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb4 = attrs.get('uidb4')
            id = force_str(urlsafe_base64_decode(uidb4))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password)
            user.save()
            return(user)
        except Exception as error:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
