from django.urls import path
from .views import signup, user_login, home, post_signup, job_finder_dashboard, employer_dashboard, send_message, view_messages,create_job_post, list_jobs,purchase_bids
from .views import apply_to_job, manage_applications, approve_application, reject_application

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('', home, name='home'),
    path('post_signup/', post_signup, name='post_signup'),
    path('job_finder_dashboard/', job_finder_dashboard, name='job_finder_dashboard'),
    path('employer_dashboard/', employer_dashboard, name='employer_dashboard'),
    path('send_message/', send_message, name='send_message'),
    path('messages/', view_messages, name='messages'),
    path('purchase_bids/', purchase_bids, name='purchase_bids'),
    path('create_job_post/', create_job_post, name='create_job_post'),
    path('jobs/', list_jobs, name='list_jobs'),
    path('apply_to_job/<int:job_id>/', apply_to_job, name='apply_to_job'),
    path('manage_applications/', manage_applications, name='manage_applications'),
    path('approve_application/<int:application_id>/', approve_application, name='approve_application'),
    path('reject_application/<int:application_id>/', reject_application, name='reject_application'),
]
