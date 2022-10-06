from django.shortcuts import render
from .models import Stylist, Review

# Create your views here.


def all_stylists(request):
    """ A view to show all stylists, including sorting and search queries """

    stylists = Stylist.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('stylists'))

            queries = Q(stylist_name__icontains=query) | Q(brand_name__icontains=query) | Q(specialty__icontains=query) | Q(requirements__icontains=query)
            stylists = stylists.filter(queries)

    context = {
        'stylists': stylists,
        'search_term': query,
    }

    return render(request, 'stylists/stylists.html', context)


def stylist_detail(request, stylist_id):
    """ A view to show individual product details """

    stylist = get_object_or_404(Stylist, pk=stylist_id)

    context = {
        'stylist': stylist,
    }

    return render(request, 'stylists/stylist_detail.html', context)
