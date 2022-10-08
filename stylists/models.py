from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django_countries.fields import CountryField


STATUS = ((0, "No"), (1, "Yes"))
LIVE = ((0, "No"), (1, "Yes"))
SERVICE = (("Braids", "Braids"), ("Wigs", "Wigs"), ("Weaves", "Weaves"), ("Locs", "Locs"), ("Men's Hair", "Men's Hair"), ("Natural Hair", "Natural Hair"), ("Kid's Hair", "Kid's Hair"))


class Stylist(models.Model):
    stylist = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    stylist_email = models.EmailField(max_length=254)
    stylist_phone = models.CharField(max_length=11)
    brand_image = CloudinaryField('image', default='placeholder')
    brand_image_url = models.URLField(max_length=1024, null=True, blank=True)
    specialty = models.CharField(max_length=15, choices=SERVICE, default=0)
    hairstyles = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    requirements = models.TextField()
    website = models.URLField(max_length=200, default='')
    mobile = models.IntegerField(choices=STATUS, default=0)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    live = models.IntegerField(choices=LIVE, default=0)
    likes = models.ManyToManyField(
        User, related_name='stylist_like', blank=True)

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return self.brand

    def number_of_likes(self):
        return self.likes.count()


class Review(models.Model):
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE,
                                related_name="reviews")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    review_title = models.TextField(max_length=30)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Review {self.body} by {self.name}"
