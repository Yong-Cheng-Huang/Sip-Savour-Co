from django.db import models

# Create your models here.
class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name='姓名')
    email = models.EmailField(verbose_name='電子郵件')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='電話')
    message = models.TextField(verbose_name='訊息內容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    
    class Meta:
        verbose_name = '聯絡訊息'
        verbose_name_plural = '聯絡訊息'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"