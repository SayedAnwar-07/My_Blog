from django.contrib import admin
from .models import Category,Profile,Post,Comment,Like

# Register your models here.

admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Post)