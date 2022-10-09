from . import views
from django.urls import path

urlpatterns = [
    path("", views.PostList.as_view(), name="posts"),
    path('int:<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('add/', views.add_post, name='add_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
]
