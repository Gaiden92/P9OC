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

from authentication import views as auth_views
from blog import views as blog_views

urlpatterns = [
    path("admin-panel/", admin.site.urls),
    path("", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
    path("home/", blog_views.home, name="home"),
    path("subscriptions/", blog_views.follow_user, name="subscriptions"),
    path(
        "subscriptions/<int:user_follow_id>/unfollow/",
        blog_views.unfollow_user,
        name="unfollow",
    ),
    path("signup/", auth_views.signup_view, name="signup"),
    path("create-ticket/", blog_views.create_ticket, name="create-ticket"),
    path("posts/", blog_views.AllPostsView, name="posts"),
    path("ticket/<int:post_id>/", blog_views.ticket_view, name="ticket-view"),
    path(
        "ticket/<int:ticket_id>/update-ticket/",
        blog_views.update_ticket,
        name="update-ticket",
    ),
    path(
        "ticket/<int:ticket_id>/delete-ticket/",
        blog_views.delete_ticket,
        name="delete-ticket",
    ),
    path(
        "create-review/",
        blog_views.create_ticket_and_review,
        name="create-ticket-and-review",
    ),
    path(
        "create-review/<int:ticket_id>",
        blog_views.create_review,
        name="create-review"
    ),
    path(
        "update-review/<int:review_id>/",
        blog_views.update_review,
        name="update-review"
    ),
    path(
        "delete-review/<int:review_id>/",
        blog_views.delete_review,
        name="delete-review"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
