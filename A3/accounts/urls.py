from django.urls import path
from accounts.views import register, loginforuser, logoutuser, view_profile, edit_profile
app_names = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', loginforuser, name='login'),
    path('logout/', logoutuser, name='logout'),
    path('profile/view/', view_profile, name='profile/view'),
    path('profile/edit/', edit_profile, name='profile/edit'),
]



