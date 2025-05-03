from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, UserProfile, Client, Agent, SecureDocument, Report
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from decouple import config
from accounts.models import Client, Agent, EmailOTP
from .utils.encryption_utils import encrypt_bytes, decrypt_bytes
from .utils.crypto_utils import sign_data, verify_signature
from .utils.audit import log_document_action

from rest_framework import generics
from .models import DocumentAuditLog
from .serializers import DocumentAuditLogSerializer

from accounts.models import EmailOTP
from accounts.utils.otp import generate_otp


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
    return redirect('index_page')

def twoFA(request):
    generate_otp(request.user)
    return render(request, 'pages/confirmOTP.html', {'twoFA': 'twoFA'})


def twoFA_otp(request):
    if request.method == 'POST':
        code = request.POST.get('otp')
        otp_obj = EmailOTP.objects.filter(user=request.user, code=code, is_verified=False).last()

        if otp_obj and not otp_obj.is_expired():
            otp_obj.is_verified = True
            otp_obj.save()
            return redirect('index_page')
    return redirect('send_otp_page')

def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if password != confirm_password:
            return render(request, 'register_step1.html')

        # Create user
        user = CustomUser.objects.create_user(email=email, password=password)
        user.save()
        user_profile = UserProfile.objects.create(
            user=user,
            full_name=full_name,
            phone_number=phone,
            role=role
        )
        user_profile.save()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Log in the user after signup

        return render(request, 'pages/register.html', {'role': role})
    return redirect('index_page')

def register_agent(request):
    if request.method == 'POST':
        bank_name = request.POST.get('bank_name')
        employee_id = request.POST.get('employee_id')
        job_title = request.POST.get('job_title')
        business_email = request.POST.get('work_email')

        agent = Agent.objects.create(
            user_profile=request.user.profile,
            bank_name=bank_name,
            employee_id=employee_id,
            job_title=job_title,
            business_email=business_email
        )
        agent.save()

    return render(request, 'pages/sendOTP.html')

def register_client(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        registration_number = request.POST.get('company_id')
        company_type = request.POST.get('company_type')
        industry_sector = request.POST.get('industry')
        address = request.POST.get('address')

        client = Client.objects.create(
            user_profile=request.user.profile,
            company_name=company_name,
            registration_number=registration_number,
            company_type=company_type,
            industry_sector=industry_sector,
            address=address
        )
        client.save()

    return render(request, 'pages/sendOTP.html')
    

def account_logout(request):
    logout(request)
    return redirect('index_page')


@login_required
def upload_secure_document(request):
    if request.method == 'POST':
        user_profile = request.user.profile
        doc_file = request.FILES.get('pdf')
        doc_name = request.POST.get('document_name')
        doc_type = request.POST.get('document_type')
        description = request.POST.get('description', '')

        if not doc_file or not doc_name or not doc_type:
            return HttpResponse("Missing required fields", status=400)

        if hasattr(user_profile, 'agent_profile'):
            client_id = request.POST.get('reciever_id')
            if not client_id:
                return HttpResponse("Client must be selected.", status=400)
            client = get_object_or_404(Client, id=client_id)
            agent = user_profile.agent_profile
            private_key_path = config('AGENT_PRIVATE_KEY_PATH')

        elif hasattr(user_profile, 'client_profile'):
            agent_id = request.POST.get('reciever_id')
            if not agent_id:
                return HttpResponse("Agent must be selected.", status=400)
            agent = get_object_or_404(Agent, id=agent_id)
            client = user_profile.client_profile
            private_key_path = config('CLIENT_PRIVATE_KEY_PATH')

        else:
            return HttpResponse("Invalid user role", status=403)

        file_data = doc_file.read()

        # Step 1: Sign file
        signature = sign_data(file_data, private_key_path)

        # Step 2: Encrypt file
        encrypted = encrypt_bytes(file_data)

        # Step 3: Save
        doc = SecureDocument.objects.create(
            document_name=doc_name,
            document_type=doc_type,
            description=description,
            encrypted_file=encrypted,
            uploader_signature=signature,
            client=client,
            agent=agent
        )
        doc.save()

        log_document_action(request.user, doc, 'upload', 'Successful upload')
    return redirect('index_page')

@login_required
def download_secure_document(request, doc_id):
    doc = SecureDocument.objects.get(id=doc_id)

    decrypted = decrypt_bytes(doc.encrypted_file)
    log_document_action(request.user, doc, 'download', 'Successful download')

    response = HttpResponse(decrypted, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="{doc.document_name}.pdf"'
    return response

@login_required
def receiver_sign_document(request, doc_id):
    doc = get_object_or_404(SecureDocument, id=doc_id)

    user_profile = request.user.profile

    # Check that user is the correct receiver
    is_agent_receiver = hasattr(user_profile, 'agent_profile') and doc.agent and doc.agent.user_profile == user_profile
    is_client_receiver = hasattr(user_profile, 'client_profile') and doc.client and doc.client.user_profile == user_profile

    if not (is_agent_receiver or is_client_receiver):
        return HttpResponse("❌ You are not authorized to sign this document.", status=403)

    # If already signed
    if doc.receiver_signature:
        return HttpResponse("❌ Document already signed by receiver.", status=400)

    # Decrypt file and re-sign
    decrypted_data = decrypt_bytes(doc.encrypted_file)

    if is_agent_receiver:
        private_key_path = config('AGENT_PRIVATE_KEY_PATH')
    else:
        private_key_path = config('CLIENT_PRIVATE_KEY_PATH')

    signature = sign_data(decrypted_data, private_key_path)

    doc.receiver_signature = signature
    doc.save()


    log_document_action(request.user, doc, 'sign', 'Successful signed')

    return redirect("index_page")



class DocumentAuditLogListCreate(generics.ListCreateAPIView):
    queryset = DocumentAuditLog.objects.all()
    serializer_class = DocumentAuditLogSerializer

class DocumentAuditLogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentAuditLog.objects.all()
    serializer_class = DocumentAuditLogSerializer
