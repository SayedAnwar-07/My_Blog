from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import os

def blogger_name_dict(instance, filename):
    return os.path.join("blog/media/", instance.user.username, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to=blogger_name_dict, 
        default="defaults/user-icon.png",
        blank=True, 
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to="categories_logo/")

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="post_images/")
    description = models.TextField()
    created_date = models.DateField(default=now)
    created_time = models.TimeField(default=now)
    view_count = models.PositiveIntegerField(default=0)

    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_date = models.DateField(default=now)
    created_time = models.TimeField(default=now)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_date = models.DateField(default=now)
    created_time = models.TimeField(default=now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_like')
        ]

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"
