from django.db import models
from django.contrib.auth.models import User
from .property_listing import PropertyListing

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    listing = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} favorited {self.listing.title}"

    class Meta:
        unique_together = ('user', 'listing')