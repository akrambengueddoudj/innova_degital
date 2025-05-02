from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_page'),
    path('signin/', views.signin_page, name='signin_page'),
    path('signup/', views.signup_page, name='signup_page'),
    path('register/', views.register_page, name='register_page'),
    path('sendOTP/', views.send_otp_page, name='send_otp_page'),
    path('confirmOTP/', views.confirm_otp_page, name='confirm_otp_page'),
    path('changePassword/', views.change_password_page, name='change_password_page'),
    path('manageMFA/', views.manage_mfa_page, name='manage_mfa_page'),
    path('uploadFile/', views.upload_file_page, name='upload_file_page'),
    path('documents/', views.documents_page, name='documents_page'),
    path('file/', views.file_page, name='file_page'),
    path('report/', views.report_page, name='report_page'),
    path('reports/', views.reports_page, name='reports_page'),
]
