from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import WebsiteReview
from .forms import WebsiteReviewForm

@login_required
def add_website_review(request):
    if request.method == 'POST':
        form = WebsiteReviewForm(request.POST)
        if form.is_valid():
            # Check if user already reviewed the website
            if WebsiteReview.objects.filter(user=request.user).exists():
                messages.error(request, 'You have already reviewed this website.')
                return redirect('listings:website_reviews')
            
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully.')
            return redirect('listings:website_reviews')
    else:
        form = WebsiteReviewForm()
    
    return render(request, 'listings/reviews/add_website_review.html', {
        'form': form
    })

@login_required
def edit_website_review(request, review_id):
    review = get_object_or_404(WebsiteReview, id=review_id, user=request.user)
    if request.method == 'POST':
        form = WebsiteReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated successfully.')
            return redirect('listings:website_reviews')
    else:
        form = WebsiteReviewForm(instance=review)
    
    return render(request, 'listings/reviews/edit_website_review.html', {
        'form': form,
        'review': review
    })

@login_required
def delete_website_review(request, review_id):
    review = get_object_or_404(WebsiteReview, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review has been deleted successfully.')
        return redirect('listings:website_reviews')
    
    return render(request, 'listings/reviews/delete_website_review.html', {
        'review': review
    })

def website_reviews(request):
    reviews = WebsiteReview.objects.all().order_by('-created_at')
    has_reviewed = False
    if request.user.is_authenticated:
        has_reviewed = WebsiteReview.objects.filter(user=request.user).exists()
    return render(request, 'listings/reviews/website_reviews.html', {
        'reviews': reviews,
        'has_reviewed': has_reviewed
    })