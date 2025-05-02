from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('C', 'Client'),
        ('A', 'Agent'),
    ]
    
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=17,
        blank=True
    )
    role = models.CharField(
        max_length=1,
        choices=ROLE_CHOICES,
        default='C'
    )

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

class Client(models.Model):
    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='client_profile'
    )
    company_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=50)
    company_type = models.CharField(max_length=4)
    industry_sector = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return f"{self.company_name} (Client)"

class ClientDocument(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    file = models.FileField(upload_to='client_documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.client.company_name}"
    
class Agent(models.Model):
    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='agent_profile'
    )
    bank_name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=50)
    job_title = models.CharField(max_length=100)
    business_email = models.EmailField()

    def __str__(self):
        return f"{self.user_profile.full_name} ({self.bank_name})"

class AgentDocument(models.Model):
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    file = models.FileField(upload_to='agent_documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.agent.user_profile.full_name}"

# models.py

class SecureDocument(models.Model):
    document_name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=50, choices=[
        ('contract', 'Contract'),
        ('report', 'Report'),
        ('form', 'Form'),
        ('other', 'Other'),
    ])
    description = models.TextField(blank=True)

    encrypted_file = models.BinaryField()
    uploader_signature = models.BinaryField()
    receiver_signature = models.BinaryField(null=True, blank=True)  # will be added later

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document_name
