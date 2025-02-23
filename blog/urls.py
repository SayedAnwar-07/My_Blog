from django.urls import path
from .views import (
    register_user, login_user, logout_user, get_profile, 
    edit_profile,post_form,delete_post,post_details,like_post,home_page,all_posts,user_dashboard,create_or_update_category,get_category,delete_category,contact,user_posts,forgot_password_request,forgot_password_confirm
)

urlpatterns = [
    path('', home_page, name='home_page'),
    path('all-posts/', all_posts, name='all_posts'),
    path("user/<int:user_id>/", user_posts, name="user_posts"),
    path('contact/', contact, name='contact'),
    
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', get_profile, name='get_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    
    path('forgot-password/', forgot_password_request, name='forgot_password_request'),
    path('forgot-password-confirm/<uidb64>/<token>/', forgot_password_confirm, name='forgot_password_confirm'),
    
    path('create/', post_form, name='create_post'),
    path('edit/<int:post_id>/', post_form, name='edit_post'),
    path('delete/<int:post_id>/', delete_post, name='delete_post'),
    path('post/<int:post_id>/', post_details, name='post_details'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    
    # dashboard
    path('dashboard/<int:user_id>/', user_dashboard, name='user_dashboard'),
    path('category/create/', create_or_update_category, name='create_category'),
    path('category/update/<int:category_id>/', create_or_update_category, name='update_category'),
    path('category/<int:category_id>/', get_category, name='get_category'),
    path('category/delete/<int:category_id>/', delete_category, name='delete_category'),
    
]
