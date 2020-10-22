import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.core.serializers import get_serializer
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode

from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg import openapi
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view,permission_classes
from.serializers import *
from.renderers import *
from django.urls import reverse
from .utils import *


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer_class = SignUpSerializer
        renderer_classes = (UserRenderer,)
        user = request.data
        serializer = serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email_verification')
        absolute_url = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.first_name+' Use the link below to verify your email \n'+absolute_url
        data = {'email_subject': 'Verify your email', 'email_body': email_body, 'to_email': user.email}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description',
                                               type=openapi.TYPE_STRING)

@swagger_auto_schema(method='GET',manual_parameters=[token_param_config])
@api_view(['GET'])
def EmailVerification(request):
    token = request.GET.get('token')
    if request.method == "GET":
        renderer_classes = (UserRenderer,)
        serializer_class = EmailVerificationSerializer
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully Activated Your Account'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Link is Expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def LoginView(request):
    renderer_classes = (UserRenderer,)
    if request.method == 'POST':
        serializer_class = LoginSerializer
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def password_reset_view(request):
    renderer_classes = (UserRenderer,)
    if request.method=="POST":
        serializer_class = PasswordResetSerializer
        serializer = serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb4 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password_reset', kwargs={'uidb4': uidb4, 'token': token})
            absolute_url = 'http://' + current_site + relativeLink
            email_body = 'Hello, \n Use the link below to reset your password. \n' + absolute_url
            data = {'email_subject': 'Reset your Password', 'email_body': email_body, 'to_email': user.email}
            Util.send_email(data)

        return Response({'success': 'We have sent you the link to reset your password..!!'}, status=status.HTTP_200_OK)



@api_view(['GET'])
def password_reset_token_check(request, uidb4, token):
    renderer_classes = (UserRenderer,)
    if request.method == "GET":
        try:
            id = smart_str(urlsafe_base64_decode(uidb4))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, Please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials is Valid', 'uidb4': uidb4, 'token': token},
                            status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as error:
            return Response({'error': 'Token is not valid, Please request a new one'},
                            status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PATCH'])
def set_new_password(request):
    renderer_classes = (UserRenderer,)
    if request.method == "PATCH":
        serializer_class = SetNewPasswordSerializer
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password Reset Success..!!'}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def logout_view(request):
    renderer_classes = (UserRenderer,)
    if request.method == "POST":
        serializer = RefreshTokenSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'message': 'You Have Logged Out..!!'}, status=status.HTTP_204_NO_CONTENT)



