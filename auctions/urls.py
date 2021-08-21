from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:listing_name>",views.Listing_view,name='listing'),
    path("watchlist",views.watchlist,name='watchlist'),
    path("add_to_watchlist/<str:listing_name>",views.add_to_watchlist,name="add_to_watchlist"),
    path("remove_from_watchlist/<str:listing_name>",views.remove_from_watchlist,name="remove_from_watchlist"),
    path("addlisting",views.addListing,name='add_listing'),
    path("bid/<str:listing_name>",views.addbid,name="add_bid"),
    path("closelisting/<str:listing_name>",views.closelisting,name='close_listing'),
    path("category/<str:category_name>",views.categorylisting,name='categorylisting'),
    path("categories",views.categoryview,name='categoryview')

]
