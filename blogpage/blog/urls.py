from django.contrib import admin
from django.urls import path
from core.views import *
from core import views

urlpatterns = [
    path('create_post', views.create_post, name='create_post'),
    path('mypost/<int:id>/', views.single_post, name='single_post'),
    path('category/<int:id>/', views.category, name='category_post'),

    # Native rest endpoint exaple
    path('post/', views.rest_post, name='rest_post'),
    path('post/<int:id>/', views.rest_post, name='rest_post'),
    path('posts/', views.rest_posts, name='rest_posts'),

]