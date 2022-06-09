from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:item_id>", views.listing_page, name="listing"),
    path("create_listing", views.create_listing, name="create listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("postcomment/<int:item_id>", views.postcomment, name="postcomment"),
    path("postbid/<int:item_id>", views.postbid, name="postbid"),
    path("addwatchlist/<int:item_id>", views.addwatchlist, name="addwatchlist")
]

