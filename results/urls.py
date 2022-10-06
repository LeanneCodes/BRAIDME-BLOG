from django.urls import path
from . import views

urlpatterns = [
    # path('', views.all_posts, name='results'),
    # path('', views.all_products, name='results'),
    # path('', views.all_stylists, name='results'),
    path('', views.all_results, name='results'),
]
