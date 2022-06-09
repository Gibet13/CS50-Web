from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Comment, Follower, Like, Post, Profile, User


def index(request):
    return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile.objects.create(user = user)
            followers = Follower.objects.create(user = user)
            profile.save()
            followers.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def view_post(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(id = post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(post.serialize())
    pass


def load_posts(request, postbox):

    # Filter posts returned based on postbox
    if postbox == "all":
        posts = Post.objects.all()

    elif postbox == "following":
        follow_list = Follower.objects.filter(user = request.user).values_list('followers')
        posts = Post.objects.filter(author__in = follow_list)

    else:
        return JsonResponse({"error": "Invalid filter."}, status=400)

    # Return posts in reverse chronologial order
    posts = posts.order_by("-date").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


def load_profile(request, user_id):

    try:
        profile = Profile.objects.get(user = user_id)
    except Profile.DoesNotExist:
        return JsonResponse({"error": "Profile not found."}, status=404)

    if request.method == "GET":
        posts = Post.objects.filter(author = user_id)
        return JsonResponse([profile.serialize(), [post.serialize() for post in posts]], safe=False)
    pass


@csrf_exempt
@login_required
def create_post(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
        
    # Get contents of post
    title = data.get("title", "")
    body = data.get("body", "")

    new_post = Post(
        author=request.user,
        title=title,
        body=body,
    )
    
    new_post.save()
    post_likes = Like.objects.create(post = new_post)
    post_likes.save()

    return JsonResponse({"message": "post sent successfully."}, status=201)


@csrf_exempt
@login_required
def edit_post(request, post_id):
    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
        
    try:
        post = Post.objects.get(id = post_id)
    except Like.DoesNotExist:
        return JsonResponse({"error": "post not found."}, status=404)

    data = json.loads(request.body)
        
    # Get contents of post
    title = data.get("title", "")
    body = data.get("body", "")

    post.title = title
    post.body = body

    post.save()
    
    return JsonResponse({"message": "post edited successfully."}, status=201)


@csrf_exempt
@login_required
def post_comment(request, post_id):
    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
        
    # Get contents of post
    body = data.get("body", "")

    new_comment = Comment(
        author=request.user,
        post = Post.objects.get(id = post_id),
        body=body,
    )
    new_comment.save()

    return JsonResponse({"message": "comment posted successfully."}, status=201)


@login_required
def load_comments(request, post_id):
    
    comments = Comment.objects.filter(post = post_id)
    comments = comments.order_by("-date").all()

    return JsonResponse([comment.serialize() for comment in comments], safe=False)


@csrf_exempt
@login_required
def follow_user(request, follow_id):
    if request.method == "POST":

        try:
            user = Follower.objects.get(user_id = follow_id)
        except Follower.DoesNotExist:
            return JsonResponse({"error": "user not found."}, status=404)

        followed_user = Profile.objects.get(id = follow_id)
        following_user = Profile.objects.get(id = request.user.id)

        if user.followers.filter(id = request.user.id).exists():
            user.followers.remove(request.user)
            followed_user.follower_count -= 1
            following_user.following_count -= 1
            return JsonResponse({"message": "succesful unfolllow."}, status=201)
        else:
            user.followers.add(request.user)
            followed_user.follower_count += 1
            following_user.following_count += 1
            return JsonResponse({"message": "succesful follow."}, status=201)
    

@csrf_exempt    
@login_required
def like_post(request, post_id):
    if request.method == "POST":
        
        try:
            post = Like.objects.get(post_id = post_id)
        except Like.DoesNotExist:
            return JsonResponse({"error": "post not found."}, status=404)

        liked_post = Post.objects.get(id = post_id)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked_post.like_count -= 1
            return JsonResponse({"message": "post successfully disliked."}, status=201)
        else:
            post.likes.add(request.user)
            liked_post.like_count += 1
            return JsonResponse({"message": "post successfully liked."}, status=201)

    
    