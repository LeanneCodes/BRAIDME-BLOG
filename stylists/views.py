from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Stylist, Review
from .forms import ReviewForm

# Create your views here.


class StylistList(generic.ListView):
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        stylists = Stylist.objects.all()
        query = None
        sort = None
        direction = None

        if request.GET:
            if 'sort' in request.GET:
                sortkey = request.GET['sort']
                sort = sortkey
                if sortkey == 'stylist':
                    stylists = stylists.annotate(lower_name=Lower('stylist'))
                if 'direction' in request.GET:
                    direction = request.GET['direction']
                    if direction == 'desc':
                        sortkey = f'-{sortkey}'
                stylists = stylists.order_by(sortkey)

            if 'q' in request.GET:
                query = request.GET['q']
                if not query:
                    messages.error(request, "You didn't enter any search criteria!")
                    return redirect(reverse('stylists'))

                queries = Q(stylist__icontains=query) | Q(requirements__icontains=query)
                stylists = stylists.filter(queries)

        current_sorting = f'{sort}_{direction}'

        context = {
            'stylists': stylists,
            'search_term': query,
            'current_sorting': current_sorting,
        }

        return render(request, 'stylists/stylists.html', context)


class StylistDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Stylist.objects.filter(live=1)
        stylist = get_object_or_404(queryset, slug=slug)
        reviews = stylist.reviews.filter(approved=True).order_by("created_on")
        liked = False
        if stylist.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "stylists/stylist_detail.html",
            {
                "stylist": stylist,
                "reviews": reviews,
                "reviewed": False,
                "liked": liked,
                "review_form": ReviewForm()
            },
        )

    def stylist(self, request, slug, *args, **kwargs):

        queryset = Stylist.objects.filter(live=1)
        stylist = get_object_or_404(queryset, slug=slug)
        reviews = stylist.reviews.filter(approved=True).order_by("created_on")
        liked = False
        if stylist.likes.filter(id=self.request.user.id).exists():
            liked = True

        review_form = ReviewForm(data=request.Stylist)
        if review_form.is_valid():
            review_form.instance.email = request.user.email
            review_form.instance.name = request.user.username
            review = review_form.save(commit=False)
            review.stylist = stylist
            messages.success(request, 'Success! review submitted, pending approval.')
            review.save()
        else:
            review_form = reviewForm()
            messages.warning(request, 'Review failed. Please try again.')

        return render(
            request,
            "stylists/stylist_detail.html",
            {
                "stylist": stylist,
                "reviews": reviews,
                "reviewed": True,
                "review_form": review_form,
                "liked": liked
            },
        )


class StylistLike(View):

    def stylist(self, request, slug, *args, **kwargs):
        stylist = get_object_or_404(stylist, slug=slug)
        if stylist.likes.filter(id=request.user.id).exists():
            stylist.likes.remove(request.user)
        else:
            stylist.likes.add(request.user)

        return HttpResponseRedirect(reverse('stylist_detail', args=[slug]))
