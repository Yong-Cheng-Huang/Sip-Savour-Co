"""
URL configuration for sipsavour project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# from django.views.generic import TemplateView
from django.conf.urls import include
from products import views as product_views
from account import views as account_views


urlpatterns = [
    # path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("", product_views.home, name="home"),
    path("admin/", admin.site.urls),
    path("products/", include("products.urls")),
    path("register/", account_views.register, name="register"),
    path("login/", account_views.login, name="login"),
    path("logout/", account_views.logout, name="logout"),
    path("contact/", include("contact.urls")),
    path("about/", include("about.urls")),
    path("news/", include("news.urls")),
]

# 處理媒體檔案
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
