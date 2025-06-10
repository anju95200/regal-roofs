from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from listings.models import UserProfile

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.user.email
        if email:
            try:
                existing_user = User.objects.get(email=email)
                if not sociallogin.is_existing:
                    sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                pass

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.first_name = data.get('given_name', '')
        user.last_name = data.get('family_name', '')
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        # Get extra data from Google
        data = sociallogin.account.extra_data

        user.first_name = data.get('given_name', '')
        user.last_name = data.get('family_name', '')
        user.save()  # You must call save here!

        # Optional: create or update profile
        from listings.models import UserProfile
        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': '',
            }
        )

        return user
