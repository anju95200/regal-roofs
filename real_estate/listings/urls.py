from django.urls import path
from .auth.views import register, login_view, logout_view, CustomPasswordResetView, CustomPasswordResetConfirmView
from .listings.views import listing_list, listing_detail, listing_create, listing_update, listing_delete, listing_mark_status
from .search.views import search_listings
from .favorites.views import favorite_toggle
from .inquiries.views import inquiry_create
from .dashboard.views import dashboard, edit_profile, delete_listing, remove_favorite, delete_inquiry, change_password
from .reviews.views import add_website_review, website_reviews, edit_website_review, delete_website_review
from .contact.views import contact_admin
from .views import home, services, about, vision, mission, terms, privacy, partners, business, careers, faq, blog
from django.contrib.auth import views as auth_views

app_name = 'listings'

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('listings/', listing_list, name='listing_list'),
    path('listings/create/', listing_create, name='listing_create'),
    path('listings/<slug:slug>/', listing_detail, name='listing_detail'),
    path('listings/<slug:slug>/update/', listing_update, name='listing_update'),
    path('listings/<slug:slug>/delete/', listing_delete, name='listing_delete'),
    path('listings/<slug:slug>/mark-status/', listing_mark_status, name='listing_mark_status'),
    path('search/', search_listings, name='search_listings'),
    path('favorites/<slug:slug>/', favorite_toggle, name='favorite_toggle'),
    path('inquiries/<slug:slug>/', inquiry_create, name='inquiry_create'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/edit_profile/', edit_profile, name='edit_profile'),
    path('dashboard/change_password/', change_password, name='change_password'),
    path('dashboard/listing/delete/<slug:slug>/', delete_listing, name='delete_listing'),
    path('dashboard/favorite/remove/<slug:slug>/', remove_favorite, name='remove_favorite'),
    path('dashboard/inquiry/delete/<int:inquiry_id>/', delete_inquiry, name='delete_inquiry'),
    path('services/', services, name='services'),
    path('about/', about, name='about'),
    path('vision/', vision, name='vision'),
    path('mission/', mission, name='mission'),
    path('terms/', terms, name='terms'),
    path('privacy/', privacy, name='privacy'),
    path('partners/', partners, name='partners'),
    path('business/', business, name='business'),
    path('careers/', careers, name='careers'),
    path('blog/', blog, name='blog'),
    path('faq/', faq, name='faq'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='listings/auth/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='listings/auth/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('reviews/add/', add_website_review, name='add_website_review'),
    path('reviews/edit/<int:review_id>/', edit_website_review, name='edit_website_review'),
    path('reviews/delete/<int:review_id>/', delete_website_review, name='delete_website_review'),
    path('reviews/', website_reviews, name='website_reviews'),
    path('contact/', contact_admin, name='contact_admin'),
]