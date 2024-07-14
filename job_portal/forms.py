from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Message,Job,JobApplication

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_job_finder', 'is_employer')

from django import forms
from .models import JobFinderProfile, EmployerProfile

class JobFinderProfileForm(forms.ModelForm):
    class Meta:
        model = JobFinderProfile
        fields = '__all__'
        exclude = ['user']

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = '__all__'
        exclude = ['user']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']

class BidPurchaseForm(forms.Form):
    bid_count = forms.IntegerField(min_value=1, label='Number of Bids')

class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description','location','salary']

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['bid_count']

