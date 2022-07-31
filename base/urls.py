from django.contrib import admin
from django.urls import path

from base import views

app_name = 'base'

urlpatterns = [
    path('<blog_id>/', views.blog_view, name = 'blog'),
    path('update-blog/<str:pk>/', views.update_blog, name = 'update-blog'),
    path('delete-blog/<str:pk>/', views.delete_blog, name = 'delete-blog'),
    path('delete-comment/<str:pk>/', views.delete_comment, name = 'delete-comment'),
    # path('update-blog-image/<str:pk>/', views.update_blog_image, name = 'update-blog-image'),
]