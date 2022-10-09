from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Post
from .forms import CommentForm, PostForm


class PostList(generic.ListView):

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        query = None
        sort = None
        direction = None

        if request.GET:
            if 'sort' in request.GET:
                sortkey = request.GET['sort']
                sort = sortkey
                if sortkey == 'title':
                    posts = posts.annotate(lower_name=Lower('title'))
                if 'direction' in request.GET:
                    direction = request.GET['direction']
                    if direction == 'desc':
                        sortkey = f'-{sortkey}'
                posts = posts.order_by(sortkey)

            if 'q' in request.GET:
                query = request.GET['q']
                if not query:
                    messages.error(request, "You didn't enter any search criteria!")
                    return redirect(reverse('posts'))

                queries = Q(title__icontains=query) | Q(content__icontains=query)
                posts = posts.filter(queries)

        current_sorting = f'{sort}_{direction}'

        context = {
            'posts': posts,
            'search_term': query,
            'current_sorting': current_sorting,
        }

        return render(request, 'posts/posts.html', context)


class PostDetail(View):

    def get(self, request, post_id, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(Post, pk=post_id)
        comments = post.comments.filter(approved=True).order_by("-created")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "posts/post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, post_id, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(Post, pk=post_id)
        comments = post.comments.filter(approved=True).order_by("-created")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            messages.success(request, 'Success! Comment submitted, pending approval.')
            comment.save()
        else:
            comment_form = CommentForm()
            messages.warning(request, 'Comment failed. Please try again.')

        return render(
            request,
            "posts/post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostLike(View):

    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, pk=post_id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[post.id]))


@login_required
def add_post(request):
    """ Add a post """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin users can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Successfully added post!')
            return redirect(reverse('post_detail', args=[post.id]))
        else:
            messages.error(request, 'Failed to add post. Please ensure the form is valid.')
    else:
        form = PostForm()
        
    template = 'posts/add_post.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_post(request, post_id):
    """ Edit a post """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin users can do that.')
        return redirect(reverse('home'))

    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated post!')
            return redirect(reverse('post_detail', args=[post.id]))
        else:
            messages.error(request, 'Failed to update post. Please ensure the form is valid.')
    else:
        form = PostForm(instance=post)
        messages.info(request, f'You are editing {post.title}')

    template = 'posts/edit_post.html'
    context = {
        'form': form,
        'post': post,
    }

    return render(request, template, context)


@login_required
def delete_post(request, post_id):
    """ Delete a post """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin users can do that.')
        return redirect(reverse('home'))

    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    messages.success(request, 'Post deleted!')
    return redirect(reverse('posts'))
