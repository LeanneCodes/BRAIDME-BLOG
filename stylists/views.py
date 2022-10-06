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
