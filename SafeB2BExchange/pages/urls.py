from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_page'),
    path('signin/', views.signin_page, name='signin_page'),
    path('signup/', views.signup_page, name='signup_page'),
    path('register/', views.register_page, name='register_page'),
    path('sendOTP/', views.send_otp_page, name='send_otp_page'),
    path('confirmOTP/', views.confirm_otp_page, name='confirm_otp_page'),
    path('verifyOTP/', views.verify_otp, name='verify_otp'),
    path('changePassword/', views.change_password_page, name='change_password_page'),
    path('manageMFA/', views.manage_mfa_page, name='manage_mfa_page'),
    path('uploadFile/', views.upload_file_page, name='upload_file_page'),
    path('documents/', views.documents_page, name='documents_page'),
    path('file/<int:doc_id>/', views.file_page, name='file_page'),
    path('report/<int:report_id>/', views.report_page, name='report_page'),
    path('reports/', views.reports_page, name='reports_page'),
    path('submitReport/', views.submit_report, name='submit_report'),
]
