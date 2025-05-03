from django.contrib import admin
from .models import CustomUser, UserProfile, Agent, AgentDocument, Client, ClientDocument, SecureDocument, DocumentAuditLog, Report

admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Agent)
admin.site.register(AgentDocument)
admin.site.register(Client)
admin.site.register(ClientDocument)
admin.site.register(SecureDocument)
admin.site.register(DocumentAuditLog)
admin.site.register(Report)
