from django.shortcuts import render
from .models import Stylist, Review

# Create your views here.


def all_stylists(request):
    """ A view to show all stylists, including sorting and search queries """

    stylists = Stylist.objects.all()
    context = {
        'stylists': stylists,
    }
    return render(request, 'stylists/stylists.html', context)


def stylist_detail(request, stylist_id):
    """ A view to show individual product details """

    stylist = get_object_or_404(Stylist, pk=stylist_id)

    context = {
        'stylist': stylist,
    }

    return render(request, 'stylists/stylist_detail.html', context)
