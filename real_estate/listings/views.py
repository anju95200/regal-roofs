from django.shortcuts import render
from django.db.models import Count, Case, When, IntegerField
from django.contrib.auth.models import User
from .models import PropertyListing, WebsiteReview, Favorite

def home(request):
    listings = PropertyListing.objects.all()[:6]
    reviews = WebsiteReview.objects.all().order_by('-created_at')[:4]
    
    # Get counts using aggregation
    total_listings = PropertyListing.objects.all()
    counts = total_listings.aggregate(
        total_count=Count('id'),
        rent_count=Count(Case(When(listing_type='rent', then=0), output_field=IntegerField())),
        sale_count=Count(Case(When(listing_type='sale', then=0), output_field=IntegerField())),
    )
    total_users_non_admin = User.objects.filter(is_superuser=False).count()
    
    # Handle favorites
    if request.user.is_authenticated:
        favorites = set(
            Favorite.objects.filter(user=request.user).values_list('listing_id', flat=True)
        )
        for listing in listings:
            listing.is_favorite = listing.id in favorites
    else:
        for listing in listings:
            listing.is_favorite = False
            
    return render(request, 'listings/home.html', {
        'listings': listings,
        'reviews': reviews,
        'total_count': counts['total_count'],
        'rent_count': counts['rent_count'],
        'sale_count': counts['sale_count'],
        'total_users': total_users_non_admin,
    })

def services(request):
    return render(request, 'listings/services.html')

def about(request):
    return render(request, 'listings/about.html')

def vision(request):
    return render(request, 'listings/vision.html')

def mission(request):
    return render(request, 'listings/mission.html')

def terms(request):
    return render(request, 'listings/terms.html')

def privacy(request):
    return render(request, 'listings/privacy.html')

def partners(request):
    return render(request, 'listings/partners.html')

def business(request):
    return render(request, 'listings/business.html')

def careers(request):
    return render(request, 'listings/careers.html')

def blog(request):
    return render(request, 'listings/blog.html')

def faq(request):
    return render(request, 'listings/faq.html')