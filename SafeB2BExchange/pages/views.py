from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts import models


@login_required(login_url='signin_page')
def index(request):
    return render(request, 'pages/index.html')

def signin_page(request):
    return render(request, 'pages/signin.html')

def signup_page(request):
    return render(request, 'pages/signup.html')

def register_page(request):
    # create temporary account
    created_user = {
        'id': 1,
        'username': 'akram',
        'role': 'a'
    }
    context = {
        'user': created_user
    }
    return render(request, 'pages/register.html', context=context)

def send_otp_page(request):
    return render(request, 'pages/sendOTP.html')

def confirm_otp_page(request):
    return render(request, 'pages/confirmOTP.html')


@login_required(login_url='signin_page')
def change_password_page(request):
    return render(request, 'pages/changePassword.html')

@login_required(login_url='signin_page')
def manage_mfa_page(request):
    return render(request, 'pages/manageMFA.html')

@login_required(login_url='signin_page')
def upload_file_page(request):
    return render(request, 'pages/uploadFile.html')

@login_required(login_url='signin_page')
def documents_page(request):
    user_profile = request.user.profile
    documents = []
    if hasattr(user_profile, 'agent_profile'):
        documents = models.SecureDocument.objects.filter(agent=user_profile.agent_profile)
    elif hasattr(user_profile, 'client_profile'):
        documents = models.SecureDocument.objects.filter(client=user_profile.client_profile)
    context = {
        'documents': documents
    }
    return render(request, 'pages/documents.html', context)

@login_required(login_url='signin_page')
def file_page(request):
    return render(request, 'pages/file.html')

@login_required(login_url='signin_page')
def report_page(request):
    return render(request, 'pages/report.html')

@login_required(login_url='signin_page')
def reports_page(request):
    return render(request, 'pages/reports.html')