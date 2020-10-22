from django.urls import path
from .views import *

urlpatterns =[
    path('signup', signup, name='signup'),
    path('email_verification', EmailVerification, name='email_verification'),
    path('login', LoginView, name='login'),
    path('password_reset_request', password_reset_view, name='password_reset_request'),
    path('password_reset_request/<uidb4>/<token>',password_reset_token_check, name='password_reset'),
    path('password_reset', set_new_password, name='password_reset_complete'),
    path('logout', logout_view, name='logout'),
]