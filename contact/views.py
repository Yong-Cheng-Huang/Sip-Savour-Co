from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        
        messages.success(request, '您的訊息已成功送出！')
        return redirect('contact:contact')
    
    return render(request, 'contact/contact.html')