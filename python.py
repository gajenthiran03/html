# 1. Model Setup (Django ORM) :
# models.py

from django.db import models

class UserAccess(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    location_type = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    # Add any other relevant fields here

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

#2. Form Setup

# forms.py

from django import forms
from .models import UserAccess

class UserAccessForm(forms.ModelForm):
    class Meta:
        model = UserAccess
        fields = ['first_name', 'last_name', 'location_type', 'department', 'designation', 'email']  # Add any other relevant fields

#3. View to Handle Form Submission

# views.py

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import UserAccessForm
from django.conf import settings

def user_access_view(request):
    if request.method == 'POST':
        form = UserAccessForm(request.POST)
        if form.is_valid():
            user_access = form.save()

            # Send email to reporting manager
            send_mail(
                subject='New User Access Request Submitted',
                message=f"A new user access request has been submitted by {user_access.first_name} {user_access.last_name}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['manager@example.com'],  # Replace with reporting manager's email
            )
            return redirect('success_page')  # Redirect to a success page
    else:
        form = UserAccessForm()

    return render(request, 'user_access_form.html', {'form': form})


#4. Configure Email Settings
# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.your-email-provider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
DEFAULT_FROM_EMAIL = 'your-email@example.com'


#5. Template for the Form
<!-- templates/user_access_form.html -->
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>

#6. URL Configuration
# urls.py

from django.urls import path
from .views import user_access_view

urlpatterns = [
    path('user-access/', user_access_view, name='user_access'),
]

#7. Success Page
# views.py

def success_page(request):
    return render(request, 'success.html')
