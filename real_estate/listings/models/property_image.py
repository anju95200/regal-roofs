from django.db import models
from .property_listing import PropertyListing

class PropertyImage(models.Model):
    listing = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.listing.title}"