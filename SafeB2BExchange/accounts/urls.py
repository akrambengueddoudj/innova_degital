from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name='account_signin'),
    path('signup/', views.signup, name='account_signup'),
    path('account_logout/', views.account_logout, name='account_logout'),
    path('register_agent/', views.register_agent, name='register_agent'),
    path('register_client/', views.register_client, name='register_client'),
    path('upload_file/', views.upload_secure_document, name='upload_secure_document'),
    path('download_file/<int:doc_id>/', views.download_secure_document, name='download_secure_document'),
    path('receiver_sign_file/<int:doc_id>/', views.receiver_sign_document, name='receiver_sign_document'),


    # REST API
    path('api/documents/', views.DocumentAuditLogListCreate.as_view(), name='document-audit-list-create'),
    path('api/documents/<int:pk>/', views.DocumentAuditLogDetail.as_view(), name='document-audit-detail'),
]