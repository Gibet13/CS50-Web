from django.contrib.auth import authenticate, login, logout, models
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models.base import Model
from django.forms import fields
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms

from .models import Category, User, Listing, Bid, Comment, Watchlist, Winner

class listing_form(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['name','descryption','category','image','price']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'descryption': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'})
        }

class bid_form(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['value']

        widgets = {
            'value': forms.NumberInput(attrs={'class': 'form-control'})
        }

class comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'})
        }


def index(request):
    
    if request.GET.get("filter"):
        filter = request.GET.get("filter")
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(category = filter, opened = True),
            "categories": Category.objects.all()
        })
    else:
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(opened = True),
            "categories": Category.objects.all()
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

@login_required
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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    
    if request.method == "POST":
        listform = listing_form(request.POST, request.FILES)

        if listform.is_valid():
            new_listing = listform.save(commit=False)
            new_listing.author = request.user
            new_listing.save()
            return redirect('index')
        else:
            return render(request, "auctions/create_listing.html",{"form":listform})

    return render(request, "auctions/create_listing.html", {
        "form": listing_form()
    })

def listing_page(request, item_id):

    is_watched = False
    is_author = False
    is_winner = False
    entry = Listing.objects.get(id = item_id)

    if request.method == "POST":
        Listing.objects.filter(id = item_id).update(opened = False)
        if Bid.objects.filter(listing = entry).order_by('value').first():
            best_bid = Bid.objects.filter(listing = entry).order_by('value').first()
            Winner.objects.create(user = best_bid.author, listings = entry)
        return redirect('index')

    if request.user.is_authenticated:
        if Watchlist.objects.filter(user = request.user, listings = entry):
            is_watched = True
        if entry.author == request.user:
            is_author = True
        if Winner.objects.filter(user = request.user, listings = entry):
            is_winner = True

    return render(request, "auctions/listing.html", {
        "listing": entry,
        "is_watched": is_watched,
        "is_author": is_author,
        "is_winner": is_winner,
        "comments": Comment.objects.filter(listing = entry),
        "bids": Bid.objects.filter(listing = entry),
        "commentform": comment_form(),
        "bidform": bid_form()
    })

@login_required
def watchlist(request):
    user_watchlist = Watchlist.objects.filter(user = request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": user_watchlist
    })

@login_required
def postcomment(request, item_id):
    current_listing = Listing.objects.get(id = item_id)
    if request.method == "POST":
        commform =comment_form(request.POST)
        if commform.is_valid():
            new_comment = commform.save(commit=False)
            new_comment.author = request.user
            new_comment.listing = current_listing
            new_comment.save()
            return redirect('listing', item_id)

@login_required
def postbid(request, item_id):

    current_listing = Listing.objects.get(id = item_id)

    if Bid.objects.filter(listing = current_listing).order_by('value').first():
        best_bid = Bid.objects.filter(listing = current_listing).order_by('value').first()
        match = best_bid.value
    else:
        match = current_listing.price

    if request.method == "POST":
        bidform = bid_form(request.POST)

        if bidform.is_valid():
            new_bid = bidform.save(commit=False)
            new_bid.author = request.user
            new_bid.listing = current_listing

            if new_bid.value > match:
                if Bid.objects.filter(author = request.user, listing = current_listing):
                    Bid.objects.filter(author = request.user, listing = current_listing).update(value = new_bid.value)
                else:
                    new_bid.save()
                return redirect('listing', item_id)
            else:
                return redirect('listing', item_id)

@login_required
def addwatchlist(request, item_id):

    if request.method == "POST":
        if not Watchlist.objects.filter(user = request.user, listings = Listing.objects.get(id = item_id)):
            Watchlist.objects.create(
                user = request.user,
                listings = Listing.objects.get(id = item_id)
            )
        else:
            watched_item = Watchlist.objects.get(
                user = request.user,
                listings = Listing.objects.get(id = item_id)
            )
            watched_item.delete()
        return redirect('listing', item_id)

