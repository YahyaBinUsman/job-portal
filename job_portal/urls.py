from django.urls import path
from .views import signup, user_login, home, post_signup, job_finder_dashboard, employer_dashboard

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('', home, name='home'),
    path('post_signup/', post_signup, name='post_signup'),
    path('job_finder_dashboard/', job_finder_dashboard, name='job_finder_dashboard'),
    path('employer_dashboard/', employer_dashboard, name='employer_dashboard'),
]
