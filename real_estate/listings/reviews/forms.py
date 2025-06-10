from django import forms
from ..models import WebsiteReview

class WebsiteReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = WebsiteReview
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }