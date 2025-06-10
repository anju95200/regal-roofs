import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from ..models import ContactMessage
from django.contrib import messages

logger = logging.getLogger(__name__)

def superuser_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('listings:home')
        return view_func(request, *args, **kwargs)
    return wrapper

def contact_admin(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            subject = f"New Contact Message: {contact_message.subject}"
            message = f"""
            New message from {contact_message.name} ({contact_message.email}):
            
            Subject: {contact_message.subject}
            Message: {contact_message.message}
            
            Sent on: {contact_message.created_at}
            """
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, "Your message has been sent successfully!")
            except Exception as e:
                logger.error(f"Email sending failed: {str(e)}")
                messages.error(request, f"Failed to send message: {str(e)}")
            return redirect('listings:contact_admin')
    else:
        form = ContactForm()
    
    return render(request, 'listings/contact/contact.html', {'form': form})

@superuser_required
def admin_contact_messages(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        message_id = request.POST.get('message_id')
        message = get_object_or_404(ContactMessage, id=message_id)
        
        if action == 'delete':
            message.delete()
            messages.success(request, "Message deleted successfully!")
        elif action == 'edit':
            form = ContactForm(request.POST, instance=message)
            if form.is_valid():
                form.save()
                messages.success(request, "Message updated successfully!")
            else:
                messages.error(request, "Failed to update message. Please check the form.")
        return redirect('listings_admin:admin_contact_messages')
    
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    form = ContactForm()  # For rendering edit forms
    return render(request, 'listings/admin/admin_contact.html', {
        'messages': messages_list,
        'form': form,
    })