from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import CustomUser, EmployerProfile, JobFinderProfile, Message, JobApplication, Notification, FriendList
from .forms import CustomUserCreationForm, JobFinderProfileForm, EmployerProfileForm, MessageForm, BidPurchaseForm, JobPostForm, JobApplicationForm
from django.db.models import Q

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
                    return redirect('home')
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
    profile, created = JobFinderProfile.objects.get_or_create(user=request.user)
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    jobs = Job.objects.all()  # Add this to fetch job listings
    
    if request.method == 'POST':
        form = JobFinderProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('job_finder_dashboard')
    else:
        form = JobFinderProfileForm(instance=profile)
    
    profile_filled = profile.name and profile.skills and profile.experience
    
    return render(request, 'job_portal/job_finder_dashboard.html', {
        'form': form,
        'notifications': notifications,
        'profile': profile,
        'profile_filled': profile_filled,
        'jobs': jobs,  # Add this to pass job listings to the template
    })

def employer_dashboard(request):
    profile, created = EmployerProfile.objects.get_or_create(user=request.user)
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    applications = JobApplication.objects.filter(job__employer=request.user)
    hired_job_finders = applications.filter(is_approved=True)
    
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('employer_dashboard')
    else:
        form = EmployerProfileForm(instance=profile)
    
    return render(request, 'job_portal/employer_dashboard.html', {
        'form': form,
        'notifications': notifications,
        'applications': applications,
        'hired_job_finders': hired_job_finders,
        'profile': profile,
    })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

def messaging(request):
    friends = request.user.friends.friends.all()
    current_friend = None
    if friends:
        current_friend = friends[0]
    friend_messages = {friend: Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=friend)) |
        (Q(sender=friend) & Q(receiver=request.user))
    ).order_by('timestamp') for friend in friends}
    return render(request, 'job_portal/messaging.html', {
        'friend_messages': friend_messages,
        'current_friend': current_friend,
        'notifications': Notification.objects.filter(user=request.user).order_by('-timestamp')
    })

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')
        receiver = CustomUser.objects.get(id=receiver_id)
        message = Message(sender=request.user, receiver=receiver, content=content)
        message.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


from django.shortcuts import render
from .models import Notification
from django.shortcuts import render
from .models import Notification

def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'job_portal/notifications.html', {'notifications': notifications})


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
            # Create notification for employer
            Notification.objects.create(
                user=job.employer,
                message=f'A job finder named {request.user.username} has bid {application.bid_count} on your job post. Want to chat with them?'
            )
            return redirect('job_finder_dashboard')
    else:
        form = JobApplicationForm()
    return render(request, 'job_portal/apply_to_job.html', {'form': form, 'job': job})

# Manage Applications view
def manage_applications(request):
    applications = JobApplication.objects.filter(job__employer=request.user)
    return render(request, 'job_portal/manage_applications.html', {'applications': applications})

# Approve Application view
def approve_application(request, application_id):
    application = JobApplication.objects.get(id=application_id)
    application.is_approved = True
    application.save()
    # Create notification for job finder
    Notification.objects.create(
        user=application.applicant,
        message='Your bid request was approved. Go to chat to discuss further.'
    )
    # Add job finder to employer's friend list
    employer_friends, created = FriendList.objects.get_or_create(user=request.user)
    employer_friends.friends.add(application.applicant)
    job_finder_friends, created = FriendList.objects.get_or_create(user=application.applicant)
    job_finder_friends.friends.add(request.user)
    return redirect('employer_dashboard')



def reject_application(request, application_id):
    application = JobApplication.objects.get(id=application_id)
    application.delete()
    return redirect('employer_dashboard')

def hire_job_finder(request, job_finder_id):
    job_finder = CustomUser.objects.get(id=job_finder_id)
    # Logic to mark job finder as hired and notify them
    Notification.objects.create(
        user=job_finder,
        message=f'You have been hired by {request.user.username}.'
    )
    return redirect('messaging')

def job_finder_profile(request, job_finder_id):
    job_finder = CustomUser.objects.get(id=job_finder_id)
    profile = JobFinderProfile.objects.get(user=job_finder)
    return render(request, 'job_portal/job_finder_profile.html', {'profile': profile})

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Message, CustomUser

@login_required
def fetch_messages(request):
    friend_id = request.GET.get('friend_id')
    friend = CustomUser.objects.get(id=friend_id)
    messages = Message.objects.filter(sender=request.user, receiver=friend) | Message.objects.filter(sender=friend, receiver=request.user)
    messages = messages.order_by('timestamp')

    messages_list = []
    for message in messages:
        messages_list.append({
            'content': message.content,
            'sender': message.sender.id,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })

    return JsonResponse({'status': 'success', 'messages': messages_list})
