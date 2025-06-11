from django.db import models
from django.utils.text import slugify

class Location(models.Model):
    landmark = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.landmark}-{self.city}-{self.state}-{self.country}-{self.zip_code}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.city}, {self.state}, {self.country}"
