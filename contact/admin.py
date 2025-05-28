from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'message_preview')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    def message_preview(self, obj):
        # 顯示訊息的前50個字符
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = '訊息預覽'