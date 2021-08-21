from collections import namedtuple
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import widgets
from django.forms.forms import Form
from django.forms.models import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Bids, Comment, User,Listing, Watchlist,Category
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django import forms


class ListingForm(ModelForm):
    class Meta:
        model=Listing
        fields={'listed_by','name','description','current_bid','category','image_url'}
        exclude=['listed_by']
        
class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields={'user','comment','listing'}
        exclude=['user','listing']
        widgets={'comment':forms.TextInput()}

class BidForm(ModelForm):
    class Meta:
        model=Bids
        fields={'bid_by','listing_name','bid'}
        exclude=['bid_by','listing_name']
   
        

        
    

def index(request):

    return render(request, "auctions/index.html",{
        "Listings":Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        Watchlist.objects.create(
            user=user
        )
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def Listing_view(request,listing_name):
    if not request.user.is_authenticated:
        
        return HttpResponseRedirect(reverse("login"))
    else:

        bidForm=BidForm()
        commentForm=CommentForm()
        listing1=Listing.objects.get(name=listing_name)
        comments=Comment.objects.filter(listing=listing1)
        if listing1.closed:
            winningbid=Bids.objects.get(bid=listing1.current_bid)
            return render(request, 'auctions/listing.html',{
            'listing':listing1,
            'commentForm':commentForm,
            'comments':comments,
            "bidform":bidForm,
            'minbiderror':"",
            'winner':winningbid.bid_by
            })
        if request.method=='GET':

            return render(request, 'auctions/listing.html',{
            'listing':listing1,
            'commentForm':commentForm,
            'comments':comments,
            "bidform":bidForm,
            'minbiderror':"",
            
            })
        else:
            
            commentform=CommentForm(request.POST)
            if commentform.is_valid():
                comment=commentform.cleaned_data['comment']
                commentCreated=Comment.objects.create(
                    user=request.user,
                    listing=listing1,
                    comment=comment
                )
            
            return HttpResponseRedirect(reverse("listing",kwargs={'listing_name':listing1.name}))
    
@login_required
def watchlist(request):
    if not request.user.is_authenticated:
        
        return HttpResponseRedirect(reverse("login"))

    else:
        watchlist=Watchlist.objects.get(user= request.user)
        return render(request, 'auctions/watchlist.html',{
        "watchlist":watchlist.listing.all()
        })
@login_required
def add_to_watchlist(request,listing_name):
    if not request.user.is_authenticated:
        
        return HttpResponseRedirect(reverse("login"))
    
    elif request.method=='POST':
        watchlist=Watchlist.objects.get(user= request.user)
        

        listing=Listing.objects.get(name=listing_name)
        if listing:
            watchlist.listing.add(listing)
            watchlist.save()
        
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def remove_from_watchlist(request,listing_name):
    if not request.user.is_authenticated:
        
        return HttpResponseRedirect(reverse("login"))
    elif request.method=='POST':
        watchlist=Watchlist.objects.get(user= request.user)
        listing=Listing.objects.get(name=listing_name)
        watchlist.listing.remove(listing)
        watchlist.save()
        
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def addListing(request):
    user=request.user
    if not request.user.is_authenticated:
        
        return HttpResponseRedirect(reverse("login"))
    
    elif request.method=='GET':
        return render(request, "auctions/add_listing.html", {
            "form":ListingForm()
        })
    else:
        form=ListingForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            current_bid = form.cleaned_data['current_bid']
            category = form.cleaned_data['category']
            image_url = form.cleaned_data['image_url']

            ListingCreated = Listing.objects.create(
                listed_by=request.user,
                name=name, 
                description=description, 
                current_bid=current_bid,
                category=category,
                image_url=image_url,
            )
            bidCreated=Bids.objects.create(
                bid_by= request.user,
                listing=ListingCreated,
                bid=current_bid
            )
        return HttpResponseRedirect(reverse("index"))
def addbid(request,listing_name):
        bidForm=BidForm()
        commentForm=CommentForm()
        listing1=Listing.objects.get(name=listing_name)
        comments=Comment.objects.filter(listing=listing1)
        bidform=BidForm(request.POST)
    
        if bidform.is_valid():
                bid=bidform.cleaned_data['bid']
                
                bidCreated=Bids.objects.create(
                        bid_by=request.user,
                        listing=listing1,
                        bid=bid
                )
                if bid>listing1.current_bid:
                    listing1.current_bid=bid
                    listing1.save()
                    return HttpResponseRedirect(reverse("listing",kwargs={'listing_name':listing1.name}))
                else:
                    return render(request, 'auctions/listing.html',{
            'listing':listing1,
            'commentForm':commentForm,
            'comments':comments,
            "bidform":bidForm,
            'minbiderror':"minimum value of bid should be greater than current price"
            })
                
def closelisting(request,listing_name):
    listing1=Listing.objects.get(name=listing_name)
    listing1.closed=True
    listing1.save()
    return HttpResponseRedirect(reverse("listing",kwargs={'listing_name':listing1.name})) 

def categoryview(request):
    return render(request, "auctions/categories.html",{
        "categories":Category.objects.all()
    })

def categorylisting(request,category_name):
    category1=Category.objects.get(category_name=category_name)
    return render(request, "auctions/categorylisting.html",{
        "Listings":Listing.objects.filter(category=category1)
    })