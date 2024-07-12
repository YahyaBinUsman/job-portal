from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_signup')
    else:
        form = CustomUserCreationForm()
    return render(request, 'job_portal/signup.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_job_finder:
                    return redirect('job_finder_dashboard')
                elif user.is_employer:
                    return redirect('employer_dashboard')
                else:
                    return redirect('home')  # fallback in case neither role is set
    else:
        form = AuthenticationForm()
    return render(request, 'job_portal/login.html', {'form': form})


def home(request):
    return render(request, 'job_portal/home.html')

def post_signup(request):
    return render(request, 'job_portal/post_signup.html')

from .forms import JobFinderProfileForm, EmployerProfileForm
from django.shortcuts import render, redirect
from .forms import JobFinderProfileForm, EmployerProfileForm

def job_finder_dashboard(request):
    if request.method == 'POST':
        form = JobFinderProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('job_finder_dashboard')
    else:
        form = JobFinderProfileForm()
    return render(request, 'job_portal/job_finder_dashboard.html', {'form': form})

def employer_dashboard(request):
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('employer_dashboard')
    else:
        form = EmployerProfileForm()
    return render(request, 'job_portal/employer_dashboard.html', {'form': form})


from .forms import MessageForm
from .models import Message

def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('messages')
    else:
        form = MessageForm()
    return render(request, 'job_portal/send_message.html', {'form': form})

def view_messages(request):
    messages_sent = Message.objects.filter(sender=request.user)
    messages_received = Message.objects.filter(receiver=request.user)
    return render(request, 'job_portal/messages.html', {
        'messages_sent': messages_sent,
        'messages_received': messages_received,
    })

from .models import Bid
from .forms import BidPurchaseForm

def purchase_bids(request):
    if request.method == 'POST':
        form = BidPurchaseForm(request.POST)
        if form.is_valid():
            bid_count = form.cleaned_data['bid_count']
            # Add logic to process payment through Jazz Cash
            bid, created = Bid.objects.get_or_create(user=request.user)
            bid.count += bid_count
            bid.save()
            return redirect('job_finder_dashboard')
    else:
        form = BidPurchaseForm()
    return render(request, 'job_portal/purchase_bids.html', {'form': form})


from .models import Job
from .forms import JobPostForm

def create_job_post(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect('employer_dashboard')
    else:
        form = JobPostForm()
    return render(request, 'job_portal/create_job_post.html', {'form': form})

def list_jobs(request):
    jobs = Job.objects.all()
    return render(request, 'job_portal/jobs.html', {'jobs': jobs})

from .models import JobApplication
from .forms import JobApplicationForm

def apply_to_job(request, job_id):
    job = Job.objects.get(id=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            # Deduct bids from user
            bid = Bid.objects.get(user=request.user)
            bid.count -= application.bid_count
            bid.save()
            return redirect('job_finder_dashboard')
    else:
        form = JobApplicationForm()
    return render(request, 'job_portal/apply_to_job.html', {'form': form, 'job': job})

def manage_applications(request):
    applications = JobApplication.objects.filter(job__employer=request.user)
    return render(request, 'job_portal/manage_applications.html', {'applications': applications})

def approve_application(request, application_id):
    application = JobApplication.objects.get(id=application_id)
    application.is_approved = True
    application.save()
    return redirect('manage_applications')

def reject_application(request, application_id):
    application = JobApplication.objects.get(id=application_id)
    application.delete()
    return redirect('manage_applications')
