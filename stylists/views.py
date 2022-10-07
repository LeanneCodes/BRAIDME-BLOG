from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Stylist, Review

# Create your views here.


def all_stylists(request):
    """ A view to show all stylists, including sorting and search queries """

    stylists = Stylist.objects.all()
    query = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'brand':
                # sortkey = 'lower_brand_name'
                stylists = stylists.annotate(lower_name=Lower('brand'))
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

            queries = Q(stylist__icontains=query) | Q(brand__icontains=query) | Q(specialty__icontains=query) | Q(requirements__icontains=query)
            stylists = stylists.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'stylists': stylists,
        'search_term': query,
        'current_sorting': current_sorting,
    }

    return render(request, 'stylists/stylists.html', context)


def stylists_detail(request, stylist_id):
    """ A view to show individual product details """

    stylist = get_object_or_404(Stylist, pk=stylist_id)

    context = {
        'stylist': stylist,
    }

    return render(request, 'stylists/stylists_detail.html', context)
