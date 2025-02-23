from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm,CategoryForm
from .models import Profile, Post, Comment, Like, Category
from django.db.models import Count
from .models import Post, Category, Comment, Like
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Max
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse

# all posts
def all_posts(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    search_query = request.GET.get('search', '')

    posts = Post.objects.all()

    if selected_category:
        posts = posts.filter(category_id=selected_category)

    if search_query:
        posts = posts.filter(title__icontains=search_query)

    posts = posts.annotate(
        like_count=Count('likes'),
        comment_count=Count('comments')
    )

    # Pagination
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
    }
    
    return render(request, 'blog/all_post.html', context)

# Home Page
def home_page(request):
    category_id = request.GET.get('category')
    
    if category_id:
        return HttpResponseRedirect(reverse('all_posts') + f'?category={category_id}')
    
    posts_queryset = Post.objects.annotate(
        like_count=Count('likes'),
        comment_count=Count('comments')
    )

    posts = posts_queryset.order_by('-created_date')

    most_liked_posts = posts_queryset.order_by('-like_count')[:8]

    recent_posts = posts_queryset.order_by('-created_date')[:8]

    most_commented_posts = posts_queryset.order_by('-comment_count')[:5]

    most_viewed_posts = posts_queryset.order_by('-view_count')[:8]

    categories = Category.objects.all()
    users = User.objects.all()
    
    context = {
        'posts': posts,
        'users': users,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'most_liked_posts': most_liked_posts,
        'recent_posts': recent_posts,
        'most_viewed_posts': most_viewed_posts,
        'most_commented_posts': most_commented_posts,
    }
    
    return render(request, 'blog/home_page.html', context)

@login_required
def user_posts(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user).order_by("-created_date")
    return render(request, "blog/user_posts.html", {"user": user, "posts": posts})

# User Registration
def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Fix: Removed duplicate save()
            messages.success(request, f"Your account has been created successfully! Welcome, {user.username}! Please log in to continue.")
            return redirect('login')
        else:
            messages.error(request, "Please review the form and try again")
    else:
        form = UserRegisterForm()
    
    return render(request, 'blog/register.html', {'form': form})

# User Login
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"{user.username} successfully logged in")
            return redirect('home_page')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'blog/login.html')

# User Logout
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

# Get Profile
@login_required
def get_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    user_posts = Post.objects.filter(user=request.user) 
    return render(request, 'blog/profile.html', {'profile': profile, 'posts': user_posts})

# Edit Profile
@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    user = request.user  

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        bio = request.POST.get("bio")
        profile_picture = request.FILES.get("profile_picture")

        if username and username != user.username:
            user.username = username
        if email and email != user.email:
            user.email = email
        user.save()

        if bio:
            profile.bio = bio
        if profile_picture:
            profile.profile_picture = profile_picture
        profile.save()

        messages.success(request, f"{user.username} profile updated successfully!")
        return redirect("get_profile")

    return render(request, "blog/edit_profile.html", {"profile": profile})

# Create or Edit a Post
@login_required
def post_form(request, post_id=None):
    post = get_object_or_404(Post, id=post_id, user=request.user) if post_id else None
    errors = {} 

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

       # Validate required fields
        if not title:
            errors['title'] = 'Title is required.'
        if not description:
            errors['description'] = 'Description is required.'
        if not category_id:
            errors['category'] = 'Category is required.'
        if not image and not post: 
            errors['image'] = 'Image is required.'

        if not errors:  
            category = get_object_or_404(Category, id=category_id)

            if post:
                post.title = title
                post.description = description
                post.category = category
                post.image = image or post.image
                post.save()
                messages.success(request, f"Post successfully updated by {post.user.username}")
                return redirect('post_details', post_id=post.id)
            else:
                post = Post.objects.create(
                    title=title,
                    description=description,
                    user=request.user,
                    category=category,
                    image=image
                )
                messages.success(request, "Post created successfully!")
                return redirect('all_posts')

    categories = Category.objects.all()
    return render(request, 'blog/post_forms.html', {'post': post, 'categories': categories, 'errors': errors})

# Delete a Post
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully")
        return redirect('home_page')
    return render(request, 'blog/delete_post.html', {'post': post})

# View Post Details & Handle Comments
def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Increment view count and save
    post.view_count += 1
    post.save(update_fields=['view_count'])  

    comments = post.comments.all().order_by('-created_date')  
    liked = request.user.is_authenticated and Like.objects.filter(user=request.user, post=post).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('content', '').strip()
        if text:
            Comment.objects.create(user=request.user, post=post, text=text)
            messages.success(request, 'Comment added successfully!')
            return redirect('post_details', post_id=post.id)
        messages.error(request, 'Comment cannot be empty.')

    return render(request, 'blog/post_details.html', {
        'post': post,
        'comments': comments,
        'liked': liked,
    })

# Like a Post
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()  # Unlike the post if already liked

    return redirect('post_details', post_id=post.id)

# dashboard
@login_required
def user_dashboard(request, user_id):
    user = get_object_or_404(User, id=user_id) 
    user_posts = Post.objects.filter(user=user) 
    categories = Category.objects.filter(user=user) 

    total_likes = sum(post.like_count() for post in user_posts)
    total_views = sum(post.view_count for post in user_posts)
    total_comments = sum(post.comments.count() for post in user_posts)

    max_likes = Post.objects.annotate(likes_count=Count('likes')).aggregate(Max('likes_count'))['likes_count__max'] or 1
    max_views = Post.objects.aggregate(Max('view_count'))['view_count__max'] or 1
    max_comments = Post.objects.annotate(comment_count=Count('comments')).aggregate(Max('comment_count'))['comment_count__max'] or 1

    # Calculate progress percentages
    like_progress = (total_likes / max_likes) * 1 if max_likes > 0 else 0
    view_progress = (total_views / max_views) * 1 if max_views > 0 else 0
    comment_progress = (total_comments / max_comments) * 1 if max_comments > 0 else 0

    post_data = {
        'like_count': total_likes,
        'view_count': total_views,
        'comment_count': total_comments,
        'like_progress': round(like_progress),
        'view_progress': round(view_progress),
        'comment_progress': round(comment_progress),
    }

    context = {
        'post_data': post_data,
        'user_posts': user_posts,
        'user': user,
        'categories': categories,  
    }

    return render(request, 'blog/dashboard.html', context)

# user can create and update category
@login_required
def create_or_update_category(request, category_id=None):
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        if category.user != request.user:
            messages.error(request, "You are not authorized to edit this category.")
            return redirect('user_dashboard', user_id=request.user.id)
    else:
        category = None

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.user = request.user 
            new_category.save() 
            if category:
                messages.success(request, f"Category '{new_category.name}' updated successfully!")
            else:
                messages.success(request, f"Category '{new_category.name}' created successfully!")
            return redirect('user_dashboard', user_id=request.user.id)
        else:
            messages.error(request, "There was an error saving the category. Please check the form.")
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'blog/category_form.html', context)

# user can read category
@login_required
def get_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    context = {
        'category': category,
    }
    return render(request, 'blog/category_detail.html', context)

# user can create a category
@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f"Category '{category_name}' has been deleted successfully!")
        return redirect('user_dashboard', user_id=request.user.id)

    return render(request, 'blog/delete_category.html', {'category': category})

# contact
def contact(request):
    return render(request, 'blog/contact.html')


def forgot_password_request(request):
    return render(request, 'blog/forgot_password_request.html')

def forgot_password_confirm(request, uidb64, token):
    return render(request, 'blog/forgot_password_confirm.html')
