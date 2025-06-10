from django import forms
from ..models import Category, Location

class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search')
    listing_type = forms.ChoiceField(choices=[('', 'Any'), ('sale', 'Sale'), ('rent', 'Rent')], required=False)
    min_price = forms.DecimalField(required=False, label='Min Price')
    max_price = forms.DecimalField(required=False, label='Max Price')
    bedrooms = forms.IntegerField(required=False, label='Bedrooms')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label='Any Category')
    location = forms.ModelChoiceField(queryset=Location.objects.all(), required=False, empty_label='Any Location')