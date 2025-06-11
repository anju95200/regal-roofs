from django import forms
from django.forms import inlineformset_factory
from ..models import PropertyListing, PropertyImage, Location, Category

class PropertyListingForm(forms.ModelForm):
    landmark = forms.CharField(max_length=200, required=False)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    country = forms.CharField(max_length=100, required=True)
    zip_code = forms.CharField(max_length=6, required=True)
    

    class Meta:
        model = PropertyListing
        fields = ['title', 'description', 'price', 'listing_type', 'category', 'bedrooms', 'bathrooms', 'area']
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If an instance is provided (i.e., editing an existing listing), populate location fields
        if self.instance and self.instance.pk and self.instance.location:
            self.fields['landmark'].initial = self.instance.location.landmark
            self.fields['city'].initial = self.instance.location.city
            self.fields['state'].initial = self.instance.location.state
            self.fields['country'].initial = self.instance.location.country
            self.fields['zip_code'].initial = self.instance.location.zip_code

    def save(self, commit=True):
        location, created = Location.objects.get_or_create(
            landmark=self.cleaned_data['landmark'],
            city=self.cleaned_data['city'],
            state=self.cleaned_data['state'],
            country=self.cleaned_data['country'],
            zip_code=self.cleaned_data['zip_code']
        )
        instance = super().save(commit=False)
        instance.location = location
        if commit:
            instance.save()
        return instance


class PropertyFilterForm(forms.Form):
    listing_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(PropertyListing.TYPE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label='All Categories',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_category'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + list(PropertyListing.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    price_min = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min Price'})
    )
    price_max = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Price'})
    )
    bedrooms = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bedrooms', 'id': 'id_bedrooms'})
    )
    bathrooms = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bathrooms', 'id': 'id_bathrooms'})
    )
    area_min = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min Area (sq ft)'})
    )
    area_max = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Area (sq ft)'})
    )
    landmark = forms.CharField(
        max_length=200, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Landmark'})
    )
    city = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_city'})
    )
    state = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_state'})
    )
    country = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_country'})
    )
    zip_code = forms.IntegerField(
        max_value=999999, required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_zip_code'})
    )

    def __init__(self, *args, **kwargs):
        super(PropertyFilterForm, self).__init__(*args, **kwargs)

        # Populate distinct values for dropdowns
        self.fields['city'].choices = [('', 'All Cities')] + [
            (item['city'], item['city']) for item in Location.objects.values('city').distinct().exclude(city__isnull=True).exclude(city__exact='')
        ]
        self.fields['state'].choices = [('', 'All States')] + [
            (item['state'], item['state']) for item in Location.objects.values('state').distinct().exclude(state__isnull=True).exclude(state__exact='')
        ]
        self.fields['country'].choices = [('', 'All Countries')] + [
            (item['country'], item['country']) for item in Location.objects.values('country').distinct().exclude(country__isnull=True).exclude(country__exact='')
        ]


PropertyImageFormSet = inlineformset_factory(
    PropertyListing,
    PropertyImage,
    fields=['image'],
    extra=3,
    can_delete=True
)
