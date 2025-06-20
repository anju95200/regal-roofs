from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/listings/', include('listings.urls_admin', namespace='listings_admin')),  # Admin routes
    path('admin/', admin.site.urls),  # Django admin site
    path('accounts/', include('allauth.urls')), # Google account
    path('', include('listings.urls', namespace='listings')),  # Non-admin routes
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)