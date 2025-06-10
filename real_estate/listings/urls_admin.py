from django.urls import path
from listings.auth.views import (
    admin_dashboard, admin_properties, admin_property_create, admin_property_detail,
    admin_property_edit, admin_property_delete, admin_property_verify, admin_categories,
    admin_category_create, admin_category_edit, admin_category_delete, admin_locations,
    admin_location_create, admin_location_edit, admin_location_delete, admin_users,
    admin_user_create, admin_user_detail, admin_user_edit, admin_user_delete,
)
from listings.contact.views import (admin_contact_messages)

app_name = 'listings_admin'

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('properties/', admin_properties, name='admin_properties'),
    path('properties/create/', admin_property_create, name='admin_property_create'),
    path('properties/<slug:slug>/', admin_property_detail, name='admin_property_detail'),
    path('properties/<slug:slug>/edit/', admin_property_edit, name='admin_property_edit'),
    path('properties/<slug:slug>/delete/', admin_property_delete, name='admin_property_delete'),
    path('properties/<slug:slug>/verify/', admin_property_verify, name='admin_property_verify'),
    path('categories/', admin_categories, name='admin_categories'),
    path('categories/create/', admin_category_create, name='admin_category_create'),
    path('categories/<slug:slug>/edit/', admin_category_edit, name='admin_category_edit'),
    path('categories/<slug:slug>/delete/', admin_category_delete, name='admin_category_delete'),
    path('locations/', admin_locations, name='admin_locations'),
    path('locations/create/', admin_location_create, name='admin_location_create'),
    path('locations/<slug:slug>/edit/', admin_location_edit, name='admin_location_edit'),
    path('locations/<slug:slug>/delete/', admin_location_delete, name='admin_location_delete'),
    path('users/', admin_users, name='admin_users'),
    path('users/create/', admin_user_create, name='admin_user_create'),
    path('users/<str:username>/', admin_user_detail, name='admin_user_detail'),
    path('users/<str:username>/edit/', admin_user_edit, name='admin_user_edit'),
    path('users/<str:username>/delete/', admin_user_delete, name='admin_user_delete'),
    path('contact/', admin_contact_messages, name='admin_contact_messages'),
]