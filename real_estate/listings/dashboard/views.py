import logging
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from ..models import PropertyListing, Favorite, Inquiry, UserProfile
from .forms import UserForm, UserProfileForm, CustomPasswordChangeForm

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    listings = PropertyListing.objects.filter(user=request.user).select_related('location')
    favorites = Favorite.objects.filter(user=request.user).select_related('listing__location')
    inquiries = Inquiry.objects.filter(sender=request.user).select_related('listing')
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    return render(request, 'listings/dashboard/dashboard.html', {
        'listings': listings,
        'favorites': favorites,
        'inquiries': inquiries,
        'user_profile': user_profile,
    })

@login_required
def edit_profile(request):
    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        logger.info(f"POST data: {request.POST}")
        logger.info(f"FILES: {request.FILES}")
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            # Check if a new profile picture is uploaded
            if 'profile_picture' in request.FILES:
                # New image uploaded, save it
                profile_form.save()
            elif profile_form.cleaned_data.get('delete_profile_picture') and profile.profile_picture:
                # No new image, delete existing if requested
                profile.profile_picture.delete(save=False)
                profile.profile_picture = None
                profile_form.save()
            else:
                # No new image or deletion, save other fields
                profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('listings:dashboard')
        else:
            logger.error(f"UserForm errors: {user_form.errors}")
            logger.error(f"ProfileForm errors: {profile_form.errors}")
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'listings/dashboard/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = CustomPasswordChangeForm(request.user, request.POST)
        logger.info(f"POST data: {request.POST}")
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('listings:dashboard')
        else:
            logger.error(f"PasswordForm errors: {password_form.errors}")
            messages.error(request, 'Please correct the errors below.')
    else:
        password_form = CustomPasswordChangeForm(request.user)

    return render(request, 'listings/dashboard/change_password.html', {
        'password_form': password_form,
    })

@login_required
def delete_listing(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug, user=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing deleted successfully!')
    return redirect('listings:dashboard')

@login_required
def remove_favorite(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug)
    favorite = Favorite.objects.filter(user=request.user, listing=listing).first()
    if favorite and request.method == 'POST':
        favorite.delete()
        messages.success(request, 'Removed from favorites!')
    return redirect('listings:dashboard')

@login_required
def delete_inquiry(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id, sender=request.user)
    if request.method == 'POST':
        inquiry.delete()
        messages.success(request, 'Inquiry deleted successfully!')
    return redirect('listings:dashboard')