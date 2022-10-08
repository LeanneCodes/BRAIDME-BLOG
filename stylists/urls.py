from django.urls import path
from . import views

urlpatterns = [
    path("", views.StylistList.as_view(), name="stylists"),
    path('<slug:slug>/', views.StylistDetail.as_view(), name='stylist_detail'),
    path('like/<slug:slug>', views.StylistLike.as_view(), name='stylist_like'),
]
