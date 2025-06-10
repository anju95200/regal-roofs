from django.contrib import admin
from .models import Category, Location, UserProfile, PropertyListing, PropertyImage, Favorite, Inquiry, WebsiteReview, ContactMessage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['landmark', 'city', 'state', 'country', 'zip_code', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('city', 'state', 'country')}

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email', 'phone_number', 'profile_picture', 'created_at']

@admin.register(PropertyListing)
class PropertyListingAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'slug', 'description', 'price', 'listing_type', 'category', 'location', 'status', 'bedrooms', 'bathrooms', 'area', 'is_verified', 'view_count', 'created_at', 'updated_at']
    list_filter = ['category', 'location', 'listing_type', 'status']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['listing', 'image', 'uploaded_at']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'created_at']

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['sender', 'listing', 'message', 'is_read']
    list_filter = ['is_read']

@admin.register(WebsiteReview)
class WebsiteReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'comment', 'created_at', 'updated_at']
    
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message', 'created_at']