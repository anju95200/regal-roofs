from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import PropertyListing, Favorite
from .forms import PropertyListingForm, PropertyImageFormSet, PropertyFilterForm, PropertyImageFormSet, PropertyImage

def listing_list(request):
    # Initialize filter form
    filter_form = PropertyFilterForm(request.GET or None)
    listings = PropertyListing.objects.all()

    # Apply filters
    if filter_form.is_valid():
        if filter_form.cleaned_data['listing_type']:
            listings = listings.filter(listing_type=filter_form.cleaned_data['listing_type'])
        if filter_form.cleaned_data['category']:
            listings = listings.filter(category=filter_form.cleaned_data['category'])
        if filter_form.cleaned_data['status']:
            listings = listings.filter(status=filter_form.cleaned_data['status'])
        if filter_form.cleaned_data['price_min']:
            listings = listings.filter(price__gte=filter_form.cleaned_data['price_min'])
        if filter_form.cleaned_data['price_max']:
            listings = listings.filter(price__lte=filter_form.cleaned_data['price_max'])
        if filter_form.cleaned_data['bedrooms']:
            listings = listings.filter(bedrooms=filter_form.cleaned_data['bedrooms'])
        if filter_form.cleaned_data['bathrooms']:
            listings = listings.filter(bathrooms=filter_form.cleaned_data['bathrooms'])
        if filter_form.cleaned_data['area_min']:
            listings = listings.filter(area__gte=filter_form.cleaned_data['area_min'])
        if filter_form.cleaned_data['area_max']:
            listings = listings.filter(area__lte=filter_form.cleaned_data['area_max'])
        if filter_form.cleaned_data['landmark']:
            listings = listings.filter(location__landmark__icontains=filter_form.cleaned_data['landmark'])
        if filter_form.cleaned_data['city']:
            listings = listings.filter(location__city__icontains=filter_form.cleaned_data['city'])
        if filter_form.cleaned_data['state']:
            listings = listings.filter(location__state__icontains=filter_form.cleaned_data['state'])
        if filter_form.cleaned_data['country']:
            listings = listings.filter(location__country__icontains=filter_form.cleaned_data['country'])
        if filter_form.cleaned_data['zip_code']:
            listings = listings.filter(zip_code=filter_form.cleaned_data['zip_code'])

    # Pagination
    paginator = Paginator(listings, 6)  # Show 6 listings per page
    page = request.GET.get('page')
    try:
        listings_paginated = paginator.page(page)
    except PageNotAnInteger:
        listings_paginated = paginator.page(1)
    except EmptyPage:
        listings_paginated = paginator.page(paginator.num_pages)

    # Handle favorites
    if request.user.is_authenticated:
        favorites = set(
            Favorite.objects.filter(user=request.user).values_list('listing_id', flat=True)
        )
        for listing in listings_paginated:
            listing.is_favorite = listing.id in favorites
    else:
        for listing in listings_paginated:
            listing.is_favorite = False

    context = {
        'listings': listings_paginated,
        'filter_form': filter_form,
        'paginator': paginator,
        'page_obj': listings_paginated,
    }
    return render(request, 'listings/listings/listing_list.html', context)

def listing_detail(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, listing=listing).exists()
    context = {
        'listing': listing,
        'is_favorite': is_favorite,
    }
    return render(request, 'listings/listings/listing_detail.html', context)

@login_required
def listing_create(request):
    if request.method == 'POST':
        form = PropertyListingForm(request.POST)
        formset = PropertyImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            formset.instance = listing
            formset.save()
            messages.success(request, 'Listing created successfully!')
            return redirect('listings:listing_list')
        else:
            messages.error(request, 'Error creating listing.')
    else:
        form = PropertyListingForm()
        formset = PropertyImageFormSet(queryset=PropertyImage.objects.none())
    return render(request, 'listings/listings/listing_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Create Listing'
    })

@login_required
def listing_update(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug, user=request.user)
    if request.method == 'POST':
        form = PropertyListingForm(request.POST, instance=listing)
        formset = PropertyImageFormSet(request.POST, request.FILES, instance=listing)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Listing updated successfully!')
            return redirect('listings:listing_detail', slug=slug)
        else:
            messages.error(request, 'Error updating listing.')
    else:
        form = PropertyListingForm(instance=listing)
        existing_images = listing.images.all()
        existing_count = existing_images.count()
        max_forms = 3  # Total forms (existing + new) should not exceed 3
        extra_forms = max(0, max_forms - existing_count)
        
        formset = PropertyImageFormSet(instance=listing)
        formset.extra = extra_forms  # Pass to template for rendering logic
        if existing_count > max_forms:
            formset.queryset = existing_images[:max_forms]
        
    return render(request, 'listings/listings/listing_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Update Listing'
    })

@login_required
def listing_delete(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug, user=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing deleted successfully!')
        return redirect('listings:listing_list')
    return render(request, 'listings/listings/listing_confirm_delete.html', {'listing': listing})

@login_required
def listing_mark_status(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug, user=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'mark' and listing.status == 'available':
            if listing.listing_type == 'sale':
                listing.status = 'sold'
            elif listing.listing_type == 'rent':
                listing.status = 'rented'
            listing.save()
            messages.success(request, f'Listing marked as {"Sold" if listing.listing_type == "sale" else "Rented"} successfully!')
        elif action == 'unmark' and listing.status in ['sold', 'rented']:
            listing.status = 'available'
            listing.save()
            messages.success(request, 'Listing marked as Available successfully!')
        else:
            messages.error(request, 'Invalid action or listing status.')
        return redirect('listings:listing_detail', slug=slug)
    return redirect('listings:listing_detail', slug=slug)