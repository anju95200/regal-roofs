from django.db import models
from django.contrib.auth.models import User
from .property_listing import PropertyListing

class Inquiry(models.Model):
    listing = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='inquiries')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_inquiries')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Inquiry from {self.sender.username} for {self.listing.title}"
    
    class Meta:
        verbose_name_plural = "Inquiries"