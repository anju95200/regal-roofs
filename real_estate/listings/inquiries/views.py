from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from ..models import PropertyListing, Inquiry
from .forms import InquiryForm

@login_required
def inquiry_create(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug)
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.sender = request.user
            inquiry.listing = listing
            inquiry.save()

            # Send email to the property owner
            if listing.user.email:
                try:
                    subject = f"New Inquiry for Your Property: {listing.title}"
                    context = {
                        'owner_username': listing.user.username,
                        'owner_name': f"{listing.user.first_name} {listing.user.last_name}",
                        'listing_title': listing.title,
                        'sender_username': f"{request.user.first_name} {request.user.last_name}",
                        'message': inquiry.message,
                        'sender_email': request.user.email,
                        'listing_price': f"₹{listing.price:,.2f}",
                        'listing_type': listing.get_listing_type_display(),
                        'location': str(listing.location) if listing.location else 'Not specified',
                        'listing_url': request.build_absolute_uri(listing.get_absolute_url()) if hasattr(listing, 'get_absolute_url') else 'Not available',
                    }
                    plain_message = (
                        f"Dear {listing.user.first_name} {listing.user.last_name},\n\n"
                        f"You have received a new inquiry for your property '{listing.title}' from {request.user.first_name} {request.user.last_name}.\n\n"
                        f"Property Details:\n"
                        f"- Type: {context['listing_type']}\n"
                        f"- Price: {context['listing_price']}\n"
                        f"- Location: {context['location']}\n\n"
                        f"Message:\n{inquiry.message}\n\n"
                        f"Contact the sender at: {request.user.email}\n\n"
                        f"View the listing: {context['listing_url']}\n"
                        f"View the inquiry in your dashboard for more details."
                    )
                    html_message = render_to_string('listings/inquiries/inquiry_notification.html', context)
                    email = EmailMultiAlternatives(
                        subject=subject,
                        body=plain_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[listing.user.email],
                    )
                    email.attach_alternative(html_message, "text/html")
                    email.send()
                    messages.success(request, 'Inquiry sent successfully! The property owner has been notified.')
                except Exception as e:
                    messages.error(request, f'Inquiry sent, but failed to notify the owner: {str(e)}')
            else:
                messages.warning(request, 'Inquiry sent, but the property owner has no email address set.')

            return redirect('listings:listing_detail', slug=slug)
        else:
            messages.error(request, 'Error sending inquiry.')
    else:
        form = InquiryForm()
    return render(request, 'listings/inquiries/inquiry_form.html', {'form': form, 'listing': listing})