from django.contrib import admin
from .models import Stylist, Review
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Stylist)
class StylistAdmin(SummernoteModelAdmin):

    list_display = ('stylist', 'brand', 'specialty', 'price', 'mobile', 'town_or_city',)
    search_fields = ['stylist', 'brand', 'specialty', 'mobile', 'town_or_city']
    list_filter = ('stylist', 'brand',)
    prepopulated_fields = {'slug': ('brand',)}
    summernote_fields = ('requirements', 'hairstyles',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'review_title', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(approved=True)
