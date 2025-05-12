from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.


def register(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            message = "使用者名稱已存在"
        else:
            User.objects.create_user(username=username, password=password)
            message = "註冊成功，請登入"
            return redirect("login")
    return render(request, "account/register.html", {"message": message})


def login(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect("home")
        else:
            message = "帳號或密碼錯誤"
    return render(request, "account/login.html", {"message": message})


def logout(request):
    auth_logout(request)
    return redirect("login")
