from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.UserUpdateView.as_view(), name='profile_update'),
    path('background-check/', views.background_check_view, name='background_check'),
]
