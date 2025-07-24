from django.contrib import admin
from .models import UserMetaData

@admin.register(UserMetaData)
class UserMetaDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'email')
    search_fields = ('user__username', 'phone_number', 'email')
    ordering = ('user__username',)