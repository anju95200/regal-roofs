from django.shortcuts import render
from django.db.models import Q
from ..models import PropertyListing
from .forms import SearchForm

def search_listings(request):
    form = SearchForm(request.GET or None)
    listings = PropertyListing.objects.all()
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        location = form.cleaned_data.get('location')
        listing_type = form.cleaned_data.get('listing_type')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        bedrooms = form.cleaned_data.get('bedrooms')
        if query:
            listings = listings.filter(Q(title__icontains=query) | Q(description__icontains=query))
        if category:
            listings = listings.filter(category=category)
        if location:
            listings = listings.filter(location=location)
        if listing_type:
            listings = listings.filter(listing_type=listing_type)
        if min_price:
            listings = listings.filter(price__gte=min_price)
        if max_price:
            listings = listings.filter(price__lte=max_price)
        if bedrooms:
            listings = listings.filter(bedrooms__gte=bedrooms)
    return render(request, 'listings/search/search_results.html', {'form': form, 'listings': listings})