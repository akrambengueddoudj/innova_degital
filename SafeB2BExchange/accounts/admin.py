from django.contrib import admin
from .models import CustomUser, UserProfile, Agent, AgentDocument, Client, ClientDocument, SecureDocument

admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Agent)
admin.site.register(AgentDocument)
admin.site.register(Client)
admin.site.register(ClientDocument)
admin.site.register(SecureDocument)
