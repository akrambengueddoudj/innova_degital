from rest_framework import serializers
from .models import DocumentAuditLog

class DocumentAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentAuditLog
        fields = '__all__'