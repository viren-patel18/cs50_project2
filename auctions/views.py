from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    if "category_id" in request.GET:
        listings = Category.objects.get(pk=request.GET["category_id"]).listings.all()
    else:
        listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if "watchlist_flag" in request.GET:
        watchlist = Watchlist.objects.filter(user=request.user).first()
        if not watchlist:
            watchlist = Watchlist(user = request.user)
            watchlist.save()
        if request.GET["watchlist_flag"] == "0":
            watchlist.listings.remove(listing)
        else:
            watchlist.listings.add(listing)

    if "comment" in request.GET:
        comment = Comment(
            content = request.GET["comment"],
            listing = listing,
            author = request.user,
            timestamp = datetime.date.today()
        )
        comment.save()

    bidMessage = ""
    bidPlaced= 0
    currentBid = listing.bids.last()
    if request.method == "POST" and "amount" in request.POST:
        if currentBid:
            condition = float(request.POST["amount"]) > float(str(currentBid))
        else:
            condition = float(request.POST["amount"]) >= float(listing.startBid)
        if condition:
            bid = Bid(
                amount = request.POST["amount"],
                listing = listing,
                bidder = request.user
            )
            bid.save()
            bidMessage = "Bid placed!"
            bidPlaced = 1
        else:
            bidMessage = "Amount entered must be higher than the current bid amount."

    if "close" in request.GET:
        if request.GET["close"] == "1":
            listing.active = False
            listing.save()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "currentBid": listing.bids.last(),
        "comments": listing.comments.all().order_by("-id"),
        "categories": listing.categories.all(),
        # ", ".join([str(cat) for cat in listing.categories.all()]),
        "watchlist_flag": 0 if request.user in [wl.user for wl in listing.watchlists.all()] else 1,
        "bidMessage": bidMessage,
        "bidPlaced": bidPlaced
    })

@login_required
def create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        listing = Listing(
            title = request.POST["title"],
            description = request.POST["description"],
            imageUrl = request.POST["imageUrl"],
            startBid = request.POST["startBid"],
            creator = request.user,
            timestamp = datetime.date.today()
        )
        listing.save()
        if "categories" in request.POST:
            for category in request.POST.getlist("categories"):
                listing.categories.add(Category.objects.get(pk=int(category)))
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    else:
        return render(request, "auctions/create.html", {
            "categories": Category.objects.all()
        })

@login_required
def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    watchlist = Watchlist.objects.filter(user = request.user).first()
    return render(request, "auctions/watchlist.html", {
        "listings": watchlist.listings.all() if watchlist else None
    })

def categories(request):
    return render(request, "auctions/categories.html", {
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
