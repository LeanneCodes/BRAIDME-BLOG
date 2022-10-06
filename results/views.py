from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.views import View
from django.db.models import Q
from posts.models import Post
from products.models import Product
from stylists.models import Stylist

# Create your views here.


def all_results(request):
    """ A view to show all products, posts and stylists, including sorting and search queries """

    stylists = Stylist.objects.all()
    posts = Post.objects.all()
    products = Product.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('results'))

            stylist_queries = Q(stylist_name__icontains=query) | Q(brand_name__icontains=query) | Q(specialty__icontains=query) | Q(requirements__icontains=query)
            stylists = stylists.filter(stylist_queries)
            product_queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(product_queries)
            post_queries = Q(title__icontains=query) | Q(content__icontains=query)
            posts = posts.filter(post_queries)

    context = {
        'stylists': stylists,
        'products': products,
        'posts': posts,
        'search_term': query,
    }

    return render(request, 'results/results.html', context)
