from django.shortcuts import render
from .models import Post, Comment

# Create your views here.


def all_posts(request):
    """ A view to show all posts, including sorting and search queries """

    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/posts.html', context)


def post_detail(request, post_id):
    """ A view to show individual post details """

    post = get_object_or_404(Post, pk=post_id)

    context = {
        'post': post,
    }

    return render(request, 'posts/post_detail.html', context)
