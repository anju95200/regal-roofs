from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from ..models import PropertyListing, Favorite

@login_required
def favorite_toggle(request, slug):
    listing = get_object_or_404(PropertyListing, slug=slug)
    favorite, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
    if not created:
        favorite.delete()
        message = "Removed from favorites."
        is_favorite = False
    else:
        message = "Added to favorites."
        is_favorite = True

    button_html = render_to_string("listings/partials/favorite_button.html", {
        "listing": listing,
        "is_favorite": is_favorite
    })
    icon_html = render_to_string("listings/partials/favorite_icon.html", {
        "listing": listing,
        "is_favorite": is_favorite
    })
    message_html = render_to_string("listings/partials/message.html", {
        "message": message
    })
    return HttpResponse(button_html + icon_html + message_html)
