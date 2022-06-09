
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    # API Routes
    path("posts", views.create_post, name="create_post"),
    path("posts/<int:post_id>", views.view_post, name="view_post"),
    path("posts/edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("comment/<int:post_id>", views.post_comment, name="post_comment"),
    path("posts/<int:post_id>/comments", views.load_comments, name="load_comments"),
    path("posts/<str:postbox>", views.load_posts, name="load_posts"),
    path("profile/<int:user_id>", views.load_profile, name="load_profile"),
    path("follow/<int:follow_id>", views.follow_user, name="follow_user"),
    path("like/<int:post_id>", views.like_post, name="like_post")

]

