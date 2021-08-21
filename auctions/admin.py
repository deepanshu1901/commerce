from auctions.views import BidForm
from django.contrib import admin

# Register your models here.
from .models import Bids, Category, Comment, User,Listing, Watchlist
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bids)