"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import urls

from authentication import views as authentication_views
from blog import views as blog_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", authentication_views.LoginPageView, name="login"),
    path("logout/", authentication_views.LogoutPageView, name="logout"),
    path("home/", blog_views.home, name="home"),
    path("signup/", authentication_views.signup, name="signup"),
    path("create-ticket/", blog_views.create_ticket, name="create-ticket"),
    path("posts/", blog_views.AllPostsView, name="posts"),
    path("post/<int:post_id>", blog_views.PostView, name="view-post"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

