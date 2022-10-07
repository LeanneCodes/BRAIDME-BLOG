from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_stylists, name='stylists'),
    path('<stylist_id>', views.stylists_detail, name='stylists_detail'),
]
