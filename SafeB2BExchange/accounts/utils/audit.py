from ..models import DocumentAuditLog, SecureDocument
from datetime import timedelta
from django.utils import timezone
from django.db.models import F

def log_document_action(user, document, action, details=""):
    audit = DocumentAuditLog.objects.create(
        user=user,
        document=document,
        action=action,
        details=details
    )
    audit.save()

def get_user_stats(user):
    if hasattr(user.profile, 'agent_profile'):
        now = timezone.now()
        one_week_ago = now - timedelta(days=7)
        two_weeks_ago = now - timedelta(days=14)

        logs = DocumentAuditLog.objects.filter(user=user)
        unsigned_logs = SecureDocument.objects.filter(agent=user.profile.agent_profile, receiver_signature__isnull=True).count()
        old_unsigned_logs = SecureDocument.objects.filter(agent=user.profile.agent_profile, receiver_signature__isnull=True, uploaded_at__lt=now - timedelta(days=3)).count()
        signed_logs = SecureDocument.objects.filter(agent=user.profile.agent_profile, receiver_signature__isnull=False).count()

        if unsigned_logs + signed_logs == 0:
            completion_percentage = 0
        else:
            completion_percentage = (signed_logs / (unsigned_logs + signed_logs)) * 100

        # Current and previous week downloads
        downloads_this_week = logs.filter(
            action="download",
            timestamp__gte=one_week_ago,
            timestamp__lt=now
        ).count()

        downloads_last_week = logs.filter(
            action="download",
            timestamp__gte=two_weeks_ago,
            timestamp__lt=one_week_ago
        ).count()

        # Calculate percentage change
        if downloads_last_week == 0:
            if downloads_this_week > 0:
                percent_change = 100  # From 0 to something = full increase
            else:
                percent_change = 0  # No activity either week
        else:
            percent_change = ((downloads_this_week - downloads_last_week) / downloads_last_week) * 100

        return {
            "uploads": logs.filter(action="upload").count(),
            "downloads": logs.filter(action="download").count(),
            "signatures": logs.filter(action="sign").count(),
            "last_activity": logs.order_by('-timestamp').first(),
            "downloads_this_week": downloads_this_week,
            "downloads_last_week": downloads_last_week,
            "download_change_percent": round(percent_change, 2),
            'unsigned_logs': unsigned_logs,
            'signed_logs': signed_logs,
            'old_unsigned_logs': old_unsigned_logs,
            'completion_percentage': round(completion_percentage, 2),
        }
    return {
        "uploads": None,
        "downloads": None,
        "signatures": None,
        "last_activity": None,
        "downloads_this_week": None,
        "downloads_last_week": None,
        "download_change_percent": None,
    }