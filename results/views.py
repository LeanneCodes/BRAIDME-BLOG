from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.views import View
from django.db.models import Q
from posts.models import Post

# Create your views here.


def all_results(request):
    """ A view to show all posts, including sorting and search queries """

    posts = Post.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('results'))

            post_queries = Q(title__icontains=query) | Q(content__icontains=query)
            posts = posts.filter(post_queries)

    context = {
        'posts': posts,
        'search_term': query,
    }

    return render(request, 'results/results.html', context)
