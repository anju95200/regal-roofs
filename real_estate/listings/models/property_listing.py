from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from .category import Category
from .location import Location

class PropertyListing(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
    )

    TYPE_CHOICES = (
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    listing_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='sale')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='listings')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='listings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    bedrooms = models.PositiveIntegerField(blank=True, null=True)
    bathrooms = models.PositiveIntegerField(blank=True, null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # in square feet
    is_verified = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse('listings:listing_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            counter = 1
            while PropertyListing.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title