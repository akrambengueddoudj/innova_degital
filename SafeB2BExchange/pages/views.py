from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts import models
from accounts.utils.encryption_utils import decrypt_bytes
from accounts.utils.audit import log_document_action, get_user_stats
from accounts.models import EmailOTP, UserProfile
from accounts.utils.otp import generate_otp
from django.contrib.auth import logout


@login_required(login_url='signin_page')
def index(request):
    if hasattr(request.user, 'profile'):
        user_profile = request.user.profile
        if hasattr(user_profile, 'agent_profile'):
            documents = models.SecureDocument.objects.filter(agent=user_profile.agent_profile, receiver_signature__isnull=True)
            audits = models.DocumentAuditLog.objects.filter(user=request.user)
            stats = get_user_stats(request.user)
            context = {
                'documents': documents,
                'audits': audits,
                'stats': stats,
            }
            return render(request, 'pages/index.html', context)
        return redirect(documents_page)
    else:
        logout(request)
        return redirect('index_page')

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
    generate_otp(request.user)
    return render(request, 'pages/confirmOTP.html')

@login_required
def verify_otp(request):
    if request.method == 'POST':
        code = request.POST.get('otp')
        otp_obj = EmailOTP.objects.filter(user=request.user, code=code, is_verified=False).last()

        if otp_obj and not otp_obj.is_expired():
            otp_obj.is_verified = True
            otp_obj.save()
            return redirect('index_page')
    return redirect('send_otp_page')


@login_required(login_url='signin_page')
def change_password_page(request):
    return render(request, 'pages/changePassword.html')

@login_required(login_url='signin_page')
def manage_mfa_page(request):
    return render(request, 'pages/manageMFA.html')

@login_required(login_url='signin_page')
def upload_file_page(request):
    user_profile = request.user.profile
    if hasattr(user_profile, 'client_profile'):
        return render(request, 'pages/uploadFile.html')
    return redirect('index_page')

@login_required(login_url='signin_page')
def documents_page(request):
    user_profile = request.user.profile
    documents = []
    if hasattr(user_profile, 'client_profile'):
        documents = models.SecureDocument.objects.filter(client=user_profile.client_profile)
        audits = models.DocumentAuditLog.objects.filter(user=request.user)
        context = {
            'documents': documents,
            'audits': audits
        }
        return render(request, 'pages/documents.html', context)
    return redirect('index_page')

@login_required(login_url='signin_page')
def file_page(request, doc_id):
    context = {}
    if models.SecureDocument.objects.filter(id=doc_id).exists:
        file = models.SecureDocument.objects.get(id=doc_id)
        context = {
            'document': file
        }
        
        log_document_action(request.user, file, 'view', '')
        return render(request, 'pages/file.html', context)
    return redirect('index_page')

@login_required(login_url='signin_page')
def report_page(request, report_id):
    context = {}
    if models.Report.objects.filter(id=report_id).exists():
        report = models.Report.objects.get(id=report_id)
        context = {
            'report': report
        }
    return render(request, 'pages/report.html', context)

@login_required(login_url='signin_page')
def reports_page(request):
    reports = models.Report.objects.filter(user=request.user)
    context = {
        'reports': reports
    }
    return render(request, 'pages/reports.html', context)

def submit_report(request):
    if request.method == "POST":
        issue_type = request.POST.get("issue_type")
        description = request.POST.get("description")

        if not issue_type or not description:
            return redirect('index_page')

        report = models.Report.objects.create(
            user=request.user,
            issue_type=issue_type,
            description=description
        )
        report.save()
    return redirect('index_page')