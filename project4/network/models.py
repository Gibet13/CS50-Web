from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import CharField, DateField, TextField
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.user.id,
            "name": self.user.username,
            "followers":self.follower_count,
            "following":self.following_count
    }


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    date = models.DateField(auto_now_add=True)
    body = models.TextField(blank=True)
    like_count = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id":self.id,
            "author": self.author.username,
            "author_id": self.author.id,
            "title":self.title,
            "date":self.date,
            "body":self.body,
            "like_count":self.like_count
    }


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    body = models.TextField(blank=True)

    def serialize(self):
        return {
            "id":self.id,
            "author": self.author.username,
            "author_id": self.author.id,
            "date":self.date,
            "body":self.body
    }


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,blank=True, related_name='liked_posts')


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    