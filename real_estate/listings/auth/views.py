from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from ..models import UserProfile, PropertyListing, Category, Location
from .forms import (
    CustomUserCreationForm, CustomPasswordResetForm, PropertyListingForm, 
    PropertyImageFormSet, CategoryForm, LocationForm, UserForm, UserProfileForm
)
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

def superuser_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('listings:home')
        return view_func(request, *args, **kwargs)
    return wrapper

def register(request):
    if request.user.is_authenticated:
        return redirect('listings:home') 
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('listings:home')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'listings/auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('listings_admin:admin_dashboard')
        else:
            return redirect('listings:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            if request.user.is_superuser:
                return redirect('listings_admin:admin_dashboard')
            else:
                return redirect('listings:home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'listings/auth/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('listings:home')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'listings/auth/password_reset_form.html'
    email_template_name = 'listings/auth/password_reset_email.txt'
    html_email_template_name = 'listings/auth/password_reset_email.html'
    subject_template_name = 'listings/auth/password_reset_subject.txt'
    success_url = reverse_lazy('listings:password_reset_done')
    form_class = CustomPasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email, is_active=True)

        if user:
            context = {
                'email': user.email,
                'domain': self.request.get_host(),
                'site_name': 'Regal Roofs Real Estate',
                'uid': urlsafe_base64_encode(force_bytes(str(user.pk))),
                'user': user,
                'token': self.token_generator.make_token(user),
                'protocol': 'https' if self.request.is_secure() else 'http',
            }
            self.send_mail(
                self.subject_template_name,
                self.email_template_name,
                context,
                settings.DEFAULT_FROM_EMAIL,
                user.email,
                html_email_template_name=self.html_email_template_name,
            )
        return redirect(self.get_success_url())

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        subject = render_to_string(subject_template_name, context)
        body = render_to_string(email_template_name, context)
        email_message = EmailMultiAlternatives(subject=subject, body=body, from_email=from_email, to=[to_email])

        if html_email_template_name:
            html_email = render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'listings/auth/password_reset_confirm.html'
    success_url = reverse_lazy('listings:password_reset_complete')

@superuser_required
def admin_dashboard(request):
    property_count = PropertyListing.objects.count()
    category_count = Category.objects.count()
    location_count = Location.objects.count()
    user_count = User.objects.count()
    context = {
        'property_count': property_count,
        'category_count': category_count,
        'location_count': location_count,
        'user_count': user_count,
    }
    return render(request, 'listings/admin/dashboard.html', context)

@superuser_required
def admin_properties(request):
    listings = PropertyListing.objects.select_related('user', 'category', 'location').all()
    return render(request, 'listings/admin/properties.html', {'listings': listings})

@superuser_required
def admin_property_create(request):
    if request.method == 'POST':
        form = PropertyListingForm(request.POST)
        formset = PropertyImageFormSet(request.POST, request.FILES, instance=PropertyListing())
        if form.is_valid() and formset.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user  # Assign to superuser; adjust if needed
            listing.save()
            formset.instance = listing
            formset.save()
            messages.success(request, 'Property created successfully!')
            return redirect('listings_admin:admin_properties')
        else:
            messages.error(request, 'Error creating property. Please correct the errors.')
    else:
        form = PropertyListingForm()
        formset = PropertyImageFormSet(instance=PropertyListing())
    return render(request, 'listings/admin/property_create.html', {'form': form, 'formset': formset})

@superuser_required
def admin_property_detail(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug)
    return render(request, 'listings/admin/property_detail.html', {'listing': listing})

@superuser_required
def admin_property_edit(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug)
    if request.method == 'POST':
        form = PropertyListingForm(request.POST, instance=listing)
        formset = PropertyImageFormSet(request.POST, request.FILES, instance=listing)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('listings_admin:admin_property_detail', slug=listing.slug)
        else:
            messages.error(request, 'Error updating property. Please correct the errors.')
    else:
        form = PropertyListingForm(instance=listing)
        formset = PropertyImageFormSet(instance=listing)
    return render(request, 'listings/admin/property_edit.html', {'form': form, 'formset': formset, 'listing': listing})

@superuser_required
def admin_property_delete(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('listings_admin:admin_properties')
    return render(request, 'listings/admin/property_delete.html', {'listing': listing})

@superuser_required
def admin_property_verify(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug)
    if request.method == 'POST':
        listing.is_verified = not listing.is_verified
        listing.save()
        messages.success(request, f'Listing {"verified" if listing.is_verified else "unverified"} successfully!')
        return redirect('listings_admin:admin_properties')
    return redirect('listings_admin:admin_property_detail', slug=slug)

@superuser_required
def admin_categories(request):
    categories = Category.objects.all()
    return render(request, 'listings/admin/categories.html', {'categories': categories})

@superuser_required
def admin_category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('listings_admin:admin_categories')
        else:
            messages.error(request, 'Error creating category. Please correct the errors.')
    else:
        form = CategoryForm()
    return render(request, 'listings/admin/category_create.html', {'form': form})

@superuser_required
def admin_category_edit(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('listings_admin:admin_categories')
        else:
            messages.error(request, 'Error updating category. Please correct the errors.')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'listings/admin/category_edit.html', {'form': form, 'category': category})

@superuser_required
def admin_category_delete(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('listings_admin:admin_categories')
    return render(request, 'listings/admin/category_delete.html', {'category': category})

@superuser_required
def admin_locations(request):
    locations = Location.objects.all()
    return render(request, 'listings/admin/locations.html', {'locations': locations})

@superuser_required
def admin_location_create(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location created successfully!')
            return redirect('listings_admin:admin_locations')
        else:
            messages.error(request, 'Error creating location. Please correct the errors.')
    else:
        form = LocationForm()
    return render(request, 'listings/admin/location_create.html', {'form': form})

@superuser_required
def admin_location_edit(request, slug):
    location = get_object_or_404(Location, slug=slug)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location updated successfully!')
            return redirect('listings_admin:admin_locations')
        else:
            messages.error(request, 'Error updating location. Please correct the errors.')
    else:
        form = LocationForm(instance=location)
    return render(request, 'listings/admin/location_edit.html', {'form': form, 'location': location})

@superuser_required
def admin_location_delete(request, slug):
    location = get_object_or_404(Location, slug=slug)
    if request.method == 'POST':
        location.delete()
        messages.success(request, 'Location deleted successfully!')
        return redirect('listings_admin:admin_locations')
    return render(request, 'listings/admin/location_delete.html', {'location': location})

@superuser_required
def admin_users(request):
    users = User.objects.select_related('profile').all()
    return render(request, 'listings/admin/users.html', {'users': users})

@superuser_required
def admin_user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect('listings_admin:admin_users')
        else:
            messages.error(request, 'Error creating user. Please correct the errors.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'listings/admin/user_create.html', {'form': form})

@superuser_required
def admin_user_detail(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'listings/admin/user_detail.html', {'user': user})

@superuser_required
def admin_user_edit(request, username):
    user = get_object_or_404(User, username=username)
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('listings_admin:admin_user_detail', username=user.username)
        else:
            messages.error(request, 'Error updating user. Please correct the errors.')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    return render(request, 'listings/admin/user_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user
    })

@superuser_required
def admin_user_delete(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('listings_admin:admin_users')
    return render(request, 'listings/admin/user_delete.html', {'user': user})